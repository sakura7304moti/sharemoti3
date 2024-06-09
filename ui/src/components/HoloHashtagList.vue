<template>
  <div>
    com
    <a href="#"><img src="../assets/holo_icon.jpg" /></a>
  </div>
</template>
<script lant="ts">
import { defineComponent, ref } from 'vue';
export default defineComponent({
  name: 'holo-hashtag-list',

  setup() {
    return {
      dialogShow: ref(false),
    };
  },
});
</script>
