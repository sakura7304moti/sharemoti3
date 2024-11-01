<template>
  <q-page class="" style="padding-left: 32px">
    <!--あいさつ-->
    <div class="row q-gutter-md fadeLeft" style="padding-top: 48px">
      <div>
        <img src="../assets/obachan.jpg" height="130" id="oba-profile" />
        <div class="profile-name" @click="router.replace('/imagelist')">
          韓国のおばあちゃん
        </div>
      </div>
      <balloon-left :text="obamessage" style="height: 120px" />
    </div>

    <!--ここどこ?-->
    <div style="padding-top: 32px" class="fadeIn">
      <div class="sub-article">
        <span class="box-title"> ここはどこ? </span>
        <p>
          数々の思い出が保管されているおばあちゃんち。名言やボイスやウルトラCなど...
        </p>
      </div>
    </div>

    <!--ここどこ?-->
    <div style="padding-top: 16px" class="fadeIn">
      <div class="sub-article">
        <span class="box-title"> 私はだれ? </span>
        <p>今日からお前は...{{ ssbuName }}だ！！</p>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import api from 'src/api/main/NameList2Api';
import balloonLeft from 'src/components/balloonLeft.vue';
import { useRouter } from 'vue-router';
export default defineComponent({
  name: 'IndexPage',
  components: {
    balloonLeft,
  },
  setup() {
    const router = useRouter();
    const ssbuName = ref('');
    const getName = async function () {
      await api.search().then((response) => {
        if (response) {
          const filreco = response.filter((it) => it.name != it.ssbuName);
          const rowCount = filreco.length;
          const index = Math.floor(Math.random() * (rowCount - 1));
          ssbuName.value = filreco[index].name;
        }
      });
    };

    getName();

    return {
      router,
      obamessage: `よく来たわね
ゆっくりしていきなさい
とりあえずお茶でもどうかしら
`,
      ssbuName,
    };
  },
});
</script>
<style>
#oba-profile {
  border-radius: 50%; /* 角丸半径を50%にする(=円形にする) */
  border: 3px solid #b4b4b4; /* 枠線を付加 */
}
.profile-name {
  text-align: center;
  font-weight: bold;
  font-size: 1rem;
}
.index-page-card {
  width: 100%;
  max-width: 250px;
}
/**animation */
/* 左から */

.fadeLeft {
  animation-name: fadeLeftAnime;
  animation-duration: 0.5s;
  animation-fill-mode: forwards;
  opacity: 0;
}

@keyframes fadeLeftAnime {
  from {
    opacity: 0;
    transform: translateX(-100px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}
/*subtitle */
.sub-article {
  position: relative;
  margin: 2em 0;
  padding: 0.5em 1em;
  border: solid 3px rgba(182, 200, 155, 1);
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
}
.sub-article .box-title {
  position: absolute;
  display: inline-block;
  top: -13px;
  left: 10px;
  padding: 0 9px;
  line-height: 1;
  font-size: 19px;
  background: rgb(240, 238, 220);
  color: rgba(182, 200, 155, 1);
  font-weight: bold;
}
.sub-article p {
  margin: 0;
  padding-top: 16px;
  color: rgb(147, 129, 118);
}
/*==================================================
ふわっ
===================================*/

/* その場で */
.fadeIn {
  animation-name: fadeInAnime;
  animation-duration: 1s;
  animation-fill-mode: forwards;
  opacity: 0;
}

@keyframes fadeInAnime {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}
</style>
