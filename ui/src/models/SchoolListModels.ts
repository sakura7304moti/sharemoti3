import { useQuasar } from 'quasar';
import api from 'src/api/main/SchoolListApi';
import { ref } from 'vue';

export function useSchoolListModel() {
  const quasar = useQuasar();
  const modal = ref({
    insert: false,
    delete: false,
  } as ModalCondition);
  const condition = ref({
    search: '',
    insert: '',
    delete: '',
  } as ConditionState);
  const loading = ref({
    search: false,
    insert: false,
    delete: false,
  } as LoadingState);
  const records = ref([] as string[]);

  /*SELECT */
  const search = async function () {
    loading.value.search = true;
    await api
      .search({
        word: condition.value.search,
      })
      .then((res) => {
        if (res) {
          console.log('select', res);
          records.value.splice(0);
          res.records?.forEach((r) => {
            if (r.word) {
              records.value.push(r.word);
            }
          });
          records.value.sort();
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
    loading.value.search = false;
  };

  /*INSERT */
  const insert = async function () {
    if (records.value.includes(condition.value.insert)) {
      quasar.notify({
        color: 'red',
        position: 'top',
        message: '同じ学校がすでに...あるわよ！',
      });
    } else {
      loading.value.insert = true;
      await api
        .save({
          word: condition.value.insert.replace(/\n/g, ''),
        })
        .then((res) => {
          if (res) {
            console.log('insert', res);
            records.value.push(condition.value.insert);
            records.value.sort();
            condition.value.insert = '';
            quasar.notify({
              color: 'blue',
              position: 'top',
              message: '新しい学校が...出るわよ！',
            });
          }
        })
        .catch((e) => {
          console.log(e);

          quasar.notify({
            color: 'red',
            position: 'top',
            message: 'データの追加に失敗しました',
          });
        });
    }
    loading.value.insert = false;
  };

  /*DELETE */
  const deleteRec = async function () {
    await api
      .delete({
        word: condition.value.delete,
      })
      .then((res) => {
        if (res) {
          console.log('delete', res);
          if (res.status) {
            quasar.notify({
              color: 'blue',
              position: 'top',
              message: '削除完了しました',
            });
            const index = records.value.findIndex(
              (it) => it == condition.value.delete
            );
            records.value.splice(index, 1);
            modal.value.delete = false;
          } else {
            quasar.notify({
              color: 'red',
              position: 'top',
              message: 'データの削除に失敗しました',
            });
          }
        }
      })
      .catch((e) => {
        console.log(e);

        quasar.notify({
          color: 'red',
          position: 'top',
          message: 'データの削除に失敗しました',
        });
      });
    modal.value.delete = false;
  };

  return {
    loading,
    modal,
    condition,
    records,
    search,
    insert,
    deleteRec,
  };
}

interface ModalCondition {
  insert: boolean;
  delete: boolean;
}

interface ConditionState {
  search: string;
  insert: string;
  delete: string;
}

interface LoadingState {
  search: boolean;
  insert: boolean;
  delete: boolean;
}
