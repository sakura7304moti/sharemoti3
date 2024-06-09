<template>
  <q-select
    v-model="selectedValue"
    :options="selectOptions"
    dense
    stack-label
    :label="selectLabel"
    :style="{ width: selectWidth + 'px' }"
    transition-show="jump-up"
    transition-hide="jump-up"
  >
    <template v-slot:append>
      <q-icon
        id="yaki-select-clear-icon"
        v-if="selectedValue != ''"
        name="clear"
        @click.stop.prevent="selectedValue = ''"
      />
    </template>
  </q-select>
</template>
<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
export default defineComponent({
  name: 'yaki-select',
  props: {
    modelValue: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: false,
      default: '焼き直し種類',
    },
    width: {
      type: Number,
      required: false,
      default: 200,
    },
  },
  setup(props, { emit }) {
    const selectOptions = ref(['焼き直し', '焼き直しフェニックス']);

    // selectOptionsの変更を監視し、modelValueに反映
    watch(selectOptions, (newOptions) => {
      // conditionが選択肢に含まれていない場合、最初の選択肢を選択
      if (!newOptions.includes(props.modelValue)) {
        selectedValue.value = '';
      }
    });

    // selectedValueをmodelValueに反映
    const selectedValue = ref(props.modelValue);
    watch(selectedValue, (newValue) => {
      emit('update:modelValue', newValue);
    });

    return {
      /*props */
      selectedValue,
      selectLabel: ref(props.label),
      selectWidth: ref(props.width),
      /*datas */
      selectOptions,
    };
  },
});
</script>
<style lang="scss">
#yaki-select-clear-icon {
  color: grey;
  -webkit-transition: all 0.3s ease;
  -moz-transition: all 0.3s ease;
  -o-transition: all 0.3s ease;
  transition: all 0.3s ease;
}
#yaki-select-clear-icon:hover {
  color: $primary;
}
</style>
