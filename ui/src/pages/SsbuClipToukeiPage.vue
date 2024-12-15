<template>
  <q-page class="q-ma-md">
    <div class="text-h6">切り抜きの記録</div>
    <q-card class="q-mt-md" style="max-width: 500px; width: 100%">
      <q-card-section>
        <div class="q-mb-xs">
          <q-tabs
            v-model="selectTab"
            inline-label
            style="max-width: 360px"
            class="bg-white"
            active-color="primary"
            indicator-color="primary"
            dense
            @update:model-value="onSearchClick"
          >
            <q-tab
              :name="tab"
              :label="tab"
              v-for="tab in tabItems"
              :key="tab"
              style="width: 180px"
            />
          </q-tabs>
        </div>
        <div class="row q-gutter-md">
          <q-radio
            v-model="selectCategory"
            :val="cate"
            :label="cate"
            v-for="cate in categoryItems"
            :key="cate"
            @update:model-value="onSearchClick"
          />
        </div>
      </q-card-section>
    </q-card>
    <div class="q-mt-md" style="max-width: 400px">
      <div v-if="selectTab == 'ランキング'">
        <div v-for="rec in rankRecords" :key="rec.name">
          <div style="padding-bottom: 24px">
            <div
              class="text-subtitle1 text-weight-bold q-mr-md"
              v-if="rec.total > 0"
            >
              {{ rec.rank }}位
            </div>
            <div class="row">
              <q-avatar class="q-mr-md">
                <img
                  :src="ssbuNameOptions.find((it) => it.name == rec.name)?.icon"
                />
              </q-avatar>
              <div style="font-size: 32px" v-if="rec.total > 0">
                {{ rec.total }}<span style="font-size: 16px"> こ </span>
              </div>
            </div>

            <div class="text-body1">{{ rec.name }}</div>
          </div>
        </div>
      </div>
      <div v-if="selectTab == '記念日'">
        <div v-for="rec in firstRecords" :key="rec.name">
          <div style="padding-bottom: 24px">
            <div class="row">
              <q-avatar class="q-mr-md">
                <img
                  :src="ssbuNameOptions.find((it) => it.name == rec.name)?.icon"
                />
              </q-avatar>
              <div style="font-size: 16px; padding-top: 8px" v-if="rec.date">
                {{ rec.date }}
              </div>
            </div>

            <div class="text-body1">{{ rec.name }}</div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import api from 'src/api/file/SsbuClipToukeiApi';
import { NameListApi } from 'src/api/main/NameListApi';
const nameApi = new NameListApi();
import { useQuasar } from 'quasar';
export default defineComponent({
  name: 'ssbu-clip-toukei-page',
  setup() {
    const {
      selectCategory,
      categoryItems,
      selectTab,
      tabItems,
      rankRecords,
      firstRecords,
      ssbuNameOptions,
      getRank,
      getNames,
      onSearchClick,
    } = useModel();
    getNames();
    onSearchClick();
    return {
      selectCategory,
      categoryItems,
      selectTab,
      tabItems,
      rankRecords,
      firstRecords,
      ssbuNameOptions,
      getRank,
      getNames,
      onSearchClick,
    };
  },
});
const useModel = function () {
  const quasar = useQuasar();
  const selectCategory = ref('ウルトラC');
  const categoryItems = ref(['ウルトラC', 'ウルツラC', '思い出', '焼き直し']);
  const selectTab = ref('ランキング');
  const tabItems = ref(['ランキング', '記念日']);
  const rankRecords = ref([] as Rank[]);
  const firstRecords = ref([] as First[]);
  const ssbuNameOptions = ref([] as SsbuNameState[]);

  const getNames = async function () {
    await nameApi
      .ssbu_names()
      .then((response) => {
        if (response) {
          console.log('ssbu-names', response);
          response.records.forEach((it) => ssbuNameOptions.value.push(it));
        }
      })
      .catch((e) => {
        console.log('err', e);
      });
  };

  const getRank = async function (text: string) {
    await api
      .rank(text)
      .then((response) => {
        if (response) {
          console.log('rank response', response);
          rankRecords.value.splice(0);
          response.forEach((it) => rankRecords.value.push(it));
        }
      })
      .catch((err) => {
        console.log('rank err', err);
        quasar.notify({
          color: 'negative',
          position: 'top',
          message: 'データ取得でエラーになった...',
        });
      });
  };

  const getFirst = async function (text: string) {
    await api
      .first(text)
      .then((response) => {
        if (response) {
          console.log('first response', response);
          firstRecords.value.splice(0);
          response.forEach((it) => firstRecords.value.push(it));
        }
      })
      .catch((err) => {
        console.log('rank err', err);
        quasar.notify({
          color: 'negative',
          position: 'top',
          message: 'データ取得でエラーになった...',
        });
      });
  };

  const onSearchClick = function () {
    if (selectTab.value == 'ランキング') {
      getRank(selectCategory.value);
    }
    if (selectTab.value == '記念日') {
      getFirst(selectCategory.value);
    }
  };

  return {
    selectCategory,
    categoryItems,
    selectTab,
    tabItems,
    rankRecords,
    firstRecords,
    ssbuNameOptions,
    getRank,
    getNames,
    onSearchClick,
  };
};
interface SsbuNameState {
  name: string;
  url: string;
  icon: string;
}
interface Rank {
  name: string;
  total: number;
  rank: number;
}
interface First {
  name: string;
  date: string;
}
</script>
