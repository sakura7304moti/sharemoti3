<template>
  <q-page class="">
    <div class="text-h6">名画伯展覧会</div>
    <!--追加・検索・削除ボタン表示エリア-->
    <div></div>

    <!--画像表示エリア-->
    <div>
      <div v-for="rec in records" :key="rec.id" class="content-card">
        <div class="content-title">
          {{ rec.title }}
        </div>
        <div class="content-detail">
          {{ rec.detail }}
        </div>
        <div>
          <img class="content-img" :src="imageUrl(rec.id)" />
        </div>
        <div class="text-grey">
          <span class="q-pr-sm">最終更新日</span><span class="q-pr-sm">:</span>
          {{ rec.createAt < rec.updateAt ? rec.updateAt : rec.createAt }}
        </div>
      </div>
    </div>
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import api from 'src/api/main/ImageListApi';
export default defineComponent({
  name: 'image-page',
  setup() {
    const loadState = ref({
      isSave: false,
      isSearch: false,
      isDelete: false,
    } as LoadState);
    const pageNo = ref(1);
    const maxPage = ref(0);

    const records = ref([] as Image[]);

    const search = async function (page: number) {
      loadState.value.isSearch = true;
      await api.search(page).then((response) => {
        if (response) {
          console.log('search response', response);
          maxPage.value = response.totalCount;
          response.records.forEach((it) => records.value.push(it));
        }
      });
      loadState.value.isSearch = false;
    };

    const imageUrl = function (id: number) {
      return api.imageUrl(id);
    };
    search(pageNo.value);
    return {
      loadState,
      pageNo,
      maxPage,
      records,
      search,
      imageUrl,
    };
  },
});
interface LoadState {
  isSave: boolean;
  isSearch: boolean;
  isDelete: boolean;
}
interface Image {
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
.content-card {
  max-width: 800px;
  margin-bottom: 48px;
  padding: 16px;
}
.content-title {
  color: rgb(24, 191, 160);
  line-height: 30px;
  font-size: 20px;
  font-weight: 700;
  white-space: pre-wrap;
  font-family: 'Noto Sans JP';
}
.content-detail {
  max-width: 50%;
  margin-left: 8px;
  padding: 8px 0;
  color: rgb(15, 20, 25);
  line-height: 24px;
  font-size: 13px;
  font-family: 'Noto Sans JP';
  white-space: pre-wrap;
  font-weight: 500;
}
.content-img {
  max-width: 100%;
  width: 100%;
  max-height: 70vh;
  height: 100;
  object-fit: contain;
  object-position: left;
}
@media (max-width: 800px) {
  .content-title {
    line-height: 20px;
    font-size: 18px;
  }
  .content-detail {
    max-width: 100%;
    line-height: 20px;
  }
}
</style>
