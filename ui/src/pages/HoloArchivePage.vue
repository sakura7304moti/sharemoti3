<template>
  <q-page class="">
    <div class="holo-page-title q-pb-md">アーカイブまとめ</div>
    <div style="display: flex; flex-wrap: wrap">
      <div style="width: 640px">
        <YouTube
          v-if="playUrl != ''"
          :src="playUrl"
          @ready="true"
          ref="youtube"
          :vars="{ autoplay: 1, rel: 0 }"
          :width="pageWidth"
        />
        <div class="q-pt-md"></div>
        <search-box />
      </div>
      <div style="flex-grow: 1">
        <div style="display: flex; flex-wrap: wrap">
          <div style="display: flex; flex-wrap: wrap" id="holo-archive-cards">
            <div v-for="state in records" :key="state.id" class="q-pa-md">
              <archive-card
                :data-state="state"
                @search-start="searchStart"
                @search-end="searchEnd"
              />
            </div>
          </div>
        </div>
      </div>
      <q-pagination
        v-if="page.pageCount > 0 && !isLoading && records.length > 0"
        v-model="page.pageNo"
        :max="page.pageCount"
        max-pages="3"
        input
        direction-links
        @click="search"
      />
    </div>
  </q-page>
</template>
<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import SearchBox from 'src/components/holoarchive/SearchBox.vue';
import ArchiveCard from 'src/components/holoarchive/ArchiveCard.vue';
import { useHoloArchiveStore } from 'src/stores/HoloArchiveStore';
import YouTube from 'vue3-youtube';
export default defineComponent({
  name: 'holo-archive',
  components: {
    'search-box': SearchBox,
    'archive-card': ArchiveCard,
    YouTube,
  },
  setup() {
    const pageWidth = computed(() =>
      window.innerWidth > 640 ? 640 : window.innerWidth - 32
    );
    const store = useHoloArchiveStore();
    const records = computed(() => store.records);
    const playUrl = computed(() => store.playMovie);
    const isLoading = ref(false);

    const searchStart = function () {
      isLoading.value = true;
    };

    const searchEnd = function () {
      isLoading.value = false;
    };

    const page = ref(store.page);

    const search = function () {
      store.getMovies();

      const element = document.getElementById('holo-archive-cards');
      element?.scroll({ top: 0 });
    };

    return {
      pageWidth,
      records,
      playUrl,
      isLoading,
      page,
      searchStart,
      searchEnd,
      search,
    };
  },
});
</script>
