<template>
  <q-page class="">
    <div class="holo-page-title q-pb-md">ホロメンのつぶやき</div>
    <div class="row q-gutter-md wrap q-mb-sm">
      <div>
        <q-input label="テキスト" v-model="condition.text" dense stack-label />
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
        >
          <!--クリアー-->
          <template v-slot:append>
            <q-icon
              id="holo-select-clear-icon"
              v-if="condition.acountName != ''"
              name="clear"
              @click.stop.prevent="condition.acountName = ''"
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
            {{ selectedUser?.screenName }}
          </template>

          <!--カウンター-->
          <template v-slot:counter> </template>
        </q-select>
      </div>
      <div>
        <q-btn
          label="検索"
          @click="search(condition)"
          icon="search"
          color="primary"
        />
      </div>
    </div>
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
        <div style="white-space: pre-wrap; word-wrap: break-word">
          {{ item.text }}
        </div>
      </q-chat-message>
    </div>
  </q-page>
</template>
<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import api from 'src/api/scraper/HolotwitterApi';
export default defineComponent({
  name: 'holotwitter-page',
  setup() {
    const {
      isloading,
      condition,
      dataState,
      selectedUser,
      acounts,
      search,
      handleScroll,
      topScroll,
      getAcount,
    } = useModel();
    getAcount();
    search(condition.value);

    window.addEventListener('scroll', handleScroll);

    return {
      isloading,
      condition,
      dataState,
      acounts,
      search,
      getAcount,
      selectedUser,
      topScroll,
    };
  },
});
/*スクリプト */
const useModel = function () {
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
          response.records.forEach((it) => dataState.value.records.push(it));
          dataState.value.totalCount = response.totalCount;
        }
      })
      .catch((err) => {
        console.log('search err', err);
      });
    isloading.value = false;
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
      });
  };
  return {
    isloading,
    condition,
    dataState,
    selectedUser,
    acounts,
    search,
    handleScroll,
    topScroll,
    getAcount,
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
}

interface User {
  name: string;
  screenName: string;
  profileImage: string;
}
</script>
