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
      />動画の編集ページ
    </div>
    <q-card class="q-mt-md">
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
                v-model="movieInfo.staff"
                option-value="staffCd"
                option-label="name"
                emit-value
                map-options
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
                <q-btn label="保存" color="primary" push />
              </div>
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
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
      staffSelect,
      loadState,
      movieInfo,
      pickedFile,
      getMoieInfo,
      getDefaultStaff,
      setDefaultStaffCd,
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
        tempVideoUrl.value = '';
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

    const onNavigateTop = function () {
      router.push('/movie');
    };
    return {
      staffSelect,
      loadState,
      movieInfo,
      pickedFile,
      tempVideoUrl,
      hashtagInput,
      getMoieInfo,
      getDefaultStaff,
      setDefaultStaffCd,
      onNavigateTop,
      onClickHashtag,
    };
  },
});
</script>
