import { useQuasar } from 'quasar';
import { MovieApi } from 'src/api/file/MovieApi';
import { computed, ref } from 'vue';
const STAFF_KEY = 'movie-default-staff-cd';
export function useMovieEditModel() {
  const quasar = useQuasar();
  const lockIcon = ref(false);
  const staffSelect = ref([
    {
      staffCd: 1,
      name: 'レゴマン',
    },
    {
      staffCd: 2,
      name: '王将マン',
    },
  ] as MovieStaff[]);
  const loadState = ref({
    fetch: false,
    update: false,
    delete: false,
  } as LoadState);
  const movieInfo = ref({
    id: 0,
    title: '',
    detail: '',
    fileName: '',
    thumbnailFlg: 1,
    staff: {
      staffCd: 1,
      name: 'レゴマン',
    },
    hashtags: [],
    newHashtags: [],
  } as MovieInfo);
  const pickedFile = ref(null as File | null);
  const thumbnailFile = ref(null as File | null);
  const api = new MovieApi();
  const thumbnailUrl = computed(() =>
    api.thumbnailLink(movieInfo.value.fileName)
  );
  const deleteMovie = async function () {
    if (lockIcon.value == false) {
      return false;
    }
    loadState.value.delete = true;
    return await api
      .deleteMovie(movieInfo.value.fileName)
      .then((response) => {
        if (response) {
          console.log('delete response', response);
          quasar.notify({
            color: 'primary',
            position: 'top',
            message: movieInfo.value.title + 'の動画は削除したで！',
          });
          return true;
        } else {
          return false;
        }
      })
      .catch((e) => {
        console.log(e);

        quasar.notify({
          color: 'red',
          position: 'top',
          message: '削除に失敗した...',
        });
        return false;
      });
  };
  const updateMovie = async function () {
    if (movieInfo.value.title == '' || movieInfo.value.fileName == '') {
      quasar.notify({
        color: 'red',
        position: 'top',
        message: 'タイトルとファイルは必須！',
      });
      return;
    }
    if (movieInfo.value.thumbnailFlg == 0 && thumbnailFile.value == null) {
      quasar.notify({
        color: 'red',
        position: 'top',
        message: 'サムネイルの画像選択してね！',
      });
      return;
    }
    const hashtags = [] as string[];
    movieInfo.value.newHashtags.forEach((it) => hashtags.push(it.name));
    movieInfo.value.hashtags
      .filter((it) => it.check)
      .forEach((it) => hashtags.push(it.name));
    await api
      .updateMovie({
        id: movieInfo.value.id,
        title: movieInfo.value.title,
        detail: movieInfo.value.detail,
        thumbnailFlg: movieInfo.value.thumbnailFlg,
        fileName: movieInfo.value.fileName,
        staffCd: movieInfo.value.staff.staffCd,
        hashtags: hashtags,
      })
      .then((response) => {
        if (response) {
          console.log('movie update response', response);
          quasar.notify({
            color: 'primary',
            position: 'top',
            message: '保存したで！',
          });
        }
      });
  };
  const uploadFile = async function () {
    if (pickedFile.value == null) {
      return;
    }
    await api
      .upload(pickedFile.value)
      .then((response) => {
        if (response) {
          console.log('upload response', response);
          movieInfo.value.fileName = response.fileName;
        }
      })
      .catch((err) => {
        console.log('upload err', err);
      });
  };
  const getHashtagList = async function () {
    await api
      .hashtagList()
      .then((response) => {
        if (response) {
          console.log('hashtag list', response);
          movieInfo.value.hashtags.splice(0);
          response.forEach((it) =>
            movieInfo.value.hashtags.push({
              name: it.name,
              isGroup: it.isGroup == 1,
              check: false,
            })
          );
        }
      })
      .catch((err) => {
        console.log('hashtag list err', err);
      });
  };
  const getMoieInfo = async function (id: number) {
    loadState.value.fetch = true;
    await getHashtagList();
    await api
      .getMovieInfo(id)
      .then((response) => {
        if (response) {
          console.log('movie info response', response);
          movieInfo.value.id = response.movie.id;
          movieInfo.value.title = response.movie.title;
          movieInfo.value.detail = response.movie.detail;
          movieInfo.value.fileName = response.movie.fileName;
          movieInfo.value.thumbnailFlg = response.movie.thumbnailFlg;
          movieInfo.value.staff.staffCd = response.movie.staffCd;
          movieInfo.value.staff.name = response.movie.staffName;
          response.hashtags.forEach((h) => {
            const hs = movieInfo.value.hashtags.find((it) => it.name == h.name);
            if (hs) {
              hs.check = true;
            }
          });
          console.log('movie info result', movieInfo.value);
        }
      })
      .catch((err) => {
        console.log('upload err', err);
      });
    loadState.value.fetch = false;
  };

  const getDefaultStaff = function () {
    const code = localStorage.getItem(STAFF_KEY);
    if (code == null) {
      return;
    }

    const staff = staffSelect.value.find((it) => it.staffCd == Number(code));
    if (staff) {
      movieInfo.value.staff.staffCd = staff.staffCd;
    }
  };
  const setDefaultStaffCd = function (staffCd: number) {
    localStorage.setItem(STAFF_KEY, staffCd.toString());
  };

  const uploadThumbnail = async function () {
    // 動画のアップロードの後に実行すること
    if (thumbnailFile.value == null || movieInfo.value.thumbnailFlg == 1) {
      return;
    }
    await api
      .uploadThumbnail(thumbnailFile.value, movieInfo.value.fileName)
      .then((response) => {
        if (response) {
          console.log('upload thumbnail response', response);
        }
      })
      .catch((err) => {
        console.log('upload thumbnail err', err);
      });
  };

  return {
    staffSelect,
    loadState,
    movieInfo,
    pickedFile,
    thumbnailFile,
    lockIcon,
    thumbnailUrl,
    getMoieInfo,
    getDefaultStaff,
    setDefaultStaffCd,
    uploadFile,
    updateMovie,
    deleteMovie,
    uploadThumbnail,
  };
}
interface MovieInfo {
  id: number;
  title: string;
  detail: string;
  fileName: string;
  thumbnailFlg: number;
  staff: MovieStaff;
  hashtags: Hashtag[];
  newHashtags: Hashtag[];
}
interface Hashtag {
  name: string;
  isGroup: boolean;
  check: boolean;
}

interface LoadState {
  fetch: boolean;
  update: boolean;
  delete: boolean;
}
interface MovieStaff {
  staffCd: number;
  name: string;
}
