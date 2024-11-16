<template>
  <q-page class="">
    <!--トップ画像-->
    <div class="top-image-container zoomIn">
      <div
        style="
          margin-left: 16px;
          margin-bottom: 8px;
          font-size: 32px;
          font-family: serif;
        "
      >
        今日の一枚
      </div>
      <div
        style="
          text-align: left;
          max-width: 100vw;
          width: 100%;
          padding-bottom: 16px;
        "
      >
        <img :src="imageUrl" class="top-image fadeDown" />
      </div>
    </div>

    <!--おしらせ-->
    <div style="margin-top: 32px; text-align: center">
      <div>
        <span
          ><img
            src="../assets/lief-left.png"
            style="width: 40px; height: 20px; object-fit: contain"
        /></span>
        <span
          style="
            font-size: 32px;
            font-family: serif;
            margin-left: 16px;
            margin-right: 16px;
          "
          >お知らせ</span
        >
        <span
          ><img
            src="../assets/lief-right.png"
            style="width: 40px; height: 40px; object-fit: contain"
        /></span>
      </div>
      <div class="q-mt-md top-news-container">
        <hr />
        <div
          v-for="(rec, idx) in newsDataState.records"
          :key="idx"
          class="top-news-card"
        >
          <div class="top-news-card-child">
            <div
              style="
                text-align: left;
                padding-left: 16px;
                width: 100px;
                font-family: EB Garamond;
              "
            >
              {{ rec.createdAt }}
            </div>
            <div
              style="
                font-family: Noto Sans JP;

                padding-left: 16px;
              "
            >
              <span style="color: rgb(0, 167, 137)">{{ rec.page }}</span
              >で新しいデータが追加されたよ！
            </div>
          </div>
          <hr />
        </div>
        <q-pagination
          v-model="newsCondition"
          :max="newsDataState.totalCount"
          color="teal-6"
          @update:model-value="getNews"
          class="q-mt-sm"
        />
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import api from 'src/api/file/TopImageApi';
import { TopNewsApi } from 'src/api/file/TopNewsApi';
import { useQuasar } from 'quasar';
export default defineComponent({
  name: 'IndexPage',
  setup() {
    const quasar = useQuasar();
    const newsApi = new TopNewsApi();
    const router = useRouter();
    const imageUrl = computed(() => api.singleImageUrl());
    const isTopNewsLoading = ref(false);
    const newsCondition = ref(1);
    const newsDataState = ref({
      records: [],
      totalCount: 0,
    } as NewsDataState);

    const getNews = async function () {
      isTopNewsLoading.value = true;
      await newsApi
        .news(newsCondition.value)
        .then((response) => {
          if (response) {
            console.log('news', response);
            newsDataState.value.totalCount = response.totalCount;
            newsDataState.value.records = response.records;
          }
        })
        .catch((err) => {
          console.log('schol err', err);
          quasar.notify({
            color: 'red',
            position: 'top',
            message: 'お知らせの取得でエラーになった...',
          });
        });
      isTopNewsLoading.value = false;
    };
    getNews();
    return {
      imageUrl,
      isTopNewsLoading,
      newsCondition,
      newsDataState,
      getNews,
    };
  },
});
interface NewsDataState {
  records: Array<TopNews>;
  totalCount: number;
}

interface TopNews {
  page: string;
  createdAt: string;
  total: number;
}
</script>
<style>
/*画像 */
.top-image {
  max-width: 50vw;
  width: 100%;
  max-height: 50vh;
  height: 100%;
  display: inline-block;
  object-fit: contain;
  padding-left: 16px;
  padding-right: 16px;
}
.top-image-container {
  background-color: white;
  max-width: 50vw;
  border-radius: 20px;
  box-shadow: 10px;
}
@media (max-width: 1030px) {
  .top-image {
    max-width: 100vw;
  }
  .top-image-container {
    max-width: 100vw;
  }
}
/*ニュース */
.top-news-card {
  max-width: 800px;
  font-size: 12px;
  line-height: 20px;
}
.top-news-container {
  max-width: 60%;
  width: 100%;
  margin-right: auto;
  margin-left: auto;
}
.top-news-card-child {
  padding-top: 16px;
  padding-bottom: 16px;
  display: flex;
}
@media (max-width: 650px) {
  .top-news-container {
    max-width: 90%;
  }
  .top-news-card-child {
    display: block;
  }
}
</style>
