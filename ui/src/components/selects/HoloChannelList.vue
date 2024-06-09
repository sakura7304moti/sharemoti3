<template>
  <div class="row q-gutter-xs">
    <q-avatar v-if="selectAvatarUrl != ''">
      <img :src="selectAvatarUrl" />
    </q-avatar>
    <q-select
      v-model="selectedValue"
      :options="channel"
      option-value="channelId"
      option-label="channelName"
      emit-value
      map-options
      dense
      stack-label
      :label="selectLabel"
      :style="{ width: selectWidth + 'px' }"
      transition-show="jump-up"
      transition-hide="jump-up"
      counter
    >
      <!--クリアー-->
      <template v-slot:append>
        <q-icon
          id="holo-select-clear-icon"
          v-if="selectedValue != ''"
          name="clear"
          @click.stop.prevent="selectedValue = ''"
        />
      </template>

      <!--開いた時-->
      <template v-slot:option="scope">
        <q-item v-bind="scope.itemProps" class="holo-name-item-selected">
          <q-avatar>
            <img :src="scope.opt.avatarUrl" />
          </q-avatar>

          <q-item-label class="holo-select-text-container text-bold">
            {{ scope.opt.channelName }}
          </q-item-label>
        </q-item>
      </template>

      <!--選択時-->
      <template v-slot:selected> </template>

      <!--ヒント-->
      <template v-slot:hint>
        {{ selectchannelName }}
      </template>

      <!--カウンター-->
      <template v-slot:counter> </template>
    </q-select>
  </div>
</template>
<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue';
import { useHoloArchiveStore } from 'src/stores/HoloArchiveStore';
export default defineComponent({
  name: 'holo-channel-select',
  props: {
    modelValue: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: false,
      default: 'channel',
    },
    width: {
      type: Number,
      required: false,
      default: 220,
    },
  },
  setup(props, { emit }) {
    const store = useHoloArchiveStore();
    const channel = ref(store.channels);

    store.getChannels();
    // selectedValueをmodelValueに反映
    const selectedValue = ref(props.modelValue);
    watch(selectedValue, (newValue) => {
      emit('update:modelValue', newValue);
    });

    // selectOptionsの変更を監視し、modelValueに反映
    watch(channel, (newOptions) => {
      // conditionが選択肢に含まれていない場合、最初の選択肢を選択
      if (
        newOptions.filter((it) => it.channelId == props.modelValue).length == 0
      ) {
        selectedValue.value = '';
      }
    });

    const selectAvatarUrl = computed(() => {
      const items = channel.value.filter(
        (it) => it.channelId == selectedValue.value
      );
      if (items.length == 1) {
        return items[0].avatarUrl;
      } else {
        return '';
      }
    });

    const selectchannelName = computed(() => {
      const items = channel.value.filter(
        (it) => it.channelId == selectedValue.value
      );
      if (items.length == 1) {
        return items[0].channelName;
      } else {
        return '';
      }
    });
    const selectWidth = computed(() => {
      return selectAvatarUrl.value == '' ? props.width : props.width - 48;
    });
    return {
      /*props */
      selectWidth,
      selectedValue,
      selectLabel: ref(props.label),
      /*datas */
      channel,
      selectAvatarUrl,
      selectchannelName,
    };
  },
});
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
