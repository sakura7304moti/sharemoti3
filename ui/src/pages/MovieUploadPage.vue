<template>
  <q-page class="">
    <div class="text-h6">
      <q-btn
        class="q-mr-md q-mb-xs"
        @click="onNavigateTop"
        label="一覧に戻る"
        color="primary"
        icon="arrow_back"
        dense
      />動画アップロードページ
    </div>
    <q-stepper v-model="formStep" header-nav color="primary" animated>
      <q-step
        :name="1"
        title="動画のアップロード・入力"
        :done="createForm.title != '' && pickedFile != null"
      >
        <q-stepper-navigation>
          <div style="max-width: 700px; width: 100%">
            <div class="text-subtitle1 q-mb-sm">1. ファイルや内容の入力</div>
            <div class="q-ma-md">
              <q-input
                v-model="createForm.title"
                label="タイトル*"
                class="q-mb-lg"
                outlined
                stack-label
                clearable
                @clear="createForm.title = ''"
              />
              <q-input
                v-model="createForm.detail"
                label="詳細"
                class="q-mb-lg"
                type="textarea"
                outlined
                stack-label
              />
              <q-file
                v-model="pickedFile"
                :url="uploadUrl"
                label="クリック・ドロップして動画を選択してね*"
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
                v-model="createForm.staff"
                option-value="name"
                option-label="name"
                map-options
                emit-value
                dense
                stack-label
                style="max-width: 200px"
              />
            </div>
          </div>
          <div style="margin-top: 80px">
            <div class="text-subtitle1">
              2. 既にあるハッシュタグはここから選択してね<span
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
                <div v-for="tag in createForm.hashtags" :key="tag.name">
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
              3. 新しくハッシュタグを作る場合は入力してね<span
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
                  v-if="createForm.newHashtags.length > 0"
                >
                  <thead>
                    <tr>
                      <th></th>
                      <th>ハッシュタグ</th>
                      <th>シリーズ別で表示</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="tag in createForm.newHashtags" :key="tag.name">
                      <td>
                        <q-icon
                          name="delete"
                          color="negative"
                          size="sm"
                          class="cursor-pointer"
                          @click="
                            createForm.newHashtags =
                              createForm.newHashtags.filter(
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
                  label="次へ"
                  color="primary"
                  push
                  @click="nextCheckStep()"
                />
              </div>
            </div>
          </div>
        </q-stepper-navigation>
      </q-step>
      <q-step :name="2" title="内容確認">
        <q-stepper-navigation>
          <div style="max-width: 700px; width: 100%">
            <div class="text-subtitle1">
              確認してね！<span class="q-ml-md"
                >でも後から全項目編集できるのよ</span
              >
            </div>
            <div class="q-ma-md">
              <q-input
                v-model="createForm.title"
                label="タイトル"
                readonly
                class="q-mb-lg"
              />
              <q-input
                v-model="createForm.detail"
                label="詳細"
                class="q-mb-lg"
                type="textarea"
                readonly
                stack-label
              />
              <video
                class="q-mt-sm q-mb-lg"
                controls
                :src="tempVideoUrl"
                style="min-width: 100%; max-width: 600px; width: 100%"
              ></video>
              <q-select
                label="投稿者*"
                :options="staffSelect"
                v-model="createForm.staff"
                option-value="name"
                option-label="name"
                map-options
                emit-value
                dense
                readonly
                style="max-width: 200px"
              />
            </div>
            <div
              class="text-subtitle1"
              style="margin-top: 80px"
              v-if="
                createForm.hashtags.filter((it) => it.check).length > 0 ||
                createForm.newHashtags.length > 0
              "
            >
              動画のハッシュタグ
            </div>
            <div class="q-mt-lg">
              <q-markup-table
                separator="cell"
                style="max-width: 700px"
                v-if="createForm.newHashtags.length > 0"
              >
                <thead>
                  <tr>
                    <th></th>
                    <th>ハッシュタグ</th>
                    <th>シリーズ別で表示</th>
                  </tr>
                </thead>
                <tbody>
                  <template
                    v-for="(tags, idx) in [
                      createForm.hashtags.filter((it) => it.check),
                      createForm.newHashtags,
                    ]"
                    :key="idx"
                  >
                    <tr v-for="tag in tags" :key="tag.name">
                      <td class="text-primary text-bold">
                        <div
                          v-if="
                            createForm.newHashtags.find(
                              (it) => it.name == tag.name
                            )
                          "
                        >
                          NEW!
                        </div>
                      </td>
                      <td>
                        {{ tag.name }}
                      </td>
                      <td class="text-center">
                        {{ tag.isGroup ? '表示する' : '表示しない' }}
                      </td>
                    </tr>
                  </template>
                </tbody>
              </q-markup-table>
              <div
                style="max-width: 700px; width: 100%; margin-top: 32px"
                class="text-right"
              >
                <q-btn
                  label="動画をアップロードする！"
                  color="primary"
                  push
                  icon="upload"
                  @click="upload()"
                  :loading="isLoading"
                />
              </div>
            </div>
          </div>
        </q-stepper-navigation>
      </q-step>
      <q-step :name="3" title="アップロード完了">
        <q-stepper-navigation>
          <div class="text-subtitle1">
            <div style="margin-bottom: 40px">アップロード完了！</div>
            <img
              class="q-mt-sm thumbnail image"
              :src="thumbnailUrl"
              v-if="createForm.fileName"
            />

            <div style="margin-bottom: 20px">
              <div class="q-mb-sm">一覧のページに戻るにはこっち</div>
              <div class="text-body2 q-ml-md">
                <q-btn
                  label="動画のページへ"
                  color="primary"
                  push
                  icon="movie"
                  @click="onNavigateTop"
                />
              </div>
            </div>
            <div>
              <div class="q-mb-sm">
                続けて他の動画もアップロードするならこっち
              </div>
              <div class="text-body2 q-ml-md">
                <q-btn
                  label="登録画面へ"
                  color="primary"
                  push
                  icon="create"
                  @click="resetFormClick"
                />
              </div>
            </div>
          </div>
        </q-stepper-navigation>
      </q-step>
    </q-stepper>
  </q-page>
</template>
<script lang="ts">
import { useQuasar } from 'quasar';
import { useMovieUploadModels } from 'src/models/MovieUploadModels';
import { computed, defineComponent, ref, watch } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'movie-upload-page',
  setup() {
    const quasar = useQuasar();
    const router = useRouter();
    const {
      uploadUrl,
      isUploading,
      isHashtagLoading,
      isCreateLoading,
      pickedFile,
      createForm,
      formStep,
      staffSelect,
      thumbnailUrl,
      uploadFile,
      createMovie,
      getHashtagList,
      getDefaultStaff,
    } = useMovieUploadModels();
    // 初期化処理
    getDefaultStaff();
    getHashtagList();

    // 動画の再生用
    const tempVideoUrl = ref('');
    watch(pickedFile, () => {
      if (pickedFile.value) {
        tempVideoUrl.value = URL.createObjectURL(pickedFile.value);
        if (createForm.value.title == '') {
          createForm.value.title = pickedFile.value.name.split('.')[0];
        }
      } else {
        URL.revokeObjectURL(tempVideoUrl.value);
        tempVideoUrl.value = '';
      }
    });

    // ハッシュタグの入力用
    const hashtagInput = ref('');
    const onClickHashtag = function () {
      // フォームに追加
      createForm.value.newHashtags.push({
        name: hashtagInput.value,
        isGroup: false,
        check: true,
      });

      // 入力値のリセット
      hashtagInput.value = '';
    };

    // バリテーション
    const nextCheckStep = async function () {
      if (createForm.value.title == '' || pickedFile.value == null) {
        quasar.notify({
          color: 'red',
          position: 'top',
          message: 'タイトルとファイルが未入力！',
        });
        return;
      }
      formStep.value = 2;
    };

    // アップロード処理
    const isLoading = computed(
      () => isUploading.value || isCreateLoading.value
    );
    const upload = async function () {
      await uploadFile();
      if (createForm.value.fileName) {
        await createMovie();
      } else {
        console.log('upload err...');
      }
    };

    // 最後のボタン二種
    const resetFormClick = async function () {
      // 値のリセットしてタグを再取得
      createForm.value.title = '';
      createForm.value.detail = '';
      createForm.value.fileName = '';
      createForm.value.newHashtags.splice(0);
      pickedFile.value = null;
      await getHashtagList();

      // フォーム画面の遷移
      formStep.value = 1;
    };

    const onNavigateTop = function () {
      router.push('/movie');
    };
    return {
      uploadUrl,
      isUploading,
      isHashtagLoading,
      isCreateLoading,
      pickedFile,
      createForm,
      formStep,
      staffSelect,
      thumbnailUrl,
      uploadFile,
      createMovie,
      getHashtagList,
      getDefaultStaff,
      // 動画再生用URL
      tempVideoUrl,
      // ハッシュタグの入力用
      hashtagInput,
      onClickHashtag,
      // フォームのバリテーション用
      nextCheckStep,
      // アップロードの処理
      isLoading,
      upload,
      // 最後の画面のボタン
      resetFormClick,
      onNavigateTop,
    };
  },
});
</script>
<style>
.thumbnail {
  max-width: 100%;
  width: 100%;
  max-height: 400px;
  height: 100%;
  object-fit: contain;
  cursor: pointer;
}
</style>
