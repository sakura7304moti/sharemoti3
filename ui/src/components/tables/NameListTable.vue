<template>
  <q-table
    :title="tableName"
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
    :filter="filterCondition"
    :filter-method="filteringData"
    class="table-base scroll-table"
  >
    <!--sub 1/3 オプション-->
    <template v-slot:top-right>
      <div class="row q-gutter-md table-base-header">
        <div class="row q-gutter-md table-base-filter">
          <q-input
            dense
            debounce="300"
            v-model="filterCondition.query"
            placeholder="検索"
            class="table-base-filter-input"
            align="left"
          >
            <template v-slot:append>
              <q-spinner
                v-model="isLoading"
                v-if="isLoading"
                color="primary"
                size="md"
              />
              <q-icon
                name="search"
                v-if="
                  (filterCondition.query ?? '').length == 0 ||
                  filterCondition.query == null
                "
              />
              <q-icon name="search" v-else color="primary" />
              <div class="text-caption" v-if="records.length">
                {{ records.length }}
              </div>
            </template>
          </q-input>

          <ssbu-name-select v-model="filterCondition.charName" />
        </div>
        <div class="q-pt-md">
          <q-btn
            label="追加"
            icon-right="note_add"
            color="grey-6"
            @click="saveModalShow = true"
            outline
          />
        </div>
        <div class="q-pt-md">
          <lock-icon
            v-model="detailEditLock"
            @event-change="detailEditLock = $event"
            class="q-pt-sm"
          />
        </div>
      </div>
    </template>
    <!-- sub 2/3  ヘッダー-->
    <template v-slot:header="props">
      <q-tr :props="props">
        <q-th v-if="detailEditLock == false"> 編集 </q-th>
        <q-th v-for="col in props.cols" :key="col.name" :props="props">
          <div
            v-if="col.label == 'あだ名' || col.label == 'キャラ名'"
            class="table-base-main-column"
          >
            {{ col.label }}
          </div>
          <div v-else class="table-base-sub-column">
            {{ col.label }}
          </div>
        </q-th>
      </q-tr>
    </template>

    <!-- sub 3/3  アイテム-->
    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td v-if="detailEditLock == false">
          <a
            href="#"
            @click.prevent="
              console.log(props.row.word);
              onEditClick(props.row);
            "
            ><q-icon name="edit_note" color="secondary" size="md"></q-icon
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
    </template>
  </q-table>
  <!--追加画面-->
  <q-dialog v-model="saveModalShow" position="top">
    <q-card style="max-width: 700px">
      <q-card-section>
        <div>
          <div class="text-subtitle1 row q-gutter-md">
            <div class="text-h5" style="margin-right: auto">新規追加</div>
            <q-btn icon="close" @click="saveModalShow = false" round flat />
          </div>
          <div class="row q-gutter-md q-pa-md q-pb-lg">
            <div>
              <q-input
                label="あだ名"
                v-model="insertCondition.name"
                class="table-base-table-base-form-model"
                stack-label
                style="width: 250px"
                clearable
                dense
              />
            </div>
            <div>
              <ssbu-name-select v-model="insertCondition.ssbuName" />
            </div>
          </div>
          <div
            v-if="
              records.filter((it) => it.ssbuName == insertCondition.ssbuName)
                .length > 0
            "
          >
            <div class="text-subtitle1">追加済</div>
            <li
              v-for="n in records.filter(
                (it) => it.ssbuName == insertCondition.ssbuName
              )"
              :key="n.name"
            >
              {{ n.name }}
            </li>
          </div>

          <div class="row q-gutter-md q-pt-md">
            <q-btn
              @click.prevent="
                insertRecord(insertCondition.name, insertCondition.ssbuName)
              "
              label="追加"
              color="primary"
              outline
              icon="note_add"
              :loading="isSaveLoading"
              :disable="
                insertCondition.ssbuName == '' || insertCondition.name == ''
              "
            />
          </div>

          <div class="text-negative text-caption">
            {{ insertErr }}
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>

  <!--更新ダイアログ-->
  <q-dialog v-model="editModalShow">
    <q-card>
      <q-section>
        <div class="q-pa-md">
          <div class="row q-gutter-md">
            <div class="text-h6" style="margin-right: auto">更新・削除</div>
            <q-btn icon="close" @click="editModalShow = false" round flat />
          </div>

          <hr />
          <!--inputs-->
          <div class="row q-gutter-md">
            <q-input
              label="あだ名"
              v-model="updateCondition.name"
              class="table-base-table-base-form-model"
              dense
              outlined
              stack-label
              style="width: 250px"
              :hint="'更新前 : ' + updateBeforeCondition.name"
            />
            <div>
              <ssbu-name-select v-model="updateCondition.ssbuName" />
              <div class="q-pt-xs text-grey" style="font-size: 11px">
                {{ '更新前 : ' + updateBeforeCondition.ssbuName }}
              </div>
            </div>
          </div>
          <ul
            class="name-list-ul"
            v-if="
              records.filter((it) => it.ssbuName == updateCondition.ssbuName)
                .length > 0
            "
          >
            <div class="text-h6">登録済みのあだ名</div>
            <li
              class="name-list-li"
              v-for="n in records.filter(
                (it) => it.ssbuName == updateCondition.ssbuName
              )"
              :key="n.name"
            >
              {{ n.name }}
            </li>
          </ul>
          <!--buttons-->
          <hr />
          <div class="row q-gutter-md">
            <q-btn
              @click.prevent="
                updateRecord(
                  updateCondition.id,
                  updateCondition.name,
                  updateCondition.ssbuName
                )
              "
              label="更新"
              color="primary"
              outline
              icon="note_add"
              style="margin-right: auto"
              :loading="isSaveLoading"
            />
            <div class="text-negative text-caption">
              {{ updateErr }}
            </div>
            <q-btn
              @click.prevent="deleteCheckModalShow = true"
              label="削除"
              color="negative"
              outline
              icon="note_add"
            />
          </div>
        </div>
      </q-section>
    </q-card>
  </q-dialog>

  <!--削除確認-->
  <q-dialog v-model="deleteCheckModalShow">
    <q-card>
      <q-section>
        <div class="q-pa-md">
          <div class="row q-gutter-md">
            <div class="text-h6" style="margin-right: auto">削除確認</div>
            <q-btn
              icon="close"
              @click="deleteCheckModalShow = false"
              round
              flat
            />
          </div>
          <hr />
          <div>次のあだ名を削除してもいいかな？</div>
          <q-field label="あだ名" stack-label>{{
            updateCondition.name
          }}</q-field>
          <div class="row q-gutter-md q-pt-sm">
            <q-btn
              @click.prevent="deleteRecord(updateCondition.id)"
              label="削除する"
              color="negative"
              outline
              icon="note_add"
              dense
              :loading="isDeleteLoading"
            />
          </div>
        </div>
      </q-section>
    </q-card>
  </q-dialog>
</template>
<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import { useNameListModel } from 'src/models/NameListModels';
import SsbuNameSelect from '../selects/SsbuNameSelect.vue';
import lockIcon from 'src/components/LockIcon.vue';
export default defineComponent({
  name: 'name-list',
  props: {
    modelValue: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: false,
      default: 'あだ名一覧',
    },
    height: {
      type: Number,
      required: false,
      default: 700,
    },
  },
  components: {
    'lock-icon': lockIcon,
    'ssbu-name-select': SsbuNameSelect,
  },
  setup(props) {
    const {
      condition,
      saveModalShow,
      editModalShow,
      records,
      search,
      isLoading,
      updateRecord,
      insertCondition,
      isSaveLoading,
      deleteRecord,
      isDeleteLoading,
      detailEditLock,
      updateCondition,
      onEditClick,
      insertErr,
      insertRecord,
      updateErr,
      deleteCheckModalShow,
      columns,
      //initNameList,
      saveDisplayList,
      updateBeforeCondition,
    } = useNameListModel();
    //initNameList();
    search();

    //追加画面閉じたら初期化
    watch(editModalShow, () => {
      if (editModalShow.value == false) {
        updateCondition.value.name = '';
        updateCondition.value.ssbuName = '';
      }
    });

    //編集画面閉じたら初期化
    watch(saveModalShow, () => {
      if (saveModalShow.value == false) {
        insertCondition.value.name = '';
        insertCondition.value.ssbuName = '';
        saveDisplayList.value.splice(0);
      }
    });

    /*Filter */

    const filterCondition = ref({
      query: props.modelValue,
      charName: '',
    } as FilterState);

    const filteringData = function (rows: readonly DataState[]) {
      let letRows = rows;
      if (
        filterCondition.value.query != '' &&
        filterCondition.value.query != undefined
      ) {
        letRows = letRows.filter(
          (it) =>
            it.name.includes(filterCondition.value.query ?? '') ||
            it.ssbuName.includes(filterCondition.value.query ?? '')
        );
      }
      if (
        filterCondition.value.charName != '' &&
        filterCondition.value.charName != undefined
      ) {
        letRows = letRows.filter(
          (it) => it.ssbuName == (filterCondition.value.charName ?? '')
        );
      }
      console.log('filter', letRows);
      return letRows;
    };

    return {
      filterCondition,
      filteringData,
      tableName: ref(props.label),
      tableHeight: ref(props.height + 'px'),
      condition,
      editModalShow,
      records,
      search,
      isLoading,
      updateRecord,
      insertCondition,
      isSaveLoading,
      deleteRecord,
      isDeleteLoading,
      saveModalShow,
      visibleColumns: ref(true),
      detailEditLock,
      columns,
      updateCondition,
      onEditClick,
      insertErr,
      insertRecord,
      updateErr,
      deleteCheckModalShow,
      saveDisplayList,
      updateBeforeCondition,
    };
  },
});
interface FilterState {
  query: string;
  charName: string;
}
interface DataState {
  id: string;
  name: string;
  ssbuName: string;
  createAt: string;
  updateAt: string;
}
</script>
<style>
/*箇条書き */
.namelist-ul {
  background: #fcfcfc; /*背景色*/
  padding: 0.5em 0.5em 0.5em 2em; /*ボックス内の余白*/
  border: solid 3px gray; /*線の種類 太さ 色*/
}

.namelist-li {
  line-height: 1.5; /*文の行高*/
  padding: 0.5em 0; /*前後の文との余白*/
}
</style>
