<template>
  <q-page class=""> </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import api from 'src/api/scraper/HoloArchiveApi';
export default defineComponent({
  name: 'component-test',
  setup() {
    const pageHeight = ref(document.documentElement.scrollHeight * 0.85);
    api.search().then((it) => console.log('archive', it));
    api.channels().then((it) => console.log('channels', it));
    return {
      filter: ref(''),
      pageHeight,
    };
  },
});
</script>
