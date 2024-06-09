import { QTableColumn, useQuasar } from 'quasar';
import api from 'src/api/file/VoiceListApi';
import { ref } from 'vue';

export function useVoiceListModel() {
  const quasar = useQuasar();
  const filter = ref('');
  const selectId = ref(-1);
  const columns = [
    {
      name: 'fileName',
      label: 'ファイル名',
      field: 'fileName',
      sortable: true,
    },
  ] as QTableColumn[];
  const load = ref({
    search: false,
    download: false,
  } as Loading);
  const records = ref([] as DataState[]);

  const search = async function () {
    load.value.search = true;
    await api
      .search()
      .then((response) => {
        if (response) {
          console.log('search', response);
          records.value.splice(0);
          response.records.forEach((it) => records.value.push(it));
        }
      })

      .catch((e) => {
        console.log(e);

        quasar.notify({
          color: 'red',
          position: 'top',
          message: 'データの取得に失敗しました',
        });
      });
    load.value.search = false;
  };

  return {
    filter,
    columns,
    load,
    records,
    search,
    selectId,
  };
}
interface DataState {
  id: number;
  fileName: string;
}
interface Loading {
  search: boolean;
  download: boolean;
}
