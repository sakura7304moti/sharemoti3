<template>
  <q-page class="">
    <div>
      <!--1/5 タイトル-->
      <div class="holo-page-title q-pb-md">記念配信まとめ</div>
      <div id="holo-page-loading" v-if="isLoading" class="row q-gutter-md">
        <q-spinner color="primary" size="3em" />
        <div class="text-subtitle1 text-primary">検索中...</div>
      </div>

      <div class="q-pa-md row q-gutter-md" v-if="pageState.selectLink != ''">
        <YouTube
          v-if="!isLoading && displayMode == 'gallery'"
          :src="pageState.selectLink"
          @ready="true"
          ref="youtube"
          :vars="{ autoplay: 1, rel: 0 }"
        />
      </div>

      <!--2/5 表示切り替え-->
      <div>
        <div class="row q-gutter-md q-pb-md" v-if="pageState.totalPages != 1">
          <div>
            <q-radio
              v-model="displayMode"
              val="gallery"
              label="サムネイル"
              dense
              class="q-pr-xs"
            />
            <q-radio v-model="displayMode" val="table" label="テーブル" dense />
          </div>
          <q-pagination
            v-if="!isLoading && displayMode == 'gallery'"
            v-model="pageState.pageNo"
            :max="pageState.totalPages"
            direction-links
            :max-pages="10"
            @click.prevent="selectPage"
            class="q-pl-md"
            outlined
          />
          <a
            href="#"
            @click.prevent.stop="searchOptionShow = true"
            v-if="!isLoading && displayMode == 'gallery'"
            ><q-icon name="view_list" color="primary" size="md"
          /></a>
        </div>
      </div>

      <!--3/5　サムネリスト-->
      <div
        id="holo-song-cards"
        style="min-height: 780px"
        v-if="displayMode == 'gallery'"
      >
        <div class="row q-gutter-md">
          <div v-for="rec in pageState.records" :key="rec.link" class="q-pa-sm">
            <q-card style="width: 100%; max-width: 250px">
              <q-card-section>
                <a
                  :href="rec.link"
                  @click.prevent="pageState.selectLink = rec.link"
                  ><img
                    :src="rec.imageLink"
                    style="width: 100%; max-width: 250px"
                /></a>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
      <div
        class="row q-gutter-md q-pt-md"
        v-if="
          pageState.totalPages != 1 && !isLoading && displayMode == 'gallery'
        "
      >
        <q-pagination
          v-model="pageState.pageNo"
          :max="pageState.totalPages"
          direction-links
          :max-pages="10"
          @click.prevent="selectPage"
          class="q-pb-md"
          outlined
        />
        <a href="#" @click.prevent.stop="searchOptionShow = true"
          ><q-icon name="view_list" color="primary" size="md"
        /></a>
      </div>
    </div>

    <!--4/5  テーブル-->
    <div class="q-pa-md">
      <div class="holomovie-container">
        <div class="holomovie-left-content">
          <div v-if="pageState.selectLink != ''">
            <YouTube
              v-if="!isLoading && displayMode == 'table'"
              :src="pageState.selectLink"
              @ready="true"
              ref="youtube"
              :vars="{ autoplay: 1, rel: 0 }"
            />
          </div>

          <div v-else>
            <div
              class="holomovie-video-container"
              v-if="!isLoading && displayMode == 'table'"
            >
              <div class="holomovie-video-placeholder">
                <!-- 動画再生ボタンアイコン（例: フォントアイコンを使用） -->
                <i class="holomovie-play-icon">▶️</i>
                <div class="text-white">動画はここで再生されるよ</div>
              </div>
            </div>
          </div>
        </div>
        <div class="holomovie-right-content">
          <q-table
            :rows="rows"
            :columns="columns"
            row-key="link"
            :filter="filter"
            separator="cell"
            v-if="!isLoading && displayMode == 'table'"
            rows-per-page-label="表示行数"
            no-results-label="見つからなかった..."
            :pagination="{ rowsPerPage: 0 }"
            :rows-per-page-options="[0]"
            class="holomovie-list-table"
          >
            <!--sub 1/3 検索-->
            <template v-slot:top-right>
              <div class="q-pr-md no-shadow">
                <q-btn
                  icon="queue_music"
                  dense
                  @click="songModalShow = true"
                  round
                />
              </div>

              <q-select
                v-model="songInput"
                style="width: 200px"
                dense
                use-input
                stack-label
                label="タイトル"
                class="q-pr-md"
                :options="songOptions"
                @filter="filterFn"
              />

              <q-select
                v-model="selectedMember"
                style="width: 200px"
                dense
                stack-label
                label="メンバー"
                class="q-pr-md"
                :options="holoMembers"
              />

              <div class="q-pl-md"></div>

              <q-input dense debounce="300" v-model="filter" placeholder="検索">
                <template v-slot:append>
                  <q-icon name="search" v-if="filter.length == 0" />
                  <q-icon name="search" v-else color="primary" />
                </template>
              </q-input>
            </template>
            <!-- sub 2/3  ヘッダー-->
            <template v-slot:header="props">
              <q-tr :props="props">
                <q-th style="width: 50px"></q-th>
                <q-th v-for="col in props.cols" :key="col.name" :props="props">
                  <div v-if="col.label == 'メンバー'" style="width: 200px">
                    {{ col.label }}
                  </div>
                  <div v-if="col.label == '曲名'" style="width: 200px">
                    {{ col.label }}
                  </div>
                  <div v-if="col.label == 'タイトル'" style="width: 200px">
                    {{ col.label }}
                  </div>
                  <div v-if="col.label == '投稿日'" style="width: 100px">
                    {{ col.label }}
                  </div>
                  <div v-if="col.label == '区分'" style="width: 50px">
                    {{ col.label }}
                  </div>
                  <div v-if="col.label == '詳細'" style="width: 100px">
                    {{ col.label }}
                  </div>
                </q-th>
              </q-tr>
            </template>
            <!-- sub 3/3  アイテム-->
            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td style="width: 50px">
                  <div class="no-shadow">
                    <q-btn
                      size="md"
                      @click="pageState.selectLink = props.row.link"
                      icon="play_arrow"
                      text-color="primary"
                      outline
                    />
                  </div>
                </q-td>
                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                  <div style="white-space: normal; text-align: left">
                    {{ col.value }}
                  </div>
                </q-td>
              </q-tr>
            </template>
          </q-table>
        </div>
      </div>
    </div>

    <!--5/5  モーダル一覧-->
    <!-- sub 1/2  詳細なモーダル-->
    <q-dialog v-model="searchOptionShow">
      <q-card style="width: 400px">
        <q-card-section>
          <div class="text-h5">ページ選択</div>
          <hr />
          <q-pagination
            v-model="pageState.pageNo"
            :max="pageState.totalPages"
            @click.prevent="selectPage"
            class="q-pb-md"
            outlined
            style="width: 300px"
          />
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- sub 2/2  曲一覧-->
    <q-dialog v-model="songModalShow">
      <q-card style="width: 400px">
        <q-card-section>
          <div class="text-h6">動画タイトル一覧</div>
          <div class="q-pa-md">
            <ul v-for="song in songList" :key="song">
              <a
                href="#"
                class="holo-memory-songitem text-subtitle1"
                @click.prevent="
                  filter = song;
                  songModalShow = false;
                "
              >
                <li class="holo-memory-songli">
                  {{ song }}
                </li>
              </a>
            </ul>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script lang="ts">
import { useHoloMemoryModel } from 'src/models/HoloMemoryModels';
import { defineComponent, ref, watch } from 'vue';
import YouTube from 'vue3-youtube';
export default defineComponent({
  name: 'holomemory-page',
  components: { YouTube },
  setup() {
    const {
      records,
      pageState,
      isLoading,
      searchOptionShow,
      rows,
      columns,
      displayMode,
      holoMembers,
      songList,
      select,
      selectPage,
    } = useHoloMemoryModel();
    select();

    const selectedMember = ref('');
    const filter = ref('');

    watch(selectedMember, () => {
      if (selectedMember.value != '') {
        filter.value = selectedMember.value;
        selectedMember.value = '';
      }
    });

    const songOptions = ref([] as string[]);
    songList.value.forEach((it) => songOptions.value.push(it));

    const filterFn = (val: string, update: any) => {
      update(() => {
        const needle = val.toLowerCase();
        songOptions.value = songList.value.filter(
          (v) => v.toLowerCase().indexOf(needle) > -1
        );
      });
    };

    const songInput = ref('');

    watch(songInput, () => {
      if (songInput.value != '') {
        filter.value = songInput.value;
        songInput.value = '';
      }
    });
    /*localstrage */
    const KEY_LOCAL_STRAGE = 'holo-memory';
    const viewValue = localStorage.getItem(KEY_LOCAL_STRAGE);
    if (viewValue) {
      if (viewValue == 'gallery') {
        displayMode.value = 'gallery';
      } else {
        displayMode.value = 'table';
      }
    } else {
      localStorage.setItem(KEY_LOCAL_STRAGE, 'gallery');
    }

    watch(displayMode, () => {
      localStorage.setItem(KEY_LOCAL_STRAGE, displayMode.value);
    });

    return {
      filter,
      selectedMember,
      records,
      pageState,
      isLoading,
      searchOptionShow,
      rows,
      columns,
      displayMode,
      holoMembers,
      songList,
      selectPage,
      songOptions,
      filterFn,
      songInput,
      songModalShow: ref(false),
    };
  },
});
</script>
<style>
.holo-memory-songitem {
  text-decoration: none;
  color: black;
}
.holo-memory-songli:hover {
  background: #bedcf5;
}
.holo-memory-songli {
  position: relative;
  list-style-type: none !important; /*ポチ消す*/
  padding: 0.5em 0.5em 0.5em 0.5em;
  margin-bottom: 5px;
  line-height: 1.5;
  background: #dbebf8;
  vertical-align: middle;
  color: #505050;
  border-radius: 15px 0px 0px 15px; /*左側の角丸く*/
}
.holo-memory-songli:before {
  display: inline-block;
  vertical-align: middle;
  /*以下白丸つくる*/
  content: '';
  width: 1em;
  height: 1em;
  background: #fff;
  border-radius: 50%;
  margin-right: 8px;
}
/*テーブル用の表示 */
/*動画とテーブルのstyle */
.holomovie-container {
  display: flex;
  flex-wrap: wrap;
}

.holomovie-left-content {
  width: 640px;
}

.holomovie-right-content {
  width: 1100px;
}

@media screen and (max-width: 1740px) {
  .holomovie-container {
    flex-direction: column; /* ページの横幅が1740px未満の場合、縦に配置 */
  }

  .holomovie-left-content,
  .holomovie-right-content {
    width: 100%; /* ページの横幅が1740px未満の場合、フル幅になる */
  }
}

/*テーブルのstyle */
.holomovie-table-scrollable-container {
  height: 80vh; /* ページの高さの80%に設定 */
  overflow-y: auto; /* 縦方向にスクロール可能にする */
}

/*動画再生してないときの画面 */
.holomovie-video-container {
  width: 640px;
  height: 320px;
  position: relative;
  overflow: hidden; /* オーバーフローしたコンテンツを非表示にする */
}

.holomovie-video-placeholder {
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

.holomovie-play-icon {
  font-size: 40px;
  color: #fff; /* ボタンアイコンの色 */
  cursor: pointer;
}
/*テーブルのstyle */
.holomovie-list-table {
  max-width: 1100px;
  max-height: 70vh;
}

.holomovie-list-table .q-table__top,
.holomovie-list-table .q-table__bottom,
.holomovie-list-table thead tr:first-child th {
  /* bg color is important for th; just specify one */
  background-color: white;
}

.holomovie-list-table thead tr th {
  position: sticky;
  z-index: 1;
}

.holomovie-list-table thead tr:first-child th {
  top: 0;
}

/* this is when the loading indicator appears */
.holomovie-list-table.q-table--loading thead tr:last-child th {
  /* height of all previous header rows */
  top: 48px;
}

/* prevent scrolling behind sticky top row on focus */
.holomovie-list-table tbody {
  /* height of all previous header rows */
  scroll-margin-top: 48px;
}
</style>
