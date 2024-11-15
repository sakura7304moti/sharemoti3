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
    <div style="margin-top: 32px">
      <div>
        <span
          ><img
            src="../assets/lief-left.png"
            style="width: 40px; height: 40px; object-fit: contain"
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
    </div>
  </q-page>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import api from 'src/api/file/TopImageApi';
import { TopNewsApi } from 'src/api/file/TopNewsApi';
export default defineComponent({
  name: 'IndexPage',
  setup() {
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
      await newsApi.news(newsCondition.value).then((response) => {
        if (response) {
          console.log('news', response);
          newsDataState.value.totalCount = response.totalCount;
          newsDataState.value.records = response.records;
        }
      });
    };
    getNews();
    return { imageUrl };
  },
});
interface NewsDataState {
  records: Array<TopNews>;
  totalCount: number;
}

interface TopNews {
  page: string;
  createAt: string;
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
</style>
