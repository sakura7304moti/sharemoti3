<template>
  <q-select
    v-model="selectedValue"
    :options="selectOptions"
    option-value="name"
    option-label="name"
    emit-value
    map-options
    dense
    stack-label
    :label="selectLabel"
    :style="{ width: selectWidth + 'px' }"
    transition-show="jump-up"
    transition-hide="jump-up"
  >
    <template v-slot:append>
      <q-icon
        id="ssbu-select-clear-icon"
        v-if="selectedValue != ''"
        name="clear"
        @click.stop.prevent="selectedValue = ''"
      />
    </template>
    <template v-slot:option="scope">
      <q-item v-bind="scope.itemProps" class="ssbu-nameq-item-selected">
        <img :src="scope.opt.url" class="ssbu-names-image-container" />
        <q-item-label class="ssbu-names-text-container">
          {{ scope.opt.name }}
        </q-item-label>
      </q-item>
    </template>
  </q-select>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import api from 'src/api/main/NameListApi';

export default defineComponent({
  name: 'ssbu-char-select',
  props: {
    modelValue: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: false,
      default: 'キャラ名',
    },
    width: {
      type: Number,
      required: false,
      default: 220,
    },
  },
  setup(props, { emit }) {
    /*APIからキャラ名の一覧を取得 */
    const selectOptions = ref([] as DataState[]);
    const getNames = async function () {
      await api
        .ssbu_names()
        .then((response) => {
          if (response) {
            console.log('ssbu-names', response);
            response.records.forEach((it) => selectOptions.value.push(it));
          }
        })
        .catch((e) => {
          console.log('err', e);
        });
    };

    // selectOptionsの変更を監視し、modelValueに反映
    watch(selectOptions, (newOptions) => {
      // conditionが選択肢に含まれていない場合、最初の選択肢を選択
      if (newOptions.filter((it) => it.name == props.modelValue).length == 0) {
        selectedValue.value = '';
      }
    });

    // 初期化時にキャラ名を取得
    getNames();

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
interface DataState {
  name: string;
  url: string;
}
</script>
<style lang="scss">
/*selectのクリアアイコン */
#ssbu-select-clear-icon {
  color: grey;
  -webkit-transition: all 0.3s ease;
  -moz-transition: all 0.3s ease;
  -o-transition: all 0.3s ease;
  transition: all 0.3s ease;
}
#ssbu-select-clear-icon:hover {
  color: $primary;
}
/*selectの画像 */
.ssbu-names-image-container {
  height: 50px;
}
/*selectの文字 */
.ssbu-names-text-container {
  width: 150px;
  font-family: 'MyNoto';
}
/*selectの下線 */
.ssbu-nameq-item-selected:after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 1px;
  background-color: $grey-4; /* 下線の色を設定 */
}
</style>
