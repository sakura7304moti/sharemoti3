<template>
  <q-page class="">
    <div class="text-h6 q-mb-sm">名言コレクション</div>
    <!--検索枠-->
    <q-form @submit.prevent="searchWord">
      <div class="search-form q-mb-sm">
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
              val=""
              label="未指定"
              class="q-mr-sm"
              @update:model-value="
                resetTextOrder();
                searchWord();
              "
            />
            <q-radio
              v-model="searchCondition.dateOrder"
              val="desc"
              label="新しい順"
              class="q-mr-sm"
              @update:model-value="
                resetTextOrder();
                searchWord();
              "
            />
            <q-radio
              v-model="searchCondition.dateOrder"
              val="asc"
              label="古い順"
              @update:model-value="
                resetTextOrder();
                searchWord();
              "
            />
          </div>

          <!--検索条件 文字-->
          <div>
            <div class="text-subtitle1">
              <span class="text-bold">文字</span>の並び順
            </div>
            <q-radio
              v-model="searchCondition.textOrder"
              val=""
              label="未指定"
              class="q-mr-sm"
              @update:model-value="
                resetDateOrder();
                searchWord();
              "
            />
            <q-radio
              v-model="searchCondition.textOrder"
              val="asc"
              label="0123..."
              class="q-mr-sm"
              @update:model-value="
                resetDateOrder();
                searchWord();
              "
            />
            <q-radio
              v-model="searchCondition.textOrder"
              val="desc"
              label="漢字から..."
              @update:model-value="
                resetDateOrder();
                searchWord();
              "
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
              @update:model-value="searchWord()"
            />
          </div>
        </div>
        <div style="max-width: 890px" class="text-right">
          <q-btn
            label="検索"
            icon="search"
            color="primary"
            type="submit"
            :loading="load.search"
          />
          <span class="q-ml-md text-subtitle2">{{ records.length }}件</span>
        </div>
      </div>
    </q-form>

    <!--検索結果-->
    <div>
      <div
        v-for="rec in records"
        :key="rec.id"
        style="margin-bottom: 32px; max-width: 800px"
      >
        <div
          class="q-mt-sm"
          v-if="searchCondition.kinen != null && !load.search"
          style="font-size: 16px"
        >
          {{ rec.id }}
        </div>
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
            margin-left: 16px;
            text-align: left;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 14px;
          "
        >
          {{ rec.detail }}
        </div>
        <div class="text-right text-grey">
          {{ rec.updateAt > rec.createAt ? rec.updateAt : rec.createAt }}
        </div>
        <hr color="#D3D3D3" />
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

    const resetDateOrder = function () {
      searchCondition.value.dateOrder = '';
    };
    const resetTextOrder = function () {
      searchCondition.value.textOrder = '';
    };

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
      // search
      resetDateOrder,
      resetTextOrder,
    };
  },
});
</script>
<style>
.search-form {
  background-color: white;
  border-radius: 10px;
  padding: 16px;
  max-width: 930px;
  width: 100%;
}
</style>
