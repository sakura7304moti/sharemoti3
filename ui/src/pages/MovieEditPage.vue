<template>
  <q-page class="">
    <div class="row justify-between">
      <div class="text-h6 q-mb-md">
        <q-btn
          class="q-mr-md q-mb-xs"
          @click="onNavigateTop"
          label="一覧に戻る"
          color="primary"
          icon="arrow_back"
          dense
        />動画の編集ページ<q-spinner
          class="q-ml-sm"
          v-if="loadState.fetch"
          color="primary"
          size="sm"
        /><q-icon
          v-if="lockIcon == false"
          class="q-ml-sm cursor-pointer"
          name="lock"
          color="secondary"
          @click="lockIcon = !lockIcon"
        />
        <q-icon
          v-else
          class="q-ml-sm cursor-pointer"
          name="lock_open"
          color="secondary"
          @click="lockIcon = !lockIcon"
        />
      </div>
      <div v-if="lockIcon" class="text-right delete-btn">
        <q-btn
          class="q-mb-md"
          color="negative"
          label="動画を削除する"
          @click="deleteDialog = true"
        />
      </div>
    </div>

    <q-card v-if="!loadState.fetch">
      <q-card-section>
        <div>
          <div style="max-width: 700px; width: 100%">
            <div class="text-subtitle1 q-mb-sm">1. ファイルや内容の入力</div>
            <div class="q-ma-md">
              <q-input
                v-model="movieInfo.title"
                label="タイトル*"
                class="q-mb-lg"
                outlined
                stack-label
                clearable
                @clear="movieInfo.title = ''"
              />
              <q-input
                v-model="movieInfo.detail"
                label="詳細"
                class="q-mb-lg"
                type="textarea"
                outlined
                stack-label
              />
              <q-file
                v-model="pickedFile"
                label="動画を変更する場合、クリック・ドロップして動画を選択してね"
                outlined
                dense
                :clearable="pickedFile?.size != null"
                stack-label
                class="q-mb-lg"
                accept=".mp4, .mov, .webm, .mpg"
              />
              <div v-if="tempVideoUrl">
                <video
                  class="q-mt-sm q-mb-lg"
                  controls
                  :src="tempVideoUrl"
                  style="min-width: 100%; max-width: 600px; width: 100%"
                ></video>
              </div>

              <q-select
                label="投稿者*"
                :options="staffSelect"
                v-model="movieInfo.staff"
                option-value="staffCd"
                option-label="name"
                dense
                stack-label
                readonly
                style="max-width: 200px"
              />
            </div>
          </div>
          <div style="margin-top: 80px; max-width: 700px; width: 100%">
            <div class="text-subtitle1">2. サムネイルはどうする？</div>
            <div class="q-ma-md">
              <div class="row q-gutter-md">
                <q-radio
                  v-model="movieInfo.thumbnailFlg"
                  :val="1"
                  label="自動で作成する"
                />
                <q-radio
                  v-model="movieInfo.thumbnailFlg"
                  :val="0"
                  label="自分で設定する"
                />
              </div>
              <div v-if="movieInfo.thumbnailFlg == 0" class="q-mt-md">
                <q-file
                  v-model="thumbnailFile"
                  label="クリック・ドロップしてサムネイルの画像を選択してね"
                  outlined
                  dense
                  :clearable="thumbnailFile?.size != null"
                  stack-label
                  class="q-mb-lg"
                  accept="image/*"
                />
                <img
                  v-if="tempThumbnailUrl && thumbnailFile"
                  :src="tempThumbnailUrl"
                  class="thumbnail"
                  style="border: 1px rgba(220, 220, 220, 0.7) solid"
                />
                <img
                  v-else
                  :src="thumbnailUrl"
                  class="thumbnail"
                  style="border: 1px rgba(220, 220, 220, 0.7) solid"
                />
              </div>
            </div>
          </div>
          <div style="margin-top: 80px">
            <div class="text-subtitle1">
              3. 既にあるハッシュタグはここから選択してね<span
                class="text-grey q-ml-sm"
                >(省略可能)</span
              >
            </div>
            <div class="text-grey">
              <span class="text-body2"
                ><q-icon name="star" color="yellow" /></span
              >...シリーズ別で表示するタグ
            </div>
            <div class="q-mt-sm q-ma-md">
              <div class="row q-gutter-md">
                <div v-for="tag in movieInfo.hashtags" :key="tag.name">
                  <q-checkbox
                    v-model="tag.check"
                    :label="tag.name"
                    :class="{
                      'text-primary': tag.isGroup,
                    }"
                  />
                  <q-icon
                    name="star"
                    color="yellow"
                    size="sm"
                    v-if="tag.isGroup"
                  />
                </div>
              </div>
            </div>
          </div>
          <div style="margin-top: 80px">
            <div class="text-subtitle1">
              4. 新しくハッシュタグを作る場合は入力してね<span
                class="text-grey q-ml-sm"
                >(省略可能)</span
              >
            </div>
            <div class="q-ma-md">
              <q-form @submit.prevent="onClickHashtag">
                <div class="row">
                  <q-input
                    v-model="hashtagInput"
                    label="ハッシュタグ"
                    style="max-width: 300px"
                    outlined
                    dense
                  />
                  <q-btn
                    class="q-ml-sm"
                    color="primary"
                    label="追加"
                    type="submit"
                    outline
                  />
                </div>
              </q-form>

              <div class="q-mt-sm">
                <q-markup-table
                  separator="cell"
                  style="max-width: 700px"
                  v-if="movieInfo.newHashtags.length > 0"
                >
                  <thead>
                    <tr>
                      <th></th>
                      <th>ハッシュタグ</th>
                      <th>シリーズ別で表示</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="tag in movieInfo.newHashtags" :key="tag.name">
                      <td>
                        <q-icon
                          name="delete"
                          color="negative"
                          size="sm"
                          class="cursor-pointer"
                          @click="
                            movieInfo.newHashtags =
                              movieInfo.newHashtags.filter(
                                (it) => it.name != tag.name
                              )
                          "
                        />
                      </td>
                      <td>
                        {{ tag.name }}
                      </td>
                      <td class="text-center">
                        <q-toggle
                          v-model="tag.isGroup"
                          icon="star"
                          color="yellow"
                        />
                        {{ tag.isGroup ? '表示する' : '表示しない' }}
                      </td>
                    </tr>
                  </tbody>
                </q-markup-table>
              </div>
              <div
                style="max-width: 700px; width: 100%; margin-top: 32px"
                class="text-right"
              >
                <q-btn
                  label="保存"
                  color="primary"
                  push
                  :loading="loadState.update"
                  @click="onUpdaateClick"
                />
              </div>
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
    <q-dialog v-model="deleteDialog">
      <q-card style="max-width: 400px; width: 100%">
        <q-card-section>
          <div class="text-h6">動画の削除確認</div>
          <div class="q-ma-md">
            <div class="text-subtitle1">このページの動画を削除しますか？</div>
          </div>
          <div class="row justify-between">
            <q-btn
              label="キャンセル"
              color="grey-4"
              @click="deleteDialog = false"
            />
            <q-btn
              label="削除する"
              color="negative"
              @click="onDeleteClick"
              :loading="loadState.delete"
            />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import { useMovieEditModel } from 'src/models/MovieEditModels';
import { useRoute, useRouter } from 'vue-router';
import { MovieApi } from 'src/api/file/MovieApi';
export default defineComponent({
  setup() {
    const route = useRoute();
    const router = useRouter();
    const {
      lockIcon,
      staffSelect,
      loadState,
      movieInfo,
      pickedFile,
      thumbnailFile,
      thumbnailUrl,
      getMoieInfo,
      getDefaultStaff,
      setDefaultStaffCd,
      uploadFile,
      updateMovie,
      deleteMovie,
      uploadThumbnail,
    } = useMovieEditModel();
    const onMount = async function () {
      // 初期データ取得
      const id = Number(route.query.id);
      await getMoieInfo(id);

      // 投稿者情報取得
      await getDefaultStaff();

      //
      tempVideoUrl.value = api.thumbnailLink(movieInfo.value.fileName);
      tempVideoUrl.value = api.downloadLink(movieInfo.value.fileName);
    };
    onMount();

    // 動画の再生用
    const api = new MovieApi();
    const tempVideoUrl = ref('');
    watch(pickedFile, () => {
      if (pickedFile.value) {
        tempVideoUrl.value = URL.createObjectURL(pickedFile.value);
        if (movieInfo.value.title == '') {
          movieInfo.value.title = pickedFile.value.name.split('.')[0];
        }
      } else {
        URL.revokeObjectURL(tempVideoUrl.value);
        tempVideoUrl.value = api.thumbnailLink(movieInfo.value.fileName);
      }
    });

    // 手動サムネ
    const tempThumbnailUrl = ref('');
    watch(thumbnailFile, () => {
      if (thumbnailFile.value) {
        tempThumbnailUrl.value = URL.createObjectURL(thumbnailFile.value);
      } else {
        URL.revokeObjectURL(tempThumbnailUrl.value);
        tempThumbnailUrl.value = '';
      }
    });

    // ハッシュタグの入力用
    const hashtagInput = ref('');
    const onClickHashtag = function () {
      // フォームに追加
      movieInfo.value.newHashtags.push({
        name: hashtagInput.value,
        isGroup: false,
        check: true,
      });

      // 入力値のリセット
      hashtagInput.value = '';
    };

    // 更新処理全体
    const onUpdaateClick = async function () {
      loadState.value.update = true;
      if (pickedFile.value) {
        await uploadFile();
      }

      await updateMovie();
      await uploadThumbnail();
      loadState.value.update = false;
    };

    // 削除処理全体
    const onDeleteClick = async function () {
      const result = await deleteMovie();
      if (result) {
        onNavigateTop();
      }
    };

    const onNavigateTop = function () {
      router.push('/movie');
    };
    return {
      lockIcon,
      staffSelect,
      loadState,
      movieInfo,
      pickedFile,
      thumbnailFile,
      tempVideoUrl,
      tempThumbnailUrl,
      hashtagInput,
      thumbnailUrl,
      getMoieInfo,
      getDefaultStaff,
      setDefaultStaffCd,
      onNavigateTop,
      onClickHashtag,
      onUpdaateClick,
      onDeleteClick,
      uploadThumbnail,
      deleteDialog: ref(false),
    };
  },
});
</script>
<style>
@media (max-width: 600px) {
  .delete-btn {
    width: 100%;
  }
}
.thumbnail {
  max-width: 100%;
  width: 100%;
  max-height: 400px;
  height: 100%;
  object-fit: contain;
  cursor: pointer;
}
</style>
