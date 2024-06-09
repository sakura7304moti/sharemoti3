<template>
  <q-page class="">
    <word-list-table v-model="filter" :height="pageHeight" />
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import WordListTable from 'src/components/tables/WordListTable.vue';
export default defineComponent({
  name: 'word-list',
  components: {
    'word-list-table': WordListTable,
  },
  setup() {
    const pageHeight = ref(document.documentElement.scrollHeight * 0.85);
    const filter = ref('');
    return {
      filter,
      pageHeight,
    };
  },
});
</script>
