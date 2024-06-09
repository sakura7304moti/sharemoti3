<template>
  <q-page class=""> </q-page>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
export default defineComponent({
  name: 'holo-page-index',
  setup() {
    const router = useRouter();
    return { router };
  },
});
</script>
<style>
.index-page-card {
  width: 100%;
  max-width: 200px;
}
</style>
