<template>
  <q-page class="">
    <!--ヘッダーPC用-->
    <div id="school-detail-head">
      <div class="row justify-between" style="max-width: 600px">
        <div class="text-h6 q-pb-md">
          <span class="q-mr-md"
            ><q-btn
              icon="undo"
              label=" 学校に帰る"
              color="primary"
              dense
              @click="navigateSchool"
          /></span>
          学校掲示板のコメント
        </div>
        <div>
          <q-toggle
            class="text-subtitle1"
            v-model="editting"
            icon="edit"
            color="primary"
            label="編集の切替"
          />
        </div>
      </div>
    </div>

    <!--ヘッダーモバイル用-->
    <div id="school-detail-head-mobile">
      <div style="max-width: 600px">
        <div class="text-h6 q-pb-md">学校掲示板のコメント</div>
      </div>
      <div class="row justify-between">
        <div class="q-mr-md">
          <q-btn
            icon="undo"
            label=" 学校に帰る"
            color="primary"
            dense
            @click="navigateSchool"
          />
        </div>
        <div>
          <q-toggle
            class="text-subtitle1"
            v-model="editting"
            icon="edit"
            color="primary"
            label="編集の切替"
          />
        </div>
      </div>
    </div>

    <school-card
      :data-state="school"
      :editting="editting"
      :detail="true"
      @updated="
        getSchool();
        editting = false;
      "
      @deleted="navigateSchool"
    />

    <div class="q-pt-md text-right" style="max-width: 600px">
      <q-toggle
        class="text-subtitle1"
        v-model="editting"
        icon="edit"
        color="primary"
        label="編集の切替"
      />
    </div>
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import SchoolCard from 'src/components/school/SchoolCard.vue';
import { useQuasar } from 'quasar';
import api from 'src/api/main/SchoolApi';
import { useRouter } from 'vue-router';
export default defineComponent({
  name: 'school-page-detail',
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  components: {
    SchoolCard,
  },
  setup(props) {
    const quasar = useQuasar();
    const router = useRouter();
    const editting = ref(false);
    const school = ref({
      id: props.id,
      schoolName: '',
      principal: '',
      detail: '',
      slogan: '',
      avgStar: null,
      createAt: '',
      updateAt: '',
    } as SchoolState);
    const comments = ref([] as SchoolCommentState[]);

    const getSchool = async function () {
      await api
        .school()
        .then((response) => {
          if (response) {
            console.log('school response', response);
            const findResult = response.find((it) => it.id == props.id);
            if (findResult) {
              school.value = {
                id: props.id,
                schoolName: findResult.schoolName,
                principal: findResult.principal,
                detail: findResult.detail,
                slogan: findResult.slogan,
                avgStar: findResult.avgStar,
                createAt: findResult.createAt,
                updateAt: findResult.updateAt,
              };
            }
          }
        })
        .catch((err) => {
          console.log('schol err', err);
          quasar.notify({
            color: 'red',
            position: 'top',
            message: '学校の取得でエラーになった...',
          });
        });
    };

    const navigateSchool = function () {
      router.push({
        path: '/school',
        query: {
          id: school.value.id,
        },
      });
    };

    /**初期化処理 */
    getSchool();
    return {
      editting,
      school,
      navigateSchool,
      getSchool,
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
@media (max-width: 520px) {
  #school-detail-head {
    display: none;
  }
}
@media (min-width: 520px) {
  #school-detail-head-mobile {
    display: none;
  }
}
</style>
