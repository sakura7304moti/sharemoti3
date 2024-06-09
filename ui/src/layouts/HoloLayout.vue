<template>
  <q-layout
    style="
      background-image: url('https://hololive.hololivepro.com/wp-content/themes/hololive/images/fixed_bg.jpg');
    "
  >
    <q-header style="position: fixed">
      <div class="row">
        <div style="padding-right: 16px">
          <img
            src="https://hololive.hololivepro.com/wp-content/themes/hololive/images/head_l.png"
            class="holo-header-item"
          />
        </div>

        <!--各ページへのリンク(PC)-->
        <div
          v-for="item in pageList"
          :key="item.url"
          class="row q-gutter-md holo-header-item holo-links-pc"
          style="
            background: rgba(255, 255, 255, 0.5);
            border: solid 1px white; /*線*/
            border-radius: 10px; /*角の丸み*/
          "
        >
          <div>
            <a
              @click.prevent="router.replace(item.url)"
              href=""
              :class="{
                'holo-layout-text-selected': nowPathName == item.url,
                'holo-layout-text': nowPathName != item.url,
              }"
            >
              {{ item.title }}
            </a>
          </div>
        </div>

        <!--各ページへのリンクボタン(Android)-->
        <div
          class="row holo-links-android"
          style="width: calc(100% - 200px); padding-top: 8px"
        >
          <q-icon
            name="menu"
            id="holo-nav-button"
            size="md"
            @click="navDisplay = !navDisplay"
          />
        </div>
      </div>
    </q-header>

    <!--各ページのリンク一覧(Android)-->
    <nav id="holo-nav" :class="{ panelactive: navDisplay }">
      <div style="padding-top: 70px">
        <div
          v-for="item in pageList"
          :key="item.url"
          class="holo-header-item holo-nav-item text-center"
        >
          <div>
            <a
              @click.prevent="
                router.replace(item.url);
                navDisplay = false;
              "
              href=""
              :class="{
                'holo-layout-text-selected': nowPathName == item.url,
                'holo-layout-text': nowPathName != item.url,
              }"
            >
              {{ item.title }}
            </a>
          </div>
        </div>
      </div>
    </nav>

    <q-page-container>
      <router-view class="q-pa-md" />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { createPinia, setActivePinia } from 'pinia';
export default defineComponent({
  name: 'holo-layout',
  setup() {
    setActivePinia(createPinia());
    const route = useRoute();
    const router = useRouter();
    const nowPathName = computed(() => route.path);
    const pageList = [
      {
        url: '/twitter',
        title: 'twitter',
      },
      {
        url: '/hololewd',
        title: 'reddit',
      },
      {
        url: '/holosong',
        title: 'cover song',
      },
      {
        url: '/holoalbum',
        title: 'original song',
      },
      {
        url: '/holomemory',
        title: 'memory',
      },
      {
        url: '/holoarchive',
        title: 'archive',
      },
      {
        url: '/',
        title: 'my home',
      },
    ] as pageState[];
    return {
      navDisplay: ref(false),
      router,
      pageList,
      nowPathName,
    };
  },
});
interface pageState {
  url: string;
  title: string;
}
</script>
<style>
/*ヘッダーの文字列のスタイル */
.holo-layout-text {
  font-size: 16px;
  line-height: 3em;
  text-decoration: none;
  font-weight: 600;
  color: #116e9b;
  padding: 0 14px;
  transition: 0.2s;
}
.holo-layout-text:hover {
  font-size: 16px;
  line-height: 3em;
  text-decoration: none;
  font-weight: 600;
  color: #56c6fd;
  padding: 0 14px;
}
.holo-layout-text-selected {
  font-size: 16px;
  line-height: 3em;
  text-decoration: none;
  font-weight: 600;
  color: #56c6fd;
  padding: 0 14px;
}
.holo-page-title {
  font-family: brandon-grotesque, '游ゴシック Medium', 'Yu Gothic Medium',
    '游ゴシック体', YuGothic, sans-serif;
  font-weight: bold;
  font-size: 32px;
  line-height: 1.1em;
  color: #063f5c;
}
.q-layout__section--marginal {
  background-color: rgba(255, 255, 255, 0);
}
/*ヘッダー全体*/
@media (max-width: 700px) {
  .holo-header-item {
    height: 50px;
  }
}
@media (min-width: 700px) {
  .holo-header-item {
    height: 70px;
  }
}

/*PC用のヘッダーリンク */
@media (max-width: 700px) {
  .holo-links-pc {
    display: none;
  }
}
/*スマホ用のヘッダーリンク */
@media (min-width: 700px) {
  .holo-links-android {
    display: none;
  }
}
/*スマホのリンク表示のボタン */
#holo-nav-button {
  color: #56c6fd;
  margin: 0 0 0 auto;
}
/*スマホのリンク一覧スタイル */
#holo-nav {
  /*position:fixed;にし、z-indexの数値を大きくして前面へ*/
  position: fixed;
  z-index: 10;
  /*ナビのスタート位置と形状*/
  top: -120%;
  left: 0;
  width: 100%;
  height: 100vh; /*ナビの高さ*/
  background: white;
  /*動き*/
  transition: all 0.6s;
  overflow-y: scroll;
}
/*アクティブクラスがついたら位置を0に*/
#holo-nav.panelactive {
  top: 0;
}

/*ナビゲーションの縦スクロール*/
#holo-nav.panelactive {
  /*ナビの数が増えた場合縦スクロール*/
  position: fixed;
  width: 100%;
  height: 100vh; /*表示する高さ*/
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;
}

.holo-nav-item {
  margin: 0 0 auto auto;
}
</style>
