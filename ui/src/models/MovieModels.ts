import { ref } from 'vue';
import api from 'src/api/file/MovieApi';

export function useMovieModel() {
  const isLoading = ref(false);
  const page = ref(1);
  const playId = ref(null as number | null);
  const searchCondition = ref({
    keyword: '',
    hashtag: '',
    mode: 1,
  } as SearchCondition);
  const hashtags = ref([] as string[]);

  const pageState = ref({
    records: [],
    totalCount: 0,
  } as PageState);

  const searchMovie = async function () {
    isLoading.value = true;
    await api
      .searchMovie(
        searchCondition.value.keyword,
        searchCondition.value.hashtag,
        searchCondition.value.mode,
        page.value
      )
      .then((response) => {
        if (response) {
          console.log('search response', response);
          playId.value = null;
          pageState.value.records.splice(0);
          pageState.value.records = response.records;
          pageState.value.totalCount = response.totalCount;
        }
      })
      .catch((err) => {
        console.log('search err', err);
      });
    isLoading.value = false;
  };

  const getHashtags = async function () {
    await api.hashtagList().then((response) => {
      if (response) {
        hashtags.value = response.map((it) => it.name);
      }
    });
  };

  const getDownloadLink = function (fileName: string) {
    return api.downloadLink(fileName);
  };

  const getThumbnailLink = function (fileName: string) {
    return api.thumbnailLink(fileName);
  };

  return {
    playId,
    isLoading,
    page,
    searchCondition,
    pageState,
    hashtags,
    searchMovie,
    getDownloadLink,
    getThumbnailLink,
    getHashtags,
  };
}
interface SearchCondition {
  keyword: string | null;
  hashtag: string | null;
  mode: number;
}
interface DataState {
  id: number;
  title: string;
  detail: string;
  fileName: string;
  thumbnailFlg: number;
  staffCd: string;
  hashtags: string[];
}

interface PageState {
  records: DataState[];
  totalCount: number;
}
