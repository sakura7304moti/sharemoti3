import { MovieApi } from 'src/api/file/MovieApi';
import { computed, ref } from 'vue';
const STAFF_KEY = 'movie-default-staff-cd';
export function useMovieUploadModels() {
  const api = new MovieApi();
  /**
   * 必要変数・処理
   * ・入力内容
   * ・表示ステップ
   * ・単品のサムネイル作成処理(APIも)
   * ・入力値のチェック
   * ・アップロードしてファイル名取得処理
   * ・データの追加処理
   * ・データ追加後にサムネイル画像をつけて完了したよ！画面出したい
   */
  const getDefaultStaff = function () {
    const code = localStorage.getItem(STAFF_KEY);
    if (code == null) {
      return;
    }

    const staff = staffSelect.value.find((it) => it.staffCd == Number(code));
    if (staff) {
      createForm.value.staff = staff;
    }
  };
  const setDefaultStaffCd = function (staffCd: number) {
    localStorage.setItem(STAFF_KEY, staffCd.toString());
  };
  const isUploading = ref(false);
  const isCreateLoading = ref(false);
  const isHashtagLoading = ref(false);
  const pickedFile = ref(null as File | null);
  const createForm = ref({
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
  } as CreateMovie);

  const formStep = ref(1 as 1 | 2 | 3);
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

  const getHashtagList = async function () {
    isHashtagLoading.value = true;
    await api
      .hashtagList()
      .then((response) => {
        if (response) {
          console.log('hashtag list', response);
          createForm.value.hashtags.splice(0);
          response.forEach((it) =>
            createForm.value.hashtags.push({
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
    isHashtagLoading.value = false;
  };

  const uploadFile = async function () {
    if (pickedFile.value == null) {
      return;
    }
    isUploading.value = true;
    await api
      .upload(pickedFile.value)
      .then((response) => {
        if (response) {
          console.log('upload response', response);
          createForm.value.fileName = response.fileName;
        }
      })
      .catch((err) => {
        console.log('upload err', err);
      });
    isUploading.value = false;
  };

  const createMovie = async function () {
    if (pickedFile.value == null) {
      return;
    }
    isCreateLoading.value = true;
    setDefaultStaffCd(createForm.value.staff.staffCd);
    const hashtags = [] as string[];
    createForm.value.newHashtags.forEach((it) => hashtags.push(it.name));
    createForm.value.hashtags
      .filter((it) => it.check)
      .forEach((it) => hashtags.push(it.name));
    await api
      .createMovie({
        title: createForm.value.title,
        detail: createForm.value.detail,
        fileName: createForm.value.fileName,
        thumbnailFlg: createForm.value.thumbnailFlg,
        staffCd: createForm.value.staff.staffCd,
        hashtags: hashtags,
      })
      .then(async (response) => {
        if (response) {
          console.log('create response', response);
          await updateGroupHashtag();
          formStep.value = 3;
        }
      });
  };

  const uploadUrl = computed(() => api.uploadUrl());
  const thumbnailUrl = computed(() =>
    api.thumbnailLink(createForm.value.fileName)
  );

  const updateGroupHashtag = async function () {
    const hashtags = createForm.value.newHashtags.filter((it) => it.isGroup);
    hashtags.forEach(async (tag) => {
      await api
        .createHashtag(createForm.value.fileName, tag.name, tag.isGroup)
        .then((response) => {
          if (response) {
            console.log(
              `update hashtag ${tag.name} is ${tag.isGroup}`,
              response
            );
          }
        })
        .catch((err) => {
          console.log(`update hashtag ${tag.name} is ${tag.isGroup}`, err);
        });
    });
  };

  return {
    uploadUrl,
    isUploading,
    isHashtagLoading,
    isCreateLoading,
    pickedFile,
    createForm,
    formStep,
    staffSelect,
    thumbnailUrl,
    uploadFile,
    createMovie,
    getHashtagList,
    getDefaultStaff,
  };
}

interface CreateMovie {
  title: string;
  detail: string;
  fileName: string;
  thumbnailFlg: number;
  staff: MovieStaff;
  hashtags: MovieHashtag[];
  newHashtags: MovieHashtag[];
}
interface MovieHashtag {
  name: string;
  isGroup: boolean;
  check: boolean;
}

interface MovieStaff {
  staffCd: number;
  name: string;
}
