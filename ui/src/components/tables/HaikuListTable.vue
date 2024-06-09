<template>
  <q-table
    :title="tableName"
    :rows="rows"
    :columns="columns"
    row-key="id"
    separator="cell"
    rows-per-page-label="表示行数"
    no-results-label="見つからなかった..."
    no-data-label="見つからなかった..."
    :pagination="{ rowsPerPage: 0 }"
    :rows-per-page-options="[0]"
    :filter="filter"
    class="haiku-list-table"
    :style="{ height: tableHeight }"
  >
    <!--sub 1/3 オプション-->
    <template v-slot:top-right>
      <div class="row q-gutter-md">
        <div style="width: 700px">
          <q-input
            dense
            debounce="300"
            v-model="filter"
            placeholder="検索"
            style="width: 200px"
            align="left"
          >
            <template v-slot:append>
              <q-spinner
                v-model="LoadingCondition.search"
                v-if="LoadingCondition.search"
                color="primary"
                size="md"
              />
              <q-icon name="search" v-if="filter.length == 0" />
              <q-icon name="search" v-else color="primary" />
              <div class="text-caption" v-if="records.length">
                {{ records.length }}
              </div>
            </template>
          </q-input>
        </div>
        <div>
          <q-btn
            label="作成"
            icon-right="note_add"
            color="grey-6"
            @click="displayCondition.insert = true"
            outline
          />
        </div>
        <div>
          <lock-icon
            v-model="displayCondition.detail"
            @event-change="displayCondition.detail = $event"
            class="q-pt-sm"
          />
        </div>
      </div>
    </template>
    <!-- sub 2/3  ヘッダー-->
    <template v-slot:header="props">
      <q-tr :props="props">
        <q-th v-if="displayCondition.detail == false"> 編集 </q-th>
        <q-th v-if="displayCondition.detail == false"> 削除 </q-th>
        <q-th v-for="col in props.cols" :key="col.name" :props="props">
          <div
            v-if="col.label == '5' || col.label == '7' || col.label == '投稿者'"
            style="width: 100px"
          >
            {{ col.label }}
          </div>
          <div
            v-if="col.label == '作成日' || col.label == '更新日'"
            style="width: 80px"
          >
            {{ col.label }}
          </div>
          <div
            v-if="col.label == '解説'"
            style="
              width: 200px;
              text-align: left;
              white-space: pre-wrap;
              word-wrap: break-word;
            "
          >
            {{ col.label }}
          </div>
        </q-th>
      </q-tr>
    </template>

    <!-- sub 3/3  アイテム-->
    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td v-if="displayCondition.detail == false">
          <a href="#" @click.prevent="updateClick(props.row)"
            ><q-icon name="edit_note" color="secondary" size="md"></q-icon
          ></a>
        </q-td>
        <q-td v-if="displayCondition.detail == false">
          <a href="#" @click.prevent="deleteClick(props.row)"
            ><q-icon name="delete" color="negative" size="md"></q-icon
          ></a>
        </q-td>
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
          style="text-align: left; white-space: pre-wrap; word-wrap: break-word"
        >
          {{ col.value }}
        </q-td>
      </q-tr>
    </template>
  </q-table>

  <!--モーダル一覧-->
  <q-dialog v-model="displayCondition.insert">
    <q-card class="q-pa-md" style="max-width: 700px">
      <q-section>
        <div style="font-family: HinaMincho-Regular" class="text-h6">
          王将マンによる俳句審査<q-checkbox
            class="text-subtitle1 text-weight-medium"
            v-model="insertHaikuOmake"
            label="みちゃやーよ"
          />
        </div>
        <hr />
        <div class="row q-gutter-md" style="width: 700px">
          <!--inputs-->
          <div style="width: 350px">
            <q-input
              v-model="insertCondition.poster"
              label="投稿者名"
              stack-label
              style="width: 200px"
              outlined
              dense
              class="q-pb-lg"
              filled
            />
            <q-input
              v-model="insertCondition.first"
              outlined
              class="q-pb-md"
              style="width: 200px"
              label="5"
              stack-label
            />
            <q-input
              v-model="insertCondition.second"
              outlined
              class="q-pb-md"
              style="width: 300px"
              label="7"
              stack-label
            />
            <q-input
              v-model="insertCondition.third"
              outlined
              class="q-pb-md"
              style="width: 200px"
              label="5"
              stack-label
            />
          </div>
          <div>
            <q-input
              style="
                width: 250px;
                text-align: left;
                white-space: pre-wrap;
                word-wrap: break-word;
              "
              rows="12"
              type="textarea"
              v-model="insertCondition.detail"
              outlined
              stack-label
              label="解説(省略可)"
            />
          </div>
          <!--作品イメージ-->
          <div style="width: 250px" v-if="insertHaikuOmake">
            <div>
              <div>作品イメージ</div>
              <!--セリフ-->
              <div class="haiku-box">
                <div
                  style="
                    writing-mode: vertical-rl;
                    font-family: haiku;
                    font-size: 32px;
                    margin-left: auto;
                  "
                >
                  <div style="margin-right: 50px">
                    {{ insertCondition.first }}
                  </div>
                  <div style="margin-right: 20px">
                    {{ insertCondition.second }}
                  </div>
                  <div style="margin-right: 20px">
                    {{ insertCondition.third }}
                  </div>
                </div>
              </div>
              <img src="../../assets/senno_rikyu.png" width="200" />
              <div>そこにわびさびはあるんか?</div>
            </div>
          </div>
        </div>

        <hr />
        <div>
          <q-btn
            label="追加"
            color="primary"
            class="text-weight-bold"
            :disable="
              insertCondition.first == '' ||
              insertCondition.second == '' ||
              insertCondition.third == ''
            "
            style="margin-right: auto"
            @click="insert"
            :loading="LoadingCondition.insert"
          />
        </div>
      </q-section>
    </q-card>
  </q-dialog>

  <q-dialog v-model="displayCondition.update">
    <q-card class="q-pa-md" style="max-width: 1200px">
      <q-section>
        <div class="text-h6">編集</div>
        <hr />
        <div class="row q-gutter-md">
          <!--編集後-->
          <div>
            <div class="text-subtitle1">編集後</div>
            <div class="row q-gutter-xs">
              <!--inputs-->
              <div style="width: 320px">
                <q-input
                  v-model="updateCondition.poster"
                  label="投稿者名"
                  stack-label
                  style="width: 200px"
                  outlined
                  dense
                  class="q-pb-lg"
                  filled
                />
                <q-input
                  v-model="updateCondition.first"
                  outlined
                  class="q-pb-md"
                  style="width: 200px"
                  label="5"
                  stack-label
                />
                <q-input
                  v-model="updateCondition.second"
                  outlined
                  class="q-pb-md"
                  style="width: 300px"
                  label="7"
                  stack-label
                />
                <q-input
                  v-model="updateCondition.third"
                  outlined
                  class="q-pb-md"
                  style="width: 200px"
                  label="5"
                  stack-label
                />
              </div>
              <div>
                <q-input
                  style="
                    width: 250px;
                    text-align: left;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                  "
                  rows="12"
                  type="textarea"
                  v-model="updateCondition.detail"
                  outlined
                  stack-label
                  label="解説(省略可)"
                />
              </div>
            </div>
          </div>
          <!--編集前-->
          <div style="width: 300px">
            <div>
              <div class="text-subtitle1">編集前の俳句</div>
              <div class="haiku-box">
                <div
                  style="
                    writing-mode: vertical-rl;
                    font-family: haiku;
                    font-size: 32px;
                    margin-left: auto;
                  "
                >
                  <div style="margin-right: 50px">
                    {{ updateSelectedCondition.first }}
                  </div>
                  <div style="margin-right: 20px">
                    {{ updateSelectedCondition.second }}
                  </div>
                  <div style="margin-right: 20px">
                    {{ updateSelectedCondition.third }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div>
          <hr />
          <q-btn
            label="更新"
            @click="update"
            color="primary"
            :loading="LoadingCondition.update"
          />
        </div>
      </q-section>
    </q-card>
  </q-dialog>

  <q-dialog v-model="displayCondition.delete">
    <q-card class="q-pa-md" style="width: 700px">
      <q-section>
        <div class="text-h6 row q-gutter-md">
          <div>俳句の削除確認</div>
          <div style="margin-left: auto">
            <a
              href="#"
              class="text-grey"
              @click.prevent="displayCondition.delete = false"
              ><q-icon name="close"
                ><q-tooltip class="bg-white text-primary"
                  >Close</q-tooltip
                ></q-icon
              ></a
            >
          </div>
        </div>
        <hr />
        <div>次の俳句を削除してもいいかな？</div>

        <div
          style="
            writing-mode: vertical-rl;
            font-family: haiku;
            font-size: 32px;
            height: 270px;
          "
        >
          <div style="margin-right: 50px">
            {{ updateSelectedCondition.first }}
          </div>
          <div style="margin-right: 20px">
            {{ updateSelectedCondition.second }}
          </div>
          <div style="margin-right: 20px">
            {{ updateSelectedCondition.third }}
          </div>
          <div style="margin-right: 20px" class="text-right">
            {{ updateSelectedCondition.poster }}
          </div>
        </div>
        <hr />
        <q-btn
          label="削除"
          color="negative"
          @click="deleteRecord"
          :loading="LoadingCondition.delete"
        />
      </q-section>
    </q-card>
  </q-dialog>
</template>
<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import { useHaikuListModel } from 'src/models/HaikuListModels';
import lockIcon from 'src/components/LockIcon.vue';
export default defineComponent({
  name: 'table-haiku-list',
  components: {
    'lock-icon': lockIcon,
  },
  props: {
    modelValue: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: false,
      default: '俳句王決定戦',
    },
    height: {
      type: Number,
      required: false,
      default: 700,
    },
  },
  setup(props) {
    const {
      lockIconCondition,
      displayCondition,
      condition,
      insertCondition,
      updateCondition,
      updateSelectedCondition,
      LoadingCondition,
      records,
      tableView,
      columns,
      rows,
      search,
      insertClick,
      insert,
      updateClick,
      update,
      deleteClick,
      deleteRecord,
      rangeChange,
    } = useHaikuListModel();
    search();

    const detailDisplay = ref(false);

    watch(detailDisplay, () => {
      if (detailDisplay.value) {
        records.value.forEach((it) => (it.detailDisplay = false));
      } else {
        records.value.forEach((it) => (it.detailDisplay = true));
      }
    });

    return {
      //Props
      filter: ref(props.modelValue),
      tableName: ref(props.label),
      tableHeight: ref(props.height + 'px'),
      //Models
      lockIconCondition,
      displayCondition,
      condition,
      insertCondition,
      updateCondition,
      updateSelectedCondition,
      LoadingCondition,
      records,
      tableView,
      columns,
      rows,
      search,
      insertClick,
      insert,
      updateClick,
      update,
      deleteClick,
      deleteRecord,
      insertHaikuOmake: ref(false),
      detailDisplay,
      rangeChange,
    };
  },
});
</script>
<style>
@font-face {
  font-family: 'haiku';
  src: url(src/fonts/haiku2.ttf) format('truetype');
}
@font-face {
  font-family: 'HinaMincho-Regular';
  src: url(src/fonts/HinaMincho-Regular.ttf) format('truetype');
}
/*input 入力の横幅 */
.form-model {
  width: 200px;
  height: 40px;
}
/*俳句の外枠 */
.haiku-box {
  width: 300px;
  height: 350px;
  margin: 1em 0;
  position: relative;
  padding: 0.5em 1em;
  border-top: solid 2px black;
  border-bottom: solid 2px black;
}
.haiku-box:before,
.haiku-box:after {
  content: '';
  position: absolute;
  top: -10px;
  width: 2px;
  height: -webkit-calc(100% + 20px);
  height: calc(100% + 20px);
  background-color: black;
}
.haiku-box:before {
  left: 10px;
}
.haiku-box:after {
  right: 10px;
}
.haiku-box div {
  margin: 0;
  padding: 0;
}
/*解説の外枠 */
.box28 {
  position: relative;
  margin: 2em 0;
  padding: 25px 10px 7px;
  border: solid 2px #28b315;
  height: 300px;
  width: 300px;
}
.box28 .box-title {
  position: absolute;
  display: inline-block;
  top: -2px;
  left: -2px;
  padding: 0 9px;
  height: 25px;
  line-height: 25px;
  font-size: 17px;
  background: #28b315;
  color: #ffffff;
  font-weight: bold;
}
.box28 p {
  margin: 0;
  padding: 0;
}
/*テーブルのstyle */
.haiku-list-table {
  max-width: 1100px;
}

.haiku-list-table .q-table__top,
.haiku-list-table .q-table__bottom,
.haiku-list-table thead tr:first-child th {
  /* bg color is important for th; just specify one */
  background-color: white;
}

.haiku-list-table thead tr th {
  position: sticky;
  z-index: 1;
}

.haiku-list-table thead tr:first-child th {
  top: 0;
}

/* this is when the loading indicator appears */
.haiku-list-table.q-table--loading thead tr:last-child th {
  /* height of all previous header rows */
  top: 48px;
}

/* prevent scrolling behind sticky top row on focus */
.haiku-list-table tbody {
  /* height of all previous header rows */
  scroll-margin-top: 48px;
}
</style>
