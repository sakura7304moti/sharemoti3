<template>
  <q-page class="">
    <div class="text-h6 q-pb-md">スマブラの切り抜き</div>
    <q-form @submit.prevent="onSearchClick" class="q-mb-lg q-ml-md">
      <div
        class="row q-gutter-md wrap q-mb-sm"
        style="max-width: 1100px; width: 100%"
      >
        <div>
          <q-input
            label="テキスト"
            class="bg-white"
            v-model="condition.text"
            dense
            stack-label
            outlined
          />
        </div>
        <div>
          <ssbu-name-select
            class="bg-white"
            v-model="condition.ssbuName"
            outlined
          />
        </div>
        <div>
          <q-input
            label="あだ名"
            class="bg-white"
            v-model="condition.charName"
            dense
            stack-label
            outlined
          />
        </div>
      </div>
      <div
        class="row q-gutter-md wrap q-mb-sm"
        style="max-width: 1100px; width: 100%"
      >
        <div>
          <q-select
            label="日付"
            class="bg-white"
            v-model="condition.date"
            :options="dateItems"
            dense
            stack-label
            outlined
            clearable
            style="width: 173px"
          />
        </div>
        <div>
          <q-select
            label="種類"
            class="bg-white"
            v-model="condition.cate"
            :options="categoryItems"
            dense
            stack-label
            outlined
            clearable
            style="width: 173px"
          />
        </div>
      </div>
      <div class="q-pt-sm">
        <q-btn
          label="検索"
          icon="search"
          color="primary"
          type="submit"
          :loading="isLoading"
        />
      </div>
    </q-form>

    <div
      class="q-ml-md"
      v-for="item in dataState.records"
      :key="item.id"
      style="padding-bottom: 48px; max-width: 600px"
    >
      <q-card>
        <q-card-section>
          <div
            class="text-subtitle1 q-mb-md ssbu-clip-title"
            style="font-size: 1.3rem"
          >
            {{ item.title }}
          </div>
          <div class="q-mb-sm">
            <div v-if="item.isPlay">
              <q-video
                class="backgroud-video"
                :src="item.movieUrl"
                style="min-width: 100%; max-width: 600px; width: 100%"
                :ratio="16 / 9"
              />
            </div>
            <div v-else>
              <div class="ssbu-clip-video-play" @click="onPlayClick(item.id)">
                <q-icon name="play_circle" size="md" color="light-green-3" />
                <span class="q-pl-sm">再生する</span>
              </div>
            </div>
          </div>
          <div>
            <div class="row justify-between">
              <div class="row q-pt-sm">
                <q-avatar>
                  <img :src="item.smallIcon" />
                </q-avatar>
                <q-item-label class="q-pt-sm q-pl-sm text-subtitle1">
                  {{ item.charName }}
                </q-item-label>
              </div>

              <div>
                <q-field label=" " stack-label class="q-pr-md">
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="0">
                      <span v-if="item.date.length == 8">
                        {{ item.date.substring(0, 4) }}年
                        {{ item.date.substring(4, 6) }}月
                        {{ item.date.substring(6, 8) }}日
                      </span>
                      <span v-else>{{ item.date }}</span>
                    </div>
                  </template>
                </q-field>
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>
<script lang="ts">
import { useQuasar } from 'quasar';
import api, { SsbuClipApi } from 'src/api/file/SsbuClipApi';
import { ref, defineComponent } from 'vue';
import SsbuNameSelect from 'src/components/selects/SsbuNameSelect.vue';

export default defineComponent({
  name: 'ssbu-clip-page',
  components: {
    SsbuNameSelect,
  },
  setup() {
    const {
      quasar,
      isLoading,
      isShowTopButton,
      condition,
      dateItems,
      categoryItems,
      dataState,
      handleScroll,
      topScroll,
      search,
      onSearchClick,
      onCharNameClick,
      onSsbuNameClick,
      onDateClick,
      onCateClick,
      getDate,
      getCategory,
      onPlayClick,
    } = useModel();

    const onMount = function () {
      onSearchClick();
      getDate();
      getCategory();
      window.addEventListener('scroll', handleScroll);
    };

    onMount();

    return {
      quasar,
      isLoading,
      isShowTopButton,
      condition,
      dateItems,
      categoryItems,
      dataState,
      topScroll,
      search,
      onSearchClick,
      onCharNameClick,
      onSsbuNameClick,
      onDateClick,
      onCateClick,
      getDate,
      getCategory,
      onPlayClick,
    };
  },
});
const useModel = function () {
  const quasar = useQuasar();
  const isLoading = ref(false);
  const isShowTopButton = ref(false);
  const condition = ref({
    text: '',
    charName: '',
    ssbuName: '',
    date: '',
    cate: '',
    pageNo: 1,
  } as ConditionState);
  const dataState = ref({
    records: [],
    totalCount: 0,
  } as DataState);
  const dateItems = ref([] as string[]);
  const categoryItems = ref([] as string[]);

  const handleScroll = () => {
    const bottomOfWindow =
      window.innerHeight + window.scrollY >=
      document.documentElement.offsetHeight - 200;

    if (bottomOfWindow && !isLoading.value) {
      onScrollSearch();
    }
  };

  const topScroll = function () {
    window.scroll({
      top: 0,
      behavior: 'smooth',
    });
  };

  const onPlayClick = function (id: number) {
    dataState.value.records.forEach((it) => {
      if (it.id == id) {
        it.isPlay = true;
      } else {
        it.isPlay = false;
      }
    });
  };

  const search = async function (request: ConditionState, clear = true) {
    if (clear) {
      condition.value.pageNo = 1;
    }
    isLoading.value = true;
    await api
      .search({
        text: request.text,
        charName: request.charName,
        ssbuName: request.ssbuName,
        date: request.date ?? '',
        cate: request.cate ?? '',
        pageNo: request.pageNo,
      })
      .then((response) => {
        if (response) {
          console.log('search response', response);
          if (clear) {
            dataState.value.records.splice(0);
          }
          response.records.forEach((it) =>
            dataState.value.records.push({
              id: it.id,
              title: it.title,
              fileName: it.fileName,
              dirName: it.dirName,
              charName: it.charName,
              ssbuName: it.ssbuName,
              date: it.date,
              fullIcon: it.fullIcon,
              smallIcon: it.smallIcon,
              isPlay: false,
              movieUrl: SsbuClipApi.MovieUrl(it.dirName, it.fileName),
            })
          );
          dataState.value.totalCount = response.totalCount;
          console.log('search dataState', dataState.value);
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
    isLoading.value = false;
  };

  const onSearchClick = function () {
    search(condition.value, true);
  };

  const onScrollSearch = async function () {
    console.log('scroll called');
    if (
      !isLoading.value &&
      condition.value.pageNo < dataState.value.totalCount
    ) {
      console.log('scroll search...');
      condition.value.pageNo = condition.value.pageNo + 1;
      await search(condition.value, false);
    }
  };

  const onResetCondition = function () {
    condition.value.text = '';
    condition.value.charName = '';
    condition.value.ssbuName = '';
    condition.value.date = '';
    condition.value.cate = '';
  };

  const onCharNameClick = function (charName: string) {
    if (condition.value.charName == charName) {
      console.log('あだ名が変化してないため検索しません');
      return;
    }

    onResetCondition();
    condition.value.charName = charName;
    onSearchClick();

    quasar.notify({
      color: 'secondary',
      position: 'top',
      message: condition.value.charName + 'で検索！',
    });
  };

  const onSsbuNameClick = function (ssbuName: string) {
    if (condition.value.ssbuName == ssbuName) {
      console.log('スマブラの名前が変化してないため検索しません');
      return;
    }

    onResetCondition();
    condition.value.ssbuName = ssbuName;
    onSearchClick();

    quasar.notify({
      color: 'secondary',
      position: 'top',
      message: condition.value.ssbuName + 'で検索！',
    });
  };

  const onDateClick = function (date: string) {
    if (condition.value.date == date) {
      console.log('日付が変化してないため検索しません');
      return;
    }

    onResetCondition();
    condition.value.date = date;
    onSearchClick();

    quasar.notify({
      color: 'secondary',
      position: 'top',
      message: condition.value.date + 'で検索！',
    });
  };

  const onCateClick = function (cate: string) {
    if (condition.value.cate == cate) {
      console.log('種類が変化してないため検索しません');
      return;
    }

    onResetCondition();
    condition.value.cate = cate;
    onSearchClick();

    quasar.notify({
      color: 'secondary',
      position: 'top',
      message: condition.value.cate + 'で検索！',
    });
  };

  const getDate = async function () {
    await api
      .date()
      .then((response) => {
        if (response) {
          console.log('date', response);
          dateItems.value = response;
        }
      })
      .catch((err) => {
        console.log('search err', err);
        quasar.notify({
          color: 'negative',
          position: 'top',
          message: '日付の取得でエラーになった...',
        });
      });
  };

  const getCategory = async function () {
    await api
      .category()
      .then((response) => {
        if (response) {
          console.log('category', response);
          categoryItems.value = response;
        }
      })
      .catch((err) => {
        console.log('search err', err);
        quasar.notify({
          color: 'negative',
          position: 'top',
          message: '種類の取得でエラーになった...',
        });
      });
  };

  return {
    quasar,
    isLoading,
    isShowTopButton,
    condition,
    dateItems,
    categoryItems,
    dataState,
    handleScroll,
    topScroll,
    search,
    onSearchClick,
    onCharNameClick,
    onSsbuNameClick,
    onDateClick,
    onCateClick,
    getDate,
    getCategory,
    onPlayClick,
  };
};
interface ConditionState {
  text: string;
  charName: string;
  ssbuName: string;
  date: string | null;
  cate: string | null;
  pageNo: number;
}
interface DataState {
  records: SsbuClip[];
  totalCount: number;
}
interface SsbuClip {
  id: number;
  title: string;
  fileName: string;
  dirName: string;
  charName: string;
  ssbuName: string;
  date: string;
  fullIcon: string;
  smallIcon: string;
  isPlay: boolean;
  movieUrl: string;
}
</script>
<style>
.ssbu-clip-video-play {
  /*ボタンの形状*/
  text-decoration: none;
  display: inline-block;
  text-align: center;
  background: transparent;
  border-radius: 20px;
  border: solid 1px rgba(196, 194, 194, 0.5);
  outline: none;
  cursor: pointer;
  padding: 8px;
  span {
    margin-top: 8px;
    color: rgb(196, 194, 194);
  }
}
.ssbu-clip-video-play:hover {
  background-color: rgba(202, 216, 196, 0.2);
  transition: 0.4s;
  span {
    color: rgb(182, 196, 176);
    font-weight: 700;
    transition: 0.6s;
  }
}
</style>
