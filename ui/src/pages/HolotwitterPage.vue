<template>
  <q-page class="">
    <div class="holo-page-title q-pb-md">ホロメンのつぶやき</div>
    <q-form @submit="onSearchClick">
      <div class="row q-gutter-md wrap q-mb-sm">
        <div>
          <q-input
            label="テキスト"
            v-model="condition.text"
            dense
            stack-label
          />
        </div>
        <div>
          <q-select
            v-model="condition.acountName"
            :options="acounts"
            option-value="screenName"
            option-label="screenName"
            emit-value
            map-options
            dense
            stack-label
            label="ホロメン"
            transition-show="jump-up"
            transition-hide="jump-up"
            counter
            style="width: 200px"
            @update:model-value="onSearchClick"
          >
            <!--クリアー-->
            <template v-slot:append>
              <q-icon
                id="holo-select-clear-icon"
                v-if="condition.acountName != ''"
                name="clear"
                @click.stop.prevent="onAcountClearClick"
              />
            </template>

            <!--開いた時-->
            <template v-slot:option="scope">
              <q-item v-bind="scope.itemProps" class="holo-name-item-selected">
                <q-avatar>
                  <img :src="scope.opt.profileImage" />
                </q-avatar>

                <q-item-label class="holo-select-text-container text-bold">
                  {{ scope.opt.name }}
                </q-item-label>
              </q-item>
            </template>

            <!--選択時-->
            <template v-slot:selected>
              <q-chip
                v-if="selectedUser?.name != ''"
                dense
                square
                color="white"
                class="q-my-none q-ml-xs q-mr-none"
              >
                <q-avatar text-color="white">
                  <q-img :src="selectedUser?.profileImage" />
                </q-avatar>
                {{ selectedUser?.screenName }}
              </q-chip>
            </template>

            <!--ヒント-->
            <template v-slot:hint>
              {{ selectedUser?.name }}
            </template>

            <!--カウンター-->
            <template v-slot:counter> </template>
          </q-select>
        </div>
        <div>
          <q-btn
            label="検索"
            @click="onSearchClick"
            icon="search"
            color="primary"
            type="submit"
          />
        </div>
      </div>
    </q-form>

    <div
      v-for="item in dataState.records"
      :key="item.id"
      style="padding-bottom: 32px; max-width: 800px"
    >
      <q-chat-message
        :stamp="item.createdAt"
        :name="item.userName"
        :avatar="item.profileImage"
        bg-color="light-blue-1"
      >
        <div>
          <div style="white-space: pre-wrap; word-wrap: break-word">
            {{ item.text }}
          </div>
          <div
            class="q-py-md q-px-sm"
            v-for="media in item.medias"
            :key="media.url"
            style="
              max-width: 800px;
              width: 100%;
              max-height: calc(70vh + 32px);
              height: 100%;
            "
          >
            <div v-if="media.type == 'image'">
              <img
                :src="media.metaImageUrl"
                style="
                  max-width: 800px;
                  width: 100%;
                  max-height: 70vh;
                  height: 100%;
                "
              />
            </div>
            <div v-if="media.type == 'video'">
              <q-video
                class="backgroud-video"
                v-if="media.playUrl"
                :src="media.playUrl"
                style="min-width: 100%; max-width: 800px; width: 100%"
                :ratio="16 / 9"
              />
              <div
                style="
                  position: relative;
                  display: inline-block;
                  max-width: 800px;
                  width: 100%;
                "
              >
                <img
                  v-if="!media.playUrl"
                  :src="media.metaImageUrl"
                  style="max-width: 800px; width: 100%"
                  class="cursor-pointer holotwitter-movie-img"
                  @click="media.playUrl = movieDownloadUrl(media.mediaUrl)"
                />
                <!-- 再生ボタン -->
                <div
                  v-if="!media.playUrl"
                  style="
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                  "
                  class="cursor-pointer"
                  @click="media.playUrl = movieDownloadUrl(media.mediaUrl)"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    width="64px"
                    height="64px"
                    fill="#fff"
                  >
                    <path d="M8 5v14l11-7z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
        <template v-slot:avatar>
          <q-avatar
            class="q-mr-sm cursor-pointer holotwitter-user-icon"
            @click="onAcountClick(item.userScreenName)"
          >
            <img :src="item.profileImage" />
          </q-avatar>
        </template>
      </q-chat-message>
    </div>
  </q-page>
</template>
<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import api from 'src/api/scraper/HolotwitterApi';
import { LocationQueryRaw, useRoute, useRouter } from 'vue-router';
import { useQuerySupport } from 'src/utils/QuerySupport';
import { useQuasar } from 'quasar';
const { decodeQueryString } = useQuerySupport();
export default defineComponent({
  name: 'holotwitter-page',
  setup() {
    const {
      handleProps,
      isloading,
      condition,
      dataState,
      selectedUser,
      acounts,
      search,
      onSearchClick,
      onAcountClick,
      onAcountClearClick,
      handleScroll,
      topScroll,
      getAcount,
      movieDownloadUrl,
    } = useModel();

    const onMount = function () {
      getAcount();
      window.addEventListener('scroll', handleScroll);
      handleProps();
    };

    onMount(); // 初期で実行する処理

    return {
      isloading,
      condition,
      dataState,
      acounts,
      search,
      getAcount,
      selectedUser,
      topScroll,
      onSearchClick,
      onAcountClick,
      onAcountClearClick,
      movieDownloadUrl,
    };
  },
});
/*スクリプト */
const useModel = function () {
  const route = useRoute();
  const router = useRouter();
  const quasar = useQuasar();

  const setProps = function (condition: ConditionState) {
    const query = {} as LocationQueryRaw;
    if (condition.text) {
      query.text = condition.text;
    }
    if (condition.acountName) {
      query.name = condition.acountName;
    }

    router.push({
      path: '/holotwitter',
      query: query,
    });
  };

  const handleProps = function () {
    console.log('props', route.query);
    const queryText = decodeQueryString(route.query.text);
    if (queryText) {
      condition.value.text = queryText;
    }

    const queryAcountName = decodeQueryString(route.query.name);
    if (queryAcountName) {
      condition.value.acountName = queryAcountName;
    }

    search(condition.value);
  };

  const isloading = ref(false);
  const condition = ref({
    text: '',
    acountName: '',
    startDate: '',
    pageNo: 0,
  } as ConditionState);
  const dataState = ref({
    records: [],
    totalCount: 0,
  } as DataState);
  const acounts = ref([] as User[]);
  const selectedUser = computed(() =>
    acounts.value.find((it) => it.screenName == condition.value.acountName)
  );

  const handleScroll = () => {
    const bottomOfWindow =
      window.innerHeight + window.scrollY >=
      document.documentElement.offsetHeight - 200;

    if (bottomOfWindow && !isloading.value) {
      onScrollSearch();
    }
  };

  const topScroll = function () {
    window.scroll({
      top: 0,
      behavior: 'smooth',
    });
  };

  const search = async function (request: ConditionState, clear = true) {
    if (clear) {
      condition.value.pageNo = 1;
    }
    isloading.value = true;
    await api
      .searchTweet(request)
      .then((response) => {
        if (response) {
          console.log('search', response);
          if (clear) {
            dataState.value.records.splice(0);
          }
          response.records.forEach((it) =>
            dataState.value.records.push({
              id: it.id,
              text: it.text,
              createdAt: it.createdAt,
              userScreenName: it.userScreenName,
              userName: it.userName,
              profileImage: it.profileImage,
              medias: it.medias.map((m) => {
                return {
                  type: m.type,
                  url: m.url,
                  mediaUrl: m.mediaUrl,
                  metaImageUrl: m.metaImageUrl,
                  playUrl: null,
                };
              }),
            })
          );
          dataState.value.totalCount = response.totalCount;
        }
      })
      .catch((err) => {
        console.log('search err', err);
        quasar.notify({
          color: 'negative',
          position: 'top',
          message: '検索でエラーになった...',
        });
      });
    isloading.value = false;
  };

  const onSearchClick = function () {
    setProps(condition.value);
    search(condition.value, true);
  };

  const onAcountClick = function (acountName: string) {
    if (condition.value.acountName == acountName) {
      console.log('検索条件が変化しないため、検索しません');
      return;
    }
    condition.value.acountName = acountName;
    condition.value.text = '';
    onSearchClick();

    quasar.notify({
      color: 'secondary',
      position: 'top',
      message: selectedUser.value?.name + 'で検索！',
    });
  };

  const onAcountClearClick = function () {
    condition.value.acountName = '';
    onSearchClick();
  };

  const onScrollSearch = async function () {
    console.log('scroll called');
    if (
      !isloading.value &&
      condition.value.pageNo < dataState.value.totalCount
    ) {
      console.log('scroll search...');
      condition.value.pageNo = condition.value.pageNo + 1;
      await search(condition.value, false);
    }
  };

  const getAcount = async function () {
    await api
      .getAcount()
      .then((response) => {
        if (response) {
          console.log('acount data', response);
          acounts.value.splice(0);
          response.forEach((it) => acounts.value.push(it));
        }
      })
      .catch((err) => {
        console.log('acount err', err);
        quasar.notify({
          color: 'negative',
          position: 'top',
          message: 'ホロメンの取得でエラーになった...',
        });
      });
  };

  const movieDownloadUrl = function (movieUrl: string) {
    return `${api.apiEndpoint()}/holotwitter/movie?url=${movieUrl}`;
  };
  return {
    setProps,
    handleProps,
    isloading,
    condition,
    dataState,
    selectedUser,
    acounts,
    search,
    onSearchClick,
    onAcountClick,
    onAcountClearClick,
    handleScroll,
    topScroll,
    getAcount,
    movieDownloadUrl,
  };
};
interface ConditionState {
  text: string;
  acountName: string;
  startDate: string;
  pageNo: number;
}
interface DataState {
  records: Tweet[];
  totalCount: number;
}

interface Tweet {
  id: number;
  text: string;
  createdAt: string;
  userScreenName: string;
  userName: string;
  profileImage: string;
  medias: Media[];
}

interface User {
  name: string;
  screenName: string;
  profileImage: string;
}

interface Media {
  type: string;
  url: string;
  mediaUrl: string;
  metaImageUrl: string;
  playUrl: string | null;
}
</script>
<style>
.holotwitter-user-icon:hover {
  background-color: rgba(255, 255, 255, 0.2);
}
.holotwitter-movie-container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.background-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
}
</style>
