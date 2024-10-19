import { QTableColumn, useQuasar } from 'quasar';
import api from 'src/api/main/YakiListApi';
import { ref } from 'vue';

export function useYakiListModel() {
  const quasar = useQuasar();
  const saveModalShow = ref(false); //追加
  const editModalShow = ref(false); //更新・削除
  const selecter = ['焼き直し', '焼き直しフェニックス'];
  const columns = [
    {
      name: 'word',
      label: '条約',
      field: 'word',
      sortable: true,
    },
    {
      name: 'yaki',
      label: '種類',
      field: 'yaki',
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
  const condition = ref({
    word: '',
    yaki: '',
  } as ConditionState);
  const insertCondition = ref({
    word: '',
    yaki: '焼き直し',
  } as ConditionState);

  const updateCondition = ref({
    id: -1,
    word: '',
    yaki: '',
  } as UpdateCondition);
  const isLoading = ref(false);
  const isSaveLoading = ref(false);
  const isDeleteLoading = ref(false);
  const detailEditLock = ref(true);
  const records = ref([] as DataState[]);

  /*SELECT */
  const search = async function () {
    isLoading.value = true;
    await api
      .search()
      .then((response) => {
        if (response) {
          console.log('response', response);

          records.value.splice(0);
          response.forEach((rec) =>
            records.value.push({
              id: rec.id,
              word: rec.word,
              yaki: rec.yaki,
              createAt: rec.createAt.split(' ')[0],
              updateAt: rec.updateAt.split(' ')[0],
            })
          );
          sortRecords();
          if (condition.value.word == '焼き直し') {
            records.value = records.value.filter((it) => it.yaki == '焼き直し');
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
    isLoading.value = false;
  };

  /*INSERT , UPDATE*/
  const sortfn = function (a: DataState, b: DataState) {
    if (a.createAt < b.createAt) {
      return 1;
    } else {
      return -1;
    }
  };
  const sortRecords = function () {
    records.value.sort(sortfn);
  };
  const onEditClick = function (rec: ConditionState) {
    updateCondition.value = JSON.parse(JSON.stringify(rec));
    editModalShow.value = true;
  };

  const insertErr = ref('');
  const insertRecord = async function (word: string, yaki: string) {
    //バリテーション
    insertErr.value = '';
    if (word == '') {
      insertErr.value = '条約を空にはできないよ!';
    }
    if (records.value.find((it) => it.word == word)) {
      insertErr.value = '既に同じ条約が存在してるよ!';
    }
    if (insertErr.value == '') {
      isSaveLoading.value = true;
      const request = {
        word: word,
        yaki: yaki.replace(/\n/g, ''),
      } as ConditionState;
      await api
        .insert(request)
        .then((response) => {
          if (response) {
            console.log('response', response);

            //追加した場合
            search();
            insertCondition.value.word = '';
            quasar.notify({
              color: 'blue',
              position: 'top',
              message: '追加完了!',
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
            message: 'データの取得に失敗しました...',
          });
        });
      isSaveLoading.value = false;
    }
  };

  const updateErr = ref('');
  const updateRecord = async function (id: number, word: string, yaki: string) {
    //バリエーション
    updateErr.value = '';
    if (updateErr.value == '') {
      isSaveLoading.value = true;
      const request = {
        id: id,
        word: word,
        yaki: yaki.replace(/\n/g, ''),
      };
      await api
        .update(request)
        .then((response) => {
          if (response) {
            console.log('response', response);

            //更新した場合
            search();
            insertCondition.value.word = '';
            insertCondition.value.yaki = '';
            quasar.notify({
              color: 'blue',
              position: 'top',
              message: '更新完了!',
            });
            editModalShow.value = false;
          }
        })
        .catch((e) => {
          console.log(e);

          quasar.notify({
            color: 'red',
            position: 'top',
            message: 'データの取得に失敗しました...',
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
      .dell({ id: id })
      .then((response) => {
        if (response) {
          console.log('response', response);
          quasar.notify({
            color: 'blue',
            position: 'top',
            message: '削除完了しました',
          });
          search();
          editModalShow.value = false;
          deleteCheckModalShow.value = false;
        }
      })
      .catch((e) => {
        console.log(e);

        quasar.notify({
          color: 'red',
          position: 'top',
          message: 'データの削除に失敗しました',
        });
      });
    isDeleteLoading.value = false;
  };

  return {
    condition,
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
    selecter,
    columns,
  };
}

interface ConditionState {
  word: string;
  yaki: string;
}

interface UpdateCondition {
  id: number;
  word: string;
  yaki: string;
}

interface DataState {
  id: number;
  word: string;
  yaki: string;
  createAt: string;
  updateAt: string;
}
