<template>
  <q-page class="">
    <div class="text-h5 q-pb-sm q-pt-md">画像の背景透過ページ</div>
    <div class="text-subtitle1">1.まず画像がアニメかどうかを選択して...</div>
    <div class="row q-gutter-md q-pl-md">
      <q-radio v-model="isAnime" val="anime" label="Anime" />
      <q-radio v-model="isAnime" val="" label="Other" />
    </div>
    <div class="text-subtitle1 q-pt-md">
      2.ファイルを選択するとGB画像が作成されるよ!
    </div>
    <div class="row q-gutter-md q-pa-md">
      <q-file
        v-model="file"
        label="画像を選択"
        :clearable="file?.size != null"
        style="width: 300px"
        filled
        bottom-slots
        counter
        accept=".png,.jpeg,.jpg"
      >
        <template v-slot:prepend>
          <q-icon name="image" @click.stop.prevent />
        </template>
        <template v-slot:append>
          <q-icon
            name="close"
            @click.stop.prevent="file = null"
            class="cursor-pointer"
          />
        </template>

        <template v-slot:hint> ファイルサイズ </template>
      </q-file>

      <div class="q-pt-sm" v-if="isLoading">
        <q-spinner color="brown" size="md" />
        <div class="text-caption text-grey">
          しばらく待ってね...1分以内で完了するはず
        </div>
        <div class="text-caption">経過秒数:{{ elapsedTime }}[s]</div>
      </div>
    </div>

    <div
      style="width: 100%; max-width: 800px; display: flex; flex-wrap: wrap"
      class="q-pt-md"
    >
      <div v-if="postImageUrl" style="width: 100%; max-width: 45%">
        <img :src="postImageUrl" style="width: 100%" />
      </div>
      <div style="width: 100%; max-width: 5%" v-if="resultImageUrl"></div>
      <div v-if="resultImageUrl" style="width: 100%; max-width: 45%">
        <img
          :src="resultImageUrl"
          style="
            width: 100%;
            background-image: url('https://t3.ftcdn.net/jpg/04/71/63/80/360_F_471638092_3MMZ9pE8idFf3b5lFeE9YcTdpCRB4jvF.jpg');
          "
        />
        <div class="q-pt-xs">
          <div class="text-subtitle1 q-pt-md">
            3.いい感じならダウンロードしてね!
          </div>
          <q-btn
            label="ダウンロードする"
            @click="fileDownload(resultImageUrl)"
            color="primary"
            style="border-radius: 30px"
          />
        </div>
      </div>
    </div>
  </q-page>
</template>
<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue';
import { useViewSupport } from 'src/utils/viewSupport';
import { RembgApi } from '../api/sub/RembgApi';
import { APIClient } from 'src/api/BaseApi';
import { useQuasar } from 'quasar';
const { fileDownload } = useViewSupport();
const LOCALSTRAGE_KEY = 'rembg-isanime';
export default defineComponent({
  name: 'rembg-page',
  setup() {
    const client = new APIClient();
    const api = new RembgApi();
    const quasar = useQuasar();
    const downloadFileName = ref('');
    const resultImageUrl = computed(() =>
      downloadFileName.value == ''
        ? ''
        : client.apiEndpoint() +
          '/rembg/download?fileName=' +
          downloadFileName.value
    );
    const postImageUrl = ref('');
    const file = ref<File | null>(null);
    const isLoading = ref(false);
    const isAnime = ref(localStorage.getItem(LOCALSTRAGE_KEY) ?? '');

    watch(file, () => {
      if (file.value) {
        postImageUrl.value = URL.createObjectURL(file.value);
        onFileChange();
      } else {
        postImageUrl.value = '';
        downloadFileName.value = '';
      }
    });

    const onFileChange = async function () {
      if (file.value) {
        isLoading.value = true;
        startTimer();
        localStorage.setItem(LOCALSTRAGE_KEY, isAnime.value);
        if (isAnime.value == 'anime') {
          await api
            .uploadAnime(file.value)
            .then(async (response) => {
              if (response) {
                console.log('response', response);
                downloadFileName.value = response;
              } else {
                quasar.notify({
                  color: 'red',
                  position: 'top',
                  message: 'ごめん！エラーになっちゃった...',
                });
              }
            })
            .catch((error) => {
              console.error('Error removing background:', error);
              quasar.notify({
                color: 'red',
                position: 'top',
                message: 'ごめん！エラーになっちゃった...',
              });
            });
        } else {
          await api
            .upload(file.value)
            .then(async (response) => {
              if (response) {
                console.log('response', response);
                downloadFileName.value = response;
              } else {
                quasar.notify({
                  color: 'red',
                  position: 'top',
                  message: 'ごめん！エラーになっちゃった...',
                });
              }
            })
            .catch((error) => {
              console.error('Error removing background:', error);
              quasar.notify({
                color: 'red',
                position: 'top',
                message: 'ごめん！エラーになっちゃった...',
              });
            });
        }
      }
      stopTimer();
      isLoading.value = false;
    };

    /*timer */
    const elapsedTime = ref(0);
    let timer: ReturnType<typeof setInterval> | null = null;

    const startTimer = () => {
      timer = setInterval(() => {
        elapsedTime.value++;
      }, 1000);
    };

    const stopTimer = () => {
      if (timer) {
        clearInterval(timer);
        elapsedTime.value = 0;
      }
    };

    return {
      file,
      isAnime,
      isLoading,
      elapsedTime,
      postImageUrl,
      resultImageUrl,
      fileDownload,
    };
  },
});
</script>
