<template>
  <q-page class="">
    <div class="holo-page-title q-pb-md">pixiv</div>
    <search-area />
    <div class="row wrap" style="max-width: 1200px">
      <div v-for="illust in illusts" :key="illust.id">
        <image-card :illust-id="illust.id" />
      </div>
    </div>
    <div class="q-pt-md">
      <q-pagination
        v-model="condition.pageNo"
        :max="pageState.pageCount"
        :max-pages="10"
        input
        v-if="pageState.records.length > 0"
      />
    </div>
  </q-page>
</template>
<script lang="ts">
import { PixivSearchStore } from 'src/stores/pixiv/PixivSearchStore';
import PixivSearchArea from 'src/components/pixiv/PixivSearchArea.vue';
import PixivImageCard from 'src/components/pixiv/PixivImageCard.vue';
import { computed, defineComponent, ref } from 'vue';
export default defineComponent({
  name: 'pixiv-top',
  components: {
    'search-area': PixivSearchArea,
    'image-card': PixivImageCard,
  },
  setup() {
    const store = PixivSearchStore();

    const onSearchClick = function () {
      store.searchIllust();
    };

    const condition = ref(store.condition);
    const pageState = ref(store.pageState);

    store.searchHashtags();
    store.searchUsers();
    const illusts = computed(() => store.pageState.records);

    return {
      condition,
      pageState,
      illusts,
      onSearchClick,
    };
  },
});
</script>
