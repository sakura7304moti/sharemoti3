<template>
  <q-page class="">
    <karaoke-list-table v-model="filter" :height="pageHeight" />
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import KaraokeListTable from 'src/components/tables/KaraokeListTable.vue';
export default defineComponent({
  name: 'karaoke-list',
  components: {
    'karaoke-list-table': KaraokeListTable,
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
