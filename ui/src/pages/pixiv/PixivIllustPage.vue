<template>
  <q-page class="">
    <div class="holo-page-title q-pb-md">pixiv illust</div>
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
  </q-page>
</template>
<script lang="ts">
import { PixivSearchStore } from 'src/stores/pixiv/PixivSearchStore';
import api from 'src/api/scraper/PixivApi';
import PixivSearchArea from 'src/components/pixiv/PixivSearchArea.vue';
import PixivImageCard from 'src/components/pixiv/PixivImageCard.vue';
import { computed, defineComponent, ref } from 'vue';
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
    const hashtags = ref([] as Hashtag[]);
    const store = PixivSearchStore();

    const onSearchClick = function () {
      store.searchIllust();
    };

    store.searchHashtags();
    store.searchUsers();
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
    getIllust(props.illustId);
    getHashtags(props.illustId);

    return {
      condition: store.condition,
      hashtags,
      pageState: store.pageState,
      illusts,
      onSearchClick,
      mainIllust,
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
