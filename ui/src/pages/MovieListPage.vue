<template>
  <q-page class="">
    <movie-list-table :height="pageHeight" />
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import MovieListTable from 'src/components/tables/MovieListTable.vue';
export default defineComponent({
  name: 'movie-list',
  components: {
    'movie-list-table': MovieListTable,
  },
  setup() {
    const pageHeight = ref(document.documentElement.scrollHeight * 0.85);
    return { pageHeight };
  },
});
</script>
