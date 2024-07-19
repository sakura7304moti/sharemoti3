import { defineStore } from 'pinia';
import { useQuasar } from 'quasar';
import api from 'src/api/scraper/PixivApi';
import { ref } from 'vue';
/*
 * イラストの検索
 * 検索用オプション
 */

export const PixivSearchStore = defineStore('pixiv-search', {
  state: () => {
    const quasar = useQuasar();
    const isLoading = ref({
      illust: false,
      holoname: false,
      hashtag: false,
      user: false,
    } as Loading);
    const holonames = ref([] as HoloName[]);

    const hashtagCondition = ref('');
    const findHashtags = ref([] as Hashtag[]);

    const userCondition = ref('');
    const selectedUsers = ref([] as User[]);
    const findUsers = ref([] as User[]);
    const userProfileUrl = ref('');

    const selectedHoloName = ref('');
    const condition = ref({
      text: '',
      hashtags: [],
      userIds: [],
      minTotalBookmarks: 0,
      minTotalView: 10000,
      pageNo: 1,
      pageSize: 20,
    } as Condition);
    const isR18 = ref(false);

    const isExistsHashtag = function (hashtag: string) {
      return condition.value.hashtags.includes(hashtag);
    };

    const isExistsUser = function (userId: number) {
      return condition.value.userIds.includes(userId);
    };

    const updateUserProfileImage = function () {
      userProfileUrl.value = '';
      if (selectedUsers.value.length > 0) {
        const user = selectedUsers.value[0];
        let imageUrl = '';
        if (user.profileImageUrlSquareMedium) {
          imageUrl = user.profileImageUrlSquareMedium;
        } else if (user.profileImageUrlMedium) {
          imageUrl = user.profileImageUrlMedium;
        } else if (user.profileImageUrlLarge) {
          imageUrl = user.profileImageUrlLarge;
        }
        userProfileUrl.value =
          api.apiEndpoint() + '/pixiv/image/download?url=' + imageUrl;
      }
    };

    const isConditionDefault = function () {
      if (condition.value.text.length > 0) {
        return false;
      } else if (condition.value.hashtags.length > 0) {
        return false;
      } else if (condition.value.userIds.length > 0) {
        return false;
      } else if (condition.value.minTotalBookmarks > 0) {
        return false;
      } else if (condition.value.minTotalView > 20000) {
        return false;
      } else if (isR18.value) {
        return false;
      } else {
        return true;
      }
    };

    const pageState = ref({
      records: [],
      totalCount: 0,
      pageCount: 0,
    } as PageState);

    return {
      quasar,
      isLoading,
      holonames,
      selectedHoloName,
      selectedUsers,
      userProfileUrl,
      updateUserProfileImage,
      hashtagCondition,
      findHashtags,
      userCondition,
      findUsers,
      condition,
      isR18,
      isExistsHashtag,
      isExistsUser,
      isConditionDefault,
      pageState,
    };
  },
  actions: {
    // ------------------------------
    // クリック等のアクション
    // ------------------------------
    resetCondition: function () {
      this.condition = {
        text: '',
        hashtags: [],
        userIds: [],
        minTotalBookmarks: 0,
        minTotalView: 10000,
        pageNo: 1,
        pageSize: 20,
      };
    },
    addHashtag: function (hashtag: string) {
      if (!this.isExistsHashtag(hashtag)) {
        this.condition.hashtags.push(hashtag);
        this.condition.hashtags.sort();
      }
    },
    removeHashtag: function (hashtag: string) {
      if (this.isExistsHashtag(hashtag)) {
        const index = this.condition.hashtags.findIndex((it) => it == hashtag);
        if (index != -1) {
          this.condition.hashtags.splice(index, 1);
        }
      }

      const emptyIndex = this.condition.hashtags.findIndex((it) => it == '');
      if (emptyIndex != -1) {
        this.condition.hashtags.splice(emptyIndex, 1);
      }
    },
    addUser: function (userId: number) {
      if (!this.isExistsUser(userId)) {
        this.condition.userIds.push(userId);
        const user = this.findUsers.find((it) => it.id == userId);
        if (user) {
          this.selectedUsers.push(user);
          this.updateUserProfileImage();
        }
      }
    },
    removeUser: function (userId: number) {
      if (!this.isExistsUser(userId)) {
        const index = this.condition.userIds.findIndex((it) => it == userId);
        if (index != -1) {
          this.condition.userIds.splice(index, 1);
          this.selectedUsers = this.selectedUsers.filter(
            (it) => it.id != userId
          );
          this.updateUserProfileImage();
        }
      }
    },
    clearUser: function () {
      this.condition.userIds.splice(0);
      this.selectedUsers.splice(0);
      this.updateUserProfileImage();
    },

    // ------------------------------
    // API呼び出し
    // ------------------------------
    searchIllust: async function () {
      this.isLoading.illust = true;
      const request = {
        text: this.condition.text,
        hashtags: this.condition.hashtags,
        userIds: this.condition.userIds,
        minTotalBookmarks: this.condition.minTotalBookmarks,
        minTotalView: this.condition.minTotalView,
        pageNo: this.condition.pageNo,
        pageSize: this.condition.pageSize,
      } as Condition;
      console.log('isR18', this.isR18);
      if (!request.hashtags.includes('R-18') && this.isR18) {
        request.hashtags.push('R-18');
      }
      await api
        .search_illust(request)
        .then(async (response) => {
          if (response) {
            console.log('search illust condition', this.condition);
            console.log('search illust', response);
            this.pageState.records.splice(0);
            response.forEach((it) => this.pageState.records.push(it));
            await api.search_illust_count(this.condition).then((response) => {
              if (response) {
                console.log('totalCount', response);
                this.pageState.totalCount = response;
                this.pageState.pageCount = Math.ceil(
                  response / this.condition.pageSize
                );
              }
            });
          }
        })
        .catch((err) => {
          console.log('search illust err', err);
          this.quasar.notify({
            color: 'red',
            position: 'top',
            message: 'イラストの検索に失敗...',
          });
        });
      this.isLoading.illust = false;
    },

    getHolonames: async function () {
      this.isLoading.holoname = true;
      await api
        .holoname()
        .then((response) => {
          if (response) {
            console.log('holo name', response);
            this.holonames.splice(0);
            response.forEach((it) => this.holonames.push(it));
          }
        })
        .catch((err) => {
          console.log('holo name err', err);
          this.quasar.notify({
            color: 'red',
            position: 'top',
            message: 'ホロメンの選択データの取得失敗...',
          });
        });
      this.isLoading.holoname = false;
    },

    searchHashtags: async function () {
      this.isLoading.hashtag = true;
      await api
        .search_hashtags(this.hashtagCondition)
        .then((response) => {
          if (response) {
            console.log('search hashtags', response);
            this.findHashtags.splice(0);
            response.forEach((it) => this.findHashtags.push(it));
          }
        })
        .catch((err) => {
          console.log('search hashtags err', err);
          this.quasar.notify({
            color: 'red',
            position: 'top',
            message: 'ハッシュタグの検索失敗...',
          });
        });
    },

    getHashtags: async function (id: number) {
      const hashtags = [] as Hashtag[];
      this.isLoading.hashtag = true;
      await api
        .search_hashtags('', id)
        .then((response) => {
          if (response) {
            console.log('select hashtags by id = ' + id, response);
            response.forEach((it) => hashtags.push(it));
          }
        })
        .catch((err) => {
          console.log('search hashtags err', err);
          this.quasar.notify({
            color: 'red',
            position: 'top',
            message: 'ハッシュタグの検索失敗...',
          });
        });
      return hashtags;
    },

    searchUsers: async function () {
      this.isLoading.user = true;
      await api
        .search_users(this.userCondition)
        .then((response) => {
          if (response) {
            console.log('serach user', response);
            this.findUsers.splice(0);
            response.forEach((it) => this.findUsers.push(it));
          }
        })
        .catch((err) => {
          console.log('search user err', err);
          this.quasar.notify({
            color: 'red',
            position: 'top',
            message: 'ユーザーの検索失敗...',
          });
        });
    },
    // ------------------------------
    // その他
    // ------------------------------
    getImageUrl: function (url: string) {
      return api.apiEndpoint() + '/pixiv/image/download?url=' + url;
    },

    getUserbyId: function (id: number) {
      return this.findUsers.find((it) => it.id == id);
    },

    findImageUrl: function (image: Image) {
      if ((image.imageUrlMedium ?? '') != '') {
        return image.imageUrlMedium;
      } else if ((image.imageUrlLarge ?? '') != '') {
        return image.imageUrlLarge;
      } else if ((image.originalImageUrl ?? '') != '') {
        return image.originalImageUrl;
      } else {
        return image.imageUrlSquareMedium;
      }
    },

    findUserImageUrl: function (user: User) {
      if ((user.profileImageUrlSquareMedium ?? '') != '') {
        return user.profileImageUrlSquareMedium;
      }
      if ((user.profileImageUrlMedium ?? '') != '') {
        return user.profileImageUrlMedium;
      } else {
        return user.profileImageUrlLarge;
      }
    },
  },
});
interface Loading {
  illust: boolean;
  holoname: boolean;
  hashtag: boolean;
  user: boolean;
}
interface Condition {
  text: string;
  hashtags: string[];
  userIds: number[];
  minTotalBookmarks: number;
  minTotalView: number;
  pageNo: number;
  pageSize: number;
}
interface HoloName {
  name: string;
  hashtag: string;
  url: string;
}
interface Hashtag {
  name: string;
  translatedName: string;
}
interface User {
  id: number;
  name: string;
  account: string;
  profileImageUrlSquareMedium: string;
  profileImageUrlMedium: string;
  profileImageUrlLarge: string;
}

interface PageState {
  records: Illust[];
  totalCount: number;
  pageCount: number;
}
interface Illust {
  id: number;
  title: string;
  type: string;
  userId: number;
  createDate: string;
  pageCount: number;
  width: number;
  height: number;
  sanityLevel: number;
  totalView: number;
  totalBookmarks: number;
  illustAiType: number;
}
interface IllustImage extends Illust {
  images: Image[];
}

interface Image {
  id: number;
  line: number;
  imageUrlSquareMedium: string | null;
  imageUrlMedium: string | null;
  imageUrlLarge: string | null;
  originalImageUrl: string | null;
}
