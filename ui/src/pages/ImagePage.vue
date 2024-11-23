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
          <div class="text-subtitle1">つかいかた！</div>
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
    <div class="q-mt-md q-ml-lg text-grey text-subtitle1">
      登録・編集
      <img
        src="https://img.icons8.com/ios/250/000000/edit.png"
        style="width: 13px; height: auto; object-fit: contain; margin-left: 4px"
      />
    </div>
    <div class="row flex-wrap edit-area">
      <div class="create-btn-outline">
        <div class="create-btn">
          <div class="text-center text-h6 text-white" @click="addDialog = true">
            名画を寄贈する
          </div>
        </div>
      </div>
      <div class="q-mt-sm">
        <q-toggle
          v-model="deleteBtnDisplay"
          label="削除アイコン表示"
          icon="delete"
          color="negative"
          class="q-ml-sm"
        />
      </div>
    </div>

    <!--追加ダイアログ-->
    <q-dialog v-model="addDialog">
      <q-card class="edit-dialog">
        <q-card-section>
          <div class="row justify-between">
            <div class="text-subtitle1">名画の登録審査</div>
            <div>
              <q-icon
                name="close"
                size="sm"
                style="cursor: pointer"
                @click="addDialog = false"
              />
            </div>
          </div>
          <div class="q-ma-md">
            <div class="q-mb-md">
              <q-file
                v-model="pickFile"
                :url="uploadUrl"
                label="画像を選択する・画像をドロップする"
                outlined
                dense
                :clearable="pickFile?.size != null"
                style="max-width: 300px"
                stack-label
              />
            </div>
            <div class="q-mb-md">
              <q-input
                type="textarea"
                label="タイトル"
                outlined
                stack-label
                v-model="addItem.title"
              />
            </div>
            <div class="q-mb-md">
              <q-input
                type="textarea"
                label="詳細"
                outlined
                stack-label
                v-model="addItem.detail"
              />
            </div>
            <div class="q-mb-md" v-if="addImage">
              <img :src="addImage" class="content-img editing" />
            </div>
            <div class="text-right">
              <q-btn
                label="追加する"
                color="primary"
                @click="insert()"
                :disable="(pickFile?.size ?? 0) == 0"
                :loading="loadState.isSave"
              />
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

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
          <img class="content-img" :src="rec.url" @click="editClick(rec.id)" />
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
            dense
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
        <q-bar class="bg-primary row justify-between" style="min-height: 40px">
          <div class="text-white" style="font-size: 20px">
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
      <q-card class="edit-dialog" v-if="editItem">
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
            <div class="q-mb-sm">
              <q-file
                v-model="editFile"
                :url="uploadUrl"
                label="画像を変更する"
                outlined
                dense
                :clearable="editFile?.size != null"
                style="max-width: 300px"
                stack-label
              />
              <div v-if="editFile" class="text-subtitle2 q-mt-sm">
                保存する画像を選択してね
              </div>
            </div>
            <div class="q-mb-md" v-if="editFile == null">
              <div v-if="isDefaultImage">
                <img class="content-img editing" :src="editItem.url" />
              </div>
              <div v-else>
                <img class="content-img editing" :src="editImage" />
              </div>
            </div>
            <div class="row q-mb-md" v-if="editFile">
              <div class="col-2"></div>
              <div class="col-4 q-mr-sm">
                <img
                  class="content-img select"
                  :class="{ 'not-selection': !isDefaultImage }"
                  :src="editItem.url"
                  @click="isDefaultImage = true"
                />
                <div v-if="isDefaultImage" class="text-center">
                  <q-chip size="md">そのまま</q-chip>
                </div>
              </div>
              <div class="col-4 q-ml-sm">
                <img
                  class="content-img select"
                  :class="{ 'not-selection': isDefaultImage }"
                  :src="editImage"
                  @click="isDefaultImage = false"
                />
                <div v-if="!isDefaultImage" class="text-center">
                  <q-chip size="md">New!</q-chip>
                </div>
              </div>
              <div class="col-2"></div>
            </div>
            <div class="row justify-between">
              <div>
                <q-btn
                  label="削除する"
                  color="negative"
                  @click="deleteDialog = true"
                  v-if="deleteBtnDisplay"
                />
              </div>

              <div>
                <q-btn
                  label="保存する"
                  color="primary"
                  @click="edit()"
                  :loading="loadState.isSave"
                />
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!--削除確認-->
    <q-dialog v-model="deleteDialog">
      <q-card class="edit-dialog">
        <q-card-section>
          <div class="row justify-between">
            <div class="text-subtitle1">
              削除確認<q-icon
                name="delete"
                color="negative"
                class="q-ml-sm"
                size="xs"
              />
            </div>
            <div>
              <q-icon
                name="close"
                size="sm"
                style="cursor: pointer"
                @click="deleteDialog = false"
              />
            </div>
          </div>
          <div class="q-ma-md">
            <div class="q-mb-md text-subtitle2">次の画像を削除する？</div>
            <div class="q-mb-md">
              <q-field dense label="タイトル" stack-label outlined>
                {{ editItem.title }}
              </q-field>
            </div>

            <div class="q-mb-md">
              <img class="content-img editing" :src="editItem.url" />
            </div>
            <div class="row justify-between">
              <div>
                <q-btn label="キャンセルする" @click="deleteDialog = false" />
              </div>

              <div>
                <q-btn
                  label="削除する"
                  color="negative"
                  @click="drop(editItem.id)"
                  :loading="loadState.isDelete"
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
import { computed, defineComponent, ref, watch } from 'vue';
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
            response.records.forEach((it) =>
              records.value.push({
                id: it.id,
                title: it.title,
                detail: it.detail,
                fileName: it.fileName,
                ext: it.ext,
                createAt: it.createAt,
                updateAt: it.updateAt,
                url: imageUrl(it.id),
              })
            );
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
      return api.imageUrl(id) + '?any=' + new Date().getTime();
    };

    const onScrollSearch = async function () {
      console.log('scroll called');
      if (!loadState.value.isSearch && pageNo.value < maxPage.value) {
        console.log('scroll search...');
        pageNo.value = pageNo.value + 1;
        await search(pageNo.value);
      }
    };
    const isDialogClose = computed(
      () =>
        editDialog.value == false &&
        maxDialog.value == false &&
        addDialog.value == false &&
        deleteDialog.value == false
    );
    const handleScroll = () => {
      const bottomOfWindow =
        window.innerHeight + window.scrollY >=
        document.documentElement.offsetHeight - 200;

      if (bottomOfWindow && !loadState.value.isSearch && isDialogClose.value) {
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
      search(pageNo.value);
      window.addEventListener('scroll', handleScroll);
      window.addEventListener('scroll', setTopBtn);
    };

    /**編集 */
    const editDialog = ref(false);
    const editItem = ref({} as Image);
    const editImage = ref('');
    const isDefaultImage = ref(true);
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
          url: imageUrl(id),
        };
        editDialog.value = true;
      }
    };
    const edit = async function () {
      loadState.value.isSave = true;
      if (isDefaultImage.value == false && editFile.value) {
        const fileName = await uploadImage(editFile.value);
        if (fileName == null) {
          loadState.value.isSave = false;
          return;
        }
        editItem.value.fileName = fileName.split('.')[0];
        editItem.value.ext = fileName.split('.')[1];
      }
      await update(editItem.value);
      editFile.value = null;
      loadState.value.isSave = false;
      editDialog.value = false;
    };
    const update = async function (image: Image) {
      await api
        .update(image)
        .then((response) => {
          console.log('update response', response);
          const found = records.value.find((it) => it.id == image.id);
          if (found) {
            found.title = image.title;
            found.detail = image.detail;
            found.url = imageUrl(image.id);
          }
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
    };

    /**最大化 */
    const maxDialog = ref(false);
    const editFile = ref(null as File | null);
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
    const deleteBtnDisplay = ref(false);
    const deleteDialog = ref(false);
    const drop = async function (id: number) {
      loadState.value.isDelete = true;
      await api
        .dell(id)
        .then((response) => {
          if (response) {
            console.log('delete image response', response);
            records.value = records.value.filter((it) => it.id != id); // 消したレコードを除外
            deleteDialog.value = false;
            editDialog.value = false;
            quasar.notify({
              color: 'primary',
              position: 'top',
              message: '消したでぇ〜',
            });
          }
        })
        .catch((err) => {
          console.log('delete err', err);
          quasar.notify({
            color: 'negative',
            position: 'top',
            message: '削除でエラーになった...',
          });
        });
      loadState.value.isDelete = false;
    };

    /**追加 */
    const pickFile = ref(null as File | null);
    const addDialog = ref(false);
    const addImage = ref('');
    const uploadUrl = computed(() => api.uploadUrl());
    const addItem = ref({
      fileName: '',
      ext: '',
      title: '',
      detail: '',
    } as AddImage);
    const insert = async function () {
      loadState.value.isSave = true;
      if (pickFile.value == null) {
        loadState.value.isSave = false;
        return;
      }
      const fileName = await uploadImage(pickFile.value);
      if (fileName == null) {
        loadState.value.isSave = false;
        return;
      }

      addItem.value.fileName = fileName.split('.')[0];
      addItem.value.ext = fileName.split('.')[1];
      await addRecord(addItem.value);
      loadState.value.isSave = false;
      addDialog.value = false;
      quasar.notify({
        color: 'primary',
        position: 'top',
        message: '合格！登録したで！',
      });
    };
    const uploadImage = async function (file: File) {
      let fileName = null as string | null;
      await api
        .upload(file)
        .then((response) => {
          if (response) {
            console.log('upload response', response);
            fileName = response.fileName;
          }
        })
        .catch((err) => {
          console.log('upload err', err);
          quasar.notify({
            color: 'negative',
            position: 'top',
            message: 'アップロードでエラーになった...',
          });
        });
      return fileName;
    };

    const addRecord = async function (state: AddImage) {
      await api
        .insert(state)
        .then((response) => {
          if (response) {
            console.log('insert repsonse', response);
            records.value.splice(0);
            pageNo.value = 1;
            search(pageNo.value);
            addItem.value = {
              fileName: '',
              ext: '',
              title: '',
              detail: '',
            };
            pickFile.value = null;
          }
        })
        .catch((err) => {
          console.log('insert err', err);
          quasar.notify({
            color: 'negative',
            position: 'top',
            message: '追加でエラーになった...',
          });
        });
    };
    watch(pickFile, () => {
      if (pickFile.value) {
        addImage.value = URL.createObjectURL(pickFile.value);
      } else {
        addImage.value = '';
      }
    });

    watch(editFile, () => {
      if (editFile.value) {
        editImage.value = URL.createObjectURL(editFile.value);
        isDefaultImage.value = false;
      } else {
        editImage.value = '';
        isDefaultImage.value = true;
      }
    });

    onMount();
    return {
      editItem,
      maxImageId,
      editDialog,
      maxDialog,
      ruleDialog,
      addDialog,
      editFile,
      editImage,
      pickFile,
      isShowTopButton,
      isDefaultImage,
      deleteBtnDisplay,
      deleteDialog,
      loadState,
      addImage,
      addItem,
      pageNo,
      maxPage,
      records,
      search,
      imageUrl,
      uploadUrl,
      onTopClick,
      editClick,
      edit,
      maxClick,
      maxClose,
      drop,
      insert,
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
  url: string;
}
interface AddImage {
  fileName: string;
  ext: string;
  title: string;
  detail: string;
}
</script>
<style>
/**検索欄や編集アイコンなど */
.edit-area {
  margin: 16px;
  margin-top: 0px;
  background-color: white;
  height: 120px;
  max-width: 420px;
  width: calc(100% - 16px * 2);
  border-radius: 10px;
}
@media (min-width: 500px) {
  .edit-area {
    height: 80px;
  }
}
.create-btn-outline {
  position: relative;
  top: 16px;
  left: 16px;
  height: 70px;
  margin-right: 24px;
}
.create-btn {
  cursor: pointer;
  width: 200px;
  height: 40px;
  border-radius: 10px;
  background-color: rgb(24, 191, 160);
}
.edit-dialog {
  max-width: 800px;
  width: 100%;
}
/**画像 */
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
.content-img.select {
  height: 100px;
  object-position: center;
  cursor: pointer;
  background-color: rgba(200, 200, 200, 0.5);
  border: 3px solid rgba(200, 200, 200, 1);
  border-radius: 10px;
  padding: 4px;
}
.not-selection {
  opacity: 0.5;
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
