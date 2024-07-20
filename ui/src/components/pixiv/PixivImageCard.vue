<template>
  <q-card
    style="width: 184px; height: 184px; overflow: hidden; position: relative"
    class="q-mt-md q-mr-md q-ml-md q-mb-xs pixiv-img-card"
    v-if="illustUrl.length > 0"
    @click.prevent.stop="onClickIllust(illustId)"
  >
    <q-card-section class="q-pa-none img-wrap" v-if="illustUrl.length > 0">
      <img :src="illustUrl" class="pixiv-card-img" @error="illustUrl = ''" />
      <q-btn
        v-if="hover"
        icon="zoom_in"
        class="zoom-button"
        @click="showDialog = true"
      />
    </q-card-section>
  </q-card>
  <div
    class="text-subtitle2 text-bold q-mx-md q-pl-sm"
    style="height: 100px"
    v-if="illustUrl.length > 0"
  >
    {{ cardstate.title.substring(0, 10) }}
    <span v-if="cardstate.title.length > 10">...</span>

    <!--ユーザーアイコンや名前-->
    <user-area :user-id="cardstate.userId" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue';
import api from 'src/api/scraper/PixivApi';
import { PixivSearchStore } from 'src/stores/pixiv/PixivSearchStore';
import { useRoute, useRouter } from 'vue-router';
import PixivUserArea from './PixivUserArea.vue';

export default defineComponent({
  name: 'pixiv-image-card',
  components:{
    'user-area':PixivUserArea
  },
  props: {
    illustId: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const store = PixivSearchStore();

    const route = useRoute();
    const router = useRouter();

    const showDialog = ref(false);
    const hover = ref(false);
    const illustUrl = ref('');
    const userUrl = ref('');
    const userName = ref('');

    const cardstate = ref({
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

    const getImageUrl = function (image: Image) {
      return store.findImageUrl(image);
    };

    const getUserUrl = function (user: User) {
      return store.findUserImageUrl(user);
    };

    const getImageCard = async function (id: number) {
      illustUrl.value = '';
      try {
        const response = await api.get_illust(id);
        if (response) {
          cardstate.value = response;

          const user = store.getUserbyId(response.userId);
          if (user) {
            userUrl.value = store.getImageUrl(getUserUrl(user));
            userName.value = user.name;
          }

          const imageUrl = getImageUrl(response.images[0]);
          if ((imageUrl ?? '').length > 0 && imageUrl) {
            illustUrl.value = store.getImageUrl(imageUrl);
          }
        }
      } catch (err) {
        console.error('illust data error', err);
      }
    };

    const onClickIllust = function (id: number) {
      console.log('query',route.query)
      router.push({
        path: `/pixiv/illust/${id}`,
        query: {
          ...route.query,
        },
      });
    };

    // 初回読み込み
    onMounted(() => {
      getImageCard(props.illustId);
    });

    // propsの変更を監視
    watch(
      () => props.illustId,
      (newId) => {
        getImageCard(newId);
      }
    );

    return {
      showDialog,
      hover,
      cardstate,
      illustUrl,
      userUrl,
      userName,
      onClickIllust,
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
</script>

<style>
.pixiv-card-img {
  width: 184px;
  height: 184px;
  object-fit: cover;
}
/*画像の表示をなめらかにする */
.img-wrap {
  overflow: hidden;
  position: relative;
  width: 184px;
  height: 184px;
}

.img-wrap::before {
  animation: img-wrap 2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
  background: #fff;
  content: '';
  inset: 0;
  pointer-events: none;
  position: absolute;
  z-index: 1;
}

@keyframes img-wrap {
  100% {
    transform: translateX(100%);
  }
}

/*画像のカード */
.pixiv-img-card:hover {
  cursor: pointer;
  opacity: 0.7;
  transition: 0.3s;
}
</style>
