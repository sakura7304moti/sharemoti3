<template>
  <!--サイドメニュー-->
  <q-drawer v-model="leftDrawerOpen" class="q-pa-md bg-grey-4" bordered>
    <q-list>
      <q-item-section>
        <div class="text-h6 text-grey-7">おばあちゃんち</div>
        <!--名言集-->
        <q-item clickable v-ripple @click="router.replace('/wordList')">
          <div class="menu-icon-image">
            <img src="../../assets/ichiro2.jpg" width="48" />
          </div>
          <q-item-section class="text-h6"> 名言集 </q-item-section>
        </q-item>

        <!--あだ名一覧-->
        <q-item clickable v-ripple @click="router.replace('/nameList')">
          <div class="menu-icon-image">
            <img src="../../assets/ichiro.png" width="48" />
          </div>
          <q-item-section class="text-h6"> あだ名一覧 </q-item-section>
        </q-item>

        <!--焼き直し条約-->
        <q-item clickable v-ripple @click="router.replace('/yaki')">
          <div class="menu-icon-image">
            <img src="../../assets/yaki_kururu.jpg" width="48" />
          </div>
          <q-item-section class="text-h6"> 焼き直し条約 </q-item-section>
        </q-item>

        <!--俳句王決定戦-->
        <q-item clickable v-ripple @click="router.replace('/haiku')">
          <div class="menu-icon-image">
            <img src="../../assets/senno_rikyu_icon.png" width="48" />
          </div>
          <q-item-section class="text-h6"> 俳句王決定戦 </q-item-section>
        </q-item>

        <!--学校一覧-->
        <q-item clickable v-ripple @click="router.replace('/school')">
          <div class="menu-icon-image">
            <img src="../../assets/shatyo.png" width="48" />
          </div>
          <q-item-section class="text-h6"> 学校一覧 </q-item-section>
        </q-item>
      </q-item-section>
      <q-separator />
      <q-item-section>
        <div class="text-h6 text-grey-7">お土産</div>
        <!--カラオケ-->
        <q-item clickable v-ripple @click="router.replace('/karaoke')">
          <div class="menu-icon-image">
            <img src="../../assets/karaoke_boy.jpg" width="48" />
          </div>
          <q-item-section class="text-h6"> カラオケ音楽堂 </q-item-section>
        </q-item>
        <!--ボイス-->
        <q-item clickable v-ripple @click="router.replace('/voice')">
          <div class="menu-icon-image">
            <img src="../../assets/kinen.jpg" width="48" />
          </div>
          <q-item-section class="text-h6"> ボイス販売所 </q-item-section>
        </q-item>
        <!--スマブラ切り抜き-->
        <q-item clickable v-ripple @click="router.replace('/ssbu')">
          <div class="menu-icon-image">
            <img
              src="https://pbs.twimg.com/profile_images/971877109139255296/Q13jcE4h_400x400.jpg"
              width="48"
            />
          </div>
          <q-item-section class="text-h6"> スマブラ切り抜き </q-item-section>
        </q-item>
        <!--オム子レイディオ-->
        <q-item clickable v-ripple @click="router.replace('/radio')">
          <div class="menu-icon-image">
            <img src="../../assets/omuko_icon2.jpg" width="48" />
          </div>
          <q-item-section class="text-h6"> オム子レイディオ </q-item-section>
        </q-item>
        <!--画像一覧-->
        <q-item clickable v-ripple @click="router.replace('/img')">
          <div class="menu-icon-image">
            <img src="../../assets/ichiro2.jpg" width="48" />
          </div>
          <q-item-section class="text-h6"> 画像まとめ </q-item-section>
        </q-item>
        <!--動画一覧-->
        <q-item clickable v-ripple @click="router.replace('/movie')">
          <div class="menu-icon-image">
            <img src="../../assets/legoman_profile.jpg" width="48" />
          </div>
          <q-item-section class="text-h6"> 動画まとめ </q-item-section>
        </q-item>
      </q-item-section>

      <q-separator />
      <q-item-section>
        <div class="text-h6 text-grey-7">おまけ</div>
        <!--Twitter-->
        <q-item clickable v-ripple @click="router.replace('/twitter')">
          <div class="menu-icon-image">
            <img src="../../assets/Logo_of_Twitter.jpg" width="48" />
          </div>

          <q-item-section class="text-h6"> twitter </q-item-section>
        </q-item>
        <!--youtube-->
        <q-item clickable v-ripple @click="router.replace('/holosong')">
          <div class="menu-icon-image">
            <img src="../../assets/youtube_icon.png" width="48" />
          </div>

          <q-item-section class="text-h6"> 歌みた </q-item-section>
        </q-item>
        <!--album-->
        <q-item clickable v-ripple @click="router.replace('/holoalbum')">
          <div class="menu-icon-image">
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Hololive_triangles_logo.svg/1200px-Hololive_triangles_logo.svg.png"
              height="48"
            />
          </div>

          <q-item-section class="text-h6"> オリ曲 </q-item-section>
        </q-item>
        <!--memory-->
        <q-item clickable v-ripple @click="router.replace('/holomemory')">
          <div class="menu-icon-image">
            <img src="../../assets/youtube_icon.png" height="48" />
          </div>

          <q-item-section class="text-h6"> 記念配信 </q-item-section>
        </q-item>

        <!--memory-->
        <q-item clickable v-ripple @click="router.replace('/holoarchive')">
          <div class="menu-icon-image">
            <img src="../../assets/youtube_icon.png" height="48" />
          </div>

          <q-item-section class="text-h6"> アーカイブ </q-item-section>
        </q-item>
      </q-item-section>

      <q-separator />

      <q-item-section>
        <div class="text-h6 text-grey-7">その他</div>
        <!--共有URLまとめ-->
        <q-item clickable v-ripple @click="router.replace('/info')">
          <div class="menu-icon-image">
            <img src="../../assets/google_drive_icon.png" width="48" />
          </div>
          <q-item-section class="text-h6"> お茶の間 </q-item-section>
        </q-item>

        <!--ホーム-->
        <q-item clickable v-ripple @click="router.replace('/')">
          <div class="menu-icon-image">
            <img
              src="../../assets/obachan.jpg"
              width="48"
              style="
                border-radius: 50%; /* 角丸半径を50%にする(=円形にする) */
                border: 1px solid #b4b4b4; /* 枠線を付加 */
              "
            />
          </div>
          <q-item-section class="text-h6"> リビングに戻る </q-item-section>
        </q-item>
      </q-item-section>
    </q-list>
  </q-drawer>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue';
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

    return {
      leftDrawerOpen,
      router,
    };
  },
});
</script>
<style>
.menu-icon-image {
  width: 52px;
}
</style>
