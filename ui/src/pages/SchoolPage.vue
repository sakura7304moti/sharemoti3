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

    <div class="row wrap">
      <div
        class="row q-gutter-sm q-mr-md"
        style="
          max-width: 300px;
          width: 100%;
          background-color: rgb(226, 220, 202);
          margin-bottom: 16px;
          border-radius: 20px;
        "
      >
        <div class="q-pl-sm text-subtitle1">並び順</div>
        <div>
          <q-radio
            v-model="sortType"
            val="name"
            label="名前順"
            @update:model-value="sortSchools"
          />
        </div>
        <div>
          <q-radio
            v-model="sortType"
            val="date"
            label="開講日順"
            @update:model-value="sortSchools"
          />
        </div>
      </div>
      <div
        style="
          max-width: 300px;
          width: 100%;
          background-color: rgb(226, 220, 202);
          margin-bottom: 16px;
          border-radius: 20px;
        "
      >
        <q-toggle v-model="commentDisplay" label="コメントの表示" />
      </div>
    </div>

    <school-card
      :editting="editting"
      :data-state="sc"
      :detail="false"
      :comment="commentDisplay"
      v-for="sc in schools"
      :key="sc.id"
      @updated="getSchools"
      @deleted="getSchools"
      class="q-mt-lg"
    />
  </q-page>
</template>
<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import SchoolCard from 'src/components/school/SchoolCard.vue';
import CreateSchoolButton from 'src/components/school/CreateSChoolButton.vue';
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
    const {
      isLoading,
      schools,
      getSchools,
      sortType,
      sortSchools,
      commentDisplay,
    } = useSearchModel();
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
      sortType,
      sortSchools,
      commentDisplay,
    };
  },
});
/**
 * 細かい処理は下へ
 */
function useSearchModel() {
  const isLoading = ref(false);
  const sortType = ref('name');
  const commentDisplay = ref(false);
  const sortSchools = function () {
    if (sortType.value == 'name') {
      schools.value.sort((a, b) => (a.schoolName > b.schoolName ? 1 : -1));
    }
    if (sortType.value == 'date') {
      schools.value.sort((a, b) => (a.createAt < b.createAt ? 1 : -1));
    }
  };
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
          sortSchools();
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
    sortType,
    sortSchools,
    commentDisplay,
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
