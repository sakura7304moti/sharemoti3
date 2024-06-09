<template>
  <!--与謝野晶子による焼き直し劇場-->
  <q-card style="max-width: 600px; width: 100%">
    <q-card-section>
      <div
        style="
          font-family: HinaMincho-Regular;
          font-size: 36px;
          padding-bottom: 16px;
        "
      >
        あのときの名シーンをもう一度
      </div>
      <div style="display: flex; flex-wrap: wrap; padding-bottom: 16px">
        <q-btn
          @click.prevent.stop="selectWord()"
          label="リプレイ"
          icon="autorenew"
          color="black"
          size="md"
          outline
          dense
        />
        <q-toggle
          v-model="inputView"
          label="直接編集する"
          class="q-pl-lg"
          dense
        />
      </div>
      <div v-if="inputView" class="row q-gutter-md">
        <q-input
          v-model="word"
          label="未来から来た与謝野晶子"
          type="textarea"
          filled
          style="width: 240px"
        />
        <q-input
          v-model="obamessage"
          label="韓国のおばあちゃん"
          type="textarea"
          filled
          style="width: 240px"
        />
      </div>

      <div class="neta-talk q-pt-md">
        <div class="row q-gutter-md">
          <div>
            <img
              src="../../assets/yosao.png"
              height="130"
              width="140"
              id="oba-profile"
              style="width: 140px"
            />
            <div class="profile-name" style="width: 120px">
              未来から来た与謝野晶子
            </div>
          </div>
          <div></div>
          <balloon-left :text="word" style="height: 100px" />
        </div>

        <div class="row q-gutter-md">
          <div>
            <img src="../../assets/obachan.jpg" height="130" id="oba-profile" />
            <div class="profile-name">韓国のおばあちゃん</div>
          </div>
          <balloon-left :text="obamessage" style="height: 120px" />
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>
<script lang="ts">
import WordList2Api from 'src/api/main/WordList2Api';
import balloonLeft from '../balloonLeft.vue';
import { defineComponent, ref } from 'vue';
export default defineComponent({
  name: 'word-info',
  components: {
    'balloon-left': balloonLeft,
  },
  setup() {
    //名言をランダムに取得
    const inputView = ref(false);
    const word = ref('...');
    const words = ref([] as string[]);
    const obamessage = ref('いやだああああぁぁぁ');
    const getWords = async function () {
      await WordList2Api.search({ text: '' }).then((response) => {
        if (response) {
          words.value.splice(0);
          words.value = response.records.map((it) => it.word ?? '');
          const pick =
            response.records[
              Math.floor(Math.random() * response.records.length)
            ];
          word.value = pick.word ?? '';
          selectWord();
        }
      });
    };

    const selectWord = function () {
      word.value = words.value[Math.floor(Math.random() * words.value.length)];
      obamessage.value = 'いやだああああぁぁぁ';
      inputView.value = false;
    };
    getWords();
    return {
      obamessage,
      word,
      selectWord,
      inputView,
    };
  },
});
</script>
<style>
/*pfofile */
#oba-profile {
  border-radius: 50%; /* 角丸半径を50%にする(=円形にする) */
  border: 3px solid #b4b4b4; /* 枠線を付加 */
}
.profile-name {
  font-weight: bold;
  font-size: 1rem;
  padding-bottom: 16px;
}
</style>
