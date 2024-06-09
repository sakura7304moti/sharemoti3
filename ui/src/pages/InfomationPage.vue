<template>
  <q-page class="">
    <div id="page-main">
      <div class="text-h5 q-pb-md">お茶の間</div>
      <word-info />
      <div class="q-pb-lg"></div>
      <haiku-info />
      <div class="q-pb-lg"></div>
      <link-info />
    </div>
  </q-page>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import WordInfo from 'src/components/info/WordInfo.vue';
import HaikuInfo from 'src/components/info/HaikuInfo.vue';
import LinkInfo from 'src/components/info/LinkInfo.vue';
export default defineComponent({
  name: 'InfoPage',
  components: {
    'word-info': WordInfo,
    'haiku-info': HaikuInfo,
    'link-info': LinkInfo,
  },
  setup() {
    return {};
  },
});
</script>
