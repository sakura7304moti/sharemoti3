import { QTableColumn, useQuasar } from 'quasar';
import api from 'src/api/file/SsbuListApi';
import { NameListApi } from 'src/api/main/NameListApi';
import { ref } from 'vue';

export function useSsbuListModel() {
  const { names, ssbuNames, searchName, getSsbuNames } = useNameModel();
  const quasar = useQuasar();
  const selectId = ref(-1);

  const filter = ref({
    charName: '',
    title: '',
    date: '',
    folder: '',
  } as FilterState);

  const folderList = ref([
    'ウルトラC',
    '思い出',
    'ウルツラC',
    '焼き直し',
    '焼き直しフェニックス',
    '大江戸温泉物語',
    '素材',
  ]);

  const disableFilter = ref(false);

  const filteringData = function (rows: readonly DataState[]) {
    disableFilter.value = true;
    load.value.search = true;
    let letRows = rows;

    if (filter.value.charName != '' && filter.value.charName != undefined) {
      letRows = letRows.filter((it) => it.charName == filter.value.charName);
    }

    if (filter.value.title != '') {
      letRows = letRows.filter((it) =>
        it.fileName.includes(filter.value.title)
      );
    }

    if (filter.value.date ?? ''.length > 0) {
      letRows = letRows.filter((it) =>
        it.date.includes(filter.value.date?.replaceAll('/', '') ?? '')
      );
    }

    if (filter.value.folder ?? ''.length > 0) {
      letRows = letRows.filter((it) =>
        it.fileName.includes(filter.value.folder)
      );
    }

    disableFilter.value = false;
    load.value.search = false;
    return letRows;
  };

  const countFolder = function (radioName: string, rows: readonly DataState[]) {
    let filRow = filteringData(rows);
    filRow = filRow.filter((it) => it.fileName.includes(radioName));
    return filRow.length;
  };

  const columns = [
    {
      name: 'charName',
      label: 'キャラ名',
      field: 'charName',
      sortable: true,
    },
    {
      name: 'fileName',
      label: 'タイトル',
      field: 'fileName',
      sortable: true,
    },
    {
      name: 'displayDate',
      label: '日付',
      field: 'displayDate',
      sortable: true,
    },
    {
      name: 'icon',
      label: 'アイコン',
      field: 'icon',
      sortable: false,
    },
  ] as QTableColumn[];
  const load = ref({
    search: false,
    download: false,
  } as Loading);
  const records = ref([] as DataState[]);
  const dateList = ref([] as string[]);

  const splitName = function (fileName: string) {
    if (fileName.includes('_')) {
      const split = fileName.split('_');
      return split[0];
    } else {
      return '';
    }
  };

  const getDisplayFileName = function (fileName: string) {
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

  function formatDate(yyyymmdd: string) {
    if (yyyymmdd && yyyymmdd.length === 8) {
      const year = yyyymmdd.slice(0, 4);
      const month = yyyymmdd.slice(4, 6);
      const day = yyyymmdd.slice(6, 8);
      return `${year}/${month}/${day}`;
    }
    return yyyymmdd; // 変換できない場合はそのまま返す
  }

  function isValidDate(year: number, month: number, day: number) {
    // Dateオブジェクトによる有効な日付のチェック
    const date = new Date(year, month, day);
    return (
      date.getFullYear() === year &&
      date.getMonth() === month &&
      date.getDate() === day
    );
  }

  function convertToDate(dateString: string) {
    const parts = dateString.split('/');
    if (parts.length === 3) {
      const year = parseInt(parts[0], 10);
      const month = parseInt(parts[1], 10) - 1; // 月は0から始まるため1を引きます
      const day = parseInt(parts[2], 10);

      // 有効な日付か確認
      if (isValidDate(year, month, day)) {
        return new Date(year, month, day);
      }
    }
    return null; // 変換に失敗した場合は null を返す
  }

  // 日付を表す文字列をDateオブジェクトに変換し、比較用の関数を提供
  function compareDates(a: DataState, b: DataState) {
    const dateA = convertToDate(a.displayDate);
    const dateB = convertToDate(b.displayDate);
    if (dateA == null || dateB == null) {
      return 0;
    }

    if (dateA < dateB) {
      return -1;
    }
    if (dateA > dateB) {
      return 1;
    }
    return 0;
  }

  const search = async function () {
    load.value.search = true;
    disableFilter.value = true;
    await searchName();

    await api
      .search()
      .then((res) => {
        if (res) {
          console.log('search', res);
          records.value.splice(0);
          res.records.forEach((it) => {
            const displayDate = formatDate(it.date.replaceAll('_', ''));
            let displayFileName = getDisplayFileName(it.fileName);

            /*キャラ名の取得 */
            let charName = '';
            const spName = splitName(it.fileName);
            names.value.forEach((n) => {
              if (n.key == spName) {
                charName = n.val;
              }
            });

            /*キャラ名が空なら表示用ファイル名はそのまま表示させる */
            if (spName == '') {
              displayFileName = it.fileName;
            }

            records.value.push({
              id: it.id,
              charName: charName,
              fileName: it.fileName,
              displayFileName: displayFileName,
              date: it.date,
              displayDate: displayDate,
              year: it.year,
              icon:
                ssbuNames.value.find((it) => it.name == charName)?.icon ?? '',
            });
            if (!dateList.value.includes(displayDate)) {
              dateList.value.push(displayDate);
            }
          });
          dateList.value.sort();
          dateList.value.reverse();

          records.value.sort(compareDates);
          records.value.reverse();
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
    disableFilter.value = false;
    load.value.search = false;
  };

  return {
    filter,
    filteringData,
    countFolder,
    disableFilter,
    selectId,
    columns,
    load,
    records,
    dateList,
    ssbuNames,
    folderList,
    search,
    getSsbuNames,
  };
}

function useNameModel() {
  const nameApi = new NameListApi();
  const names = ref([] as nameState[]);
  const searchName = async function () {
    names.value.splice(0);

    await nameApi.search({ key: '', val: '' }).then((response) => {
      if (response) {
        console.log('name', response);
        response.records.forEach((it) =>
          names.value.push({ key: it.key ?? '', val: it.val ?? '' })
        );
      }
    });
  };

  const getName = function (name: string) {
    names.value.forEach((it) => {
      if (name == it.key) {
        return it.val;
      }
    });
    return '';
  };

  const ssbuNames = ref([] as SsbuNameState[]);
  const getSsbuNames = async function () {
    ssbuNames.value.splice(0);

    await nameApi.ssbu_names().then((res) => {
      if (res) {
        res.records.forEach((it) => ssbuNames.value.push(it));
      }
    });
  };

  return {
    //あだな一覧とスマブラのキャラ名の一覧を取得
    names,
    searchName,
    getSsbuNames,
    ssbuNames,
    getName,
  };
}

interface nameState {
  key: string;
  val: string;
}

interface Loading {
  search: boolean;
  download: boolean;
}

interface DataState {
  id: number;
  charName: string;
  fileName: string;
  displayFileName: string;
  date: string;
  displayDate: string;
  year: string;
  icon: string;
}

interface FilterState {
  charName: string;
  title: string;
  date: string | null;
  folder: string;
}

interface SsbuNameState {
  name: string;
  url: string;
  icon: string;
}
