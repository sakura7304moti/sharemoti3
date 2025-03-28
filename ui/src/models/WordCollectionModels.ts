import { WordList2Api } from 'src/api/main/WordList2Api';
import { WordCollectionApi } from 'src/api/main/WordCollectionApi';
import { ref } from 'vue';
import { useQuasar } from 'quasar';

export function useWordCollectionModel() {
  const quasar = useQuasar();
  const load = ref({
    save: false,
    search: false,
    delete: false,
  } as LoadState);

  const wordApi = new WordList2Api();
  const wordCollectionApi = new WordCollectionApi();

  /**
   * 検索機能
   */

  const searchCondition = ref({
    keyword: '',
    dateOrder: '',
    textOrder: '',
    kinen: null,
    year: null,
  } as ConditionState);

  const records = ref([] as DataState[]);
  const kinenList = ref([] as number[]);
  const yearList = ref([] as number[]);

  const searchWord = async function () {
    load.value.search = true;
    await wordCollectionApi
      .searchWord({
        keyword: searchCondition.value.keyword ?? '',
        dateOrder: searchCondition.value.dateOrder ?? '',
        textOrder: searchCondition.value.textOrder ?? '',
        kinen: searchCondition.value.kinen ?? 0,
        year: searchCondition.value.year ?? 0,
      })
      .then((response) => {
        if (response) {
          console.log('search response', response);
          records.value.splice(0);
          response.forEach((res) => records.value.push(res));
        }
      })
      .catch((err) => {
        console.log('search response', err);
        quasar.notify({
          position: 'top',
          color: 'negative',
          message: '検索したらエラーになった...',
        });
      });
    load.value.search = false;
  };

  const getKinenList = async function () {
    await wordCollectionApi.getKinens().then((response) => {
      if (response) {
        console.log('kinen response', response);
        kinenList.value = response;
      }
    });
  };

  const getYearList = async function () {
    await wordCollectionApi.getYears().then((response) => {
      if (response) {
        console.log('year response', response);
        yearList.value = response;
      }
    });
  };

  return {
    load,
    searchCondition,
    records,
    kinenList,
    yearList,
    searchWord,
    getKinenList,
    getYearList,
  };
}
interface LoadState {
  save: boolean;
  search: boolean;
  delete: boolean;
}
interface ConditionState {
  keyword: string | null;
  dateOrder: string | null;
  textOrder: string | null;
  kinen: number | null;
  year: number | null;
}
interface DataState {
  id: number;
  word: string;
  detail: string;
  wordRank: number;
  createAt: string;
  updateAt: string;
}
