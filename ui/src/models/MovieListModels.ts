import { QTableColumn, useQuasar } from 'quasar';
import api from 'src/api/file/MovieListApi';
import { ref } from 'vue';

export function useMovieListModel() {
  const quasar = useQuasar();
  const records = ref([] as DataState[]);
  const load = ref({
    search: false,
    download: false,
  } as Loading);
  const columns = [
    {
      name: 'fileName',
      label: 'ファイル名',
      field: 'fileName',
      sortable: true,
    },
  ] as QTableColumn[];
  const filter = ref({
    fileName: '',
    poster: '',
  } as FilterState);
  const posterOptions = ref([] as string[]);

  const filteringData = function (rows: readonly DataState[]) {
    let letRows = rows;
    if (filter.value.fileName != '' && filter.value.fileName != undefined) {
      letRows = letRows.filter((it) =>
        it.fileName.includes(filter.value.fileName)
      );
    }
    if (filter.value.poster != '' && filter.value.poster != undefined) {
      letRows = letRows.filter((it) => it.poster == filter.value.poster);
    }
    return letRows;
  };

  const search = async function () {
    load.value.search = true;
    await api
      .search()
      .then((response) => {
        if (response) {
          console.log('search', response);
          //動画
          records.value.splice(0);
          response.records.forEach((it) => records.value.push(it));
          //投稿者
          posterOptions.value.splice(0);
          Array.from(new Set(records.value.map((it) => it.poster))).forEach(
            (it) => posterOptions.value.push(it)
          );

          records.value.sort((a, b) => {
            const posterComparison = b.poster.localeCompare(a.poster);
            if (posterComparison !== 0) {
              return posterComparison; // posterが異なればそれでソート
            }
            // posterが同じならfileNameでソート
            return a.fileName.localeCompare(b.fileName);
          });
          posterOptions.value.reverse();
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
    columns,
    quasar,
    records,
    load,
    search,
    filter,
    filteringData,
    posterOptions,
  };
}
interface FilterState {
  fileName: string;
  poster: string;
}
interface DataState {
  id: number;
  fileName: string;
  poster: string;
}
interface Loading {
  search: boolean;
  download: boolean;
}
