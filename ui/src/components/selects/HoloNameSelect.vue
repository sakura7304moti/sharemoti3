<template>
  <div class="row q-gutter-xs">
    <q-select
      v-model="selectedValue"
      :options="selectOptions"
      option-value="hashtag"
      option-label="hashtag"
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
          id="holo-select-clear-icon"
          v-if="selectedValue != ''"
          name="clear"
          @click.stop.prevent="selectedValue = ''"
        />
      </template>
      <template v-slot:option="scope">
        <q-item v-bind="scope.itemProps" class="holo-name-item-selected">
          <q-avatar>
            <img :src="scope.opt.url" />
          </q-avatar>

          <q-item-label class="holo-select-text-container text-bold">
            {{ scope.opt.hashtag }}
          </q-item-label>
        </q-item>
      </template>
      <template v-slot:selected>
        <q-chip
          v-if="selectedValue != ''"
          dense
          square
          color="white"
          class="q-my-none q-ml-xs q-mr-none"
        >
          <q-avatar text-color="white">
            <q-img
              :src="
                selectOptions.find((it) => it.hashtag == selectedValue)?.url
              "
            />
          </q-avatar>
          {{ selectedValue }}
        </q-chip>
      </template>
    </q-select>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import api from 'src/api/scraper/TwitterApi';
export default defineComponent({
  name: 'holo-hashtag-select',
  props: {
    modelValue: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: false,
      default: 'hashtag',
    },
    width: {
      type: Number,
      required: false,
      default: 220,
    },
  },
  setup(props, { emit }) {
    const selectOptions = ref([] as HoloName[]);
    const getNames = async function () {
      selectOptions.value.splice(0);
      api
        .holoList()
        .then((response) => {
          if (response) {
            console.log('holo-name', response);
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
      if (
        newOptions.filter((it) => it.hashtag == props.modelValue).length == 0
      ) {
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
interface HoloName {
  hashtag: string;
  url: string;
}
</script>
<style lang="scss">
/*selectのクリアアイコン */
#holo-select-clear-icon {
  color: grey;
  -webkit-transition: all 0.3s ease;
  -moz-transition: all 0.3s ease;
  -o-transition: all 0.3s ease;
  transition: all 0.3s ease;
}
#holo-select-clear-icon:hover {
  color: $primary;
}
/*selectの文字 */
.holo-select-text-container {
  padding-left: 16px;
  font-size: 16px;
}
/*selectの下線 */
.holo-name-item-selected:after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 1px;
  background-color: $grey-4; /* 下線の色を設定 */
}
</style>
