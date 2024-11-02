<template>
  <router-view />
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
});
window.addEventListener('error', (event) => {
  if (event.message.includes('Failed to fetch dynamically')) {
    // エラーをキャッチしたら自動リロード
    window.location.reload();
  }
});
</script>
