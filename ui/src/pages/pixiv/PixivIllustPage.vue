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
        <user-area :user-id="mainIllust.userId" :short-view="false"/>
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
      <div class="q-pt-md">
      <q-pagination
        v-model="condition.pageNo"
        :max="pageState.pageCount"
        :max-pages="10"
        input
        v-if="pageState.records.length > 0"
      />
    </div>
    </div>
  </q-page>
</template>
<script lang="ts">
import { PixivSearchStore } from 'src/stores/pixiv/PixivSearchStore';
import api from 'src/api/scraper/PixivApi';
import PixivSearchArea from 'src/components/pixiv/PixivSearchArea.vue';
import PixivImageCard from 'src/components/pixiv/PixivImageCard.vue';
import PixivUserArea from 'src/components/pixiv/PixivUserArea.vue';
import { computed, defineComponent, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
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
    'user-area':PixivUserArea
  },
  setup(props) {
    const router = useRouter();
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

    const formatOriginalImageUrl = function(url:string){
      let imgUrl = 'https://i.pximg.net/img-master/img/'
      const ls = url.split('img/');
      if(ls.length > 1){
        imgUrl = imgUrl + ls[1];
        return imgUrl.replace('_square','')
      }
    }

    const getImageUrl = function (image: Image) {
      if (image.originalImageUrl) {
        return store.getImageUrl(image.originalImageUrl ?? '');
      } else if(image.imageUrlLarge) {
        return store.getImageUrl(formatOriginalImageUrl(image.imageUrlLarge) ?? image.imageUrlLarge)
      }else if(image.imageUrlMedium){
        return store.getImageUrl(formatOriginalImageUrl(image.imageUrlMedium) ?? image.imageUrlMedium)
      }
      else{
        return store.getImageUrl(formatOriginalImageUrl(image.imageUrlSquareMedium ?? '') ?? image.imageUrlSquareMedium ?? '')
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
          minview:10000,
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
