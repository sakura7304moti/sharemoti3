<template>
  <q-page class="">
    <div class="text-h6">リフォーム履歴</div>
    <div v-for="rec in records" :key="rec.createAt.toString()">
      <historyCard :dataState="rec" />
    </div>
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import HistoryCard from 'src/components/HistoryCard.vue';
export default defineComponent({
  name: 'renovation-history',
  components: { historyCard: HistoryCard },
  setup() {
    //ここに履歴を書く
    const records = ref([
      {
        contents: [
          '俳句とホロ歌のページで、前回開いたときの表示形式を保持するようにした',
          'ページに使用する画像をサーバーの画像ではなく、googleDriveの画像を読み取るようにした',
        ],
        createAt: new Date(2023, 10, 26),
      },
    ] as DataState[]);
    return { records };
  },
});
interface DataState {
  contents: string[];
  createAt: Date;
}
</script>
