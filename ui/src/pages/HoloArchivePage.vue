<template>
  <q-page class="">
    <div class="holo-page-title q-pb-md" style="display: none">
      アーカイブまとめ
    </div>
    <div style="display: flex">
      <div style="width: 640px">
        <YouTube
          v-if="playUrl != ''"
          :src="playUrl"
          @ready="true"
          ref="youtube"
          :vars="{ autoplay: 1, rel: 0 }"
        />
        <div class="q-pt-md"></div>
        <search-box />
      </div>
      <div style="flex-grow: 1">
        <div style="display: flex; flex-wrap: wrap">
          <div
            style="
              display: flex;
              flex-wrap: wrap;
              overflow-y: auto;
              height: 80vh;
            "
            id="holo-archive-cards"
          >
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

    return { records, playUrl, isLoading, searchStart, searchEnd };
  },
});
</script>
