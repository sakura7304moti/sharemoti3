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
    <div class="q-mt-md" style="max-width: 500px">
      <q-markup-table v-if="selectTab == 'ランキング'">
        <thead>
          <tr>
            <th>キャラ名</th>
            <th class="text-right">数</th>
            <th class="text-right">順位</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rec in rankRecords" :key="rec.name">
            <td>
              <div>
                <img
                  v-if="rec.rank == 1"
                  src="../assets/rank_1.png"
                  style="height: 40px"
                />
                <img
                  v-if="rec.rank == 2"
                  src="../assets/rank_2.png"
                  style="height: 40px"
                />
                <img
                  v-if="rec.rank == 3"
                  src="../assets/rank_3.png"
                  style="height: 40px"
                />
              </div>
              <q-avatar>
                <img
                  :src="ssbuNameOptions.find((it) => it.name == rec.name)?.icon"
                /> </q-avatar
              ><span class="q-ml-sm text-body1">{{ rec.name }}</span>
            </td>
            <td class="text-right">
              <span class="text-body1 text-primary" v-if="rec.total > 0">{{
                rec.total
              }}</span>
            </td>
            <td class="text-right">
              <span class="text-body1" v-if="rec.total > 0">{{
                rec.rank
              }}</span>
            </td>
          </tr>
        </tbody>
      </q-markup-table>
      <q-markup-table v-if="selectTab == '記念日'">
        <thead>
          <tr>
            <th>キャラ名</th>
            <th>初めての</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rec in firstRecords" :key="rec.name">
            <td>
              <q-avatar>
                <img
                  :src="ssbuNameOptions.find((it) => it.name == rec.name)?.icon"
                /> </q-avatar
              ><span class="q-ml-sm text-body1">{{ rec.name }}</span>
            </td>
            <td>
              <span class="text-body2"> {{ rec.date }}</span>
            </td>
          </tr>
        </tbody>
      </q-markup-table>
    </div>
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import SsbuNameSelect from 'src/components/selects/SsbuNameSelect.vue';
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
