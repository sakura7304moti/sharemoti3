<template>
  <q-btn label="開校する" color="primary" icon="add" @click="dialog = true" />
  <q-dialog v-model="dialog">
    <q-card style="min-width: 300px">
      <q-card-section style="max-width: 100%; width: 100%">
        <div class="text-h6 row">
          <div class="col text-left">学校登録画面！</div>
          <div>
            <q-btn
              label="作成する"
              class="col"
              color="primary"
              dense
              @click="createSchol(condition)"
              :disable="condition.schoolName == ''"
            />
          </div>
        </div>
      </q-card-section>
      <q-card-section>
        <q-input
          class="q-mb-md"
          v-model="condition.schoolName"
          label="学校名"
          :rules="[(val) => !!val || '入力必須']"
          dense
          outlined
          type="textarea"
        />
        <q-input
          class="q-mb-md"
          v-model="condition.principal"
          label="校長先生"
          dense
          outlined
          type="textarea"
        />
        <q-input
          v-model="condition.detail"
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
          v-model="condition.slogan"
          label="スローガン"
          dense
          outlined
          type="textarea"
        />
        <div class="text-caption text-grey">スローガンのイメージ</div>
        <school-slogan v-model="condition.slogan" />
      </q-card-section>
      <q-card-actions class="q-pa-md row" align="right">
        <span class="text-caption text-grey q-pr-md">学校名以外は空でもok</span>
        <q-btn
          label="作成する"
          color="primary"
          dense
          @click="createSchol(condition)"
          :disable="condition.schoolName == ''"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import api from 'src/api/main/SchoolApi';
import { useQuasar } from 'quasar';

import SchoolSlogan from 'src/components/school/SchoolSlogan.vue';
export default defineComponent({
  name: 'school-create-btn',
  components: {
    SchoolSlogan,
  },
  setup(_, context) {
    const quasar = useQuasar();
    const dialog = ref(false);
    const condition = ref({
      id: 0,
      schoolName: '',
      principal: '',
      detail: '',
      slogan: '',
      avgStar: null,
    } as School);

    const createSchol = async function (school: School) {
      await api
        .createSchool(school)
        .then((_) => {
          context.emit('created');
          dialog.value = false;
          condition.value = {
            id: 0,
            schoolName: '',
            principal: '',
            detail: '',
            slogan: '',
            avgStar: null,
          };
          quasar.notify({
            color: 'primary',
            position: 'top',
            message: '学校設立！',
          });
        })
        .catch((err) => {
          console.log('create err', err);
          quasar.notify({
            color: 'negative',
            position: 'top',
            message: '学校の作成でエラーになった...',
          });
        });
    };

    return { dialog, condition, createSchol };
  },
});
interface School {
  id: number;
  schoolName: string;
  principal: string;
  detail: string;
  slogan: string;
  avgStar: null | number;
}
</script>
