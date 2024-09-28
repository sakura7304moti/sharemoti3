<template>
  <q-page class="">
    <!--ページタイトル-->
    <div class="holo-page-title">twitter</div>
    <!--入力フォーム-->
    <q-form @submit="search">
      <div class="row q-gutter-md wrap">
        <div>
          <holo-select
            v-if="condition.mode == 'holo'"
            v-model="condition.hashtag"
            label="hololive fanart"
          />
        </div>
        <div>
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
        </div>
        <div>
          <q-btn
            color="primary"
            icon="search"
            type="submit"
            :loading="isLoading"
            label="検索"
          />
        </div>

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
    </q-form>

    <!--gallery-->
    <div
      v-for="rec in dataState.records"
      :key="rec.image"
      style="margin-bottom: 32px"
    >
      <img
        :src="rec.image.replace('&name=orig', '&name=small')"
        style="
          max-height: 70vh;
          height: 100%;
          max-width: 90vw;
          object-fit: contain;
          align-items: left;
          cursor: pointer;
        "
        :class="{
          'twitter-im-selected': rec.displayMenu,
        }"
        @click="rec.displayMenu = !rec.displayMenu"
      />
      <q-card
        v-if="rec.displayMenu"
        style="width: 200px; height: 40px; padding-left: 16px; padding-top: 2px"
      >
        <div class="row q-gutter-md">
          <div>
            <q-btn
              icon="file_download"
              @click.prevent="fileDownload(rec.image)"
              color="primary"
              flat
              round
              ><q-tooltip :delay="1000">download</q-tooltip></q-btn
            >
          </div>
          <div>
            <q-btn
              icon="image"
              @click.prevent="fullScViewClick(rec.image)"
              color="secondary"
              round
              flat
              ><q-tooltip :delay="1000">image view</q-tooltip></q-btn
            >
          </div>
          <div>
            <q-btn
              icon="info"
              @click.prevent="pageOpenClick(rec.url)"
              color="black"
              round
              flat
              ><q-tooltip :delay="1000">tweet link</q-tooltip></q-btn
            >
          </div>
        </div>
      </q-card>
    </div>

    <!--pagi-->
    <div class="q-pt-sm" v-if="dataState.totalPages > 1 && !isLoading">
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
        <q-card-section style="max-height: 90vh; height: 100%; padding: 0">
          <q-bar style="max-width: 100%; width: 100%">
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
          <img
            :src="fullScreenViewUrl"
            style="max-height: 100%; height: 100%; object-fit: contain"
          />
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
