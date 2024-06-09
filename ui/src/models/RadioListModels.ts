import { QTableColumn, useQuasar } from 'quasar';
import api from 'src/api/file/RadioListApi';
import { ref } from 'vue';

export function useRadioListModel() {
  const quasar = useQuasar();
  const filter = ref({
    text: '',
    date: '',
  } as FilterState);
  const dateFilter = ref('');
  const selectId = ref(-1);
  const columns = [
    {
      name: 'displayName',
      label: 'タイトル',
      field: 'displayName',
      sortable: true,
    },
    {
      name: 'date',
      label: '日時',
      field: 'date',
      sortable: true,
    },
    {
      name: 'fileName',
      label: 'ファイル名',
      field: 'fileName',
      sortable: true,
    },
  ] as QTableColumn[];
  const load = ref({
    search: false,
    download: false,
  } as Loading);
  const records = ref([] as DataState[]);
  const dateList = ref([] as string[]);

  const search = async function () {
    load.value.search = true;
    await api
      .search()
      .then((response) => {
        if (response) {
          console.log('search', response);
          records.value.splice(0);
          dateList.value.splice(0);
          const revDateList = [] as string[];

          response.records.forEach((it) => {
            if (!dateList.value.includes(it.date.split(' ')[0])) {
              dateList.value.push(it.date.split(' ')[0]);
              revDateList.push(it.date.split(' ')[0]);
            }

            const rec = {
              id: it.id,
              fileName: it.fileName,
              displayName: '',
              date: it.date,
            } as DataState;
            records.value.push(rec);
          });

          records.value.sort((a, b) => (a.date > b.date ? -1 : 1));

          revDateList.reverse();
          records.value.forEach((it) => {
            const displayName = `第${
              revDateList.indexOf(it.date.split(' ')[0]) + 1
            }回`;
            it.displayName = displayName;
          });
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
    load.value.search = false;
  };

  const filteringData = function (rows: readonly DataState[]) {
    let letRows = rows;
    if (filter.value.text != '') {
      letRows = letRows.filter(
        (it) =>
          it.displayName.includes(filter.value.text) ||
          it.fileName.includes(filter.value.text)
      );
    }
    if (filter.value.date != '' && filter.value.date != undefined) {
      letRows = letRows.filter((it) => it.date.includes(filter.value.date));
    }
    return letRows;
  };

  return {
    filter,
    columns,
    load,
    records,
    search,
    selectId,
    dateList,
    dateFilter,
    filteringData,
  };
}
interface DataState {
  id: number;
  fileName: string;
  displayName: string;
  date: string;
}
interface FilterState {
  text: string;
  date: string;
}
interface Loading {
  search: boolean;
  download: boolean;
}
