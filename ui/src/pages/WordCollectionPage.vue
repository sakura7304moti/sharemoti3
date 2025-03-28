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
              <span class="text-bold">
                <span v-if="searchCondition.kinen == null"> xxxこ記念 </span>
                <span v-else> {{ searchCondition.kinen }}こ記念！ </span>
              </span>
            </div>
            <q-select
              v-model="searchCondition.kinen"
              :options="kinenList"
              dense
              outlined
              class="bg-white"
              clearable
              style="min-width: 100px"
              @update:model-value="
                resetYear();
                searchWord();
              "
            />
          </div>

          <!--検索条件 年-->
          <div>
            <div class="text-subtitle1">
              <span class="text-bold">
                <span v-if="searchCondition.year == null"> 20xx年 </span>
                <span v-else> {{ searchCondition.year }}年まとめ！ </span>
              </span>
            </div>
            <q-select
              v-model="searchCondition.year"
              :options="yearList"
              dense
              outlined
              class="bg-white"
              clearable
              style="min-width: 100px"
              @update:model-value="
                resetKinen();
                searchWord();
              "
            />
          </div>
        </div>
        <div style="max-width: 1065px" class="text-right">
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
      <div v-for="(rec, index) in records" :key="rec.id" class="search-card">
        <!--日付表示用-->
        <div v-if="isDateDisplay()">
          <!--日付異なるよ条件 ・前回の行と比較して作成日が異なれば日付を表示する-->
          <div
            v-if="
              records[index].updateAt !=
                records[Math.max(index - 1, 0)].updateAt || index == 0
            "
          >
            <div class="last-date">{{ formatDateWithDay(rec.updateAt) }}</div>
          </div>
        </div>
        <!--記念用の連番-->
        <div
          class="q-mt-sm no"
          :class="{ 'q-ml-sm': isDateDisplay() }"
          v-if="searchCondition.kinen != null && !load.search"
        >
          {{ rec.wordRank + searchCondition.kinen - 500 }}
        </div>

        <div :class="{ 'q-ml-sm': isDateDisplay() }">
          <div class="word-space">
            <div class="word">
              {{ rec.word }}
            </div>
          </div>
          <div class="word-space q-ml-sm">
            <div class="detail">
              {{ rec.detail }}
            </div>
          </div>
          <div class="text-right text-grey date" v-if="!isDateDisplay()">
            {{ rec.updateAt > rec.createAt ? rec.updateAt : rec.createAt }}
          </div>
          <q-separator />
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
      yearList,
      searchWord,
      getKinenList,
      getYearList,
    } = useWordCollectionModel();
    getKinenList();
    getYearList();
    searchWord();

    const resetDateOrder = function () {
      searchCondition.value.dateOrder = '';
    };
    const resetTextOrder = function () {
      searchCondition.value.textOrder = '';
    };
    const resetKinen = function () {
      searchCondition.value.kinen = null;
    };
    const resetYear = function () {
      searchCondition.value.year = null;
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

    function formatDateWithDay(dateStr: string): string {
      // 曜日つきの日付に変換
      const date = new Date(`${dateStr}T00:00:00+09:00`);
      const daysOfWeek = ['日', '月', '火', '水', '木', '金', '土'];
      const dayOfWeek = daysOfWeek[date.getDay()];
      return `${dateStr} (${dayOfWeek})`;
    }

    function isDateDisplay() {
      // 緑色の日付の表示フラグ
      if (
        searchCondition.value.kinen != null &&
        searchCondition.value.textOrder == '' &&
        searchCondition.value.dateOrder == ''
      ) {
        return false;
      }
      return searchCondition.value.textOrder == '';
    }

    return {
      load,
      searchCondition,
      records,
      kinenList,
      yearList,
      searchWord,
      getKinenList,
      getYearList,
      // scroll
      isShowTopButton,
      onTopScrollClick,
      // search
      resetDateOrder,
      resetTextOrder,
      resetKinen,
      resetYear,
      // date display
      formatDateWithDay,
      isDateDisplay,
    };
  },
});
</script>
<style>
.search-form {
  background-color: white;
  border-radius: 10px;
  padding: 16px;
  max-width: 1130px;
  width: 100%;
}
/*
@media (max-width: 800px) {
  .scroll-to-top {
    display: block;
  }
}*/
.date {
  font-size: 14px;
  font-family: serif;
}
.last-date {
  font-size: 24px;
  color: rgb(0, 167, 137);
  font-family: serif;
  margin-bottom: 8px;
}
.no {
  font-size: 14px;
  font-family: serif;
}
.word-space {
  text-align: left;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: serif;
  .word {
    font-size: 24px;
    font-weight: 550;
  }
  .detail {
    font-size: 16px;
  }
}
.search-card {
  margin-bottom: 24px;
  /*max-width: calc(min(800px, 100vw - 130px));*/
  max-width: 800px;
}
@media (max-width: 800px) {
  .word-space {
    .word {
      font-size: 20px;
    }
    .detail {
      font-size: 14px;
    }
  }
  .date {
    font-size: 12px;
  }

  .search-card {
    margin-bottom: 16px;
  }
}
</style>
