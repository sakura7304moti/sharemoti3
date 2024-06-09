import { QTableColumn, useQuasar } from 'quasar';
import api from 'src/api/scraper/HoloSongApi';
import { ref } from 'vue';

export function useHoloSongModel() {
  const { getVideoId, getImageLink, getAlterImageLink, getDisplayName } =
    subModel();

  const quasar = useQuasar();

  const columns = [
    {
      name: 'member',
      label: 'メンバー',
      field: 'member',
      sortable: true,
    },
    {
      name: 'songName',
      label: '曲名',
      field: 'songName',
      sortable: true,
    },
    {
      name: 'date',
      label: '投稿日',
      field: 'date',
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
    await api
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
      .search()
      .then((response) => {
        if (response) {
          //レコードのリスト
          response.records.forEach((it) => {
            if (it.link.includes('you') && !it.detail.includes('非公開')) {
              const addRec = {
                date: it.date,
                member: it.member,
                link: it.link.replace('youtu.be/', 'www.youtube.com/watch?v='),
                songName: it.songName,
                detail: it.detail,
                imageLink: getImageLink(it.link),
                alterLink: getAlterImageLink(it.link),
                videoId: getVideoId(it.link),
              } as DataState;
              records.value.push(addRec);
            }
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
            rows.value.push({
              member: rec.member,
              displayMember: getDisplayName(rec.member),
              songName: rec.songName,
              date: rec.date,
              detail: rec.detail,
              link: rec.link,
            } as TableRow);
          });

          //曲名の一覧を取得
          songList.value.splice(0);
          songList.value = [
            ...new Set(records.value.map((it) => it.songName.trim())),
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
    // YouTubeの動画IDを抽出する正規表現
    const regExp =
      /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = url.match(regExp);

    if (match && match[2].length == 11) {
      // YouTubeのサムネイルURLを生成
      return match[2];
    } else {
      // 適切なURLが得られなかった場合はnullを返す
      return '';
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
  date: string;
  member: string;
  link: string;
  songName: string;
  detail: string;
  imageLink: string;
  alterLink: string;
  videoId: string;
}
interface PageState {
  selectLink: string;
  pageNo: number;
  totalPages: number;
  pageSize: number;
  records: DataState[];
}
interface TableRow {
  member: string;
  displayMember: string;
  link: string;
  songName: string;
  date: string;
  detail: string;
}
