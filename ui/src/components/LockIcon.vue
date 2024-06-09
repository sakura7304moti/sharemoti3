<template>
  <div class="lock-icon">
    <a href="#" @click.prevent="onToggleClick" class="row q-gutter-xs">
      <q-icon v-if="toggle" name="lock" size="sm" color="secondary" />
      <q-icon v-else name="lock_open" size="sm" color="secondary" />
      <div class="text-subtitle text-black lock-icon">{{ iconText }}</div>
    </a>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
export default defineComponent({
  name: 'LockIcon',
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
    label: {
      type: String,
      required: false,
    },
  },
  setup(props, context) {
    const toggle = ref(props.modelValue);
    const iconText = ref(props.label ?? '');

    const onToggleClick = function () {
      toggle.value = !toggle.value;
    };

    watch(toggle, () => {
      context.emit('event-change', toggle.value);
    });
    return {
      toggle,
      iconText,
      onToggleClick,
    };
  },
});
</script>
<style>
.lock-icon {
  height: 32px;
}
.lock-icon a {
  text-decoration: none;
}
.lock-icon a:hover {
  background-color: rgba(221, 238, 255, 0.5);
}
</style>
