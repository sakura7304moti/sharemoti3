<template>
  <q-page class="">
    <div
      class="text-h5 q-pb-md"
      style="display: flex; max-width: 600px; width: 100%"
    >
      <div style="width: 40%">学校掲示板</div>
      <div
        class="row wrap"
        style="width: 60%; display: flex; justify-content: flex-end"
      >
        <q-spinner v-if="isLoading" color="primary" class="q-ml-md" />
        <div class="q-pr-sm">
          <create-school-button @created="getSchools" />
        </div>

        <q-toggle
          class="text-subtitle1"
          v-model="editting"
          icon="edit"
          color="primary"
          label="編集の切替"
        />
      </div>
    </div>
    <school-card
      :editting="editting"
      :data-state="sc"
      :detail="false"
      v-for="sc in schools"
      :key="sc.id"
      @updated="getSchools"
      @deleted="getSchools"
      class="q-mt-lg"
    />
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import SchoolCard from 'src/components/school/SchoolCard.vue';
import CreateSchoolButton from 'src/components/school/CreateSchoolButton.vue';
import api from 'src/api/main/SchoolApi';
import { useQuasar } from 'quasar';
import { useRoute, useRouter } from 'vue-router';
const quasar = useQuasar();
export default defineComponent({
  name: 'school-page',
  components: {
    SchoolCard,
    CreateSchoolButton,
  },
  setup() {
    const { isLoading, schools, getSchools } = useSearchModel();
    const editting = ref(false);
    const route = useRoute();

    const scrollScholl = function () {
      const id = route.query.id;
      if (id) {
        const element = document.getElementById('school-card-' + id.toString());
        if (element) {
          element.scrollIntoView({ behavior: 'instant' });
        }
      }
    };

    const onMount = async function () {
      await getSchools();
      scrollScholl();
    };

    onMount();

    return {
      isLoading,
      schools,
      editting,
      getSchools,
    };
  },
});
/**
 * 細かい処理は下へ
 */
function useSearchModel() {
  const isLoading = ref(false);
  const schools = ref([] as SchoolState[]);
  const getSchools = async function () {
    isLoading.value = true;
    await api
      .school()
      .then((response) => {
        if (response) {
          console.log('school', response);
          schools.value.splice(0);
          response.forEach(async (it) => {
            schools.value.push({
              id: it.id,
              schoolName: it.schoolName,
              principal: it.principal,
              detail: it.detail,
              slogan: it.slogan,
              avgStar: it.avgStar,
              createAt: it.createAt,
              updateAt: it.updateAt,
            });
          });
        }
      })
      .catch((err) => {
        console.log('err', err);
        quasar.notify({
          color: 'red',
          position: 'top',
          message: '学校のデータ取得できなかった...',
        });
      });
    isLoading.value = false;
  };

  const getComment = async function (id: number) {
    const response = await api.comment(id);
    return response ?? [];
  };
  return {
    isLoading,
    schools,
    getSchools,
  };
}
/**
 * インターフェース
 */
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
