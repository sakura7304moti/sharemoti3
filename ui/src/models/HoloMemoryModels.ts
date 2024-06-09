import { QTableColumn, useQuasar } from 'quasar';
import api from 'src/api/scraper/HoloMovieApi';
import { HoloSongApi } from 'src/api/scraper/HoloSongApi';
import { ref } from 'vue';

export function useHoloMemoryModel() {
  const songApi = new HoloSongApi();
  const { getImageLink } = subModel();
  const quasar = useQuasar();

  const columns = [
    {
      name: 'member',
      label: 'メンバー',
      field: 'member',
      sortable: true,
    },
    {
      name: 'title',
      label: 'タイトル',
      field: 'title',
      sortable: true,
    },
    {
      name: 'date',
      label: '投稿日',
      field: 'date',
      sortable: true,
    },
    {
      name: 'memory',
      label: '区分',
      field: 'memory',
      sortable: true,
    },
    {
      name: 'detail',
      label: '詳細',
      field: 'detail',
      sortable: true,
    },
  ] as QTableColumn[];

  const rows = ref([] as TableRow[]);
  const displayMode = ref('gallery');

  const records = ref([] as DataState[]);
  const pageState = ref({
    selectLink: '',
    pageNo: 1,
    totalPages: 1,
    pageSize: 20,
    records: [] as DataState[],
  } as PageState);
  const holoMembers = ref([] as string[]);
  const getMembers = async function () {
    holoMembers.value.splice(0);
    await songApi
      .holoList()
      .then((response) => {
        if (response) {
          console.log('holo member', response);
          response.forEach((it) => holoMembers.value.push(it));
          console.log(
            'max length',
            Math.max(...holoMembers.value.map((it) => it.length))
          );
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
  };
  const songList = ref([] as string[]);

  const isLoading = ref(false);
  const searchOptionShow = ref(false);

  const select = async function () {
    isLoading.value = true;
    getMembers();
    records.value.splice(0);
    await api
      .memory()
      .then((response) => {
        if (response) {
          console.log('search', response);
          //レコードのリスト
          response.records.forEach((it) => {
            records.value.push({
              title: it.title,
              member: it.member,
              link: it.link,
              date: it.date,
              memory: it.memory,
              detail: it.detail,
              imageLink: getImageLink(it.link),
            });
          });
          records.value.reverse();
          console.log('add list', records.value.length);

          //ページング用オブジェクトを準備
          pageState.value.totalPages = Math.ceil(
            records.value.length / pageState.value.pageSize
          );
          selectPage();

          //テーブル
          rows.value.splice(0);
          records.value.forEach((rec) => {
            rows.value.push(rec);
          });

          //曲名の一覧を取得
          songList.value.splice(0);
          songList.value = [
            ...new Set(records.value.map((it) => it.title.trim())),
          ];
          songList.value.sort();
          console.log('songs', songList.value.length);
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

  const selectPage = function () {
    pageState.value.records.splice(0);
    //1ページ目 -> 0 ~ 19
    //2ページ目 -> 20 ~ 39
    //3ページ目 -> 40 ~ 59
    const startIndex =
      Math.max(pageState.value.pageNo - 1, -1) * pageState.value.pageSize;
    const lastIndex = Math.min(
      startIndex + pageState.value.pageSize - 1,
      records.value.length
    );
    records.value.slice(startIndex, lastIndex).forEach((rec) => {
      pageState.value.records.push(rec);
    });
    console.log('data', pageState.value);
  };

  return {
    quasar,
    records,
    holoMembers,
    pageState,
    isLoading,
    searchOptionShow,
    rows,
    columns,
    displayMode,
    songList,
    select,
    selectPage,
    getMembers,
  };
}

function subModel() {
  const getVideoId = function (url: string) {
    const v = url.split('v=')[1];
    if (v != undefined) {
      return v;
    } else {
      const s = url.split('/')[url.split('/').length - 1];
      return s;
    }
  };

  const getImageLink = function (url: string) {
    const baseUrl = 'https://img.youtube.com/vi/query/mqdefault.jpg';
    return baseUrl.replace('query', getVideoId(url));
  };

  const getAlterImageLink = function (url: string) {
    const baseUrl = 'https://img.youtube.com/vi/query/default.jpg';
    return baseUrl.replace('query', getVideoId(url));
  };

  const getDisplayName = function (text: string) {
    if (text.length > 19) {
      return text.substring(0, 19) + '...';
    } else {
      return text;
    }
  };
  return {
    getVideoId,
    getImageLink,
    getAlterImageLink,
    getDisplayName,
  };
}
interface DataState {
  title: string;
  member: string;
  link: string;
  date: string;
  memory: string;
  detail: string;
  imageLink: string;
}
interface PageState {
  selectLink: string;
  pageNo: number;
  totalPages: number;
  pageSize: number;
  records: DataState[];
}
interface TableRow {
  title: string;
  member: string;
  link: string;
  date: string;
  memory: string;
  detail: string;
}
