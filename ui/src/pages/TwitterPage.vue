<template>
  <q-page class="">
    <!--ページタイトル-->
    <div class="holo-page-title holo-twitter-title-android">twitter</div>
    <!--入力フォーム-->
    <div id="holotwitter-search-form">
      <div>
        <div class="row q-gutter-md">
          <div class="holo-page-title holo-twitter-title-pc">twitter</div>
        </div>
      </div>
      <div>
        <holo-select
          v-if="condition.mode == 'holo'"
          v-model="condition.hashtag"
          label="hololive fanart"
        />
      </div>

      <div class="row q-gutter-md q-pt-md">
        <q-select
          label="♡"
          v-model="condition.minLike"
          :options="selectItems"
          emit-value
          map-options
          stack-label
          dense
          style="height: 40px; width: 80px"
        />
        <q-btn
          color="primary"
          icon="search"
          @click="search"
          :loading="isLoading"
        />
        <div class="q-pl-md">
          <q-btn
            icon="settings"
            color="grey"
            size="sm"
            round
            @click="searchOptionShow = true"
          />
        </div>
      </div>
      <!--pagi-->
      <div class="q-pt-sm" v-if="dataState.totalPages > 1">
        <q-pagination
          v-model="condition.pageNo"
          size="md"
          :max="dataState.totalPages"
          direction-links
          input
          :max-pages="3"
          @update:model-value="search()"
          style="width: 250px"
        />
      </div>
    </div>

    <!--gallery-->
    <div id="holo-twitter-images">
      <ul class="gallery">
        <li v-for="r in dataState.records" :key="r.image">
          <a
            :href="r.image"
            @click.prevent.stop="r.displayMenu = !r.displayMenu"
            class="image-container"
            :class="{
              'image-selected': r.displayMenu,
            }"
          >
            <img :src="r.image.replace('&name=orig', '&name=small')" />
            <div class="button-overlay" v-if="r.displayMenu">
              <div class="row q-gutter-md button">
                <!--Download-->
                <q-btn
                  icon="file_download"
                  @click.prevent="fileDownload(r.image)"
                  color="primary"
                  round
                  ><q-tooltip :delay="1000">download</q-tooltip></q-btn
                >
                <!--View-->
                <q-btn
                  icon="image"
                  @click.prevent="fullScViewClick(r.image)"
                  color="secondary"
                  round
                  ><q-tooltip :delay="1000">image view</q-tooltip></q-btn
                >
                <!--tweet <link-->
                <q-btn
                  icon="info"
                  @click.prevent="pageOpenClick(r.url)"
                  color="black"
                  round
                  ><q-tooltip :delay="1000">tweet link</q-tooltip></q-btn
                >
              </div>
            </div>
          </a>
        </li>
      </ul>
    </div>

    <!--search option dialog-->
    <q-dialog v-model="searchOptionShow">
      <q-card style="height: 100%">
        <q-card-section>
          <div class="text-h5">検索オプション</div>
          <hr />
          <div class="text-subtitle1">ハッシュタグ</div>
          <div class="row q-gutter-md">
            <q-input
              v-model="condition.hashtag"
              class="form-model"
              dense
              stack-label
              filled
            />
            <holo-select
              v-model="condition.hashtag"
              label="ホロライブファンアート"
            />
          </div>

          <div class="q-pt-md text-subtitle1">ツイート日</div>
          <div class="row q-gutter-md">
            <q-input
              v-model="condition.startDate"
              class="form-model"
              dense
              type="date"
              filled
            />
            <div class="text-h6 q-pt-sm form-date-span">~</div>
            <q-input
              v-model="condition.endDate"
              class="form-model"
              dense
              type="date"
              filled
            />
          </div>
          <div class="q-pt-md">
            <div class="text-subtitle1">ユーザー名</div>
            <q-input
              v-model="condition.userName"
              class="form-model"
              stack-label
              dense
              filled
            />
          </div>
          <div class="q-pt-md">
            <div class="text-subtitle1">いいね</div>
            <div class="row q-gutter-md">
              <q-input
                v-model="condition.minLike"
                class="form-model"
                type="number"
                dense
                filled
              />
              <div class="text-h6 q-pt-sm form-date-span">~</div>
              <q-select
                v-model="condition.maxLike"
                :options="selectItems"
                class="form-model"
                emit-value
                map-options
                stack-label
                dense
                filled
              />
            </div>
          </div>
          <div class="q-pt-md row q-gutter-cs">
            <div>
              <q-checkbox
                true-value="holo"
                false-value=""
                v-model="condition.mode"
                color="cyan"
              />
            </div>
            <div>
              <img
                v-if="condition.mode == 'holo'"
                src="../assets/holo_icon.jpg"
                style="height: 30px"
              />
              <div v-else class="text-subtitle2 q-pt-sm">
                ホロライブの画像のみ
              </div>
            </div>
          </div>
          <div class="q-pt-md">
            <q-btn
              color="primary"
              dense
              icon="search"
              @click="search"
              :loading="isLoading"
              label="検索"
            />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!--View Modal-->
    <q-dialog
      v-model="fullSc"
      persistent
      full-height
      full-width
      transition-show="slide-up"
      transition-hide="slide-down"
    >
      <q-card>
        <q-card-section>
          <q-bar>
            <q-btn
              dense
              flat
              icon="close"
              v-close-popup
              style="margin-left: auto"
            >
              <q-tooltip class="bg-white text-primary">Close</q-tooltip>
            </q-btn>
          </q-bar>
          <img :src="fullScreenViewUrl" :height="pageHeight" />
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>
<script lang="ts">
import { useViewSupport } from 'src/utils/viewSupport';
import { useTwitterModel } from 'src/models/TwitterModels';
import { computed, defineComponent, ref } from 'vue';
import HoloNameSelect from 'src/components/selects/HoloNameSelect.vue';
export default defineComponent({
  name: 'twitter-page',
  components: {
    'holo-select': HoloNameSelect,
  },
  setup() {
    const { fileDownload, imageDownload } = useViewSupport();

    const {
      condition,
      dataState,
      search,
      isLoading,
      dateModalShow,
      selectItems,
      imageLinkOpen,
      searchOptionShow,
    } = useTwitterModel();

    const downloadMode = ref(false);

    const fullScreenViewUrl = ref('');
    const fullSc = ref(false);
    const fullScViewClick = function (url: string) {
      fullScreenViewUrl.value = url;
      fullSc.value = true;
    };

    const pageOpenClick = function (url: string) {
      window.open(url);
    };

    const pageWidth = computed(() => {
      return window.innerWidth;
    });

    const pageHeight = computed(() => {
      return window.innerHeight - 100;
    });

    return {
      condition,
      dataState,
      search,
      isLoading,
      dateModalShow,
      selectItems,
      imageLinkOpen,
      imageDownload,
      fileDownload,
      downloadMode,
      fullSc,
      fullScreenViewUrl,
      fullScViewClick,
      maximizedToggle: ref(true),
      pageOpenClick,
      pageWidth,
      pageHeight,
      searchOptionShow,
      test: ref(''),
    };
  },
});
</script>
<style>
/*input */
.form-model {
  width: 200px;
  height: 40px;
}
.form-date-span {
  width: 10px;
}
.gallery {
  columns: 4; /*段組みの数*/
  padding: 0 15px; /*ギャラリー左右に余白をつける*/
}

.gallery li {
  margin-bottom: 20px; /*各画像下に余白をつける*/
}

/*ギャラリー内のイメージは横幅100%にする*/
.gallery img {
  width: 100%;
  height: auto;
  vertical-align: bottom; /*画像の下にできる余白を削除*/
}
/*===== メニュー表示用 ===== */
.image-container {
  position: relative;
  display: inline-block;
}

.image-container img {
  display: block;
  width: 100%;
  height: auto;
}

.button-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.button-overlay .button {
  width: 100%;
  height: 40px;
  background-color: rgba(128, 128, 128, 0);
}

/*　横幅900px以下の段組み設定　*/
@media only screen and (max-width: 900px) {
  .gallery {
    columns: 2;
  }
}

@media only screen and (max-width: 768px) {
  .gallery {
    columns: 1;
  }
}

/*========= レイアウトのためのCSS ===============*/

ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

a {
  color: #333;
}

h1 {
  text-align: center;
  font-size: 6vw;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin: 30px 0;
}

p {
  margin: 0 10px 10px 10px;
  word-wrap: break-word;
}

/*image select */
.image-selected {
  background: #f0f7ff;
  border: dashed 2px #5b8bd0; /*点線*/
}

/*ギャラリー全体のコンテナ */
#holo-twitter-images {
  overflow-y: auto;
  height: calc(100vh - 280px);
}

@media (max-width: 768px) {
  #holo-twitter-images {
    height: calc(100vh - 230px);
  }
}

@media (max-width: 768px) {
  #holo-twitter-images {
    width: calc(100% - 48px);
  }
}

/*ぺーじタイトル */
@media (max-width: 768px) {
  .holo-twitter-title-pc {
    display: none;
  }
}

@media (max-width: 768px) {
  .holo-twitter-title-android {
    position: fixed;
    top: 8px; /*自分が固定したい位置(例は上から0pxの位置)*/
    left: 150px; /*自分が固定したい位置(例は左から10pxの位置)*/
  }
}

@media (min-width: 768px) {
  .holo-twitter-title-android {
    display: none;
  }
}

/*検索欄 */
@media (min-width: 768px) {
  #holotwitter-search-form {
    height: 200px;
  }
}

@media (max-width: 768px) {
  #holotwitter-search-form {
    height: 150px;
  }
}
</style>
