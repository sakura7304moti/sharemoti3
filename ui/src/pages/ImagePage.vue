<template>
  <q-page class="">
    <div class="text-h6">
      <span class="q-mr-sm">名画伯展覧会</span
      ><q-icon
        class="cursor-pointer"
        name="info"
        color="teal-4"
        size="sm"
        @click="ruleDialog = true"
      ></q-icon>
    </div>
    <!--使い方ダイアログ-->
    <q-dialog v-model="ruleDialog">
      <q-card style="max-width: 500px">
        <q-card-section>
          <div class="text-h6">つかいかた！</div>
          <div class="q-ma-md text-body1">
            <div>1.編集は画像をクリックしてねっ</div>
          </div>
          <div>
            <q-btn
              icon="thumb_up_alt"
              color="primary"
              label="分かったよ、、、おれ、、、駄菓子屋になるよっ！！"
              @click="ruleDialog = false"
            />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
    <!--追加・検索・削除ボタン表示エリア-->
    <div
      style="
        margin: 16px;
        background-color: white;
        height: 100px;
        max-width: 400px;
        border-radius: 10px;
      "
    >
      <div style="position: relative; top: 16px; left: 16px; height: 60px">
        <div
          style="
            cursor: pointer;
            width: 200px;
            height: 40px;
            border-radius: 10px;
            background-color: rgb(24, 191, 160);
          "
        >
          <div class="text-center text-h6 text-white">歴史を刻む</div>
        </div>
      </div>
      <q-toggle
        v-model="deleteOpen"
        label="削除アイコン表示"
        icon="delete"
        color="negative"
      />
    </div>

    <!--画像表示エリア-->
    <div>
      <div v-for="rec in records" :key="rec.id" class="content-card">
        <div class="content-title">
          {{ rec.title }}
        </div>
        <div class="content-detail">
          {{ rec.detail }}
        </div>
        <div class="flipDown">
          <img
            class="content-img"
            :src="imageUrl(rec.id)"
            @click="editClick(rec.id)"
          />
        </div>
        <div class="text-grey q-mb-sm">
          <span class="q-pr-sm">最終更新日</span><span class="q-pr-sm">:</span>
          <span class="q-pr-lg">{{
            rec.createAt < rec.updateAt ? rec.updateAt : rec.createAt
          }}</span>
        </div>
        <div>
          <q-btn
            label="最大化する"
            icon="crop_free"
            size="md"
            @click="maxClick(rec.id)"
          />
        </div>
      </div>
    </div>

    <!--スクロールボタン-->
    <button v-if="isShowTopButton" class="scroll-to-top" @click="onTopClick">
      <img
        style="height: 70px"
        class="holotwitter-top-scroll-img"
        src="../assets/Rocket Base 512x512.png"
      />
      <div>トップに戻る</div>
    </button>
    <!--最大化ダイアログ-->
    <q-dialog v-model="maxDialog" maximized>
      <q-card>
        <q-bar class="bg-primary row justify-between" style="height: 40px">
          <div class="text-white" style="font-size: 24px">
            {{ records.find((it) => it.id == maxImageId)?.title }}
          </div>
          <div>
            <q-icon
              name="close"
              color="white"
              size="md"
              style="cursor: pointer"
              @click="maxDialog = false"
            >
              <q-tooltip>閉じる</q-tooltip>
            </q-icon>
          </div>
        </q-bar>
        <div>
          <img
            :src="imageUrl(maxImageId)"
            style="
              max-width: 100%;
              width: 100%;
              height: auto;
              object-fit: contain;
            "
          />
        </div>
      </q-card>
    </q-dialog>
    <!--編集ダイアログ-->
    <q-dialog v-model="editDialog">
      <q-card style="max-width: 800px; width: 100%" v-if="editItem">
        <q-card-section>
          <div class="row justify-between">
            <div class="text-subtitle1">名画に手を加える</div>
            <div>
              <q-icon
                name="close"
                size="sm"
                style="cursor: pointer"
                @click="editDialog = false"
              />
            </div>
          </div>

          <div class="q-ma-md">
            <div class="q-mb-md">
              <q-input
                type="textarea"
                label="タイトル"
                outlined
                stack-label
                v-model="editItem.title"
              />
            </div>
            <div class="q-mb-md">
              <q-input
                type="textarea"
                label="詳細"
                outlined
                stack-label
                v-model="editItem.detail"
              />
            </div>
            <div class="q-mb-md">
              <img
                class="content-img editing"
                :src="imageUrl(editItem.id)"
                @click="editClick(editItem.id)"
              />
            </div>
            <div class="row justify-between">
              <div>
                <q-btn
                  label="削除する"
                  color="negative"
                  @click="editDialog = false"
                  v-if="deleteOpen"
                />
              </div>

              <div>
                <q-btn
                  label="保存する"
                  color="primary"
                  @click="edit(editItem)"
                  :loading="loadState.isSave"
                />
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import api from 'src/api/main/ImageListApi';
import { useQuasar } from 'quasar';
export default defineComponent({
  name: 'image-page',
  setup() {
    const quasar = useQuasar();
    /**検索 */
    const isShowTopButton = ref(false);
    const loadState = ref({
      isSave: false,
      isSearch: false,
      isDelete: false,
    } as LoadState);
    const pageNo = ref(1);
    const maxPage = ref(1);

    const records = ref([] as Image[]);

    const search = async function (page: number) {
      loadState.value.isSearch = true;
      await api
        .search(page)
        .then((response) => {
          if (response) {
            console.log('search response', response);
            maxPage.value = response.totalCount;
            response.records.forEach((it) => records.value.push(it));
          }
        })
        .catch((err) => {
          console.log('search err', err);
          quasar.notify({
            color: 'negative',
            position: 'top',
            message: '検索でエラーになった...',
          });
        });
      loadState.value.isSearch = false;
    };

    const imageUrl = function (id: number) {
      return api.imageUrl(id);
    };
    search(pageNo.value);

    const onScrollSearch = async function () {
      console.log('scroll called');
      if (!loadState.value.isSearch && pageNo.value < maxPage.value) {
        console.log('scroll search...');
        pageNo.value = pageNo.value + 1;
        await search(pageNo.value);
      }
    };
    const handleScroll = () => {
      const bottomOfWindow =
        window.innerHeight + window.scrollY >=
        document.documentElement.offsetHeight - 200;

      if (
        bottomOfWindow &&
        !loadState.value.isSearch &&
        editDialog.value == false
      ) {
        onScrollSearch();
      }
    };

    const onTopClick = function () {
      // スムーズにページのトップに戻る
      window.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    };

    const setTopBtn = function () {
      isShowTopButton.value = window.scrollY > 100;
    };

    const onMount = function () {
      window.addEventListener('scroll', handleScroll);
      window.addEventListener('scroll', setTopBtn);
    };

    /**編集 */
    const editDialog = ref(false);
    const editItem = ref({} as Image);
    const editClick = function (id: number) {
      const found = records.value.find((it) => it.id == id);
      if (found) {
        editItem.value = {
          id: found.id,
          fileName: found.fileName,
          ext: found.ext,
          title: found.title,
          detail: found.detail,
          createAt: found.createAt,
          updateAt: found.updateAt,
        };
        editDialog.value = true;
      }
    };
    const edit = async function (image: Image) {
      loadState.value.isSave = true;
      await api
        .update(image)
        .then((response) => {
          console.log('update response', response);
          const found = records.value.find((it) => it.id == image.id);
          if (found) {
            found.title = image.title;
            found.detail = image.detail;
          }
          editDialog.value = false;
          quasar.notify({
            color: 'primary',
            position: 'top',
            message: '変更を保存したよ！！',
          });
        })
        .catch((err) => {
          console.log('update err', err);
          quasar.notify({
            color: 'negative',
            position: 'top',
            message: '更新でエラーになった...',
          });
        });
      loadState.value.isSave = false;
    };

    /**最大化 */
    const maxDialog = ref(false);
    const maxImageId = ref(-1);
    const maxClick = function (id: number) {
      maxDialog.value = true;
      maxImageId.value = id;
    };

    const maxClose = function () {
      maxDialog.value = false;
      maxImageId.value = -1;
    };

    /**使い方説明 */
    const ruleDialog = ref(false);

    /**削除 */
    const deleteOpen = ref(false);

    onMount();
    return {
      editItem,
      maxImageId,
      editDialog,
      maxDialog,
      ruleDialog,
      isShowTopButton,
      deleteOpen,
      loadState,
      pageNo,
      maxPage,
      records,
      search,
      imageUrl,
      onTopClick,
      editClick,
      edit,
      maxClick,
      maxClose,
    };
  },
});
interface LoadState {
  isSave: boolean;
  isSearch: boolean;
  isDelete: boolean;
}
interface Image {
  id: number;
  fileName: string;
  ext: string;
  title: string;
  detail: string;
  createAt: string;
  updateAt: string;
}
</script>
<style>
.content-card {
  max-width: 680px;
  margin-bottom: 48px;
  padding: 16px;
}
.content-title {
  color: rgb(24, 191, 160);
  line-height: 30px;
  font-size: 20px;
  font-weight: 700;
  white-space: pre-wrap;
  font-family: 'Noto Sans JP';
}
.content-detail {
  max-width: 100%;
  margin-left: 8px;
  padding: 8px 0;
  color: rgb(15, 20, 25);
  line-height: 24px;
  font-size: 13px;
  font-family: 'Noto Sans JP';
  white-space: pre-wrap;
  font-weight: 500;
}
.content-img {
  max-width: 100%;
  width: 100%;
  max-height: 70vh;
  height: 100;
  object-fit: contain;
  object-position: left;
  cursor: pointer;
}
.content-img.editing {
  max-height: 400px;
  object-position: center;
  cursor: default;
}
.zoom-text {
  cursor: pointer;
}
.zoom-text:hover {
  transition: 0.4s;
  color: rgb(24, 191, 160);
}
@media (max-width: 680px) {
  .content-title {
    line-height: 20px;
    font-size: 18px;
  }
  .content-detail {
    max-width: 100%;
    line-height: 20px;
  }
}
/* 下へ */
.flipDown {
  animation-name: flipDownAnime;
  animation-duration: 1.5s;
  animation-fill-mode: forwards;
  opacity: 0;
}

@keyframes flipDownAnime {
  from {
    transform: perspective(2500px) rotateX(100deg);
    opacity: 0;
  }

  to {
    transform: perspective(2500px) rotateX(0);
    opacity: 1;
  }
}
/* 左へ */
.flipLeft {
  animation-name: flipLeftAnime;
  animation-duration: 1s;
  animation-fill-mode: forwards;
  perspective-origin: left center;
  opacity: 0;
}

@keyframes flipLeftAnime {
  from {
    transform: perspective(600px) translate3d(0, 0, 0) rotateY(30deg);
    opacity: 0;
  }

  to {
    transform: perspective(600px) translate3d(0, 0, 0) rotateY(0deg);
    opacity: 1;
  }
}
</style>
