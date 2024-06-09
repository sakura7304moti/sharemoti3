<template>
  <q-card class="history-card">
    <q-card-section>
      <div class="text-h6">更新日：{{ formatDate(state.createAt) }}</div>
      <q-separator />
      <div>
        <ul>
          <li v-for="text in state.contents" :key="text">
            {{ text }}
          </li>
        </ul>
      </div>
    </q-card-section>
  </q-card>
</template>
<script lang="ts">
import { PropType, defineComponent } from 'vue';
import { useViewSupport } from 'src/utils/viewSupport';
const { formatDate } = useViewSupport();
export default defineComponent({
  name: 'renovation-history-card',
  props: {
    dataState: {
      type: Object as PropType<CardState>,
    },
  },
  setup(props) {
    const state = props.dataState as CardState;
    return { state, formatDate };
  },
});
interface CardState {
  contents: string[];
  createAt: Date;
}
</script>
<style>
/*カード全体 */
.history-card {
  width: 500px;
  height: 300px;
}
</style>
