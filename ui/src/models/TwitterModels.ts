import { useQuasar } from 'quasar';
import api, { TwitterRequest } from 'src/api/scraper/TwitterApi';
import { selectItem } from 'src/types/selectorType';
import { ref } from 'vue';

export function useTwitterModel() {
  //yyyy/mm/dd
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const day = String(today.getDate()).padStart(2, '0');
  const formattedDate = `${year}/${month}/${day}`;
  const searchOptionShow = ref(false);

  //val
  const quasar = useQuasar();
  const condition = ref({
    pageNo: 1,
    pageSize: 20,
    hashtag: '',
    startDate: '',
    endDate: formattedDate,
    userName: '',
    mode: 'holo',
    minLike: 100,
    maxLike: 0,
  } as ConditionState);

  const fetchedCondition = ref({
    pageNo: 0,
    pageSize: 20,
    hashtag: '',
    startDate: '',
    endDate: formattedDate,
    userName: '',
    minLike: 100,
    maxLike: 0,
  } as ConditionState);

  const dataState = ref({
    totalPages: 0,
    records: [] as TwitterRecord[],
  } as DataState);

  const dateModalShow = ref(false);

  const selectItems = [
    {
      label: '未指定',
      value: 0,
    },
    {
      label: '100',
      value: 100,
    },
    {
      label: '1000',
      value: 1000,
    },
    {
      label: '5000',
      value: 5000,
    },
    {
      label: '10000',
      value: 10000,
    },
    {
      label: '20000',
      value: 20000,
    },
    {
      label: '50000',
      value: 50000,
    },
    {
      label: '100000',
      value: 100000,
    },
  ] as Array<selectItem>;

  const dateToString = function (date: string) {
    if (date) {
      return date.replaceAll('/', '-');
    } else {
      return '';
    }
  };

  const isLoading = ref(false);
  //検索条件変わっていたらページを1にする
  const compareCondition = function () {
    if (condition.value.hashtag != fetchedCondition.value.hashtag) {
      condition.value.pageNo = 1;
    }
    if (condition.value.startDate != fetchedCondition.value.startDate) {
      condition.value.pageNo = 1;
    }
    if (condition.value.endDate != fetchedCondition.value.endDate) {
      condition.value.pageNo = 1;
    }
    if (condition.value.userName != fetchedCondition.value.userName) {
      condition.value.pageNo = 1;
    }
    if (condition.value.minLike != fetchedCondition.value.minLike) {
      condition.value.pageNo = 1;
    }
    if (condition.value.maxLike != fetchedCondition.value.maxLike) {
      condition.value.pageNo = 1;
    }
  };
  const search = async function () {
    isLoading.value = true;
    dataState.value.records.splice(0);
    compareCondition(); //検索条件変わったらページ数1にする
    if (
      condition.value.minLike == null ||
      condition.value.minLike == undefined
    ) {
      condition.value.minLike = 0;
    }
    const request = {
      page_no: condition.value.pageNo,
      page_size: condition.value.pageSize,
      hashtag: condition.value.hashtag,
      start_date: dateToString(condition.value.startDate),
      end_date: dateToString(condition.value.endDate),
      user_name: condition.value.userName,
      mode: condition.value.mode,
      min_like: condition.value.minLike ?? 0,
      max_like: condition.value.maxLike ?? 0,
      displayMenu: false,
    } as TwitterRequest;

    await api
      .search(request)
      .then((response) => {
        if (response) {
          console.log('response', response);

          dataState.value.totalPages = response.totalPages;

          response.records.forEach((rec) => {
            rec.images.forEach((r) => {
              if (
                dataState.value.records.filter(
                  (it) => it.image == convertImageLink(r)
                ).length == 0
              ) {
                const url = rec.url.includes('pic.twitter.com')
                  ? 'https://' + rec.url
                  : rec.url;
                dataState.value.records.push({
                  hashtag: rec.hashtag,
                  mode: rec.mode,
                  url: url,
                  date: rec.date,
                  image: convertImageLink(r),
                  userId: rec.userId,
                  userName: rec.userName,
                  likeCount: rec.likeCount,
                } as TwitterRecord);
              }
            });
          });

          const c: ConditionState = JSON.parse(JSON.stringify(condition.value));
          fetchedCondition.value = {
            hashtag: c.hashtag,
            startDate: c.startDate,
            endDate: c.endDate,
            userName: c.userName,
            mode: c.mode,
            minLike: c.minLike,
            maxLike: c.maxLike,
            pageNo: c.pageNo,
            pageSize: c.pageSize,
          };
          searchOptionShow.value = false;
        } else {
          dataState.value.totalPages = 1;
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

  const imageLinkOpen = function (url: string) {
    window.open(url);
  };

  //nitterの画像URLをtwitterのやつに変換する
  const convertImageLink = function (nitterUrl: string) {
    if (nitterUrl.includes('nitter')) {
      const fileNameExt = nitterUrl.split('%2F');
      const fileName = fileNameExt[fileNameExt.length - 1]
        .replace('.jpg', '')
        .replace('.png', '');
      if (fileNameExt[fileNameExt.length - 1].includes('jpg')) {
        const twitterUrl = `https://pbs.twimg.com/media/${fileName}?format=jpg&name=orig`;
        return twitterUrl;
      } else if (fileNameExt[fileNameExt.length - 1].includes('png')) {
        const twitterUrl = `https://pbs.twimg.com/media/${fileName}?format=png&name=orig`;
        return twitterUrl;
      }
    } else {
      return nitterUrl;
    }
  };

  return {
    condition,
    dataState,
    search,
    isLoading,
    dateModalShow,
    selectItems,
    imageLinkOpen,
    searchOptionShow,
  };
}
interface ConditionState {
  pageNo: number;
  pageSize: number;
  hashtag: string;
  startDate: string;
  endDate: string;
  userName: string;
  mode: string;
  minLike: number | null;
  maxLike: number | null;
}
interface TwitterRecord {
  hashtag: string;
  mode: string;
  url: string;
  date: string;
  image: string;
  userId: string;
  userName: string;
  likeCount: number;
  displayMenu: boolean;
}
interface DataState {
  totalPages: number;
  records: Array<TwitterRecord>;
}
