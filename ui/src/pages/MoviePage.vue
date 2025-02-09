<template>
  <q-page class="">
    <img
      src="../assets/movie_icon.webp"
      style="
        max-width: calc(min(90vw, 400px));
        width: 100%;
        height: 100%;
        object-fit: contain;
      "
    />
    <div class="q-my-md" style="margin-bottom: 48px">
      <div class="text-subtitle1">登録・編集は以下のリンクから！</div>
      <div class="q-ml-md row q-gutter-md">
        <div class="q-mr-md">
          <a
            href="/#/movie/upload"
            @click.prevent.stop="onNavigateUpload"
            class="nav-text text-subtitle1"
          >
            <q-icon name="upload" />
            動画を投稿する
          </a>
        </div>
        <div class="q-mr-md">
          <a href="#" class="nav-text text-subtitle1">
            <q-icon name="edit" />
            動画を編集する
          </a>
        </div>
        <div>
          <a href="#" class="nav-text text-subtitle1">
            <q-icon name="tag" />
            ハッシュタグを編集する
          </a>
        </div>
      </div>
    </div>
    <q-card style="max-width: 400px" id="search-card">
      <q-card-section>
        <div class="text-subtitle1">検索条件</div>
        <div class="q-pt-xs row q-gutter-md" style="padding-left: 12px">
          <div style="max-width: 300px; width: 100%">
            <q-input
              outlined
              dense
              stack-label
              v-model="searchCondition.keyword"
              label="キーワード"
              class="bg-white"
            />
          </div>
          <div style="max-width: 300px; width: 100%">
            <q-select
              outlined
              dense
              stack-label
              :options="hashtags"
              v-model="searchCondition.hashtag"
              label="ハッシュタグ"
              class="bg-white"
              clearable
              @update:model-value="onHashtagClick($event)"
            />
          </div>
        </div>
        <div class="q-mt-lg">
          <div class="text-subtitle1">表示方法</div>
          <!--表示条件に応じて表示を切り替えたい(API)-->
          <div>
            <q-radio v-model="searchCondition.mode" :val="1" label="サムネ" />
            <q-radio v-model="searchCondition.mode" :val="2" label="リスト" />
            <q-radio
              v-model="searchCondition.mode"
              :val="3"
              label="シリーズ別"
            />
          </div>
        </div>
        <div class="text-right q-mt-md">
          <q-btn
            label="検索"
            color="primary"
            icon="search"
            @click="searchMovie"
            :loading="isLoading"
          />
        </div>
      </q-card-section>
    </q-card>

    <!--検索結果-->
    <div class="q-mt-md">
      <div v-for="mv in pageState.records" :key="mv.id" class="q-mb-lg">
        <div style="max-width: 400px; margin-bottom: 80px">
          <div class="content-title">
            {{ mv.title }}
          </div>
          <div class="content-detail" v-if="mv.detail">{{ mv.detail }}</div>
          <div>
            <span
              class="content-hashtag"
              v-for="tag in mv.hashtags"
              :key="tag.name"
              @click="onHashtagClick(tag.name)"
              >#{{ tag.name }}</span
            >
          </div>
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
import { useRoute, useRouter } from 'vue-router';
export default defineComponent({
  name: 'movie-page',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const {
      playId,
      isLoading,
      page,
      searchCondition,
      pageState,
      hashtags,
      searchMovie,
      getDownloadLink,
      getThumbnailLink,
      getHashtags,
    } = useMovieModel();
    searchMovie();
    getHashtags();

    const onNavigateUpload = function () {
      router.push('/movie/upload');
    };

    const onHashtagClick = function (name: string) {
      // 検索
      searchCondition.value.hashtag = name;
      page.value = 1;
      searchMovie();

      // スクロール
      const element = document.getElementById('search-card');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    };

    return {
      playId,
      isLoading,
      page,
      searchCondition,
      pageState,
      hashtags,
      searchMovie,
      getDownloadLink,
      getThumbnailLink,
      getHashtags,
      onHashtagClick,
      // navi
      onNavigateUpload,
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
.content-hashtag {
  cursor: pointer;
  color: var(--q-primary);
  margin-right: 16px;
}
.content-hashtag:hover {
  color: orange;
  transition: 0.4s;
}
.nav-text {
  color: var(--q-primary);
  font-weight: bolder;
}
.nav-text:hover {
  color: orange;
  transition: 0.4s;
}
</style>
