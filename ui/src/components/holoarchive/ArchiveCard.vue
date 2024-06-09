<template>
  <img
    :src="state.thumbnailUrl"
    class="holo-archive-card"
    style="cursor: pointer"
    @click.prevent="playMovie"
  />
  <div
    class="row"
    style="max-width: 240px; cursor: pointer"
    @click.prevent="playMovie"
  >
    <div style="width: 20%">
      <q-avatar>
        <img :src="state.avatarUrl" />
      </q-avatar>
    </div>
    <div style="width: 80%">
      <div class="text-weight-bold">{{ state.title }}</div>
      <div style="width: 100%">
        {{ displayDateByDate(state.date) }}
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, PropType, ref } from 'vue';
import { useViewSupport } from 'src/utils/viewSupport';
import { useHoloArchiveStore } from 'src/stores/HoloArchiveStore';
export default defineComponent({
  name: 'holo-archive-card',
  props: {
    dataState: {
      type: Object as PropType<DataState>,
      required: true,
    },
  },
  setup(props) {
    const store = useHoloArchiveStore();
    const { displayDateByDate } = useViewSupport();
    const state = ref(props.dataState);
    const playMovie = function () {
      store.setPlayMovie(state.value.url);
    };
    return { state, displayDateByDate, playMovie };
  },
});
interface DataState {
  id: string;
  url: string;
  title: string;
  date: Date;
  channelId: string;
  avatarUrl: string;
  viewCount: number;
  thumbnailUrl: string;
  movieType: 'movie' | 'live' | 'short';
}
</script>
<style>
.holo-archive-card {
  max-width: 240px;
  border-radius: 10px;
}
</style>
