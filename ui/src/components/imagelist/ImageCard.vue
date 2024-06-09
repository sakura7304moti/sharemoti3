<template>
  <q-card :class="{ 'image-tweet-card-lg': cardSize == 'lg' }">
    <q-card-section>
      <!--タイトル-->
      <div class="text-h6 text-bold text-grey-4" v-if="state.title == ''">
        タイトル無し
      </div>
      <div class="text-h6 text-bold" v-else>{{ state.title }}</div>

      <!--画像-->
      <div class="image-tweet-card-img">
        <img :src="downloadUrl" />
      </div>

      <q-separator />
      <!--詳細-->
      <div
        v-if="state.detail == '' && cardSize == 'lg'"
        class="text-grey-4 image-tweet-card-detail"
      >
        詳細無し
      </div>
      <div
        v-if="state.detail != '' && cardSize == 'lg'"
        class="image-tweet-card-detail"
      >
        {{ state.detail }}
      </div>
      <q-separator />

      <!--ボタン一覧-->
      <div class="row q-gutter-xs q-pt-md">
        <div>
          <q-btn
            round
            dense
            icon="download"
            text-color="primary"
            @click="fileDownload(downloadUrl)"
          />
        </div>
        <a
          :href="downloadUrl"
          class="q-pt-sm q-pr-md image-list-button-text"
          @click.prevent="fileDownload(downloadUrl)"
          style="text-decoration: none"
          >ダウンロード</a
        >
        <div>
          <imageUpdate :data-state="state" :download-url="downloadUrl" />
        </div>
        <div v-if="deleteDisplay">
          <imageDelete
            :data-state="state"
            :download-url="downloadUrl"
            @deleted="deleteNotify"
          />
        </div>
        <div>
          <q-btn
            round
            dense
            icon="image"
            @click.prevent="fullDisplay = true"
            text-color="grey"
          /><a
            :href="downloadUrl"
            class="q-pl-xs q-pr-md text-grey"
            style="text-decoration: none"
            @click.prevent="fullDisplay = true"
            >全画面表示</a
          >
        </div>
      </div>

      <!--日付-->
      <div
        class="row q-gutter-xs q-pt-md text-grey-8"
        v-if="cardSize == 'lg' || cardSize == 'md'"
      >
        <div>作成日:</div>
        <div class="q-pr-md">
          {{ state.createAt }}
        </div>
        <div>更新日:</div>
        <div>
          {{ state.updateAt }}
        </div>
      </div>
    </q-card-section>
  </q-card>

  <q-dialog
    v-model="fullDisplay"
    :maximized="maximizedToggle"
    transition-show="slide-up"
    transition-hide="slide-down"
  >
    <q-card class="text-white">
      <q-bar>
        <q-space />

        <q-btn
          dense
          flat
          icon="minimize"
          @click="maximizedToggle = false"
          :disable="!maximizedToggle"
        >
          <q-tooltip v-if="maximizedToggle">小さくする</q-tooltip>
        </q-btn>
        <q-btn
          dense
          flat
          icon="crop_square"
          @click="maximizedToggle = true"
          :disable="maximizedToggle"
        >
          <q-tooltip v-if="!maximizedToggle">最大化</q-tooltip>
        </q-btn>
        <q-btn dense flat icon="close" v-close-popup>
          <q-tooltip>閉じる</q-tooltip>
        </q-btn>
      </q-bar>

      <q-card-section>
        <img :src="downloadUrl" style="max-width: 90%; max-height: 90%" />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref, SetupContext } from 'vue';
import { MainAPIClient } from 'src/api/main/MainBaseApi';
import { useViewSupport } from 'src/utils/viewSupport';
import ImageUpdate from './ImageUpdate.vue';
import ImageDelete from 'src/components/imagelist/ImageDelete.vue';
export default defineComponent({
  name: 'image-list-tweet',
  props: {
    dataState: {
      type: Object as PropType<DataState>,
      required: true,
    },
    deleteDisplay: {
      type: Boolean,
      default: false,
    },
    size: {
      type: String,
      default: 'lg',
    },
  },
  components: {
    imageUpdate: ImageUpdate,
    imageDelete: ImageDelete,
  },
  setup(props, context: SetupContext) {
    const cardSize = computed(() => props.size);
    const { fileDownload } = useViewSupport();
    const state = ref(props.dataState);
    const deleteView = computed(() => props.deleteDisplay);
    const client = new MainAPIClient();
    const downloadUrl = ref(
      `${client.apiEndpoint()}/imageList/download?fileName=${
        props.dataState.fileName
      }&ext=${props.dataState.ext}`
    );

    const deleteNotify = function () {
      context.emit('deleted');
    };

    return {
      state,
      downloadUrl,
      emptyText: ref('詳細無し'),
      fileDownload,
      deleteView,
      deleteNotify,
      cardSize,
      fullDisplay: ref(false),
      maximizedToggle: ref(false),
    };
  },
});

interface DataState {
  id: number;
  fileName: string;
  ext: string;
  title: string;
  detail: string;
  createAt: string;
  updateAt: string;
}
</script>

<style>
/*カード全体 */
.image-tweet-card-lg {
  width: 400px;
  height: 580px;
}
/*画像の表示 */
.image-tweet-card-img {
  margin-bottom: 30px;
  width: 100%;
  max-width: 400px;
  background-color: #ffffff;
  overflow: hidden;
  position: relative;
}
.image-tweet-card-img img {
  position: absolute;
  width: auto;
  height: auto;
  top: 0%;
  left: 50%;
  max-width: 100%;
  max-height: 100%;
  -webkit-transform: translate(-50%, 0%);
  -moz-transform: translate(-50%, 0%);
  -ms-transform: translate(-50%, 0%);
  transform: translate(-50%, 0%);
}
.image-tweet-card-img:after {
  display: block;
  padding-top: 75%;
  content: '';
}
@media screen and (max-width: 768px) {
  .image-tweet-card-img {
    max-width: 300px;
  }
  .image-tweet-card {
    width: 350px;
  }
}

/*詳細 */
.image-tweet-card-detail {
  height: 100px;
  width: 370px;
  overflow: scroll;
  text-align: left;
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-wrap: normal;
}
</style>
