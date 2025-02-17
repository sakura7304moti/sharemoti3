<template>
  <q-page class="">
    <div style="display: flex; flex-wrap: wrap">
      <div style="height: 100%; padding-right: 32px">
        <img
          src="../assets/movie_icon.webp"
          style="
            max-width: calc(min(90vw, 400px));
            width: 100%;
            height: 100%;
            object-fit: contain;
          "
        />
        <div class="q-my-md" style="margin-bottom: 24px">
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
            <div>
              <a
                href="#/movie/hashtag"
                @click.prevent.stop="onNavigateHashtag"
                class="nav-text text-subtitle1"
              >
                <q-icon name="tag" />
                ハッシュタグを編集する
              </a>
            </div>
          </div>
        </div>
      </div>
      <div style="max-width: 400px; width: 100%">
        <q-card id="search-card">
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
            <div class="q-mt-lg" v-if="false">
              <div class="text-subtitle1">表示方法</div>
              <!--表示条件に応じて表示を切り替えたい(API)-->
              <div>
                <q-radio
                  @update:model-value="onSearchClick"
                  v-model="searchCondition.mode"
                  :val="1"
                  label="サムネ"
                />
                <q-radio
                  @update:model-value="onSearchClick"
                  v-model="searchCondition.mode"
                  :val="2"
                  label="リスト"
                />
                <q-radio
                  @update:model-value="onSearchClick"
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
                @click="
                  page = 1;
                  searchMovie();
                "
                :loading="isLoading"
              />
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!--検索結果-->
    <div
      class="q-mt-md"
      v-if="searchCondition.mode == 1"
      style="display: flex; flex-wrap: wrap; /* 画面幅に応じて折り返し */"
    >
      <div
        v-for="mv in pageState.records"
        :key="mv.id"
        class="q-mb-lg"
        style="max-width: 400px; width: 100%"
      >
        <div style="max-width: 400px; margin-bottom: 80px; padding-right: 32px">
          <div class="content-title" @click="onNavigateEdit(mv.id)">
            <q-tooltip class="text-subtitle2"> 動画の内容を変更する </q-tooltip>
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
          <div class="q-mt-sm">
            <q-avatar>
              <img
                :src="
                  mv.staffCd == 1
                    ? 'src/assets/legoman_profile.jpg'
                    : 'src/assets/yosao.png'
                "
              />
            </q-avatar>
            <span class="q-ml-sm">{{ mv.staffName }}</span>
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
    <div class="q-mt-md" v-if="searchCondition.mode == 2">
      <q-markup-table>
        <thead>
          <tr>
            <th style="min-width: 200px"></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="mv in pageState.records" :key="mv.id">
            <td>
              <q-btn class="q-ma-md" @click="playId = mv.id"
                ><img
                  class="thumbnail image"
                  :src="getThumbnailLink(mv.fileName)"
              /></q-btn>
            </td>
            <td style="height: 100%">
              <q-video
                v-if="playId == mv.id"
                class="q-ma-md thumbnail"
                :src="getDownloadLink(mv.fileName)"
                style="min-width: 100%; max-width: 600px; width: 100%"
                :ratio="16 / 9"
              />
              <div class="text-subtitle1">
                {{ mv.title }}
              </div>
              <div class="q-ml-md">
                <div class="text-body2">
                  {{ mv.detail }}
                </div>
                <div>
                  <span
                    class="content-hashtag"
                    v-for="tag in mv.hashtags"
                    :key="tag.name"
                    @click="onHashtagClick(tag.name)"
                    >#{{ tag.name }}</span
                  >
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </q-markup-table>
    </div>
    <!--ロード-->
    <div class="text-center" v-if="page > 1 && isLoading">
      <q-spinner color="primary" size="md" class="q-mr-md" /><sapn
        >読み込み中...</sapn
      >
    </div>
    <!--スクロールボタン-->
    <button v-if="isShowTopButton" class="scroll-to-top" @click="onTopClick">
      <img
        style="height: 70px"
        class="holotwitter-top-scroll-img"
        src="../assets/Rocket Base 512x512.png"
      />
      <div>トップに戻る</div>
    </button>
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useMovieModel } from 'src/models/MovieModels';
import { useRouter } from 'vue-router';
export default defineComponent({
  name: 'movie-page',
  setup() {
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

    // スクロール系
    const isShowTopButton = ref(false);
    const onScrollSearch = async function () {
      console.log('scroll called', !isLoading);
      if (isLoading.value == false && page.value < pageState.value.totalCount) {
        console.log('scroll search...');
        page.value = page.value + 1;
        await searchMovie();
      }
    };
    const handleScroll = () => {
      const bottomOfWindow =
        window.innerHeight + window.scrollY >=
        document.documentElement.offsetHeight - 200;

      if (
        bottomOfWindow &&
        !isLoading.value &&
        searchCondition.value.mode != 2
      ) {
        onScrollSearch();
      }
    };

    const onTopClick = function () {
      // スムーズにページのトップに戻る
      window.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    };

    const setTopBtn = function () {
      isShowTopButton.value = window.scrollY > 100;
    };

    searchMovie();
    getHashtags();
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('scroll', setTopBtn);

    const onNavigateUpload = function () {
      router.push('/movie/upload');
    };

    const onNavigateEdit = function (id: number) {
      router.push('/movie/edit?id=' + id);
    };

    const onNavigateHashtag = function () {
      router.push('/movie/hashtag');
    };

    const onHashtagClick = function (name: string) {
      // 検索
      searchCondition.value.hashtag = name;
      page.value = 1;
      searchMovie();

      // スクロール
      if (window.scrollY < 400) {
        return;
      }
      const element = document.getElementById('search-card');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    };

    const onSearchClick = function () {
      page.value = 1;
      searchMovie();
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
      onNavigateHashtag,
      onSearchClick,
      // navi
      onNavigateUpload,
      onNavigateEdit,
      // スクロール
      isShowTopButton,
      onTopClick,
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
  cursor: pointer;
  color: rgb(24, 191, 160);
  line-height: 30px;
  font-size: 20px;
  font-weight: 700;
  white-space: pre-wrap;
  font-family: 'Noto Sans JP';
}
.content-title:hover {
  transition: 0.4s;
  opacity: 0.5;
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
