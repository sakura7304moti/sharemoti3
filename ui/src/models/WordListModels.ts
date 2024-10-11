import { QTableColumn, useQuasar } from 'quasar';
import api from 'src/api/main/WordList2Api';
import { ref } from 'vue';

export function useWordListModel() {
  const quasar = useQuasar();
  const saveModalShow = ref(false); //追加
  const editModalShow = ref(false); //更新・削除

  const columns = [
    {
      name: 'word',
      label: '名言',
      field: 'word',
      sortable: true,
    },
    {
      name: 'detail',
      label: '詳細',
      field: 'detail',
      sortable: true,
    },
    {
      name: 'createAt',
      label: '作成日',
      field: 'createAt',
      sortable: true,
    },
    {
      name: 'updateAt',
      label: '更新日',
      field: 'updateAt',
      sortable: true,
    },
  ] as QTableColumn[];

  const searchCondition = ref('');
  const insertCondition = ref({
    word: '',
    detail: '',
  } as InsertCondition);

  const updateCondition = ref({
    id: -1,
    word: '',
    detail: '',
  } as UpdateCondition);
  const isLoading = ref(false);
  const isSaveLoading = ref(false);
  const isDeleteLoading = ref(false);
  const detailEditLock = ref(true);
  const records = ref([] as DataState[]);

  /*SORT */
  const wordSortState = ref('');
  const wordSort = function () {
    //言葉の昇順 -> 降順 -> デフォルトの繰り返し
    //日付のソートはリセットする
    if (wordSortState.value == '') {
      dateSortState.value = '';
      records.value.sort(compare);
      wordSortState.value = 'up';
    } else if (wordSortState.value == 'up') {
      dateSortState.value = '';
      records.value.sort(compareDown);
      wordSortState.value = 'down';
    } else if (wordSortState.value == 'down') {
      dateSortState.value = '';
      records.value.sort(compare);
      wordSortState.value = '';
    }

    function compare(a: DataState, b: DataState) {
      return a.word >= b.word ? 1 : -1;
    }

    function compareDown(a: DataState, b: DataState) {
      return a.word >= b.word ? -1 : 1;
    }
  };

  const dateSortState = ref('');
  const dateSort = function () {
    //言葉の昇順 -> 降順 -> デフォルトの繰り返し
    //言葉のソートはリセットする
    if (dateSortState.value == '') {
      wordSortState.value = '';
      records.value.sort(compare);
      dateSortState.value = 'up';
    } else if (dateSortState.value == 'up') {
      wordSortState.value = '';
      records.value.sort(compareDown);
      dateSortState.value = 'down';
    } else if (dateSortState.value == 'down') {
      wordSortState.value = '';
      records.value.sort(compare);
      dateSortState.value = '';
    }

    function compare(a: DataState, b: DataState) {
      const date1 = a.createAt >= a.updateAt ? a.createAt : a.updateAt;
      const date2 = b.createAt >= b.updateAt ? b.createAt : b.updateAt;
      return date1 >= date2 ? 1 : -1;
    }

    function compareDown(a: DataState, b: DataState) {
      const date1 = a.createAt >= a.updateAt ? a.createAt : a.updateAt;
      const date2 = b.createAt >= b.updateAt ? b.createAt : b.updateAt;
      return date1 >= date2 ? -1 : 1;
    }
  };

  /*SELECT */
  const search = async function () {
    isLoading.value = true;
    await api
      .search({
        text: searchCondition.value,
      })
      .then((response) => {
        if (response) {
          console.log('response', response);

          records.value.splice(0);
          response.forEach((rec) =>
            records.value.push({
              id: rec.id,
              word: rec.word ?? '',
              detail: rec.detail ?? '',
              createAt: rec.createAt,
              updateAt: rec.updateAt,
            })
          );
          sortRecords();
          console.log('select', records.value);
        }
      })
      .catch((e) => {
        console.log(e);

        quasar.notify({
          color: 'red',
          position: 'top',
          message: 'データの取得に失敗...',
        });
      });
    isLoading.value = false;
  };

  /*INSERT , UPDATE*/
  const sortfn = function (a: DataState, b: DataState) {
    if (a.word > b.word) {
      return 1;
    } else {
      return -1;
    }
  };
  const sortRecords = function () {
    records.value.sort(sortfn);
  };
  const onEditClick = function (rec: DataState) {
    updateCondition.value = JSON.parse(JSON.stringify(rec));
    editModalShow.value = true;
  };

  const insertErr = ref('');
  const insertRecord = async function (condition: InsertCondition) {
    //バリテーション
    insertErr.value = '';
    if (condition.word == '') {
      insertErr.value = '名言を空にはできないよ!';
    }
    if (records.value.find((it) => it.word == condition.word)) {
      insertErr.value = '既に同じ名言が存在してるよ!';
    }
    if (insertErr.value == '') {
      isSaveLoading.value = true;
      await api
        .insert(condition)
        .then((response) => {
          if (response) {
            console.log('response', response);
            search();
            insertCondition.value.word = '';
            insertCondition.value.detail = '';
            quasar.notify({
              color: 'blue',
              position: 'top',
              message: '追加したわよっ！',
            });
            sortRecords();
            insertErr.value = '';
          }
        })
        .catch((e) => {
          console.log(e);

          quasar.notify({
            color: 'red',
            position: 'top',
            message: 'データの追加に失敗した...',
          });
        });
      isSaveLoading.value = false;
    }
  };

  const updateErr = ref('');
  const updateRecord = async function (condition: UpdateCondition) {
    //バリエーション
    updateErr.value = '';
    if (condition.word == '') {
      updateErr.value = '名言を空にはできないよ!';
    }
    if (updateErr.value == '') {
      isSaveLoading.value = true;
      await api
        .update(condition)
        .then((response) => {
          if (response) {
            console.log('response', response);
            search();
            updateCondition.value.id = -1;
            updateCondition.value.word = '';
            updateCondition.value.detail = '';
            quasar.notify({
              color: 'blue',
              position: 'top',
              message: '更新した！',
            });
            editModalShow.value = false;
          }
        })
        .catch((e) => {
          console.log(e);

          quasar.notify({
            color: 'red',
            position: 'top',
            message: 'データの取得に失敗...',
          });
        });
      isSaveLoading.value = false;
    }
  };

  /*DELETE */
  const deleteCheckModalShow = ref(false);
  const deleteRecord = async function (id: number) {
    isDeleteLoading.value = true;

    await api
      .delete({ id: id })
      .then((response) => {
        if (response) {
          console.log('response', response);

          //削除成功した場合
          if (response.status) {
            quasar.notify({
              color: 'blue',
              position: 'top',
              message: '消したでぇ',
            });
            const index = records.value.findIndex((it) => it.id == id);
            records.value.splice(index, 1);
            updateCondition.value.word = '';
            updateCondition.value.detail = '';
            editModalShow.value = false;
            deleteCheckModalShow.value = false;
          } else {
            quasar.notify({
              color: 'red',
              position: 'top',
              message: 'データの削除に失敗...',
            });
          }
        }
      })
      .catch((e) => {
        console.log(e);

        quasar.notify({
          color: 'red',
          position: 'top',
          message: 'データの取得に失敗しました',
        });
      });
    isDeleteLoading.value = false;
  };

  return {
    searchCondition,
    saveModalShow,
    editModalShow,
    records,
    search,
    isLoading,
    insertCondition,
    updateRecord,
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
    /*sort */
    wordSortState,
    wordSort,
    dateSortState,
    dateSort,
  };
}

interface InsertCondition {
  word: string;
  detail: string | null;
}

interface UpdateCondition {
  id: number;
  word: string;
  detail: string | null;
}

interface DataState {
  id: number;
  word: string;
  detail: string | null;
  createAt: string;
  updateAt: string;
}
