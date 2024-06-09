<template>
  <div class="balloon2-left">
    <p>{{ text }}</p>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'BallonLeft',
  props: {
    text: {
      type: String,
      requered: true,
    },
  },
  setup() {
    return {};
  },
});
</script>
<style>
.balloon2-left {
  position: relative;
  display: inline-block;
  margin: 1.5em 0 1.5em 15px;
  padding: 7px 10px;
  width: 300px;
  color: #555;
  font-size: 16px;
  background: #fff;
  border: solid 3px #cccccc;
  box-sizing: border-box;
}

.balloon2-left:before {
  content: '';
  position: absolute;
  top: 50%;
  left: -24px;
  margin-top: -12px;
  border: 12px solid transparent;
  border-right: 12px solid #fff;
  z-index: 2;
}

.balloon2-left:after {
  content: '';
  position: absolute;
  top: 50%;
  left: -30px;
  margin-top: -14px;
  border: 14px solid transparent;
  border-right: 14px solid #cccccc;
  z-index: 1;
}

.balloon2-left p {
  margin: 0;
  padding: 0;
  white-space: pre-wrap;
  text-align: left;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
