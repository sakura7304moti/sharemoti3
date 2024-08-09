<template>
  <q-page class="">
    <div class="q-pb-md text-h5" id="ssbu-title">スマブラ切り抜き集</div>
    <div class="ssbu-mobile hukidasi" v-if="playNameMobile != ''">
      <p>{{ playNameMobile }}</p>
    </div>
    <div class="ssbu-vt">
      <q-video
        :src="playUrlDesktop"
        volume="0.5"
        class="ssbu-desktop"
        v-if="playUrlDesktop != ''"
        style="
          width: 569px;
          height: 320px;
          position: relative;
          overflow: hidden; /* オーバーフローしたコンテンツを非表示にする */
        "
      />
      <q-table
        :rows="records"
        :columns="columns"
        row-id="id"
        separator="cell"
        rows-per-page-label="表示行数"
        no-results-label="見つからなかった..."
        no-data-label="見つからなかった..."
        :pagination="{ rowsPerPage: initTablePage }"
        :rows-per-page-options="pageOption"
        :filter="filter"
        :filter-method="filteringData"
        id="ssbu-table"
      >
        <!--sub 1/3 オプション-->
        <template v-slot:top-left>
          <div class="row q-gutter-md" id="ssbu-option-desktop">
            <div>
              <q-input
                dense
                debounce="300"
                v-model="filter.title"
                placeholder="検索"
                style="width: 200px"
                align="left"
                :readonly="disableFilter"
              >
                <template v-slot:append>
                  <q-spinner
                    v-model="load.search"
                    v-if="load.search"
                    color="primary"
                    size="md"
                  />
                  <q-icon name="search" v-if="filter.title.length == 0" />
                  <q-icon name="search" v-else color="primary" />
                  <div class="text-caption" v-if="records.length > 0">
                    {{ records.length }}
                  </div>
                </template>
              </q-input>
            </div>
            <div>
              <ssbu-name-select
                v-model="filter.charName"
                :readonly="disableFilter"
              />
            </div>
            <div>
              <q-select
                v-model="filter.date"
                :options="dateList"
                dense
                stack-label
                clearable
                label="日付"
                transition-show="jump-up"
                transition-hide="jump-up"
                style="width: 130px"
                :readonly="disableFilter"
              />
            </div>
            <div>
              <q-select
                v-model="filter.folder"
                :options="folderList"
                dense
                stack-label
                clearable
                label="種類"
                transition-show="jump-up"
                transition-hide="jump-up"
                style="width: 130px"
                :readonly="disableFilter"
              />
            </div>
          </div>
          <div
            id="ssbu-option-mobile"
            style="position: fixed; top: 10%; left: 5%"
          >
            <div class="text-h6 q-pl-sm">スマブラ切り抜き</div>
            <q-btn
              icon="search"
              round
              size="sm"
              class="ssbu-mobile"
              @click="searchOptionDialog = true"
            />
          </div>
          <div
            class="ssbu-mobile q-pt-sm"
            v-if="playUrlMobile != ''"
            style="height: 240px"
          >
            <q-video
              :src="playUrlMobile"
              volume="0.5"
              style="
                max-width: 90%;
                width: 100%;
                position: fixed;
                top: 15%;
                left: 5%;
                height: 200px;
              "
            />
          </div>
          <div v-else style="height: 24px"></div>
        </template>

        <!-- sub 2/3  ヘッダー-->
        <template v-slot:header="props">
          <q-tr :props="props" class="ssbu-desktop">
            <q-th class="ssbu-desktop">再生</q-th>
            <q-th
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
              class="ssbu-desktop"
              :class="{
                'mobile-only': col.label == 'アイコン',
              }"
            >
              <div v-if="col.label == '再生'" style="width: 50px">
                {{ col.label }}
              </div>

              <div v-if="col.label == 'キャラ名'" style="width: 150px">
                {{ col.label }}
              </div>

              <div v-if="col.label == 'タイトル'" style="width: 400px">
                {{ col.label }}
              </div>

              <div v-if="col.label == '日付'" style="width: 50px">
                {{ col.label }}
              </div>
            </q-th>
          </q-tr>
        </template>

        <!-- sub 3/3  アイテム-->
        <template v-slot:body="props">
          <q-tr :props="props" class="ssbu-tr-desktop">
            <q-td>
              <q-btn
                icon="play_arrow"
                :href="api.apiEndpoint() + '/ssbu/download?path=' + props.row.path"
                @click.prevent="
                  console.log('play', props.row);
                  playUrlDesktop =
                    api.apiEndpoint() + '/ssbu/download?path=' + props.row.path;
                  playNameDesktop = props.row.fileName;
                "
              />
            </q-td>
            <q-td
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
              :class="{
                'mobile-only': col.label == 'アイコン',
              }"
              style="white-space: normal; text-align: left"
            >
              {{ col.value }}
            </q-td>
          </q-tr>
          <q-tr :props="props" class="ssbu-tr-mobile">
            <q-td
              style="
                max-width: 90vw;
                width: 100%;
                vertical-align: top;
                cursor: pointer;
              "
              @click.prevent="
                console.log('play', props.row);
                playUrlMobile =
                  api.apiEndpoint() + '/ssbu/download?path=' + props.row.path;
                playNameMobile = props.row.fileName;
              "
            >
              <div style="display: flex">
                <div
                  style="padding-top: 16px; padding-left: 8px"
                  class="text-subtitle1"
                >
                  {{ props.cols[1].value.split('_')[0] }}
                </div>
                <div
                  style="padding-top: 18px; padding-left: 8px"
                  class="text-subtitle2 text-grey"
                  v-if="props.cols[0].value != ''"
                >
                  ({{ props.cols[0].value }})
                </div>
              </div>

              <div>
                <div
                  style="
                    padding: 0.5em 0.5em;
                    margin: 1em 0;
                    font-weight: bold;
                    color: rgb(51, 51, 51); /*文字色*/
                    background: #fff;
                    border: solid 1px rgb(182, 200, 155); /*線*/
                    border-radius: 10px; /*角の丸み*/
                    font-weight: 400;
                  "
                >
                  <div
                    class="text-h6"
                    style="
                      text-align: left;
                      white-space: pre-wrap;
                      word-wrap: break-word;
                    "
                  >
                    {{ props.cols[1].value.split('_')[1] }}
                    <div class="text-caption text-right">
                      {{ props.cols[2].value }}
                    </div>
                  </div>
                </div>
              </div>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>

    <!--スマホ用検索ウィンドウ-->
    <q-dialog v-model="searchOptionDialog" position="bottom">
      <q-card id="ssbu-option-dialog">
        <q-card-section>
          <div style="width: 100%; text-align: right">
            <div>
              <q-icon
                name="close"
                size="sm"
                @click="searchOptionDialog = false"
              />
            </div>
          </div>
          <div class="row q-gutter-sm q-pb-sm">
            <q-input
              dense
              debounce="300"
              v-model="filter.title"
              placeholder="検索"
              style="width: 220px"
              align="left"
              :readonly="disableFilter"
            >
              <template v-slot:append>
                <q-spinner
                  v-model="load.search"
                  v-if="load.search"
                  color="primary"
                  size="md"
                />
                <q-icon name="search" v-if="filter.title.length == 0" />
                <q-icon name="search" v-else color="primary" />
                <div class="text-caption" v-if="records.length > 0">
                  {{ records.length }}
                </div>
              </template>
            </q-input>
            <q-select
              v-model="filter.date"
              :options="dateList"
              dense
              stack-label
              clearable
              label="日付"
              transition-show="jump-up"
              transition-hide="jump-up"
              style="width: 130px"
              :readonly="disableFilter"
            />
          </div>
          <div class="row q-gutter-sm">
            <ssbu-name-select
              v-model="filter.charName"
              :readonly="disableFilter"
            />
          </div>
          <div
            style="
              display: flex;
              max-width: 300px;
              width: 100%;
              flex-wrap: wrap;
            "
          >
            <div v-for="ls in folderList" :key="ls">
              <q-radio
                v-model="filter.folder"
                :val="ls"
                :label="ls"
                style="width: 150px"
              />
            </div>
            <q-radio v-model="filter.folder" val="" label="未指定" />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useSsbuListModel } from 'src/models/SsbuListModels';
import SsbuNameSelect from 'src/components/selects/SsbuNameSelect.vue';
import api from 'src/api/file/SsbuListApi';
export default defineComponent({
  name: 'ssbu-list',
  components: {
    'ssbu-name-select': SsbuNameSelect,
  },
  setup() {
    const {
      filter,
      filteringData,
      countFolder,
      disableFilter,
      folderList,
      selectId,
      columns,
      load,
      records,
      dateList,
      ssbuNames,
      search,
      getSsbuNames,
    } = useSsbuListModel();
    getSsbuNames();
    search();

    /*ちょうどいいくらいのページ数を取得 */
    const initTablePage = ref(100);
    const pageOption = ref([100, 500, 0] as number[]);

    const resetOption = function () {
      filter.value.title = '';
      filter.value.charName = '';
      filter.value.date = '';
      filter.value.folder = '';
    };

    return {
      filter,
      filteringData,
      countFolder,
      disableFilter,
      folderList,
      selectId,
      columns,
      load,
      records,
      dateList,
      ssbuNames,
      search,
      api,
      playUrlDesktop: ref(''),
      playNameDesktop: ref(''),
      playUrlMobile: ref(''),
      playNameMobile: ref(''),
      initTablePage,
      pageOption,
      searchOptionDialog: ref(false),
      resetOption,
    };
  },
});
</script>
<style>
@media screen and (min-width: 1412px) {
  .ssbu-vt {
    display: flex;
  }
}
#ssbu-table {
  height: 80vh;
  overflow-y: auto;
  max-width: 810px;
  width: 100%;

  .q-table{
    max-width: 810px;
    width: 100%;
  }
}
#ssbu-option-mobile {
  display: flex;
  width: 100%;
  max-width: 90vw;
  justify-content: space-between;
  align-items: center;
}
#ssbu-option-dialog {
  height: 320px;
}
/*スマホ用 */
@media screen and (max-width: 810px) {
  #ssbu-option-desktop {
    display: none;
  }
  #ssbu-title {
    display: none;
  }
  #ssbu-table {
    height: 90vh;
  }
  .ssbu-desktop {
    display: none;
  }
  .ssbu-tr-desktop {
    display: none;
  }
}
/*PC用 */
@media screen and (min-width: 810px) {
  #ssbu-option-mobile {
    display: none;
  }
  .ssbu-mobile {
    display: none;
  }
  .ssbu-tr-mobile {
    display: none;
  }
}
/*吹き出し */
.hukidasi {
  background: #fff0c6;
  border-radius: 30px;
  position: fixed;
  max-width: 80vw;
  top: 8px;
  left: 8px;
  height: 64px;
  padding: 15px;
  z-index: 10000;
}

.hukidasi p {
  margin: 0;
  padding: 0;
}
</style>
