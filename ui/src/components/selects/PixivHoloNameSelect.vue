<template>
  <div class="row q-gutter-xs">
    <q-select
      v-model="holoname"
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
          id="holo-select-clear-icon"
          v-if="holoname != ''"
          name="clear"
          @click.stop.prevent="holoname = ''"
        />
      </template>
      <template v-slot:option="scope">
        <q-item v-bind="scope.itemProps" class="holo-name-item-selected">
          <q-avatar>
            <img :src="scope.opt.url" />
          </q-avatar>

          <q-item-label class="holo-select-text-container text-bold">
            {{ scope.opt.name }}
          </q-item-label>
        </q-item>
      </template>
      <template v-slot:selected>
        <q-chip
          v-if="holoname != ''"
          dense
          square
          color="white"
          class="q-my-none q-ml-xs q-mr-none"
        >
          <q-avatar text-color="white">
            <q-img
              :src="selectOptions.find((it) => it.name == holoname)?.url"
            />
          </q-avatar>
          {{ holoname }}
        </q-chip>
      </template>
    </q-select>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import { PixivSearchStore } from 'src/stores/pixiv/PixivSearchStore';
export default defineComponent({
  name: 'holo-name-select',
  props: {
    label: {
      type: String,
      required: false,
      default: 'ホロメン',
    },
    width: {
      type: Number,
      required: false,
      default: 300,
    },
  },
  setup(props, { emit }) {
    const store = PixivSearchStore();
    const holoname = ref('');
    const selectOptions = ref([] as HoloName[]);
    const getNames = async function () {
      selectOptions.value.splice(0);
      await store.getHolonames();
      store.holonames.forEach((it) => selectOptions.value.push(it));
    };

    // 初期化時にキャラ名を取得
    getNames();

    watch(holoname, (newValue, oldValue) => {
      store.removeHashtag(oldValue);
      if (newValue?.length > 0) {
        store.addHashtag(newValue);
      }
    });

    watch(store.condition, (newValue, oldValue) => {
      if (!newValue.hashtags.includes(holoname.value)) {
        store.removeHashtag(holoname.value);
        holoname.value = '';
      }
    });
    return {
      /*props */
      holoname,
      selectLabel: ref(props.label),
      selectWidth: ref(props.width),
      /*datas */
      selectOptions,
    };
  },
});
interface HoloName {
  name: string;
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
