<template>
  <q-page class="">
    <div class="row q-gutter-md">
      <div style="max-width: 200px">
        <q-input
          outlined
          dense
          stack-label
          v-model="searchCondition.keyword"
          label="キーワード"
          class="bg-white"
        />
      </div>
      <div>
        <q-btn
          label="検索"
          color="primary"
          icon="search"
          @click="searchMovie"
          :loading="isLoading"
        />
      </div>
    </div>

    <!--検索結果-->
    <div class="q-mt-md">
      <div v-for="mv in pageState.records" :key="mv.id" class="q-mb-lg">
        <div style="max-width: 400px">
          <div class="content-title">{{ mv.title }}</div>
          <div class="content-detail" v-if="mv.detail">{{ mv.detail }}</div>
          <img
            class="q-mt-sm thumbnail image"
            :src="getThumbnailLink(mv.fileName)"
            v-if="mv.id != playId"
            @click="playId = mv.id"
          />
          <q-video
            v-else
            class="q-mt-sm thumbnail"
            :src="getDownloadLink(mv.fileName)"
            style="min-width: 100%; max-width: 600px; width: 100%"
            :ratio="16 / 9"
          />
        </div>
      </div>
    </div>
  </q-page>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import { useMovieModel } from 'src/models/MovieModels';
export default defineComponent({
  name: 'movie-page',
  setup() {
    const {
      isLoading,
      playId,
      page,
      searchCondition,
      pageState,
      searchMovie,
      getDownloadLink,
      getThumbnailLink,
    } = useMovieModel();

    return {
      isLoading,
      playId,
      page,
      searchCondition,
      pageState,
      searchMovie,
      getDownloadLink,
      getThumbnailLink,
    };
  },
});
</script>
<style>
.thumbnail {
  max-width: 100%;
  width: 100%;
  max-height: 400px;
  height: 100%;
  object-fit: contain;
  cursor: pointer;
}
.thumbnail:hover.image {
  transition: 0.4s;
  opacity: 0.5;
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
  max-width: 100%;
  margin-left: 8px;
  padding: 8px 0;
  color: rgb(15, 20, 25);
  line-height: 24px;
  font-size: 13px;
  font-family: 'Noto Sans JP';
  white-space: pre-wrap;
  font-weight: 500;
}
</style>
