<template>
  <!--サイドメニュー-->
  <q-drawer v-model="leftDrawerOpen" class="q-pa-md bg-grey-4" bordered>
    <q-list>
      <!--Main-->
      <q-item-section>
        <div class="text-h6 text-grey-7">おばあちゃんち</div>
        <div v-for="state in mainPages" :key="state.url">
          <q-item clickable v-ripple @click="router.replace(state.url)">
            <q-item-section class="light-drawer-text">
              {{ state.title }}
            </q-item-section>
          </q-item>
        </div>
      </q-item-section>
      <q-separator />

      <!--File-->
      <q-item-section>
        <div class="text-h6 text-grey-7">お土産</div>
        <div v-for="state in filePages" :key="state.url">
          <q-item clickable v-ripple @click="router.replace(state.url)">
            <q-item-section class="light-drawer-text">
              {{ state.title }}
            </q-item-section>
          </q-item>
        </div>
      </q-item-section>
      <q-separator />

      <!--Scraper-->
      <q-item-section>
        <div class="text-h6 text-grey-7">おまけ</div>
        <div v-for="state in scraperPages" :key="state.url">
          <q-item clickable v-ripple @click="router.replace(state.url)">
            <q-item-section class="light-drawer-text">
              {{ state.title }}
            </q-item-section>
          </q-item>
        </div>
      </q-item-section>
      <q-separator />

      <q-item-section>
        <div class="text-h6 text-grey-7">その他</div>
        <!--ホーム-->
        <q-item clickable v-ripple @click="router.replace('/')">
          <q-item-section class="light-drawer-text">
            リビングに戻る
          </q-item-section>
        </q-item>
      </q-item-section>
    </q-list>
  </q-drawer>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'layout-drawer',
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
  },
  setup(props) {
    const leftDrawerOpen = computed(() => props.modelValue);
    const router = useRouter();

    const mainPages = ref([
      {
        title: '名言集',
        url: '/wordlist',
      },
      {
        title: 'あだ名一覧',
        url: '/namelist',
      },
      {
        title: '焼き直し条約',
        url: '/yaki',
      },
      {
        title: '俳句王',
        url: '/haiku',
      },
      {
        title: '学校',
        url: '/school',
      },
      {
        title: 'お茶の間',
        url: '/info',
      },
    ] as PageState[]);

    const filePages = ref([
      {
        title: 'カラオケ',
        url: '/karaoke',
      },
      {
        title: 'ボイス',
        url: '/voice',
      },
      {
        title: 'スマブラ',
        url: '/ssbu',
      },
      {
        title: 'オム子レイディオ',
        url: '/radio',
      },
      {
        title: '画像',
        url: '/img',
      },
      {
        title: '動画',
        url: '/movie',
      },
    ] as PageState[]);

    const scraperPages = ref([
      {
        title: 'twitter',
        url: '/twitter',
      },
      {
        title: '歌みた',
        url: '/holosong',
      },
      {
        title: 'オリ曲',
        url: '/holoalbum',
      },
      {
        title: '記念配信',
        url: '/holomemory',
      },
      {
        title: 'アーカイブ',
        url: '/holoarchive',
      },
    ] as PageState[]);

    return {
      leftDrawerOpen,
      router,
      mainPages,
      filePages,
      scraperPages,
    };
  },
});
interface PageState {
  title: string;
  url: string;
}
</script>
<style>
.menu-icon-image {
  width: 52px;
}
.light-drawer-text {
  font-size: 1.2rem;
  line-height: 2rem;
  font-weight: 500;
}
</style>
