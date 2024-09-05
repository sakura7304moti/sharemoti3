<template>
  <q-btn label="開校する" color="primary" icon="add" />
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import api from 'src/api/main/SchoolApi';
import { useQuasar } from 'quasar';
const quasar = useQuasar();
const emit = defineEmits(['created']);
export default defineComponent({
  name: 'school-create-btn',
  setup() {
    const dialog = ref(false);

    return {};
  },
});
</script>
