<template>
  <q-page class="">
    <table-yaki-list v-model="filter" :height="pageHeight" />
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import YakiListTable from 'components/tables/YakiListTable.vue';
export default defineComponent({
  name: 'yaki-list',
  components: {
    'table-yaki-list': YakiListTable,
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
