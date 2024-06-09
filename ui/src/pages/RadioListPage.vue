<template>
  <q-page class="">
    <radio-list-table :height="pageHeight" />
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import RadioListTable from 'src/components/tables/RadioListTable.vue';
export default defineComponent({
  name: 'karaoke-list',
  components: {
    'radio-list-table': RadioListTable,
  },
  setup() {
    const pageHeight = ref(document.documentElement.scrollHeight * 0.85);
    return {
      pageHeight,
    };
  },
});
</script>
