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
      />ハッシュタグの編集ページ<q-spinner
        class="q-ml-sm"
        v-if="isLoading"
        color="primary"
        size="sm"
      />
      <q-icon
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
    <q-stepper
      header-nav
      class="q-mt-md"
      v-model="formStep"
      color="primary"
      animated
    >
      <q-step :name="1" title="ハッシュタグの編集" header-nav :done="isEdit">
        <q-markup-table separator="cell">
          <thead>
            <tr>
              <th>ハッシュタグ</th>
              <th>変更後のハッシュタグ</th>
              <th>シリーズ別で表示</th>
              <th v-if="lockIcon">削除</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="tag in editHashtag"
              :key="tag.name"
              :class="{
                'bg-blue-1': tag.isDelete ? false : tag.isChanged,
                'bg-red-1': tag.isDelete,
              }"
            >
              <td>
                <div class="text-subtitle1">{{ tag.name }}</div>
              </td>
              <td>
                <q-input
                  v-model="tag.afterName"
                  label="変更後のタグ名"
                  stack-label
                  outlined
                  style="min-width: 200px"
                />
              </td>
              <td>
                <q-toggle v-model="tag.isGroup" icon="star" color="yellow" />
                <span>{{
                  tag.isGroup
                    ? 'シリーズ別で表示する'
                    : 'シリーズ別で表示しない'
                }}</span>
              </td>
              <td v-if="lockIcon">
                <q-checkbox
                  color="negative"
                  v-model="tag.isDelete"
                  label="削除する"
                />
              </td>
            </tr>
          </tbody>
        </q-markup-table>
        <div class="q-mt-md text-right">
          <q-btn
            label="次へ"
            color="primary"
            push
            :disable="!isEdit"
            @click="formStep = 2"
          />
        </div>
      </q-step>
      <q-step :header-nav="isEdit" :name="2" title="編集内容の確認">
        <div id="edit-tags" style="margin-bottom: 40px">
          <div class="text-subtitle1">1. 変更するハッシュタグ</div>
          <div class="text-caption text-grey q-mb-md">
            <q-icon
              name="star"
              color="yellow"
              style="font-size: 18px; position: relative; top: -2px"
            />はシリーズ別で表示されるハッシュタグ
          </div>
          <div class="q-ml-md">
            <div
              v-for="tag in editHashtag.filter((it) => it.isChanged)"
              :key="tag.name"
              class="text-body1"
              style="max-width: 800px"
            >
              <div class="row" v-if="tag.isDelete == false">
                <div class="col">
                  <div class="text-primary">
                    {{ tag.name
                    }}<q-icon
                      name="star"
                      :color="
                        beforeHashtag.find((it) => it.name == tag.name)?.isGroup
                          ? 'yellow'
                          : 'white'
                      "
                      class="q-ml-sm"
                      size="sm"
                    />
                  </div>
                </div>
                <div class="col">
                  <div>
                    <q-icon name="arrow_forward" style="font-size: 28px" />
                  </div>
                </div>
                <div class="col">
                  <div class="text-primary">
                    {{ tag.afterName == '' ? tag.name : tag.afterName
                    }}<q-icon
                      class="q-ml-sm"
                      size="sm"
                      name="star"
                      :color="tag.isGroup ? 'yellow' : 'white'"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div
          id="delete-tags"
          v-if="editHashtag.filter((it) => it.isDelete).length > 0"
        >
          <div class="text-subtitle1 q-mb-md">
            2. 削除するハッシュタグ<q-icon
              class="q-ml-sm"
              name="delete"
              color="negative"
            />
          </div>
          <div class="q-ml-md">
            <div
              v-for="tag in editHashtag.filter((it) => it.isDelete)"
              :key="tag.name"
              class="text-body1"
              style="max-width: 800px"
            >
              ・{{ tag.name }}
            </div>
          </div>
        </div>
        <div class="q-mt-md text-right">
          <q-btn
            label="保存する"
            color="primary"
            push
            :disable="!isEdit"
            @click="updateHashtag"
            :loading="isUpdateLoading"
          />
        </div>
      </q-step>
      <q-step :name="3" title="保存完了">
        <div class="text-subtitle1">コブラのお仕事が完了したよ！</div>
        <img src="../assets/kobura_good.webp" />
      </q-step>
    </q-stepper>
  </q-page>
</template>
<script lang="ts">
import { useQuasar } from 'quasar';
import { MovieApi } from 'src/api/file/MovieApi';
import { computed, defineComponent, ref, watch } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'movie-hashtag-edit-page',
  setup() {
    const router = useRouter();
    const quasar = useQuasar();
    const api = new MovieApi();
    const isLoading = ref(false);
    const lockIcon = ref(false);
    const formStep = ref(1 as 1 | 2 | 3);
    const beforeHashtag = ref([] as MovieHashtag[]);
    const editHashtag = ref([] as MovieHashtag[]);

    const fetchHashtag = async function () {
      isLoading.value = true;
      beforeHashtag.value.splice(0);
      editHashtag.value.splice(0);
      await api
        .hashtagList()
        .then((response) => {
          if (response) {
            response.forEach((it) => {
              beforeHashtag.value.push({
                name: it.name,
                afterName: '',
                isGroup: it.isGroup == 1,
                isChanged: false,
                isDelete: false,
              });
              editHashtag.value.push({
                name: it.name,
                afterName: '',
                isGroup: it.isGroup == 1,
                isChanged: false,
                isDelete: false,
              });
            });
          }
        })
        .catch((err) => {
          console.log('fetch err', err);
          quasar.notify({
            color: 'red',
            position: 'top',
            message: 'ハッシュタグの一覧取得に失敗した...',
          });
        });
      isLoading.value = false;
    };

    const isUpdateLoading = ref(false);
    const updateHashtag = async function () {
      isUpdateLoading.value = true;
      const editTags = editHashtag.value.filter(
        (it) => it.isChanged && it.isDelete == false
      );
      editTags.forEach(async (tag) => {
        const result = await api.createHashtag(tag.name, tag.isGroup);
        console.log('update hashtag', result);

        if (tag.afterName != '') {
          const result = await api.changeHashtagName(tag.name, tag.afterName);
          console.log('change name hashtag', result);
        }
      });

      const deleteTags = editHashtag.value.filter((it) => it.isDelete);
      deleteTags.forEach(async (tag) => {
        const result = await api.deleteHashtag(tag.name);
        console.log('delete hashtag', result);
      });
      fetchHashtag();
      isUpdateLoading.value = false;
      formStep.value = 3;
    };

    const hashtagComputed = computed(() => JSON.stringify(editHashtag.value));
    watch(hashtagComputed, () => {
      editHashtag.value.forEach((after) => {
        const beforeItem = beforeHashtag.value.find(
          (b) => b.name == after.name
        );
        if (beforeItem) {
          if (
            beforeItem.isGroup != after.isGroup ||
            after.afterName != '' ||
            after.isDelete
          ) {
            after.isChanged = true;
          } else {
            after.isChanged = false;
          }
        }
      });
    });

    const onNavigateTop = function () {
      router.push('/movie');
    };

    const isEdit = computed(
      () => editHashtag.value.filter((it) => it.isChanged).length > 0
    );

    const onMount = async function () {
      fetchHashtag();
    };
    onMount();

    return {
      isLoading,
      isUpdateLoading,
      lockIcon,
      formStep,
      beforeHashtag,
      editHashtag,
      isEdit,
      fetchHashtag,
      onNavigateTop,
      updateHashtag,
    };
  },
});
interface MovieHashtag {
  name: string;
  afterName: string;
  isGroup: boolean;
  isChanged: boolean;
  isDelete: boolean;
}
</script>
