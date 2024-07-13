<template>
  <q-select
    label="ハッシュタグ"
    v-model="condition.hashtags"
    use-input
    use-chips
    multiple
    hide-dropdown-icon
    input-debounce="0"
    new-value-mode="add-unique"
    stack-label
    dense
    hint="入力後 Enter・決定 で追加できるよ"
    style="width: 300px"
  >
    <template v-slot:append>
      <q-btn round dense flat icon="toc" @click="dialogOpen = true">
        <q-tooltip> ハッシュタグを一覧から選ぶ </q-tooltip>
      </q-btn>
    </template>
  </q-select>
  <q-dialog v-model="dialogOpen">
    <q-card
      style="width: 100%; max-width: 80vw; height: 100%; max-height: 80vh"
      class="q-pa-md"
    >
      <div class="full-width row justify-end">
        <div>
          <q-btn
            icon="close"
            flat
            color="primary"
            text-color="black"
            size="md"
            label="とじる"
            @click="dialogOpen = false"
          />
        </div>
      </div>
      <q-card-section>
        <div class="text-h6 q-pb-sm">ハッシュタグ検索</div>
        <q-table
          :rows="findHashtags"
          :columns="columns"
          :filter="hashtagCondition"
          row-key="name"
          separator="cell"
          :rows-per-page-options="[5, 100, 500, 1000]"
          :pagination="{ rowsPerPage: 1000 }"
          id="pixiv-hashtag-table"
          class="scroll-table"
        >
          <template v-slot:top-left>
            <q-input
              dense
              debounce="400"
              v-model="hashtagCondition"
              placeholder="検索"
              class="q-pb-mr"
            >
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </template>
          <template v-slot:top-right>
            <div class="full-width row wrap">
              <div v-for="tag in condition.hashtags" :key="tag">
                <q-chip
                  @remove="removeHashtag(tag)"
                  removable
                  dense
                  color="white"
                  text-color="primary"
                  class="q-ma-none"
                >
                  {{ tag }}
                </q-chip>
              </div>
            </div>
          </template>
          <template v-slot:header="props">
            <q-tr :props="props">
              <q-th style="width: 100px">選択</q-th>
              <q-th v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.label }}
              </q-th>
            </q-tr>
          </template>
          <template v-slot:body="props">
            <q-tr :props="props">
              <q-td
                class="text-center cursor-pointer"
                v-if="condition.hashtags.includes(props.row.name)"
                @click="removeHashtag(props.row.name)"
              >
                <q-icon name="check_box" size="md" color="primary" />
              </q-td>
              <q-td
                class="text-center cursor-pointer"
                v-else
                @click="addHashtag(props.row.name)"
              >
                <q-icon
                  name="check_box_outline_blank"
                  size="md"
                  color="primary"
                />
              </q-td>
              <q-td
                v-for="col in props.cols"
                :key="col.name"
                :props="props"
                style="white-space: normal; text-align: right"
              >
                {{ col.value }}
              </q-td>
            </q-tr>
          </template>
        </q-table>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import { PixivSearchStore } from 'src/stores/pixiv/PixivSearchStore';
import { QTableColumn } from 'quasar';
export default defineComponent({
  name: 'pixiv-hashtag-input',
  setup() {
    const store = PixivSearchStore();
    const isLoading = ref(store.isLoading.hashtag);
    const condition = ref(store.condition);

    const addHashtag = function (hashtag: string) {
      store.addHashtag(hashtag);
    };

    const removeHashtag = function (hashtag: string) {
      store.removeHashtag(hashtag);
    };

    watch(condition, (newValue, oldValue) => {
      oldValue.hashtags.forEach((it) => store.removeHashtag(it));
      newValue.hashtags.forEach((it) => store.addHashtag(it));
    });
    // -------------------
    // テーブル
    // -------------------

    const dialogOpen = ref(false);
    const hashtagCondition = ref(store.hashtagCondition);
    const searchHashtags = async function () {
      await store.searchHashtags();
    };
    const findHashtags = ref(store.findHashtags);
    const columns = [
      {
        name: 'name',
        label: 'ハッシュタグ',
        field: 'name',
        sortable: true,
      },
      {
        name: 'translatedName',
        label: '英語',
        field: 'translatedName',
        sortable: true,
      },
    ] as QTableColumn[];

    return {
      isLoading,
      condition,
      dialogOpen,
      findHashtags,
      addHashtag,
      removeHashtag,
      searchHashtags,
      hashtagCondition,
      columns,
    };
  },
});
</script>
<style>
#pixiv-hashtag-table {
  height: 60vh;
  overflow-y: auto;
}
/*テーブルのstyle */

#pixiv-hashtag-table .q-table__top,
#pixiv-hashtag-table .q-table__bottom,
#pixiv-hashtag-table thead tr:first-child th {
  /* bg color is important for th; just specify one */
  background-color: white;
}

#pixiv-hashtag-table thead tr th {
  position: sticky;
  z-index: 1;
}

#pixiv-hashtag-table thead tr:first-child th {
  top: 0;
}

/* this is when the loading indicator appears */
#pixiv-hashtag-table.q-table--loading thead tr:last-child th {
  /* height of all previous header rows */
  top: 48px;
}

/* prevent scrolling behind sticky top row on focus */
#pixiv-hashtag-table tbody {
  /* height of all previous header rows */
  scroll-margin-top: 48px;
}
</style>
