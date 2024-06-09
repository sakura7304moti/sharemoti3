<template>
  <div class="row q-gutter-xs">
    <div>
      <q-btn
        round
        dense
        icon="delete"
        text-color="negative"
        @click="modalView = true"
      />
    </div>

    <a
      href="#"
      class="q-pt-sm image-list-button-text"
      style="text-decoration: none"
      @click.prevent="modalView = true"
      >削除</a
    >
  </div>

  <q-dialog v-model="modalView">
    <q-card class="image-list-update-card">
      <q-card-section class="q-pa-md">
        <div class="text-h6 q-pb-md row justify-between">
          <div class="row q-gutter-xs">
            <div>削除確認</div>
            <div><q-icon name="delete" /></div>
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
          <q-input
            v-model="state.title"
            label="タイトル"
            stack-label
            readonly
          />
          <q-input
            v-model="state.detail"
            label="詳細"
            stack-label
            type="textarea"
            readonly
          />
        </div>
        <div style="width: 100%">
          <div style="text-align: right" class="q-pb-sm">
            <q-btn label="削除する" color="negative" @click="deleteRecord" />
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
import { defineComponent, PropType, ref, SetupContext } from 'vue';
import api from 'src/api/main/ImageListApi';
import { useQuasar } from 'quasar';
export default defineComponent({
  name: 'image-list-delete',
  props: {
    dataState: {
      type: Object as PropType<DataState>,
      required: true,
    },
    downloadUrl: {
      type: String,
    },
  },
  setup(props, context: SetupContext) {
    const quasar = useQuasar();
    const modalView = ref(false);
    const state = ref(props.dataState);

    const deleteRecord = async function () {
      await api
        .dell({ id: state.value.id })
        .then((response) => {
          if (response) {
            console.log('delete', response);
            if (response.success) {
              quasar.notify({
                message: '画像を消したわよ！',
                color: 'primary',
                position: 'top',
              });
              context.emit('deleted');
              modalView.value = false;
            }
          }
        })
        .catch((e) => console.log('update err', e));
    };
    return { modalView, state, deleteRecord };
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
</script>
<style>
.image-list-update-card {
  width: 500px;
  height: 600px;
}
</style>
