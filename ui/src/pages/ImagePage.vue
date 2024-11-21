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
        <div class="flipDown">
          <img class="content-img" :src="imageUrl(rec.id)" />
        </div>
        <div class="text-grey">
          <span class="q-pr-sm">最終更新日</span><span class="q-pr-sm">:</span>
          {{ rec.createAt < rec.updateAt ? rec.updateAt : rec.createAt }}
        </div>
      </div>
    </div>
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
import api from 'src/api/main/ImageListApi';
export default defineComponent({
  name: 'image-page',
  setup() {
    const isShowTopButton = ref(false);
    const loadState = ref({
      isSave: false,
      isSearch: false,
      isDelete: false,
    } as LoadState);
    const pageNo = ref(1);
    const maxPage = ref(1);

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

    const onScrollSearch = async function () {
      console.log('scroll called');
      if (!loadState.value.isSearch && pageNo.value < maxPage.value) {
        console.log('scroll search...');
        pageNo.value = pageNo.value + 1;
        await search(pageNo.value);
      }
    };
    const handleScroll = () => {
      const bottomOfWindow =
        window.innerHeight + window.scrollY >=
        document.documentElement.offsetHeight - 200;

      if (bottomOfWindow && !loadState.value.isSearch) {
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

    const onMount = function () {
      window.addEventListener('scroll', handleScroll);
      window.addEventListener('scroll', setTopBtn);
    };

    onMount();
    return {
      isShowTopButton,
      loadState,
      pageNo,
      maxPage,
      records,
      search,
      imageUrl,
      onTopClick,
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
  max-width: 680px;
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
@media (max-width: 680px) {
  .content-title {
    line-height: 20px;
    font-size: 18px;
  }
  .content-detail {
    max-width: 100%;
    line-height: 20px;
  }
}
/* 下へ */
.flipDown {
  animation-name: flipDownAnime;
  animation-duration: 1.5s;
  animation-fill-mode: forwards;
  opacity: 0;
}

@keyframes flipDownAnime {
  from {
    transform: perspective(2500px) rotateX(100deg);
    opacity: 0;
  }

  to {
    transform: perspective(2500px) rotateX(0);
    opacity: 1;
  }
}
/* 左へ */
.flipLeft {
  animation-name: flipLeftAnime;
  animation-duration: 1s;
  animation-fill-mode: forwards;
  perspective-origin: left center;
  opacity: 0;
}

@keyframes flipLeftAnime {
  from {
    transform: perspective(600px) translate3d(0, 0, 0) rotateY(30deg);
    opacity: 0;
  }

  to {
    transform: perspective(600px) translate3d(0, 0, 0) rotateY(0deg);
    opacity: 1;
  }
}
</style>
