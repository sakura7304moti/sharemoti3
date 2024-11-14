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
          justify-content: space-between;
        "
      >
        <!--ヘッダーの左側-->
        <div
          style="
            font-size: 18px;
            width: 200px;
            color: rgb(51, 51, 51);
            background-color: white;
            border-radius: 0px 10px 10px 0px;
            position: relative;
            left: -24px;
          "
          class="fadeDown"
          v-if="!menuView"
        >
          <div
            style="padding-left: 8px; padding-top: 8px; cursor: pointer"
            @click="router.replace('/')"
          >
            韓国のおばあちゃんち
          </div>
        </div>

        <!--ヘッダーの右側(PC用)-->
        <div class="nav-top fadeRight bg-white">
          <div class="nav-child">
            <span
              @click.prevent="
                router.replace('/');
                headerClose();
              "
              >トップ</span
            >
          </div>
          <div class="nav-child">
            <div @mouseover="headerOpen(1)" @click="headerOpen(1)">
              <q-icon name="expand_more" />ページ
            </div>
          </div>

          <!--info-->
          <div class="nav-child">
            <div @mouseover="headerOpen(2)" @click="headerOpen(2)">
              <q-icon name="expand_more" />リンク
            </div>
          </div>
        </div>
      </div>
      <div class="nav-top" style="width: 100%; max-width: 100%">
        <div style="width: 200px"></div>
        <div class="nav-child">
          <div
            class="balloon1-top fadeRight"
            :class="{ 'hover-page': head.id == 1, 'hover-other': head.id != 1 }"
            v-if="head.id > 0"
          >
            <div>
              <div class="row">
                <div
                  class="col"
                  v-for="page in nowPage(head.id)"
                  :key="page.id"
                  style="color: rgb(0, 167, 137); font-size: 16px"
                >
                  <div class="q-mb-sm">{{ page.title }}</div>

                  <div
                    v-for="item in nowPageList(page.id, head.id)"
                    :key="item.title"
                    style="color: rgb(51, 51, 51)"
                  >
                    <a
                      class="nav-content q-pb-xs"
                      @click.prevent="
                        router.replace(item.url);
                        headerClose();
                      "
                    >
                      {{ item.title }}
                    </a>
                  </div>
                </div>
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
    const {
      callPageList,
      pages,
      otherPages,
      callOtherPageList,
      nowPage,
      nowPageList,
    } = usePage();

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
      otherPages,
      callOtherPageList,
      nowPage,
      nowPageList,
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

  const otherPages = ref([
    {
      id: 1,
      title: 'YouTube',
    },
    {
      id: 2,
      title: '共有',
    },
  ] as headItem[]);

  const youtubePages = ref([
    {
      title: 'スマブラ',
      url: 'https://www.youtube.com/playlist?list=PLbP5km9K7tgfHKxHvk9nOx7hcbLbnHSuS',
    },
    {
      title: '荒野行動',
      url: 'https://www.youtube.com/playlist?list=PLbP5km9K7tgfq6DVQHvM3-8TSmOd6rALY',
    },
    {
      title: 'オンライン飲み会',
      url: 'https://www.youtube.com/playlist?list=PLbP5km9K7tgfeI0AQkD--BCUIW0syQ_3K',
    },
  ] as PageState[]);

  const sharePages = ref([
    {
      title: 'Google Drive',
      url: 'https://drive.google.com/drive/folders/1XSRGqBx5FeJaOSJj9UtF3e2M7S3Z3PsG?usp=sharing',
    },
    {
      title: 'Notion',
      url: 'https://brindle-spring-0d6.notion.site/URL-2998ca28318d430cbdd7d5b7ad034ccf?pvs=4',
    },
  ] as PageState[]);

  function callOtherPageList(no: number) {
    if (no == 1) return youtubePages.value;
    if (no == 2) return sharePages.value;
    return [] as PageState[];
  }

  function nowPage(id: number) {
    if (id == 1) {
      return pages.value;
    }
    if (id == 2) {
      return otherPages.value;
    }
    return [];
  }

  function nowPageList(id: number, headId: number) {
    if (headId == 1) {
      return callPageList(id);
    }
    if (headId == 2) {
      return callOtherPageList(id);
    }
    return [];
  }

  return {
    pages,
    callPageList,
    otherPages,
    callOtherPageList,
    nowPage,
    nowPageList,
  };
}
</script>
<style>
@import '../css/q-table.css';
.menu-icon-image {
  width: 52px;
}
body {
  background-color: rgb(255, 246, 230);
  color: #333;
  font-family: 'Noto Sans JP', sans-serif;
}
/*navigation */
.nav-top {
  justify-content: flex-end;
  display: flex;
  padding-top: 10px;
  padding-right: 20px;
  padding-left: 10px;
  width: calc(100% - 200px);
  max-width: 600px;
  height: 100%;
  border-radius: 10px 0 0 10px;
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
  transition: color 0.3s ease;
  padding-right: 32px;
  height: 100%;
  width: 120px;
  position: relative;
  z-index: 2;
}
.nav-child:hover {
  color: #498e677a;
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
.balloon1-top {
  position: absolute;
  left: -400px;
  margin: 1.5em 0;
  padding: 10px 14px;
  width: 500px;
  color: #555;
  font-size: 16px;
  background: white;
}

.balloon1-top:before {
  content: '';
  position: absolute;
  top: -30px;
  left: 60%;
  margin-left: -15px;
  border: 15px solid transparent;
  border-bottom: 15px solid white;
}

.balloon1-top p {
  margin: 0;
  padding: 0;
}
.nav-content {
  cursor: pointer;
  font-size: 14px;
}
.nav-content:hover {
  transition: 0.3s;
  color: rgb(0, 167, 137);
}
body {
  overflow-x: hidden;
}
.nav-select {
  justify-content: flex-end;
  display: flex;
  padding-top: 10px;
  padding-right: 20px;
  padding-left: 10px;
  width: calc(100% - 200px);
  max-width: 600px;
  height: 100%;
  border-radius: 10px 0 0 10px;
}
.hover-page::before {
  left: 60%;
}

.hover-other::before {
  left: 85%;
}
</style>
