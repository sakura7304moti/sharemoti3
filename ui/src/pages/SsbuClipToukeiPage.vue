<template>
  <q-page class="q-ma-md">
    <div class="text-h6">切り抜きの記録</div>
    <q-card class="q-mt-md" style="max-width: 500px; width: 100%">
      <q-card-section>
        <div class="q-mb-xs">
          <q-tabs
            v-model="selectTab"
            inline-label
            style="max-width: 360px"
            class="bg-white"
            active-color="primary"
            indicator-color="primary"
            dense
            @update:model-value="onSearchClick"
          >
            <q-tab
              :name="tab"
              :label="tab"
              v-for="tab in tabItems"
              :key="tab"
              style="width: 180px"
            />
          </q-tabs>
        </div>
        <div class="row q-gutter-md">
          <q-radio
            v-model="selectCategory"
            :val="cate"
            :label="cate"
            v-for="cate in categoryItems"
            :key="cate"
            @update:model-value="onSearchClick"
          />
        </div>
      </q-card-section>
    </q-card>
    <div class="q-mt-md" style="max-width: 900px">
      <div v-if="selectTab == 'ランキング'">
        <div v-for="rec in rankRecords" :key="rec.name">
          <div style="padding-bottom: 24px">
            <div
              class="text-subtitle1 text-weight-bold q-mr-md"
              v-if="rec.total > 0"
            >
              {{ rec.rank }}位
            </div>
            <div class="row">
              <q-avatar
                class="q-mr-md ssbu-icon"
                @click="onSearchMovie(rec.name, selectCategory)"
              >
                <img
                  :src="ssbuNameOptions.find((it) => it.name == rec.name)?.icon"
                />
              </q-avatar>
              <div style="font-size: 32px" v-if="rec.total > 0">
                {{ rec.total }}<span style="font-size: 16px"> こ </span>
              </div>
            </div>

            <div class="text-body1">{{ rec.name }}</div>
          </div>
        </div>
      </div>
      <div v-if="selectTab == '記念日'">
        <div v-for="rec in firstRecords" :key="rec.name">
          <div style="padding-bottom: 24px">
            <div class="row">
              <q-avatar
                class="q-mr-md ssbu-icon"
                @click="onSearchMovie(rec.name, selectCategory)"
              >
                <img
                  :src="ssbuNameOptions.find((it) => it.name == rec.name)?.icon"
                />
              </q-avatar>
              <div style="font-size: 16px; padding-top: 8px" v-if="rec.date">
                {{ rec.date }}
              </div>
            </div>

            <div class="text-body1">{{ rec.name }}</div>
          </div>
        </div>
      </div>
      <div v-if="selectTab == 'スタンプカード'" class="row wrap">
        <div v-for="rec in stampRecords" :key="rec.name">
          <q-avatar
            class="q-mr-md q-mb-sm ssbu-icon"
            @click="onSearchMovie(rec.name, selectCategory)"
          >
            <img
              :src="ssbuNameOptions.find((it) => it.name == rec.name)?.icon"
              :class="{ 'img-default': rec.comp != 1 }"
            />
          </q-avatar>
        </div>
      </div>
    </div>
    <q-dialog v-model="dialog">
      <q-card style="max-width: 1000px; width: 100%">
        <q-card-section class="bg-black text-white q-pa-none">
          <!--ヘッダー-->
          <div class="bg-primary row justify-between">
            <div class="row">
              <q-avatar class="q-ma-xs" size="md">
                <img
                  :src="
                    ssbuNameOptions.find(
                      (it) => it.name == selectedCondition.name
                    )?.icon
                  "
                />
              </q-avatar>
              <div class="dialog-title q-pt-sm">
                {{ selectedCondition.category }}コレクション
              </div>
            </div>

            <div class="q-pr-xs q-pt-sm">
              <q-btn flat icon="close" @click="dialog = false" />
            </div>
          </div>

          <div class="row wrap">
            <!--動画再生エリア-->
            <div
              style="
                max-width: min(600px, calc(100vw - 32px));
                width: 100%;
                margin: 0 auto;
              "
            >
              <video
                class="backgroud-video"
                :src="movies.find((it) => it.isPlay)?.movieUrl ?? ''"
                style="min-width: 100%; max-width: 600px; width: 100%"
                :ratio="16 / 9"
                @ended="onVideoEnded"
                controls
                autoplay
                v-if="movies.filter((it) => it.isPlay).length == 1"
              />
              <div class="q-px-md q-mb-sm" style="font-size: 20px">
                {{ movies.find((it) => it.isPlay)?.title }}
              </div>
              <div>
                <q-radio
                  keep-color
                  color="primary"
                  v-model="playMode"
                  val="base"
                  label="通常再生"
                />
                <q-radio
                  keep-color
                  color="primary"
                  v-model="playMode"
                  val="auto"
                  label="自動"
                />
                <q-radio
                  keep-color
                  color="primary"
                  v-model="playMode"
                  val="shuffle"
                  label="シャッフル"
                />
              </div>
            </div>

            <!--曲を選ぶドン-->
            <div id="movie-titles">
              <div
                v-for="rec in movies"
                :key="rec.id"
                class="q-pl-sm q-mt-sm movie-title"
                @click="onPlayClick(rec.id)"
                :class="{ 'text-primary': rec.isPlay }"
              >
                <q-icon
                  text-color="white"
                  :name="rec.isPlay ? 'audiotrack' : 'smart_display'"
                  size="sm"
                /><span class="q-ml-sm">
                  {{ rec.title }}
                </span>
                <hr />
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import api from 'src/api/file/SsbuClipToukeiApi';
import { NameListApi } from 'src/api/main/NameListApi';
const nameApi = new NameListApi();
import { useQuasar } from 'quasar';
import { SsbuClipApi } from 'src/api/file/SsbuClipApi';
export default defineComponent({
  name: 'ssbu-clip-toukei-page',
  setup() {
    const {
      selectCategory,
      categoryItems,
      selectTab,
      tabItems,
      rankRecords,
      firstRecords,
      stampRecords,
      ssbuNameOptions,
      getRank,
      getNames,
      onSearchClick,
    } = useModel();
    getNames();
    onSearchClick();

    const {
      isLoading,
      dialog,
      movies,
      selectedCondition,
      playMode,
      onPlayClick,
      onSearchMovie,
      onVideoEnded,
    } = useMovieModel();
    return {
      selectCategory,
      categoryItems,
      selectTab,
      tabItems,
      rankRecords,
      firstRecords,
      stampRecords,
      ssbuNameOptions,
      getRank,
      getNames,
      onSearchClick,
      // movie **
      isLoading,
      dialog,
      movies,
      selectedCondition,
      playMode,
      onPlayClick,
      onSearchMovie,
      onVideoEnded,
    };
  },
});
const useModel = function () {
  const quasar = useQuasar();
  const selectCategory = ref('ウルトラC');
  const categoryItems = ref(['ウルトラC', 'ウルツラC', '思い出', '焼き直し']);
  const selectTab = ref('ランキング');
  const tabItems = ref(['ランキング', '記念日', 'スタンプカード']);
  const rankRecords = ref([] as Rank[]);
  const firstRecords = ref([] as First[]);
  const stampRecords = ref([] as Stamp[]);
  const ssbuNameOptions = ref([] as SsbuNameState[]);

  const getNames = async function () {
    await nameApi
      .ssbu_names()
      .then((response) => {
        if (response) {
          console.log('ssbu-names', response);
          response.records.forEach((it) => ssbuNameOptions.value.push(it));
        }
      })
      .catch((e) => {
        console.log('err', e);
      });
  };

  const getRank = async function (text: string) {
    await api
      .rank(text)
      .then((response) => {
        if (response) {
          console.log('rank response', response);
          rankRecords.value.splice(0);
          response.forEach((it) => rankRecords.value.push(it));
        }
      })
      .catch((err) => {
        console.log('rank err', err);
        quasar.notify({
          color: 'negative',
          position: 'top',
          message: 'データ取得でエラーになった...',
        });
      });
  };

  const getFirst = async function (text: string) {
    await api
      .first(text)
      .then((response) => {
        if (response) {
          console.log('first response', response);
          firstRecords.value.splice(0);
          response.forEach((it) => firstRecords.value.push(it));
        }
      })
      .catch((err) => {
        console.log('rank err', err);
        quasar.notify({
          color: 'negative',
          position: 'top',
          message: 'データ取得でエラーになった...',
        });
      });
  };

  const getStamp = async function (text: string) {
    await api
      .stamp(text)
      .then((response) => {
        if (response) {
          console.log('stamp response', response);
          stampRecords.value.splice(0);
          response.forEach((it) => stampRecords.value.push(it));
        }
      })
      .catch((err) => {
        console.log('rank err', err);
        quasar.notify({
          color: 'negative',
          position: 'top',
          message: 'データ取得でエラーになった...',
        });
      });
  };

  const onSearchClick = function () {
    if (selectTab.value == 'ランキング') {
      getRank(selectCategory.value);
    }
    if (selectTab.value == '記念日') {
      getFirst(selectCategory.value);
    }
    if (selectTab.value == 'スタンプカード') {
      getStamp(selectCategory.value);
    }
  };

  return {
    selectCategory,
    categoryItems,
    selectTab,
    tabItems,
    rankRecords,
    firstRecords,
    stampRecords,
    ssbuNameOptions,
    getRank,
    getNames,
    onSearchClick,
  };
};

const useMovieModel = function () {
  const isLoading = ref(false);
  const dialog = ref(false);
  const playMode = ref('base');
  const movies = ref([] as SsbuClip[]);
  const selectedCondition = ref({
    name: '',
    category: '',
  } as ClipCondition);

  const onPlayClick = function (id: number) {
    movies.value.forEach((it) => {
      if (it.id == id) {
        it.isPlay = true;
      } else {
        it.isPlay = false;
      }
    });
  };

  const onVideoEnded = function () {
    console.log('called');
    if (playMode.value == 'base') {
      return;
    }

    const index = movies.value.findIndex((it) => it.isPlay);
    if (index == -1) {
      return;
    }

    if (playMode.value == 'auto') {
      if (index < movies.value.length) {
        const id = movies.value[index + 1].id;
        onPlayClick(id);
      } else {
        const id = movies.value[0].id;
        onPlayClick(id);
      }
    }

    if (playMode.value == 'shuffle') {
      const ids = movies.value
        .filter((it) => it.isPlay == false)
        .map((x) => x.id);
      const index = Math.floor(Math.random() * ids.length);
      const id = movies.value[index].id;
      onPlayClick(id);
    }
  };

  const onSearchMovie = async function (ssbuName: string, category: string) {
    const api = new SsbuClipApi();
    isLoading.value = true;
    await api
      .search({
        text: '',
        charName: '',
        cate: category,
        ssbuName: ssbuName,
        date: '',
        pageNo: -1,
      })
      .then((response) => {
        if (response) {
          console.log('movies', response);
          movies.value.splice(0);

          response.records.forEach((it) =>
            movies.value.push({
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
              videoIsLoading: false,
            })
          );
          selectedCondition.value.name = ssbuName;
          selectedCondition.value.category = category;
          dialog.value = true;
        }
      })
      .catch((err) => console.log('movie err', err));
    isLoading.value = false;
  };
  return {
    isLoading,
    dialog,
    movies,
    selectedCondition,
    playMode,
    onPlayClick,
    onSearchMovie,
    onVideoEnded,
  };
};
interface SsbuNameState {
  name: string;
  url: string;
  icon: string;
}
interface Rank {
  name: string;
  total: number;
  rank: number;
}
interface First {
  name: string;
  date: string;
}
interface Stamp {
  name: string;
  comp: number;
}
interface ClipCondition {
  name: string;
  category: string;
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
  videoIsLoading: boolean;
}
</script>
<style>
.img-default {
  opacity: 0.3;
}
.dialog-title {
  font-size: 22px;
}
.ssbu-icon {
  cursor: pointer;
}
.ssbu-icon:hover {
  opacity: 0.7s;
  transition: 0.3s;
}
.movie-title {
  cursor: pointer;
}
.movie-title:hover {
  transition: 0.3s;
  color: orange;
}
#movie-titles {
  max-width: min(300px, calc(100vw - 32px));
  width: 100%;
  max-height: calc(100vh - 150px);
  overflow-y: scroll;
}
@media (max-width: 1000px) {
  #movie-titles {
    margin: 4px;
    padding: 8px;
    max-width: 100%;
    width: 100%;
    border: white 2px solid;
    border-radius: 10px;
    max-height: calc(100vh - 500px);
  }
  .dialog-title {
    font-size: 18px;
  }
}
</style>
