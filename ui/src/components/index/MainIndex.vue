<template>
  <!--ページリンク一覧-->
  <div class="q-pt-md text-h4"></div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
export default defineComponent({
  name: 'main-index',
  setup() {
    const router = useRouter();
    return {
      router,
    };
  },
});
</script>
<style>
.index-page-card {
  width: 100%;
  max-width: 250px;
}
</style>
