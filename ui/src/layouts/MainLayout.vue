<template>
  <q-layout>
    <q-header style="background-color: rgba(0, 0, 0, 0)">
      <!--ヘッダー-->

      <div
        style="
          height: 60px;
          padding-top: 16px;
          padding-left: 24px;
          display: flex;
        "
      >
        <!--ヘッダーの左側-->
        <div
          style="
            font-size: 20px;
            font-weight: 500;
            width: 300px;
            color: rgb(51, 51, 51);
          "
          class="fadeDown"
          v-if="!menuView"
        >
          韓国のおばあちゃんち
        </div>

        <!--ヘッダーの右側(PC用)-->
        <div class="nav-top fadeRight">
          <div
            @click.prevent="
              router.replace('/');
              headerClose();
            "
            class="nav-child"
          >
            トップ
          </div>
          <!--各種ページ-->
          <div v-for="p in pages" :key="p.id" class="nav-child">
            <div @mouseover="headerOpen(p.id)" @click="headerOpen(p.id)">
              <q-icon name="expand_more" />{{ p.title }}
            </div>

            <div v-if="head.id == p.id">
              <div
                v-for="item in callPageList(p.id)"
                :key="item.url"
                class="nav-child-page"
                :class="{ 'nav-child-select': head.id == p.id }"
              >
                <div
                  @click="
                    router.replace(item.url);
                    headerClose();
                  "
                >
                  <div class="q-pa-sm">
                    {{ item.title }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!--info-->
          <div class="nav-child">
            <div @mouseover="headerOpen(5)" @click="headerOpen(5)">
              <q-icon name="expand_more" />その他
            </div>
            <div v-if="head.id == 5">
              <div
                class="nav-child-page q-pa-sm"
                :class="{ 'nav-child-select': head.id == 5 }"
                style="width: 100px"
                @click="
                  otherPageClick(
                    'https://drive.google.com/drive/folders/1XSRGqBx5FeJaOSJj9UtF3e2M7S3Z3PsG?usp=sharing'
                  )
                "
              >
                <img
                  src="../assets/google_drive_icon.png"
                  style="height: 32px"
                  v-if="head.id == 5"
                />
              </div>

              <div
                class="nav-child-page q-pa-sm"
                :class="{ 'nav-child-select': head.id == 5 }"
                style="width: 100px"
                @click="
                  otherPageClick(
                    'https://brindle-spring-0d6.notion.site/URL-2998ca28318d430cbdd7d5b7ad034ccf?pvs=4'
                  )
                "
              >
                <img
                  src="../assets/notion_icon.png"
                  style="height: 32px"
                  v-if="head.id == 5"
                />
              </div>

              <div
                class="nav-child-page q-pa-sm"
                :class="{ 'nav-child-select': head.id == 5 }"
                style="width: 100px"
                @click="
                  otherPageClick(
                    'https://www.youtube.com/playlist?list=PLbP5km9K7tgfHKxHvk9nOx7hcbLbnHSuS'
                  )
                "
              >
                <img
                  src="../assets/youtube_icon.png"
                  style="height: 32px"
                  v-if="head.id == 5"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!--ヘッダー右側(スマホ用)-->
      <div
        class="top-menu-button nav-top-mini"
        @click="menuView = !menuView"
        :class="{ active: menuView }"
      >
        <span> </span><span> </span><span></span>
      </div>
    </q-header>

    <nav id="g-nav" :class="{ panelactive: menuView }">
      <div id="g-nav-list">
        <ul>
          <li>
            <a
              href="#"
              @click.prevent="
                router.replace('/');
                menuView = false;
              "
            >
              <q-icon name="home" />トップに戻る
            </a>
          </li>
          <q-separator style="padding-top: 2px" />
          <li v-for="item in callPageList(1)" :key="item.url">
            <a
              href="#"
              @click.prevent="
                router.replace(item.url);
                menuView = false;
              "
            >
              {{ item.title }}
            </a>
          </li>
          <q-separator style="padding-top: 2px" />

          <li v-for="item in callPageList(2)" :key="item.url">
            <a
              href="#"
              @click.prevent="
                router.replace(item.url);
                menuView = false;
              "
            >
              {{ item.title }}
            </a>
          </li>
          <q-separator style="padding-top: 2px" />

          <li v-for="item in callPageList(3)" :key="item.url">
            <a
              href="#"
              @click.prevent="
                router.replace(item.url);
                menuView = false;
              "
            >
              {{ item.title }}
            </a>
          </li>

          <q-separator style="padding-top: 2px" />

          <li v-for="item in callPageList(4)" :key="item.url">
            <a
              href="#"
              @click.prevent="
                router.replace(item.url);
                menuView = false;
              "
            >
              {{ item.title }}
            </a>
          </li>

          <q-separator style="padding-top: 2px" />

          <li>
            <a
              href="https://drive.google.com/drive/folders/1XSRGqBx5FeJaOSJj9UtF3e2M7S3Z3PsG?usp=sharing"
            >
              Google Drive
            </a>
          </li>
          <li>
            <a
              href="https://brindle-spring-0d6.notion.site/URL-2998ca28318d430cbdd7d5b7ad034ccf?pvs=4"
            >
              Notion
            </a>
          </li>
          <li>
            <a
              href="https://brindle-spring-0d6.notion.site/e2d3e427b3574e9e8e25c729b8f7abe9?pvs=4"
            >
              俺たちの<br />旅の思い出
            </a>
          </li>
          <li>
            <a
              href="https://www.youtube.com/playlist?list=PLbP5km9K7tgfHKxHvk9nOx7hcbLbnHSuS"
            >
              YouTube
            </a>
          </li>
        </ul>
      </div>
    </nav>
    <!--ページ-->
    <q-page-container style="position: relative" @click="headerClose()">
      <router-view class="q-pa-md" />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import { createPinia, setActivePinia } from 'pinia';

export default defineComponent({
  name: 'MainLayout',

  setup() {
    const opened = ref(false);
    setActivePinia(createPinia());
    const leftDrawerOpen = computed(() => opened.value);
    const router = useRouter();

    const head = ref({
      id: 0,
      display: false,
    } as head);

    const headerOpen = function (id: number) {
      head.value.id = id;
      head.value.display = true;
    };

    const headerClose = function () {
      head.value.id = 0;
      head.value.display = false;
    };

    const headerClick = function (id: number) {
      if (head.value.id == 0 || id != 0) {
        headerOpen(id);
      } else {
        headerClose();
      }
    };

    /*page */
    const { callPageList, pages, nextcloudUrl } = usePage();

    const otherPageClick = function (url: string) {
      window.open(url);
      headerClose();
    };

    return {
      leftDrawerOpen,
      toggleLeftDrawer() {
        opened.value = !opened.value;
      },
      router,
      head,
      headerOpen,
      headerClose,
      headerClick,
      callPageList,
      pages,
      otherPageClick,
      menuView: ref(false),
      nextcloudUrl,
    };
  },
});
interface headItem {
  title: string;
  id: number;
}
interface head {
  id: number;
  display: boolean;
}
interface PageState {
  title: string;
  url: string;
}

/*page function */
function usePage() {
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
      url: '/ssbu_clip',
    },
    {
      title: '切り抜きの記録',
      url: '/ssbu_clip/toukei',
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
      title: 'つぶやき',
      url: '/holotwitter',
    },
    {
      title: 'reddit',
      url: '/hololewd',
    },
    {
      title: 'pixiv',
      url: '/pixiv',
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
  ] as PageState[]);

  function callPageList(no: number) {
    if (no == 1) return mainPages.value;
    if (no == 2) return filePages.value;
    if (no == 3) return scraperPages.value;
    return [] as PageState[];
  }

  const pages = ref([
    {
      id: 1,
      title: 'テーブル',
    },
    {
      id: 2,
      title: 'お土産',
    },
    {
      id: 3,
      title: 'hololive',
    },
  ] as headItem[]);

  const nextcloudUrl = computed(() => {
    const url = window.location.href; // 現在の URL を取得
    const parsedUrl = new URL(url);
    const baseUrl = `${parsedUrl.protocol}//${parsedUrl.host}`; // プロトコルとホスト名を組み合わせる
    return baseUrl.replace('/#/', '').replace(':9000', '') + ':1000';
  });

  return { pages, callPageList, nextcloudUrl, otherClass: 5 };
}
</script>
<style>
@import '../css/q-table.css';
.menu-icon-image {
  width: 52px;
}
body {
  background-color: rgb(240, 238, 220);
  color: #333;
  font-family: 'Noto Sans JP', sans-serif;
  font-optical-sizing: auto;
  font-weight: 500;
}
/*navigation */
.nav-top {
  justify-content: flex-end;
  display: flex;
  padding-top: 20px;
  padding-right: 20px;
  width: calc(100% - 300px);
  height: 100%;
}
@media (max-width: 1030px) {
  .nav-top {
    display: none;
  }
}
@media (max-width: 1030px) {
  /*========= ボタンのためのCSS ===============*/
  .top-menu-button {
    position: fixed;
    z-index: 9999; /*ボタンを最前面に*/
    top: 10px;
    right: 10px;
    cursor: pointer;
    width: 50px;
    height: 50px;
  }

  /*×に変化*/
  .top-menu-button span {
    display: inline-block;
    transition: all 0.4s;
    position: absolute;
    left: 14px;
    height: 3px;
    border-radius: 2px;
    background-color: #666;
    width: 45%;
  }

  .top-menu-button span:nth-of-type(1) {
    top: 15px;
  }

  .top-menu-button span:nth-of-type(2) {
    top: 23px;
  }

  .top-menu-button span:nth-of-type(3) {
    top: 31px;
  }

  .top-menu-button.active span:nth-of-type(1) {
    top: 18px;
    left: 18px;
    transform: translateY(6px) rotate(-45deg);
    width: 30%;
  }

  .top-menu-button.active span:nth-of-type(2) {
    opacity: 0;
  }

  .top-menu-button.active span:nth-of-type(3) {
    top: 30px;
    left: 18px;
    transform: translateY(-6px) rotate(45deg);
    width: 30%;
  }
}
/*========= ナビゲーションのためのCSS ===============*/

#g-nav {
  /*position:fixed;にし、z-indexの数値を大きくして前面へ*/
  position: fixed;
  z-index: 2;
  /*ナビのスタート位置と形状*/
  top: -120%;
  left: 0;
  width: 100%;
  height: 100vh; /*ナビの高さ*/
  background: #bdbbbb;
  /*動き*/
  transition: all 0.6s;
  overflow-y: scroll;
}

/*アクティブクラスがついたら位置を0に*/
#g-nav.panelactive {
  top: 0;
}

/*ナビゲーションの縦スクロール*/
#g-nav.panelactive #g-nav-list {
  /*ナビの数が増えた場合縦スクロール*/
  margin-top: 50px;
  position: fixed;
  width: 100%;
  height: calc(100vh - 60px); /*表示する高さ*/
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;
}

/*ナビゲーション*/
#g-nav ul {
  position: absolute;
  z-index: 999;
  /*ナビゲーション天地中央揃え*/
  top: 60px;
  left: 50%;
  transform: translate(-50%, -60px);
}

/*リストのレイアウト設定*/

#g-nav li {
  list-style: none;
  text-align: center;
  z-index: 10;
}

#g-nav li a {
  color: rgb(51, 51, 51);
  text-decoration: none;
  padding: 10px;
  display: block;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: bold;
}
.nav-child {
  color: #333;
  text-decoration: none;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1.85;
  transition: color 0.2s ease;
  padding-right: 32px;
  height: 100%;
  width: 120px;
  position: relative;
  z-index: 2;
}
.nav-child:hover {
  color: #808080;
}
.nav-child-select {
  background-color: rgba(202, 220, 175, 1);
  color: rgb(127, 109, 98);
  border-bottom: 1.5px dashed rgba(51, 51, 51, 0.2); /* 線の太さ、スタイル、色を指定 */
}
.nav-child-select:hover {
  background-color: rgba(182, 200, 155, 1);
}
.nav-child-page {
  height: 50px;
  width: 160px;
  cursor: pointer;
}
/* 右から */

.fadeRight {
  animation-name: fadeRightAnime;
  animation-duration: 0.5s;
  animation-fill-mode: forwards;
  opacity: 0;
  z-index: 2;
}

@keyframes fadeRightAnime {
  from {
    opacity: 0;
    transform: translateX(100px);
    z-index: 2;
  }

  to {
    opacity: 1;
    transform: translateX(0);
    z-index: 2;
  }
}
/* 上から */

.fadeDown {
  animation-name: fadeDownAnime;
  animation-duration: 0.5s;
  animation-fill-mode: forwards;
  opacity: 0;
}

@keyframes fadeDownAnime {
  from {
    opacity: 0;
    transform: translateY(-100px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
/*
  トップスクロール
*/
.scroll-to-top {
  border: none;
  background-color: rgba(0, 0, 0, 0);
  position: fixed;
  bottom: 10px;
  right: 10px;
  padding: 5px 10px;
  font-size: 16px;
  cursor: pointer;
  transition: opacity 0.3s ease;
}
@media (max-width: 800px) {
  .scroll-to-top {
    display: none;
  }
}

.scroll-to-top:hover {
  background-color: rgba(255, 255, 255, 0.2);
}
</style>
