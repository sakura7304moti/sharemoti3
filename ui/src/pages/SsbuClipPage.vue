<template>
  <q-page class="">
    <div class="text-h6">スマブラの切り抜き</div>
    <!--PC用・タブレット用の表示-->
    <q-form @submit.prevent="onSearchClick" class="q-mb-lg">
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
      v-for="item in dataState.records"
      :key="item.id"
      style="padding-bottom: 32px; max-width: 600px"
    >
      <q-card>
        <q-card-section>
          <div class="text-subtitle1 q-mb-md" style="font-size: 1.3rem">
            {{ item.title }}
          </div>
          <div class="q-mb-md">
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
            <div
              style="
                position: relative;
                height: 100px;
                background-color: rgb(51, 51, 51);
              "
            >
              <img
                :src="item.fullIcon"
                style="
                  margin-left: 20%;
                  max-width: 100%;
                  width: 80%;
                  max-height: 100%;
                  height: 100%;
                  object-fit: cover;
                "
              />
              <div
                style="
                  position: absolute;
                  left: 0;
                  top: 50%;
                  transform: translateY(-50%);
                  width: 100%;
                  text-align: left;
                  padding-left: 20px;
                  font-size: 22px;
                  font-weight: bold;
                  color: white;
                "
              >
                {{ item.charName }}
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

    onSearchClick();
    getDate();
    getCategory();
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
          }
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
  };

  const onSsbuNameClick = function (ssbuName: string) {
    if (condition.value.ssbuName == ssbuName) {
      console.log('スマブラの名前が変化してないため検索しません');
      return;
    }

    onResetCondition();
    condition.value.ssbuName = ssbuName;
    onSearchClick();
  };

  const onDateClick = function (date: string) {
    if (condition.value.date == date) {
      console.log('日付が変化してないため検索しません');
      return;
    }

    onResetCondition();
    condition.value.date = date;
    onSearchClick();
  };

  const onCateClick = function (cate: string) {
    if (condition.value.cate == cate) {
      console.log('種類が変化してないため検索しません');
      return;
    }

    onResetCondition();
    condition.value.cate = cate;
    onSearchClick();
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
