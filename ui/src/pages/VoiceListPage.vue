<template>
  <q-page class="">
    <voice-list-table v-model="filter" :height="pageHeight" />
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import VoiceListTable from 'src/components/tables/VoiceListTable.vue';
export default defineComponent({
  name: 'voice-list',
  components: {
    'voice-list-table': VoiceListTable,
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
