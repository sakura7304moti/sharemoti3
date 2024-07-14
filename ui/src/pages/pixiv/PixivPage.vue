<template>
  <q-page class="">
    <div class="holo-page-title q-pb-md">pixiv</div>
    <search-area
      :hashtags="condition.hashtags"
      :user-ids="condition.userIds"
      :min-total-bookmarks="condition.minTotalBookmarks"
      :min-total-view="condition.minTotalView"
    />

    <div class="row wrap" style="max-width: 1200px">
      <div v-for="illust in illusts" :key="illust.id">
        <image-card :illust-id="illust.id" />
      </div>
    </div>
  </q-page>
</template>
<script lang="ts">
import { PixivSearchStore } from 'src/stores/pixiv/PixivSearchStore';
import PixivSearchArea from 'src/components/pixiv/PixivSearchArea.vue';
import PixivImageCard from 'src/components/pixiv/PixivImageCard.vue';
import { computed, defineComponent } from 'vue';
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

    store.searchHashtags();
    store.searchUsers();
    const illusts = computed(() => store.pageState.records);

    return {
      condition: store.condition,
      pageState: store.pageState,
      illusts,
      onSearchClick,
    };
  },
});
</script>
