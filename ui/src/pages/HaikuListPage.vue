<template>
  <q-page class="">
    <q-toggle v-model="tableView" label="テーブル表示" />
    <haiku-list-table
      v-if="tableView"
      v-model="tableFilter"
      :height="tableHeight"
    />
    <haiku-list-component v-else v-model="listFilter" />
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
import { defineComponent, ref, watch } from 'vue';
import HaikuList from 'components/HaikuList.vue';
import HaikuListTable from 'src/components/tables/HaikuListTable.vue';
import { LocalStrageObject } from 'src/utils/localStrageSupport';
export default defineComponent({
  name: 'haiku-list',
  components: {
    'haiku-list-component': HaikuList,
    'haiku-list-table': HaikuListTable,
  },
  setup() {
    const tableView = ref(false);

    /*LocalStrage */
    const lsKey = 'haiku-list';
    const ls = new LocalStrageObject();
    const obj = ls.getterValue<HaikuDisplay>(lsKey);
    console.log('ls', obj);
    //すでに値がある場合はそれを元に表示モードを設定する
    if (obj) {
      if (obj.list) {
        tableView.value = false;
      } else {
        tableView.value = true;
      }
    }
    //値がない場合は初期値で値をセットする
    else {
      ls.setterValue<HaikuDisplay>(lsKey, { list: true, table: false });
    }

    //tableViewを監視して変更があれば、それに合わせてlocalStrageを変更させる
    const changeTableView = function () {
      if (tableView.value) {
        ls.setterValue<HaikuDisplay>(lsKey, { list: false, table: true });
      } else {
        ls.setterValue<HaikuDisplay>(lsKey, { list: true, table: false });
      }
    };
    watch(tableView, () => {
      changeTableView();
    });

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
      tableView,
      listFilter: ref(''),
      tableFilter: ref(''),
      tableHeight: ref(document.documentElement.scrollHeight * 0.85),
      changeTableView,
      isShowTopButton,
      onTopScrollClick,
    };
  },
});
interface HaikuDisplay {
  list: boolean;
  table: boolean;
}
</script>
<style>
@font-face {
  font-family: 'haiku';
  src: url(../fonts/haiku2.ttf) format('truetype');
}
@font-face {
  font-family: 'HinaMincho-Regular';
  src: url(../fonts/HinaMincho-Regular.ttf) format('truetype');
}
</style>
