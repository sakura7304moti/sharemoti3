import { QTableColumn, useQuasar } from 'quasar';
import api, {
  HaikuListInsertRequest,
  HaikuListSearchRequest,
} from 'src/api/main/HaikuListApi';
import { ref } from 'vue';

export function useHaikuListModel() {
  const KEY_LOCAL_STRAGE = 'haiku-list-sort';
  const setSortValue = function () {
    const viewValue = localStorage.getItem(KEY_LOCAL_STRAGE);
    if (viewValue) {
      displaySort.value = viewValue == 'desc';
    }
  };

  const quasar = useQuasar();
  const lockIconCondition = ref(true);
  const displaySort = ref(false);
  const displayCondition = ref({
    upper: true,
    insert: false,
    update: false,
    delete: false,
    detail: true,
  } as DisplayCondition);
  const condition = ref({
    haikuText: '',
    poster: '',
    detailContain: true,
  } as ConditionState);

  const insertCondition = ref({
    first: '',
    second: '',
    third: '',
    poster: '',
    detail: '',
  } as InsertConditionState);

  const updateSelectedCondition = ref({
    id: -1,
    first: '',
    second: '',
    third: '',
    poster: '',
    detail: '',
  } as UpdateConditionState);

  const updateCondition = ref({
    id: -1,
    first: '',
    second: '',
    third: '',
    poster: '',
    detail: '',
  } as UpdateConditionState);

  const LoadingCondition = ref({
    search: false,
    insert: false,
    update: false,
    delete: false,
  } as LoadingCondition);
  const records = ref([] as DataState[]);

  const tableView = ref(false);

  const rows = ref([] as Row[]);

  const columns = [
    {
      name: 'first',
      label: '5',
      field: 'first',
      sortable: true,
    },
    {
      name: 'second',
      label: '7',
      field: 'second',
      sortable: true,
    },
    {
      name: 'third',
      label: '5',
      field: 'third',
      sortable: true,
    },
    {
      name: 'detail',
      label: '解説',
      field: 'detail',
      sortable: true,
    },
    {
      name: 'poster',
      label: '投稿者',
      field: 'poster',
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

  const sortfn = function (a: DataState, b: DataState) {
    if (a.id > b.id) {
      return 1;
    } else {
      return -1;
    }
  };
  const sortRecords = function () {
    records.value.sort(sortfn);
  };

  const rangeChange = function () {
    if (displaySort.value == true) {
      localStorage.setItem(KEY_LOCAL_STRAGE, 'desc');
    } else {
      localStorage.setItem(KEY_LOCAL_STRAGE, 'asc');
    }

    records.value.reverse();
  };

  /*SELECT */
  const search = async function (query = '') {
    setSortValue();
    LoadingCondition.value.search = true;
    const request = {
      id: -1,
      haikuText: '',
      detail: '',
      poster: condition.value.poster,
    } as HaikuListSearchRequest;
    if (condition.value.detailContain) {
      request.detail = condition.value.haikuText;
    } else {
      request.haikuText = condition.value.haikuText;
    }
    if (query != '') {
      request.haikuText = query;
    }
    console.log('request', request);
    await api
      .search()
      .then((response) => {
        if (response) {
          console.log('response', response);
          records.value.splice(0);
          rows.value.splice(0);
          response.forEach((rec) => {
            records.value.push({
              id: rec.id,
              first: rec.first,
              second: rec.second,
              third: rec.third,
              poster: rec.poster,
              detail: rec.detail,
              createAt: rec.createAt,
              updateAt: rec.updateAt,
              detailDisplay: false,
            });
            rows.value.push({
              id: rec.id,
              first: rec.first,
              second: rec.second,
              third: rec.third,
              poster: rec.poster,
              detail: rec.detail,
              createAt: rec.createAt.split(' ')[0],
              updateAt: rec.updateAt.split(' ')[0],
            });
          });
          sortRecords();

          console.log();
          if (displaySort.value) {
            records.value.reverse();
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

    LoadingCondition.value.search = false;
  };
  /*INSERT */
  const insertClick = function () {
    insertCondition.value = {
      first: '',
      second: '',
      third: '',
      poster: '',
      detail: '',
    } as InsertConditionState;
    displayCondition.value.insert = true;
  };
  const insert = async function () {
    insertCondition.value.valitationErr = '';
    if (insertCondition.value.poster == '') {
      insertCondition.value.valitationErr = '投稿者名を空にはできないよ!';
    }
    if (insertCondition.value.valitationErr == '') {
      const request = {
        first: insertCondition.value.first.replace(/\n/g, ''),
        second: insertCondition.value.second.replace(/\n/g, ''),
        third: insertCondition.value.third.replace(/\n/g, ''),
        poster: insertCondition.value.poster.replace(/\n/g, ''),
        detail: insertCondition.value.detail,
      } as HaikuListInsertRequest;
      LoadingCondition.value.insert = true;
      await api
        .insert(request)
        .then((response) => {
          if (response) {
            console.log('response', response);
            quasar.notify({
              color: 'blue',
              position: 'top',
              message: 'いい俳句やでぇ b',
            });
            insertCondition.value = {
              first: '',
              second: '',
              third: '',
              poster: '',
              detail: '',
              valitationErr: '',
            };
            search();
          }
        })
        .catch((e) => {
          console.log(e);

          quasar.notify({
            color: 'red',
            position: 'top',
            message: 'データの追加に失敗しました',
          });
        });
      LoadingCondition.value.insert = false;
    }
  };

  /*UPDATE */
  const updateClick = function (rec: DataState) {
    updateSelectedCondition.value = JSON.parse(JSON.stringify(rec)); //編集前の表示用
    updateCondition.value = JSON.parse(JSON.stringify(rec)); //編集中
    displayCondition.value.update = true;
  };

  const update = async function () {
    updateCondition.value.valitationErr = '';
    if (updateCondition.value.poster == '') {
      updateCondition.value.valitationErr = '投稿者名を空にはできないよ!';
    }
    if (updateCondition.value.valitationErr == '') {
      LoadingCondition.value.update = true;
      await api
        .update({
          id: updateSelectedCondition.value.id,
          first: updateCondition.value.first,
          second: updateCondition.value.second,
          third: updateCondition.value.third,
          detail: updateCondition.value.detail,
          poster: updateCondition.value.poster,
        })
        .then((response) => {
          if (response) {
            console.log('response', response);

            search();

            displayCondition.value.update = false;

            quasar.notify({
              color: 'blue',
              position: 'top',
              message: '更新した！',
            });
          }
        })
        .catch((e) => {
          console.log(e);

          quasar.notify({
            color: 'red',
            position: 'top',
            message: 'データの更新に失敗しました',
          });
        });
      LoadingCondition.value.update = false;
    }
  };

  /*DELETE */
  const deleteClick = function (rec: DataState) {
    updateSelectedCondition.value = JSON.parse(JSON.stringify(rec));
    displayCondition.value.delete = true;
  };
  const deleteRecord = async function () {
    await api
      .delete(updateSelectedCondition.value.id)
      .then((response) => {
        if (response) {
          console.log('response', response);

          const index = records.value.findIndex(
            (it) => it.id == updateSelectedCondition.value.id
          );
          records.value.splice(index, 1);
          quasar.notify({
            color: 'blue',
            position: 'top',
            message: '消しといたで！',
          });
          displayCondition.value.delete = false;
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
  };
  return {
    displaySort,
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
  };
}

interface DisplayCondition {
  upper: boolean;
  insert: boolean;
  update: boolean;
  delete: boolean;
  detail: boolean;
}

interface LoadingCondition {
  search: boolean;
  insert: boolean;
  update: boolean;
  delete: boolean;
}

interface ConditionState {
  haikuText: string;
  poster: string;
  detailContain: boolean;
}

interface InsertConditionState {
  first: string;
  second: string;
  third: string;
  poster: string;
  detail: string;
  valitationErr: string;
}

interface UpdateConditionState {
  id: number;
  first: string;
  second: string;
  third: string;
  poster: string;
  detail: string;
  valitationErr: string;
}

interface DataState {
  id: number;
  first: string;
  second: string;
  third: string;
  poster: string;
  detail: string;
  createAt: string;
  updateAt: string;
  detailDisplay: boolean;
}

interface Row {
  id: number;
  first: string;
  second: string;
  third: string;
  poster: string;
  detail: string;
  createAt: string;
  updateAt: string;
}
