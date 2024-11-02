<template>
  <router-view />
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
});
// リロード回数を記録するために、`sessionStorage`を使用
if (sessionStorage.getItem('reloaded') !== 'true') {
  window.addEventListener('error', (event) => {
    if (
      (event.message && event.message.includes('404')) ||
      (event.error && event.error.message.includes('404'))
    ) {
      // 初回の404エラーのみリロード
      sessionStorage.setItem('reloaded', 'true');
      window.location.reload();
    }
  });
}
</script>
