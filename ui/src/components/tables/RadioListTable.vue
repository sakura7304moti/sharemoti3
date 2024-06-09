<template>
  <q-table
    :title="tableName"
    v-if="!load.search"
    :rows="records"
    :columns="columns"
    row-key="id"
    :style="{ height: tableHeight }"
    separator="cell"
    rows-per-page-label="表示行数"
    no-results-label="見つからなかった..."
    no-data-label="見つからなかった..."
    :pagination="{ rowsPerPage: 0 }"
    :rows-per-page-options="[0]"
    :filter="filter"
    :filter-method="filteringData"
    class="table-base scroll-table"
    ><!--sub 1/3 オプション-->
    <template v-slot:top-right>
      <div class="row q-gutter-md table-base-header">
        <div class="table-base-filter">
          <q-input
            dense
            debounce="300"
            v-model="filter.text"
            placeholder="検索"
            class="table-base-filter-input"
            align="left"
          >
            <template v-slot:append>
              <q-spinner
                v-model="load.search"
                v-if="load.search"
                color="primary"
                size="md"
              />
              <q-icon name="search" v-if="filter.text.length == 0" />
              <q-icon name="search" v-else color="primary" />
              <div class="text-caption" v-if="records.length > 0">
                {{ records.length }}
              </div>
            </template>
          </q-input>
        </div>
      </div>
      <div class="q-pt-sm">
        <q-select
          v-model="filter.date"
          :options="dateList"
          dense
          stack-label
          label="日付"
          transition-show="jump-up"
          transition-hide="jump-up"
          style="width: 150px"
          clearable
        />
      </div>
      <div v-if="playName != '' && playUrl != ''" class="row">
        <audio controls :src="playUrl" autoplay class="q-pt-sm" />
        <q-field borderless class="q-pt-sm q-pb-sm" style="height: 18px">{{
          playName
        }}</q-field>
      </div>
    </template>

    <!-- sub 2/3  ヘッダー-->
    <template v-slot:header="props">
      <q-tr :props="props">
        <q-th style="width: 50px"><div class="q-pt-md">再生</div> </q-th>
        <q-th v-for="col in props.cols" :key="col.name" :props="props">
          <div v-if="col.label == 'タイトル'" class="table-base-main-column">
            {{ col.label }}
          </div>
          <div v-if="col.label == '日時'" class="table-base-main-column">
            {{ col.label }}
          </div>
          <div v-if="col.label == 'ファイル名'" class="table-base-sub-column">
            {{ col.label }}
          </div>
        </q-th>
      </q-tr>
    </template>
    <!-- sub 3/3  アイテム-->
    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td>
          <a
            :href="api.apiEndpoint() + '/radio/download?id=' + props.row.id"
            @click.prevent="
              console.log('play', props.row);
              playUrl =
                api.apiEndpoint() + '/radio/download?id=' + props.row.id;
              playName = props.row.fileName;
            "
            class="play-btn"
            ><q-icon name="play_circle" color="primary" size="sm"></q-icon
          ></a>
        </q-td>
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
          style="white-space: normal; text-align: left"
        >
          {{ col.value }}
        </q-td>
      </q-tr>
    </template></q-table
  >
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRadioListModel } from 'src/models/RadioListModels';
import api from 'src/api/file/RadioListApi';
export default defineComponent({
  name: 'table-karaoke-list',
  props: {
    label: {
      type: String,
      required: false,
      default: 'オム子レイディオ',
    },
    height: {
      type: Number,
      required: false,
      default: 700,
    },
  },
  setup(props) {
    const {
      columns,
      load,
      records,
      search,
      selectId,
      dateList,
      filter,
      dateFilter,
      filteringData,
    } = useRadioListModel();

    search();
    return {
      tableName: ref(props.label),
      tableHeight: ref(props.height + 'px'),
      columns,
      load,
      records,
      search,
      api,
      selectId,
      playUrl: ref(''),
      playName: ref(''),
      dateList,
      filter,
      dateFilter,
      filteringData,
    };
  },
});
</script>
<style>
.playground {
  padding: 0.5em 1em;
  margin: 2em 0;
  font-weight: bold;
  background: #fff;
  border: solid 3px #5c5e5f; /*線*/
  border-radius: 10px; /*角の丸み*/
}
.playground p {
  margin: 0;
  padding: 0;
}
/*テーブルのstyle */
.radio-list-table {
  max-width: 700px;
}

.radio-list-table .q-table__top,
.radio-list-table .q-table__bottom,
.radio-list-table thead tr:first-child th {
  /* bg color is important for th; just specify one */
  background-color: white;
}

.radio-list-table thead tr th {
  position: sticky;
  z-index: 1;
}

.radio-list-table thead tr:first-child th {
  top: 0;
}

/* this is when the loading indicator appears */
.radio-list-table.q-table--loading thead tr:last-child th {
  /* height of all previous header rows */
  top: 48px;
}

/* prevent scrolling behind sticky top row on focus */
.radio-list-table tbody {
  /* height of all previous header rows */
  scroll-margin-top: 48px;
}
</style>
