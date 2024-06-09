<template>
  <div class="row q-gutter-xs">
    <div>
      <q-btn
        round
        dense
        icon="edit"
        text-color="secondary"
        @click="modalView = true"
      />
    </div>

    <a
      href="#"
      class="q-pt-sm q-pr-lg image-list-button-text"
      style="text-decoration: none"
      @click.prevent="modalView = true"
      >編集</a
    >
  </div>

  <q-dialog v-model="modalView">
    <q-card class="image-list-update-card">
      <q-card-section class="q-pa-md">
        <div class="text-h6 q-pb-md row justify-between">
          <div class="row q-gutter-xs">
            <div>タイトル・詳細の更新</div>
            <div><q-icon name="edit" /></div>
          </div>
          <div>
            <q-btn
              label="閉じる"
              flat
              color="primary"
              @click="modalView = false"
            />
          </div>
        </div>
        <div class="q-pa-md">
          <q-input v-model="updateState.title" label="タイトル" stack-label />
          <q-input
            v-model="updateState.detail"
            label="詳細"
            stack-label
            type="textarea"
          />
        </div>
        <div style="width: 100%">
          <div style="text-align: right" class="q-pb-sm">
            <q-btn
              label="保存する"
              color="primary"
              :disable="
                state.title == updateState.title &&
                state.detail == updateState.detail
              "
              @click="update"
            />
          </div>
        </div>
        <!--画像-->
        <div class="image-tweet-card-img">
          <img :src="downloadUrl" />
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script lang="ts">
import { defineComponent, PropType, ref } from 'vue';
import api from 'src/api/main/ImageListApi';
import { useQuasar } from 'quasar';
export default defineComponent({
  name: 'image-list-update',
  props: {
    dataState: {
      type: Object as PropType<DataState>,
      required: true,
    },
    downloadUrl: {
      type: String,
    },
  },
  setup(props) {
    const quasar = useQuasar();
    const modalView = ref(false);
    const d = JSON.parse(JSON.stringify(props.dataState)) as DataState;
    const updateState = ref({
      id: d.id,
      title: d.title,
      detail: d.detail,
    } as UpdateState);
    const state = ref(props.dataState);

    const update = async function () {
      await api
        .update(updateState.value)
        .then((response) => {
          if (response) {
            console.log('update', response);
            if (response.success) {
              quasar.notify({
                message: '更新完了！',
                color: 'primary',
                position: 'top',
              });
              state.value.title = updateState.value.title;
              state.value.detail = updateState.value.detail;
              modalView.value = false;
            }
          }
        })
        .catch((e) => console.log('update err', e));
    };
    return { modalView, state, updateState, update };
  },
});

interface DataState {
  id: number;
  fileName: string;
  ext: string;
  title: string;
  detail: string;
  createAt: string;
  updateAt: string;
}
interface UpdateState {
  id: number;
  title: string;
  detail: string;
}
</script>
<style>
.image-list-update-card {
  width: 500px;
  height: 600px;
}
</style>
