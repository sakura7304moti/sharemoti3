<template>
  <!--ページリンク一覧-->
  <div class="q-pt-md row q-gutter-md">
    <!--main-->
    <q-card style="width: 400px">
      <q-card-section>
        <div class="text-h6 text-grey">
          おばあちゃんち<q-icon
            name="description"
            class="q-pl-sm text-primary"
          />
        </div>
        <div class="q-pa-md">
          <div
            v-for="state in mainPages"
            :key="state.url"
            class="q-pb-sm light-index-div"
            @click.prevent="router.replace(state.url)"
          >
            <q-btn
              :label="state.title"
              align="left"
              class="light-index-item"
              flat
            >
            </q-btn>
            <q-separator />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!--file-->
    <q-card style="width: 400px">
      <q-card-section>
        <div class="text-h6 text-grey">
          お土産<q-icon name="task" class="q-pl-sm text-secondary" />
        </div>
        <div class="q-pa-md">
          <div
            v-for="state in filePages"
            :key="state.url"
            class="q-pb-sm light-index-div"
            @click.prevent="router.replace(state.url)"
          >
            <q-btn
              :label="state.title"
              align="left"
              class="light-index-item"
              flat
            >
            </q-btn>
            <q-separator />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!--file-->
    <q-card style="width: 400px">
      <q-card-section>
        <div class="text-h6 text-grey">
          おまけ<q-icon name="audio_file" class="q-pl-sm text-warning" />
        </div>
        <div class="q-pa-md">
          <div
            v-for="state in scraperPages"
            :key="state.url"
            class="q-pb-sm light-index-div"
            @click="router.replace(state.url)"
          >
            <q-btn
              :label="state.title"
              align="left"
              class="light-index-item"
              flat
            >
            </q-btn>
            <q-separator />
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
export default defineComponent({
  name: 'light-index',
  setup() {
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
/*テキスト */
.light-index-item {
  width: 100%;
  font-size: 16px;
  line-height: 3em;
  text-decoration: none;
  font-weight: 600;
  padding: 0 14px;
  color: #333;
}
</style>
