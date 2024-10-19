<template>
  <q-card style="width: 900px">
    <q-card-section>
      <div
        style="
          font-family: HinaMincho-Regular;
          font-size: 36px;
          padding-bottom: 16px;
        "
      >
        {{ new Date().getFullYear() }}年やーきー川柳 最優秀作品
      </div>
      <!--ガノンヤーキー川柳-->
      <div style="display: flex; flex-wrap: wrap">
        <div class="q-pr-md q-pt-lg">
          <q-btn
            @click.prevent.stop="selectHaiku()"
            icon="autorenew"
            color="black"
            size="sm"
            class=""
            outline
            dense
          />
        </div>
        <div class="haiku-box-big">
          <div
            style="
              writing-mode: vertical-rl;
              font-family: haiku;
              font-size: 32px;
              margin-left: auto;
            "
          >
            <div style="margin-right: 100px">{{ haiku.first }}</div>
            <div style="margin-right: 20px">{{ haiku.second }}</div>
            <div style="margin-right: 20px">{{ haiku.third }}</div>
            <div style="margin-right: 20px">
              {{ haiku.poster }}
            </div>
          </div>
        </div>
        <di>
          <img
            src="../../assets/senno_rikyu.png"
            style="padding-top: 100px; height: 400px; filter: grayscale(80%)"
          />
          <div class="text-subtitle1 text-weight-bold">
            そこにわびさびはあるんか?
          </div>
        </di>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import HaikuListApi from 'src/api/main/HaikuListApi';
export default defineComponent({
  name: 'haiku-info',
  setup() {
    //俳句をランダムに取得
    const haiku = ref({
      id: -1,
      first: '',
      second: '',
      third: '',
      poster: '',
      detail: '',
      createAt: '',
      updateAt: '',
    } as Haiku);
    const haikus = ref([] as Haiku[]);
    const getHaikus = async function () {
      await HaikuListApi.search().then((response) => {
        if (response) {
          haikus.value.splice(0);
          response.forEach((it) => haikus.value.push(it));
          selectHaiku();
        }
      });
    };
    getHaikus();
    const selectHaiku = function () {
      haiku.value =
        haikus.value[Math.floor(Math.random() * haikus.value.length)];
    };
    return { haiku, selectHaiku };
  },
});
interface Haiku {
  id: number;
  first: string;
  second: string;
  third: string;
  poster: string;
  detail: string;
  createAt: string;
  updateAt: string;
}
</script>
<style>
/*fonts */
@font-face {
  font-family: 'haiku';
  src: url(src/fonts/haiku2.ttf) format('truetype');
}
@font-face {
  font-family: 'HinaMincho-Regular';
  src: url(src/fonts/HinaMincho-Regular.ttf) format('truetype');
}
/*haiku-box-big */
.haiku-box-big {
  width: 370px;
  margin: 2em 0;
  position: relative;
  padding: 0.5em 1.5em;
  border-top: solid 2px black;
  border-bottom: solid 2px black;
}
.haiku-box-big:before,
.haiku-box-big:after {
  content: '';
  position: absolute;
  top: -10px;
  width: 2px;
  height: -webkit-calc(100% + 20px);
  height: calc(100% + 20px);
  background-color: black;
}
.haiku-box-big:before {
  left: 10px;
}
.haiku-box-big:after {
  right: 10px;
}
.haiku-box-big div {
  margin: 0;
  padding: 0;
}
</style>
