<template>
  <q-page class="">
    <name-list-table v-model="filter" :height="pageHeight" />
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import NameListTable from 'components/tables/NameListTable.vue';
export default defineComponent({
  name: 'word-list',
  components: {
    'name-list-table': NameListTable,
  },
  setup() {
    const pageHeight = ref(document.documentElement.scrollHeight * 0.85);
    return {
      filter: ref(''),
      pageHeight,
    };
  },
});
</script>
