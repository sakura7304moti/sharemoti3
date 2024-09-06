<template>
  <div class="image-container">
    <img
      src="https://www.kanazawa-it.ac.jp/h1s/images/common/page_title/page_title_about_2x.jpg"
      alt="Image"
      class="image"
    />
    <div class="text-overlay">
      {{ text }}
    </div>
  </div>
</template>
<script lang="ts">
import { computed, defineComponent } from 'vue';
export default defineComponent({
  name: 'school-slogan',
  props: {
    modelValue: {
      type: String,
      requered: true,
    },
  },
  setup(props) {
    const text = computed(() => props.modelValue);
    return { text };
  },
});
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

.image-container {
  position: relative; /* 親要素を相対位置に設定 */
  display: inline-block; /* 画像のサイズに合わせる */
}

.image {
  display: block; /* 画像の下に余白を作らない */
  max-width: 100%;
  width: 100%;
  height: auto;
  object-fit: cover;
}

.text-overlay {
  font-size: 32px;
  font-family: 'Bebas Neue';
  font-weight: 700; /* 太字 */
  position: absolute; /* 絶対位置で配置 */
  top: 20%; /* 垂直方向中央 */
  left: 50%; /* 水平方向中央 */
  transform: translate(-50%, -20%); /* 位置調整 */
  color: white; /* 文字の色を白に設定 */
  font-weight: bold; /* 太字に設定 */
  text-align: center; /* 中央揃え */
  width: 95%; /* 必要に応じて調整可能 */
  white-space: pre-wrap;
  word-wrap: break-word;
  padding: 10px; /* 余白を追加 */
  box-sizing: border-box; /* パディングを含めてサイズ計算 */
}

@media screen and (max-width: 600px) {
  .text-overlay {
    font-size: 24px;
  }
}
</style>
