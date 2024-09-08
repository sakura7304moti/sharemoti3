<template>
  <q-card
    class="q-pa-md"
    :class="{
      'bg-grey-4': editDialog || deleteDialog,
    }"
    style="max-width: 600px; margin-bottom: 24px"
  >
    <div class="row">
      <div
        class="school-title"
        :class="{
          'col-8': editIconDisplay,
        }"
      >
        {{ state.schoolName }}
      </div>
      <div class="col-4 row" v-if="editIconDisplay">
        <div class="col text-right">
          <q-btn
            icon="edit"
            color="primary"
            class="q-mr-md"
            @click="editDalogOpen"
            label="編集"
            dense
          />
        </div>

        <div class="col text-right">
          <q-btn
            icon="delete"
            color="negative"
            @click="deleteDialog = true"
            label="削除"
            dense
          />
        </div>
      </div>
    </div>
    <div class="q-pt-sm school-principal q-pb-sm" v-if="state.principal">
      校長先生：<span>{{ state.principal }}</span>
    </div>
    <hr />
    <school-slogan v-if="state.slogan" v-model="state.slogan" />

    <div class="q-pa-md" style="white-space: pre-wrap; word-wrap: break-word">
      {{ state.detail }}
    </div>
    <div class="row">
      <q-rating
        v-if="state.avgStar"
        v-model="state.avgStar"
        size="2em"
        :max="5"
        color="yellow-7"
        readonly
      />
      <div class="q-pt-xs q-pl-sm text-bold" style="font-size: 20px">
        {{ state.avgStar }}
      </div>
    </div>
    <div class="q-pt-sm">
      <q-btn
        icon-right="chat"
        label="コメントを見る"
        color="primary"
        dense
        @click="navigateDetail"
        v-if="!commentView"
      />
    </div>

    <!--コメント欄 表示モードのときだけ表示させる-->
    <div style="padding-top: 32px" v-if="commentView">
      <div class="q-pb-sm">
        <div>コメント：{{ comments.length }}件</div>
        <div class="q-py-md">
          <q-card>
            <q-card-section>
              <div class="row justify-between">
                <div class="text-h6">コメント作成</div>
                <div>
                  <q-icon
                    name="info"
                    size="sm"
                    color="primary"
                    class="cursor-pointer"
                  >
                    <q-tooltip class="text-body2">
                      ここからコメント書いてね！コメントだけ必須よ
                    </q-tooltip></q-icon
                  >
                </div>
              </div>

              <div class="q-pt-sm">
                <q-input
                  v-model="commentCreateState.comment"
                  type="textarea"
                  label="コメント内容"
                  outlined
                  dense
                />
              </div>
              <div class="q-pt-sm">
                <q-input
                  v-model="commentCreateState.postPerson"
                  label="投稿者"
                  outlined
                  dense
                />
              </div>
              <div class="q-pt-sm">
                <span class="q-pr-sm">学校の評価</span>
                <q-rating
                  v-model="commentCreateState.star"
                  size="2em"
                  :max="5"
                  color="yellow-7"
                />
              </div>
              <div class="q-pt-sm text-right">
                <div>
                  <q-btn
                    label="作成する"
                    color="primary"
                    :disable="commentCreateState.comment == ''"
                    @click="createComment()"
                  />
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
      <div v-for="cm in comments" :key="cm.id" class="q-pl-sm q-pb-md">
        <q-chat-message
          :stamp="cm.updateAt.split(' ')[0]"
          :name="cm.postPerson"
        >
          <div style="white-space: pre-wrap; word-wrap: break-word">
            <div class="q-pb-xs">
              <q-rating
                v-model="cm.star"
                size="1.5em"
                :max="5"
                color="yellow-7"
                readonly
                v-if="(cm.star ?? 0) > 0"
              />
            </div>
            <div>
              {{ cm.comment }}
            </div>
            <div v-if="editIconDisplay" class="row justify-evenly">
              <div class="col">
                <q-btn
                  icon="edit"
                  dense
                  flat
                  color="primary"
                  @click="selectComment(cm)"
                />
              </div>
              <div class="col">
                <q-btn
                  icon="delete"
                  dense
                  flat
                  color="negative"
                  @click="selectDeleteComment(cm.id)"
                />
              </div>
            </div>
            <div v-if="commentDeleteId == cm.id && commentDeleteDialog">
              <q-chip>選択中...</q-chip>
            </div>
          </div>
        </q-chat-message>
      </div>
    </div>
  </q-card>

  <!--学校編集ダイアログ-->
  <q-dialog v-model="editDialog">
    <q-card style="min-width: 300px">
      <q-card-section style="max-width: 100%; width: 100%">
        <div class="q-pb-sm">
          <q-btn
            label="キャンセル"
            icon="close"
            class="col"
            dense
            @click="editDialog = false"
          />
        </div>

        <div class="text-h6 row">
          <div class="col text-left">学校編集画面！</div>
          <div>
            <q-btn
              label="変更を保存する"
              class="col"
              color="primary"
              dense
              :disable="editState.schoolName == ''"
              @click="editSchool(editState)"
            />
          </div>
        </div>
      </q-card-section>
      <q-card-section>
        <q-input
          class="q-mb-md"
          v-model="editState.schoolName"
          label="学校名"
          :rules="[(val) => !!val || '入力必須']"
          dense
          outlined
          type="textarea"
        />
        <q-input
          class="q-mb-md"
          v-model="editState.principal"
          label="校長先生"
          dense
          outlined
          type="textarea"
        />
        <q-input
          v-model="editState.detail"
          label="説明書き"
          dense
          outlined
          type="textarea"
        />
      </q-card-section>
      <div class="q-pa-md">
        <hr />
      </div>

      <q-card-section>
        <q-input
          v-model="editState.slogan"
          label="スローガン"
          dense
          outlined
          type="textarea"
        />
        <div class="text-caption text-grey">スローガンのイメージ</div>
        <school-slogan v-model="editState.slogan" />
      </q-card-section>
      <q-card-actions class="q-pa-md row" align="right">
        <span class="text-caption text-grey q-pr-md">学校名以外は空でもok</span>
        <q-btn
          label="変更を保存する"
          color="primary"
          dense
          :disable="editState.schoolName == ''"
          @click="editSchool(editState)"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <!--学校削除ダイアログ-->
  <q-dialog v-model="deleteDialog">
    <q-card style="min-width: 300px">
      <q-card-section>
        <div class="text-h6">削除確認</div>
        <hr />
      </q-card-section>
      <q-card-section class="q-mx-md">
        <div class="text-subtitle1">次の学校を取り壊す？</div>
        <q-field label="学校名" class="q-pt-sm" stack-label filled readonly>
          {{ state.schoolName }}
        </q-field>
      </q-card-section>
      <div class="q-mx-md">
        <hr />
      </div>

      <q-card-actions class="q-mb-md q-mx-sm">
        <div class="row justify-between" style="max-width: 100%; width: 100%">
          <div class="col text-left">
            <q-btn label="キャンセル" @click="deleteDialog = false" dense />
          </div>
          <div class="col text-right">
            <q-btn
              color="negative"
              label="削除する"
              @click="deleteSchool(state.id)"
              dense
            />
          </div>
        </div>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <!--コメント編集ダイアログ-->
  <q-dialog v-model="commentEditDialog">
    <q-card style="min-width: 300px; max-width: 600px; width: 100%">
      <q-card-section>
        <div class="row justify-between">
          <div class="text-h6">コメント編集</div>
          <div>
            <q-icon
              name="info"
              size="sm"
              color="primary"
              class="cursor-pointer"
            >
              <q-tooltip class="text-body2">
                コメントだけ必須よ
              </q-tooltip></q-icon
            >
          </div>
        </div>

        <div class="q-pt-sm">
          <q-input
            v-model="commentEditState.comment"
            type="textarea"
            label="コメント内容"
            outlined
            dense
          />
        </div>
        <div class="q-pt-sm">
          <q-input
            v-model="commentEditState.postPerson"
            label="投稿者"
            outlined
            dense
          />
        </div>
        <div class="q-pt-sm">
          <span class="q-pr-sm">学校の評価</span>
          <q-rating
            v-model="commentEditState.star"
            size="2em"
            :max="5"
            color="yellow-7"
          />
        </div>
        <div class="q-pt-sm text-right">
          <div>
            <q-btn
              label="保存する"
              color="primary"
              :disable="commentEditState.comment == ''"
              @click="editComment()"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>

  <!--コメント削除ダイアログ-->
  <q-dialog v-model="commentDeleteDialog">
    <q-card style="min-width: 300px">
      <q-card-section>
        <div class="text-h6">削除確認</div>
        <hr />
      </q-card-section>
      <q-card-section class="q-mx-md">
        <div class="text-subtitle1">次のコメントを消す？</div>
        <q-field
          label="コメント"
          class="q-pt-sm"
          stack-label
          filled
          readonly
          type="textarea"
          v-if="comments.find((it) => it.id == commentDeleteId)"
        >
          {{ comments.find((it) => it.id == commentDeleteId)?.comment }}
        </q-field>
        <div class="text-grey text-caption">
          {{ comments.find((it) => it.id == commentDeleteId)?.postPerson }}
        </div>
      </q-card-section>
      <div class="q-mx-md">
        <hr />
      </div>

      <q-card-actions class="q-mb-md q-mx-sm">
        <div class="row justify-between" style="max-width: 100%; width: 100%">
          <div class="col text-left">
            <q-btn
              label="キャンセル"
              @click="commentDeleteDialog = false"
              dense
            />
          </div>
          <div class="col text-right">
            <q-btn
              color="negative"
              label="削除する"
              @click="deleteComment(commentDeleteId)"
              dense
            />
          </div>
        </div>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>
<script lang="ts">
import { computed, defineComponent, PropType, ref, watch } from 'vue';
import api from 'src/api/main/SchoolApi';
import { useQuasar } from 'quasar';
import SchoolSlogan from './SchoolSlogan.vue';
import { useRouter } from 'vue-router';
export default defineComponent({
  name: 'school-card',
  props: {
    dataState: {
      type: Object as PropType<SchoolState>,
      required: true,
    },
    editting: {
      type: Boolean,
      required: true,
    },
    detail: {
      type: Boolean,
      required: true,
      default: false,
    },
  },
  components: { SchoolSlogan },
  setup(props, context) {
    const quasar = useQuasar();
    const router = useRouter();
    const commentView = computed(() => props.detail);
    const state = ref({
      id: props.dataState.id,
      schoolName: props.dataState.schoolName,
      principal: props.dataState.principal,
      detail: props.dataState.detail,
      slogan: props.dataState.slogan,
      avgStar: props.dataState.avgStar,
      createAt: props.dataState.createAt,
      updateAt: props.dataState.updateAt,
    } as SchoolState);

    const editState = ref({
      id: props.dataState.id,
      schoolName: props.dataState.schoolName,
      principal: props.dataState.principal,
      detail: props.dataState.detail,
      slogan: props.dataState.slogan,
      avgStar: props.dataState.avgStar,
      createAt: props.dataState.createAt,
      updateAt: props.dataState.updateAt,
    } as SchoolState);

    const commentCreateState = ref({
      id: 0, //ここは未使用。API側でもチェックしてない
      schoolId: props.dataState.id,
      star: 0,
      comment: '',
      title: '',
      postPerson: '',
    } as SchoolComment);

    const commentEditState = ref({
      id: 0, //ここは未使用。API側でもチェックしてない
      schoolId: props.dataState.id,
      star: 0,
      comment: '',
      title: '',
      postPerson: '',
    } as SchoolComment);

    const comments = ref([] as SchoolCommentState[]);

    watch(props, () => {
      state.value = {
        id: props.dataState.id,
        schoolName: props.dataState.schoolName,
        principal: props.dataState.principal,
        detail: props.dataState.detail,
        slogan: props.dataState.slogan,
        avgStar: props.dataState.avgStar,
        createAt: props.dataState.createAt,
        updateAt: props.dataState.updateAt,
      };

      editState.value = {
        id: props.dataState.id,
        schoolName: props.dataState.schoolName,
        principal: props.dataState.principal,
        detail: props.dataState.detail,
        slogan: props.dataState.slogan,
        avgStar: props.dataState.avgStar,
        createAt: props.dataState.createAt,
        updateAt: props.dataState.updateAt,
      };
    });

    const editIconDisplay = computed(() => props.editting);

    const editDialog = ref(false);
    const deleteDialog = ref(false);
    const commentEditDialog = ref(false);
    const commentDeleteDialog = ref(false);
    const commentDeleteId = ref(0);

    const editDalogOpen = function () {
      /**
       * 編集ダイアログを開く
       * このとき入力欄を初期値に初期化
       */
      editState.value = {
        id: props.dataState.id,
        schoolName: props.dataState.schoolName,
        principal: props.dataState.principal,
        detail: props.dataState.detail,
        slogan: props.dataState.slogan,
        avgStar: props.dataState.avgStar,
        createAt: props.dataState.createAt,
        updateAt: props.dataState.updateAt,
      };
      editDialog.value = true;
    };

    const navigateDetail = function () {
      router.push({
        path: '/school/' + props.dataState.id,
      });
    };

    const editSchool = async function (state: School) {
      await api
        .editSchool(state)
        .then((response) => {
          console.log('update response', response);
          context.emit('updated');
          quasar.notify({
            color: 'primary',
            position: 'top',
            message: '更新したよ！',
          });
          editDialog.value = false;
        })
        .catch((err) => {
          console.log('update err', err);
          quasar.notify({
            color: 'red',
            position: 'top',
            message: '更新でエラーになった...',
          });
        });
    };

    const deleteSchool = async function (id: number) {
      await api
        .deleteSchool(id)
        .then((response) => {
          console.log('delete response', response);
          context.emit('deleted');
          quasar.notify({
            color: 'primary',
            position: 'top',
            message: '消したよ！',
          });
        })
        .catch((err) => {
          console.log('delete err', err);
          quasar.notify({
            color: 'red',
            position: 'top',
            message: '削除でエラーになった...',
          });
        });
    };

    const getComments = async function (id: number) {
      await api
        .comment(id)
        .then((response) => {
          if (response) {
            console.log('comment response', response);
            comments.value.splice(0);
            response.forEach((it) => comments.value.push(it));
          }
        })
        .catch((err) => {
          console.log('delete err', err);
          quasar.notify({
            color: 'red',
            position: 'top',
            message: '削除でエラーになった...',
          });
        });
    };

    const createComment = async function () {
      await api
        .createComment(commentCreateState.value)
        .then((response) => {
          console.log('create comment', response);
          getComments(props.dataState.id);
          commentCreateState.value = {
            id: 0, //ここは未使用。API側でもチェックしてない
            schoolId: props.dataState.id,
            star: 0,
            comment: '',
            title: '',
            postPerson: '',
          };
          quasar.notify({
            color: 'primary',
            position: 'top',
            message: 'コメント追加した！',
          });
        })
        .catch((err) => {
          console.log('delete err', err);
          quasar.notify({
            color: 'red',
            position: 'top',
            message: 'コメント追加でエラーになった...',
          });
        });
    };

    const editComment = async function () {
      await api
        .editComment(commentEditState.value)
        .then((response) => {
          console.log('edit comment', response);
          getComments(props.dataState.id);
          commentCreateState.value = {
            id: 0,
            schoolId: props.dataState.id,
            star: 0,
            comment: '',
            title: '',
            postPerson: '',
          };
          commentEditDialog.value = false;
          quasar.notify({
            color: 'primary',
            position: 'top',
            message: '更新した！',
          });
        })
        .catch((err) => {
          console.log('delete err', err);
          quasar.notify({
            color: 'red',
            position: 'top',
            message: 'コメント更新でエラーになった...',
          });
        });
    };

    const deleteComment = async function (id: number) {
      await api
        .deleteComment(id)
        .then((response) => {
          console.log('delete comment', response);
          getComments(props.dataState.id);
          commentDeleteDialog.value = false;
          quasar.notify({
            color: 'primary',
            position: 'top',
            message: '削除した！',
          });
        })
        .catch((err) => {
          console.log('delete err', err);
          quasar.notify({
            color: 'red',
            position: 'top',
            message: 'コメント削除でエラーになった...',
          });
        });
    };

    const selectComment = function (com: SchoolCommentState) {
      commentEditState.value = {
        id: com.id,
        schoolId: com.schoolId,
        star: com.star,
        title: '',
        comment: com.comment,
        postPerson: com.postPerson,
      };
      commentEditDialog.value = true;
    };

    const selectDeleteComment = function (id: number) {
      commentDeleteId.value = id;
      commentDeleteDialog.value = true;
    };
    /**初期化処理 */
    getComments(props.dataState.id);

    watch(props, () => {
      getComments(props.dataState.id);
    });
    return {
      state,
      comments,
      editState,
      commentCreateState,
      commentEditState,
      commentDeleteId,
      editIconDisplay,
      editDialog,
      deleteDialog,
      commentEditDialog,
      commentDeleteDialog,
      editDalogOpen,
      editSchool,
      deleteSchool,
      createComment,
      editComment,
      deleteComment,
      selectComment,
      selectDeleteComment,
      commentView,
      navigateDetail,
    };
  },
});
interface SchoolState extends School {
  createAt: string;
  updateAt: string;
}

interface School {
  id: number;
  schoolName: string;
  principal: string;
  detail: string;
  slogan: string;
  avgStar: null | number;
}
interface SchoolCommentState extends SchoolComment {
  createAt: string;
  updateAt: string;
}

interface SchoolComment {
  id: number;
  schoolId: number;
  star: number;
  title: string;
  comment: string;
  postPerson: string;
}
</script>

<style>
.school-title {
  font-size: 24px;
  color: rgb(51, 51, 51);
}
.school-principal {
  font-size: 16px;
}
</style>
