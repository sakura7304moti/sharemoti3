<template>
  <q-page class="">
    <div class="holo-page-title q-pb-md">pixiv illust</div>

    <!--イラスト-->
    <div class="q-ma-md">
      <div v-for="il in mainIllust.images" :key="il.id">
        <div class="pixiv-illust-img img-wrap" v-if="il.line == 0 || allView" >
          <img :src="getImageUrl(il)" :style="{'aspect-ratio':mainIllust.width / mainIllust.height}" style="object-fit: contain;max-width:100vw;width:100%;max-height:70vh;height:100%"
          />
          <br />
          <div class="q-pl-md">
            <q-btn
            :label="`全て見る : ${mainIllust.images.length}枚`"
            color="primary"
            @click="onDisplayClick()"
            size="md"
            class="text-bold q-py-xs q-px-md"
            outline
            icon="panorama"
            v-if="il.line == 0 && !allView && mainIllust.images.length > 1 && !isLoading"
          />
          </div>

        </div>
      </div>
      <!--イラスト説明-->
      <div class="q-pa-md">
        <div class="text-h6 text-bold">
          {{ mainIllust.title }}
        </div>
        <div class="full-width row wrap">
          <div v-for="tag in hashtags" :key="tag.name" class="text-primary text-bold q-pr-md cursor-pointer pixiv-tags" @click="onHashtagClick(tag.name)">
            {{ tag.name }}
          </div>
        </div>
        <div class="row full-width cursor-pointer pixiv-user-icon" @click="onUserClick(findUser?.id ?? -1)">
          <div>
            <q-avatar size="md" v-if="userProfileUrl">
              <img :src="userProfileUrl" />
            </q-avatar>
          </div>
          <div class="q-pl-sm q-pt-xs text-grey text-caption" v-if="findUser">
            {{ findUser.name.substring(0, 8) }}
            <span v-if="findUser.name.length > 8">...</span>
          </div>
        </div>
      </div>

    </div>

    <!--検索エリア-->
    <div class="text-h5 text-primary q-pt-md">
      検索<q-icon name="search" color="primary"></q-icon>
    </div>
    <div class="q-ma-md">
      <search-area
        :hashtags="condition.hashtags"
        :user-ids="condition.userIds"
        :min-total-bookmarks="condition.minTotalBookmarks"
        :min-total-view="condition.minTotalView"
      />

      <div class="row wrap" style="max-width: 1200px">
        <div v-for="illust in illusts" :key="illust.id">
          <image-card :illust-id="illust.id" />
        </div>
      </div>
    </div>
  </q-page>
</template>
<script lang="ts">
import { PixivSearchStore } from 'src/stores/pixiv/PixivSearchStore';
import api from 'src/api/scraper/PixivApi';
import PixivSearchArea from 'src/components/pixiv/PixivSearchArea.vue';
import PixivImageCard from 'src/components/pixiv/PixivImageCard.vue';
import { computed, defineComponent, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
export default defineComponent({
  name: 'pixiv-illust',
  props: {
    illustId: {
      type: Number,
      required: true,
    },
  },
  components: {
    'search-area': PixivSearchArea,
    'image-card': PixivImageCard,
  },
  setup(props) {
    const router = useRouter();
    const route = useRoute();
    const quasar = useQuasar();
    const allView = ref(false);
    const userProfileUrl = ref('');
    const findUser = ref(null as null | User) ;
    const hashtags = ref([] as Hashtag[]);
    const store = PixivSearchStore();

    const onSearchClick = function () {
      store.searchIllust();
    };


    const isLoading = ref(store.isLoading.illust);
    const illusts = computed(() => store.pageState.records);

    const mainIllust = ref({
      id: -1,
      title: '',
      type: '',
      userId: -1,
      createDate: '',
      pageCount: -1,
      width: -1,
      height: -1,
      sanityLevel: -1,
      totalView: -1,
      totalBookmarks: -1,
      illustAiType: -1,
      images: [],
    } as IllustImage);

    const getIllust = async function (id: number) {
      await api
        .get_illust(id)
        .then((response) => {
          if (response) {
            console.log('illust', response);
            mainIllust.value = response;

            // 画像の非表示
            onDisplayCloseClick();


            // ユーザー情報の取得
            const userUrl = getUserUrl();
            if(userUrl){
              userProfileUrl.value = store.getImageUrl(userUrl);
              console.log('profile user',userProfileUrl.value);
            }
          }
        })
        .catch((err) => {
          console.log('get_illust err', err);
        });
    };
    const getHashtags = async function (id: number) {
      await store
        .getHashtags(id)
        .then((response) => {
          if (response) {
            hashtags.value.splice(0);
            response.forEach((it) => hashtags.value.push(it));
          }
        })
        .catch((err) => {
          console.log('get_hashtags err', err);
        });
    };


    const getImageUrl = function (image: Image) {
      if (image.originalImageUrl) {
        return store.getImageUrl(image.originalImageUrl ?? '');
      } else {
        return store.getImageUrl(image.imageUrlLarge ?? '');
      }
    };

    const getUserUrl = function(){
      const user = store.getUserbyId(mainIllust.value.userId);
      if(user){
        findUser.value = user;
        return store.findUserImageUrl(user);
      }
    }

    const onHashtagClick = function(hashtag:string){
      store.resetCondition();
      router.push({
        path: '/pixiv',
        query: {
          hashtag:hashtag,
          minview:1000,
          fetch:'true'
        },
      });
      quasar.notify({
          color: 'secondary',
          position: 'top',
          message: '検索ハッシュタグ : ' + hashtag,
        });
    }

    const onUserClick = function(userId:number){
      if(userId == -1){
        return;
      }
      store.resetCondition();
      router.push({
        path: '/pixiv',
        query: {
          user:userId,
          minview:1000,
          fetch:'true'
        },
      });
      quasar.notify({
          color: 'secondary',
          position: 'top',
          message: 'ユーザー名で検索',
        });
    }

    const onDisplayClick = function () {
      allView.value = true;
    };

    const onDisplayCloseClick = function(){
      allView.value = false;
    }

    const onReplaceCondition = function(first:boolean){
      if(first){
        store.searchHashtags();
        store.searchUsers();
      }
      getIllust(props.illustId);
      getHashtags(props.illustId);
    }
    onReplaceCondition(true);// ページの初期化


    watch(props, () => {
      onReplaceCondition(false);
    });

    return {
      // state
      isLoading,
      allView,
      condition: store.condition,
      hashtags,
      pageState: store.pageState,
      illusts,
      mainIllust,
      userProfileUrl,
      findUser,

      // actions
      onSearchClick,
      onDisplayClick,
      onHashtagClick,
      getImageUrl,
      onUserClick
    };
  },
});
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

interface User {
  id: number;
  name: string;
  account: string;
  profileImageUrlSquareMedium: string;
  profileImageUrlMedium: string;
  profileImageUrlLarge: string;
}

interface Hashtag {
  name: string;
  translatedName: string;
}
</script>
<style>

/*
メインのイラスト
*/
.pixiv-illust-img {
  max-width:100vw;
  width:100%;
  height:auto;
}

/*
ハッシュタグ
*/
.pixiv-tags:hover{
  opacity: 0.7;
}
/*
ユーザーアイコン
*/
.pixiv-user-icon:hover{
  opacity: 0.7;
}
</style>
