<template>
  <q-page class="">
    <div class="top-image-container zoomIn">
      <div
        style="
          margin-left: 16px;
          margin-bottom: 8px;
          font-size: 32px;
          font-family: serif;
        "
      >
        今日の一枚
      </div>
      <div
        style="
          text-align: left;
          max-width: 100vw;
          width: 100%;
          padding-bottom: 16px;
        "
      >
        <img :src="imageUrl" class="top-image fadeDown" />
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import api from 'src/api/file/TopImageApi';
export default defineComponent({
  name: 'IndexPage',
  setup() {
    const router = useRouter();
    const imageUrl = computed(() => api.singleImageUrl());
    return { imageUrl };
  },
});
</script>
<style>
/*画像 */
.top-image {
  max-width: 50vw;
  width: 100%;
  max-height: 50vh;
  height: 100%;
  display: inline-block;
  object-fit: contain;
  padding-left: 16px;
  padding-right: 16px;
}
.top-image-container {
  background-color: white;
  max-width: 50vw;
  border-radius: 20px;
  box-shadow: 10px;
}
@media (max-width: 1030px) {
  .top-image {
    max-width: 100vw;
  }
  .top-image-container {
    max-width: 100vw;
  }
}
</style>
