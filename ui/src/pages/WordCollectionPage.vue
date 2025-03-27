<template>
  <q-page class="">
    <div class="text-h6">名言コレクション</div>
    <div class="q-mb-md">
      <div class="text-subtitle1">
        <span class="text-bold">なにかおもろい感じにしたい...</span>
      </div>
      <img
        src="../assets/gottu_eyan.png"
        style="height: 150px; width: 150px; object-fit: contain"
      />
    </div>
    <!--検索枠-->
    <q-form @submit.prevent="searchWord">
      <div class="search-form">
        <div class="row q-gutter-md wrap q-mb-md">
          <!--検索条件 キーワード-->
          <div>
            <div class="text-subtitle1">
              <span class="text-bold">キーワード</span>
            </div>
            <q-input
              v-model="searchCondition.keyword"
              dense
              outlined
              class="bg-white"
            />
          </div>

          <!--検索条件 日付-->
          <div>
            <div class="text-subtitle1">
              <span class="text-bold">日付</span>の並び順
            </div>
            <q-radio
              v-model="searchCondition.dateOrder"
              val="desc"
              label="新しい順"
              class="q-mr-sm"
            />
            <q-radio
              v-model="searchCondition.dateOrder"
              val="asc"
              label="古い順"
            />
          </div>

          <!--検索条件 文字-->
          <div>
            <div class="text-subtitle1">
              <span class="text-bold">文字</span>の並び順
            </div>
            <q-radio
              v-model="searchCondition.textOrder"
              val="desc"
              label="0123..."
              class="q-mr-sm"
            />
            <q-radio
              v-model="searchCondition.textOrder"
              val="asc"
              label="漢字から..."
            />
          </div>

          <!--検索条件 記念-->
          <div>
            <div class="text-subtitle1">
              <span class="text-bold">xxx回記念</span>
            </div>
            <q-select
              v-model="searchCondition.kinen"
              :options="kinenList"
              dense
              outlined
              class="bg-white"
              clearable
              style="min-width: 100px"
            />
          </div>
        </div>
        <div style="max-width: 710px" class="text-right">
          <q-btn label="検索" icon="search" color="primary" type="submit" />
        </div>
      </div>
    </q-form>

    <!--検索結果-->
    <div>
      <div v-for="rec in records" :key="rec.id" style="margin-bottom: 32px">
        <div
          style="
            text-align: left;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 24px;
          "
        >
          {{ rec.word }}
        </div>
        <div
          style="
            text-align: left;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 16px;
          "
        >
          {{ rec.detail }}
        </div>
      </div>
    </div>

    <!-- ページトップに戻るボタン -->
    <button
      v-if="isShowTopButton"
      class="scroll-to-top"
      @click="onTopScrollClick"
    >
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
import { useWordCollectionModel } from 'src/models/WordCollectionModels';
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'word-collection-page',
  setup() {
    const {
      load,
      searchCondition,
      records,
      kinenList,
      searchWord,
      getKinenList,
    } = useWordCollectionModel();
    getKinenList();
    searchWord();

    const isShowTopButton = ref(false);
    const onTopScrollClick = function () {
      // スムーズにページのトップに戻る
      window.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    };

    const checkTopButton = function () {
      isShowTopButton.value = window.scrollY > 100;
    };

    window.addEventListener('scroll', checkTopButton);
    return {
      load,
      searchCondition,
      records,
      kinenList,
      searchWord,
      getKinenList,
      // scroll
      isShowTopButton,
      onTopScrollClick,
    };
  },
});
</script>
<style>
@media (max-width: 600px) {
  .search-form {
    background-color: white;
    border-radius: 10px;
    padding: 16px;
  }
}
</style>
