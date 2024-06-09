import { QTableColumn, useQuasar } from 'quasar';
import api from 'src/api/file/KaraokeListApi';
import { ref } from 'vue';

export function useKaraokeListModel() {
  const quasar = useQuasar();
  const filter = ref('');
  const selectId = ref(-1);
  const columns = [
    {
      name: 'fileName',
      label: 'ファイル名',
      field: 'fileName',
      sortable: true,
    },
    {
      name: 'date',
      label: '日付',
      field: 'date',
      sortable: true,
    },
  ] as QTableColumn[];
  const load = ref({
    search: false,
    download: false,
  } as Loading);
  const records = ref([] as DataState[]);
  const dateList = ref([] as string[]);
  const musicList = ref([] as string[]);

  const getFileName = function (fileName: string) {
    if (fileName.includes('_')) {
      const split = fileName.split('_');
      if (split.length == 2) {
        return split[1];
      } else {
        return fileName;
      }
    } else {
      return fileName;
    }
  };

  const search = async function () {
    load.value.search = true;
    await api
      .search()
      .then((response) => {
        if (response) {
          console.log('search', response);
          records.value.splice(0);

          // 日付プロパティを持つオブジェクトのリストをソート
          const sortedDataStateList = response.records
            .map((data) => ({
              ...data,
              date: new Date(
                `${data.date.slice(0, 4)}-${data.date.slice(
                  4,
                  6
                )}-${data.date.slice(6, 8)}`
              ),
            }))
            .sort((a, b) => b.date.getTime() - a.date.getTime())
            .map((data) => ({
              ...data,
              date: data.date.toISOString().slice(0, 10),
            }));
          sortedDataStateList.forEach((it) => {
            it.fileName = getFileName(it.fileName);
            records.value.push(it);
            //日付のリスト
            if (!dateList.value.includes(it.date)) {
              dateList.value.push(it.date);
            }
            //曲のリスト
            if (!musicList.value.includes(it.fileName)) {
              musicList.value.push(it.fileName);
            }
          });
          musicList.value.sort();
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

  return {
    filter,
    columns,
    load,
    records,
    search,
    selectId,
    dateList,
    musicList,
  };
}
interface DataState {
  id: number;
  fileName: string;
  date: string;
}
interface Loading {
  search: boolean;
  download: boolean;
}
