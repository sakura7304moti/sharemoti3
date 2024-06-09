import { useQuasar } from 'quasar';
import api from 'src/api/scraper/HololewdApi';
import { selectItem } from 'src/types/selectorType';
import { ref } from 'vue';

export function useHololewdModel() {
  //val
  const quasar = useQuasar();
  const condition = ref({
    pageNo: 1,
    pageSize: 20,
    flairText: '',
    minScore: 1000,
  } as ConditionState);

  const fetchedCondition = ref({
    pageNo: 1,
    pageSize: 20,
    flairText: '',
    minScore: 1000,
  } as ConditionState);

  const dataState = ref({
    totalPages: 0,
    records: [] as HololewdRecord[],
  } as DataState);

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
      label: '2000',
      value: 2000,
    },
    {
      label: '3000',
      value: 3000,
    },
    {
      label: '4000',
      value: 4000,
    },
    {
      label: '5000',
      value: 5000,
    },
  ] as Array<selectItem>;

  const holoList = ref([] as string[]);
  //function
  const getHoloList = async function () {
    holoList.value.splice(0);
    await api
      .holoList()
      .then((response) => {
        console.log('response', response);
        response?.forEach((res) => holoList.value.push(res));
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
  getHoloList();

  const isLoading = ref(false);
  //検索条件変わっていたらページを1にする
  const compareCondition = function () {
    if (condition.value.flairText != fetchedCondition.value.flairText) {
      condition.value.pageNo = 1;
    }
    if (condition.value.minScore != fetchedCondition.value.minScore) {
      condition.value.pageNo = 1;
    }
  };

  const search = async function () {
    isLoading.value = true;
    dataState.value.records.splice(0);
    compareCondition(); //検索条件変わったらページ数1にする
    await api
      .search({
        pageNo: condition.value.pageNo,
        pageSize: condition.value.pageSize,
        flairText: condition.value.flairText ?? '',
        minScore: condition.value.minScore,
      })
      .then((response) => {
        if (response) {
          console.log('response', response);

          dataState.value.totalPages = response.totalPages;

          response.records.forEach((rec) => {
            const addRec = {
              flairText: rec.flairText,
              images: [],
              date: rec.date,
              score: rec.score,
            } as HololewdRecord;
            rec.url.split(',').forEach((it) => addRec.images.push(it));
            dataState.value.records.push(addRec);
          });

          const c: ConditionState = JSON.parse(JSON.stringify(condition.value));
          fetchedCondition.value = {
            flairText: c.flairText,
            minScore: c.minScore,
            pageNo: c.pageNo,
            pageSize: c.pageSize,
          };
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

  return {
    condition,
    dataState,
    search,
    isLoading,
    holoList,
    getHoloList,
    selectItems,
    imageLinkOpen,
  };
}

interface ConditionState {
  pageNo: number;
  pageSize: number;
  flairText: string;
  minScore: number;
}

interface HololewdRecord {
  flairText: string;
  images: string[];
  date: string;
  score: number;
}
interface DataState {
  totalPages: number;
  records: Array<HololewdRecord>;
}
