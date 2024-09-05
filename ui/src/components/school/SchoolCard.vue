<template>
  <q-card class="q-pa-md" style="max-width: 600px">
    <div class="row">
      <div class="col-9 school-title">
        {{ state.schoolName }}
      </div>
      <div class="col-3 row q-gutter-xs" v-if="editIconDisplay">
        <q-btn icon="edit" color="primary" class="q-mr-md" />
        <q-btn icon="delete" color="negative" />
      </div>
    </div>
    <div class="q-pt-sm school-principal q-pb-sm">
      校長先生：<span>{{ state.principal }}</span>
    </div>
    <hr />
    <div class="q-pa-md" style="overflow-wrap: break-word">
      {{ state.detail }}
    </div>
    <div class="row">
      <q-rating
        v-if="state.avgStar"
        v-model="state.avgStar"
        size="2em"
        :max="5"
        color="yellow-7"
      />
      <div class="q-pt-xs q-pl-sm text-bold" style="font-size: 20px">
        {{ state.avgStar }}
      </div>
    </div>
  </q-card>
</template>
<script lang="ts">
import { computed, defineComponent, PropType, ref } from 'vue';
import { defineEmits } from 'vue';
import api from 'src/api/main/SchoolApi';
import { useQuasar } from 'quasar';

const quasar = useQuasar();
const emit = defineEmits(['updated', 'deleted']);
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
  },
  setup(props) {
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

    const editIconDisplay = computed(() => props.editting);

    const { editDialog, deleteDialog, editSchool, deleteSchool } = apiModel();

    return {
      state,
      editIconDisplay,
      editDialog,
      deleteDialog,
      editSchool,
      deleteSchool,
    };
  },
});
const apiModel = function () {
  const editDialog = ref(false);
  const deleteDialog = ref(false);

  const editSchool = async function (state: School) {
    await api
      .editSchool(state)
      .then((response) => {
        if (response) {
          console.log('update response', response);
          emit('updated');
          quasar.notify({
            color: 'primary',
            position: 'top',
            message: '更新したよ！',
          });
        }
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
        if (response) {
          console.log('delete response', response);
          emit('deleted');
          quasar.notify({
            color: 'primary',
            position: 'top',
            message: '消したよ！',
          });
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
  return {
    editDialog,
    deleteDialog,
    editSchool,
    deleteSchool,
  };
};
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
</script>

<style>
.school-title {
  font-size: 24px;
  color: rgb(102, 163, 224);
}
.school-principal {
  font-size: 16px;
}
</style>
