<template>
  <div class="movielist-container">
    <div class="movielist-left-content">
      <div v-if="playState.url != ''">
        <q-video :src="playState.url" style="width: 569px; height: 320px" />
        <div class="row q-gutter-xs text-h5">
          <div style="width: 48px">
            <q-avatar
              class="q-pt-md"
              v-if="playState.poster != '' && playState.poster != undefined"
            >
              <img
                v-if="playState.poster == '緑眼鏡掛男'"
                src="../../assets/yosao.png"
              />
              <img v-else src="../../assets/legoman_profile.jpg" />
            </q-avatar>
          </div>
          <div
            class="q-pt-md"
            style="
              text-align: left;
              white-space: pre-wrap;
              word-wrap: break-word;
              width: 500px;
            "
          >
            {{ playState.title }}
          </div>
        </div>
      </div>

      <div v-else>
        <div class="video-container">
          <div class="video-placeholder">
            <!-- 動画再生ボタンアイコン（例: フォントアイコンを使用） -->
            <i class="play-icon">▶️</i>
            <div class="text-white">動画はここで再生されるよ</div>
          </div>
        </div>
      </div>
    </div>
    <div class="movielist-table">
      <q-table
        :title="tableName"
        v-if="!load.search"
        :rows="records"
        :columns="columns"
        row-key="id"
        :style="{ height: tableHeight }"
        separator="cell"
        rows-per-page-label="表示行数"
        no-results-label="見つからなかった..."
        no-data-label="見つからなかった..."
        :pagination="{ rowsPerPage: 0 }"
        :rows-per-page-options="[0]"
        :filter="filter"
        :filter-method="filteringData"
        class="table-base scroll-table"
      >
        <!--sub 1/3 オプション-->
        <template v-slot:top-right>
          <div class="row q-gutter-md table-base-header">
            <div>
              <q-input
                dense
                debounce="300"
                v-model="filter.fileName"
                placeholder="検索"
                class="table-base-filter-input"
                align="left"
              >
                <template v-slot:append>
                  <q-spinner
                    v-model="load.search"
                    v-if="load.search"
                    color="primary"
                    size="md"
                  />
                  <q-icon name="search" v-if="filter.fileName.length == 0" />
                  <q-icon name="search" v-else color="primary" />
                  <div class="text-caption" v-if="records.length > 0">
                    {{ records.length }}
                  </div>
                </template>
              </q-input>
            </div>
            <div>
              <div class="row q-gutter-xs">
                <q-avatar
                  v-if="filter.poster != '' && filter.poster != undefined"
                >
                  <img
                    v-if="filter.poster == '緑眼鏡掛男'"
                    src="../../assets/yosao.png"
                  />
                  <img v-else src="../../assets/legoman_profile.jpg" />
                </q-avatar>
                <div v-else style="width: 48px; height: 48px"></div>
                <q-select
                  v-model="filter.poster"
                  :options="posterOptions"
                  dense
                  stack-label
                  label="投稿者"
                  transition-show="jump-up"
                  transition-hide="jump-up"
                  style="width: 150px"
                  clearable
                >
                  <!--開いた時-->
                  <template v-slot:option="scope">
                    <q-item
                      v-bind="scope.itemProps"
                      class="holo-name-item-selected"
                    >
                      <q-avatar>
                        <img
                          v-if="scope.opt == '緑眼鏡掛男'"
                          src="../../assets/yosao.png"
                        />
                        <img v-else src="../../assets/legoman_profile.jpg" />
                      </q-avatar>

                      <q-item-label
                        class="holo-select-text-container text-bold"
                      >
                        {{ scope.opt }}
                      </q-item-label>
                    </q-item>
                  </template>

                  <!--ヒント-->
                  <template v-slot:hint>
                    {{ filter.poster }}
                  </template>

                  <!--カウンター-->
                  <template v-slot:counter> </template>
                </q-select>
              </div>
            </div>
          </div>
        </template>

        <!-- sub 2/3  ヘッダー-->
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th style="width: 50px"><div class="q-pt-md">再生</div> </q-th>
            <q-th v-for="col in props.cols" :key="col.name" :props="props">
              <div
                v-if="col.label == 'タイトル'"
                class="table-base-main-column"
              >
                {{ col.label }}
              </div>
              <div
                v-if="col.label == 'ファイル名'"
                class="table-base-sub-column"
              >
                {{ col.label }}
              </div>
            </q-th>
          </q-tr>
        </template>

        <!-- sub 3/3  アイテム-->
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td>
              <a
                :href="`${api.apiEndpoint()}/movieList/download?fileName=${
                  props.row.fileName
                }&poster=${props.row.poster}`"
                class="play-btn"
                @click.prevent="
                  playState.url = `${api.apiEndpoint()}/movieList/download?fileName=${
                    props.row.fileName
                  }&poster=${props.row.poster}`;
                  playState.title = props.row.fileName;
                  playState.poster = props.row.poster;
                "
                ><q-icon name="play_circle" color="negative" size="md"></q-icon
              ></a>
            </q-td>
            <q-td
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
              style="white-space: normal; text-align: left"
            >
              <div class="text-weight-medium" style="font-weight: 500">
                {{ col.value }}
              </div>
              <div class="text-weight-thin row g-gutter-md">
                <div>
                  <q-avatar size="md">
                    <img
                      v-if="
                        records.find((it) => it.fileName == col.value)
                          ?.poster == '緑眼鏡掛男'
                      "
                      src="../../assets/yosao.png"
                    />
                    <img v-else src="../../assets/legoman_profile.jpg" />
                  </q-avatar>
                </div>
                <div class="q-pt-sm q-pl-sm" style="color: gray">
                  {{ records.find((it) => it.fileName == col.value)?.poster }}
                </div>
              </div>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useMovieListModel } from 'src/models/MovieListModels';
import api from 'src/api/file/MovieListApi';
export default defineComponent({
  name: 'table-movie-list',
  props: {
    label: {
      type: String,
      required: false,
      default: '動画まとめ',
    },
    height: {
      type: Number,
      required: false,
      default: 700,
    },
  },
  setup(props) {
    const {
      columns,
      quasar,
      records,
      load,
      search,
      filter,
      filteringData,
      posterOptions,
    } = useMovieListModel();
    search();
    const playState = ref({
      url: '',
      title: '',
      poster: '',
    } as PlayState);

    return {
      tableName: ref(props.label),
      tableHeight: ref(props.height + 'px'),
      playState,
      columns,
      quasar,
      records,
      load,
      search,
      filter,
      filteringData,
      posterOptions,
      api,
    };
  },
});
interface PlayState {
  url: string;
  title: string;
  poster: string;
}
</script>
<style>
/*テーブルのstyle */
.movielist-table {
  max-width: 600px;
}

.movielist-table .q-table__top,
.movielist-table .q-table__bottom,
.movielist-table thead tr:first-child th {
  /* bg color is important for th; just specify one */
  background-color: white;
}

.movielist-table thead tr th {
  position: sticky;
  z-index: 1;
}

.movielist-table thead tr:first-child th {
  top: 0;
}

/* this is when the loading indicator appears */
.movielist-table.q-table--loading thead tr:last-child th {
  /* height of all previous header rows */
  top: 48px;
}

/* prevent scrolling behind sticky top row on focus */
.movielist-table tbody {
  /* height of all previous header rows */
  scroll-margin-top: 48px;
}
/*動画とテーブルのstyle */
.movielist-container {
  display: flex;
  flex-wrap: wrap;
}

.movielist-left-content {
  width: 570px;
}

.movielist-right-content {
  width: 600px;
}

@media screen and (max-width: 1170px) {
  .movielist-container {
    flex-direction: column;
  }

  .movielist-left-content,
  .movielist-right-content {
    width: 100%;
  }
}

/*テーブルのstyle */
.movielist-table-scrollable-container {
  height: 80vh; /* ページの高さの80%に設定 */
  overflow-y: auto; /* 縦方向にスクロール可能にする */
}

/*? */
.video-container {
  width: 569px;
  height: 320px;
  position: relative;
  overflow: hidden; /* オーバーフローしたコンテンツを非表示にする */
}

.video-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #000; /* ボタンアイコンの背景色 */
  opacity: 0.7; /* 不透明度を設定して動画の一部を透過させる */
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
}

.play-icon {
  font-size: 40px;
  color: #fff; /* ボタンアイコンの色 */
  cursor: pointer;
}
</style>
