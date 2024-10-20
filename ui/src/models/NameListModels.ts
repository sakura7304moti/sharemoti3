import { QTableColumn, useQuasar } from 'quasar';
import api from 'src/api/main/NameList2Api';
import { ref } from 'vue';

export function useNameListModel() {
  const quasar = useQuasar();
  const saveModalShow = ref(false); //追加
  const editModalShow = ref(false); //更新・削除

  const condition = ref({
    name: '',
    ssbuName: '',
  } as ConditionState);
  const insertCondition = ref({
    name: '',
    ssbuName: '',
  } as ConditionState);

  const updateCondition = ref({
    id: -1,
    name: '',
    ssbuName: '',
  } as UpdateCondition);
  const isLoading = ref(false);
  const isSaveLoading = ref(false);
  const isDeleteLoading = ref(false);
  const detailEditLock = ref(true);
  const records = ref([] as DataState[]);

  const columns = [
    {
      name: 'name',
      label: 'あだ名',
      field: 'name',
      sortable: true,
    },
    {
      name: 'ssbuName',
      label: 'キャラ名',
      field: 'ssbuName',
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

  /*SELECT */
  const search = async function () {
    isLoading.value = true;

    await api
      .search()
      .then((response) => {
        if (response) {
          console.log('response', response);

          records.value.splice(0);
          response.forEach((rec) => {
            records.value.push({
              id: rec.id,
              name: rec.name,
              ssbuName: rec.ssbuName,
              createAt: rec.createAt.split(' ')[0],
              updateAt: rec.updateAt.split(' ')[0],
            });
          });
          sortRecords();
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
  const saveDisplayList = ref([] as DataState[]);
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
    updateBeforeCondition.value = JSON.parse(JSON.stringify(rec));
    editModalShow.value = true;
  };

  const insertErr = ref('');
  const insertRecord = async function (name: string, ssbuName: string) {
    //バリテーション
    insertErr.value = '';
    if (name == '') {
      insertErr.value = 'あだ名を空にはできないよ!';
    }
    if (records.value.find((it) => it.name == name)) {
      insertErr.value = '既に同じあだ名が存在してるよ!';
    }
    if (insertErr.value == '') {
      isSaveLoading.value = true;
      const request = {
        name: name.replace(/\n/g, ''),
        ssbuName: ssbuName.replace(/\n/g, ''),
      } as ConditionState;
      await api
        .insert(request)
        .then((response) => {
          if (response) {
            console.log('response', response);

            //追加した場合
            search();
            insertCondition.value.name = '';
            insertCondition.value.ssbuName = '';
            quasar.notify({
              color: 'blue',
              position: 'top',
              message: '「' + name + '」を追加したよ！ いい名前っ b',
            });
            sortRecords();
            //saveModalShow.value = false;
            insertErr.value = '';
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
      isSaveLoading.value = false;
    }
  };

  const updateErr = ref('');
  const updateBeforeCondition = ref({
    id: -1,
    name: '',
    ssbuName: '',
  } as UpdateCondition);
  const updateRecord = async function (
    id: number,
    name: string,
    ssbuName: string
  ) {
    //バリエーション
    updateErr.value = '';
    if (updateErr.value == '') {
      isSaveLoading.value = true;
      const request = {
        id: id,
        name: name.replace(/\n/g, ''),
        ssbuName: ssbuName.replace(/\n/g, ''),
      };
      await api
        .update(request)
        .then((response) => {
          if (response) {
            console.log('response', response);

            //更新した場合
            search();
            insertCondition.value.name = '';
            insertCondition.value.ssbuName = '';
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
            message: 'データの取得に失敗しました',
          });
        });
      isSaveLoading.value = false;
    }
  };

  /*DELETE */
  const deleteCheckModalShow = ref(false);
  const deleteRecord = async function (id: number) {
    isDeleteLoading.value = true;

    const item = records.value.find((it) => it.id == id);
    const deleteName = item?.name ?? '';

    await api
      .dell({ id: id })
      .then((response) => {
        if (response) {
          console.log('response', response);

          //削除成功した場合
          quasar.notify({
            color: 'blue',
            position: 'top',
            message: deleteName + 'を消したでぇ',
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
          message: 'データの取得に失敗しました',
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
    saveDisplayList,
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
    updateBeforeCondition,
    columns,
  };
}

interface ConditionState {
  name: string;
  ssbuName: string;
}

interface UpdateCondition {
  id: number;
  name: string;
  ssbuName: string;
}

interface DataState {
  id: number;
  name: string;
  ssbuName: string;
  createAt: string;
  updateAt: string;
}
