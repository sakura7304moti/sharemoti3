<template>
  <q-page class="">
    <div class="q-pb-md text-h5">学校一覧</div>

    <!--1/3画面上部-->
    <div class="row q-gutter-md">
      <q-field dense class="form-model">
        <q-input
          label="学校名"
          v-model="condition.search"
          class="form-model"
          dense
          stack-label
          v-on:keydown.enter="search"
        />
        <q-btn
          color="primary"
          dense
          icon="search"
          @click="search"
          :loading="loading.search"
        />
      </q-field>
      <q-btn
        label="追加"
        icon-right="note_add"
        color="grey-6"
        outline
        @click="modal.insert = true"
        dense
      />
      <lock-icon
        v-model="deleteIcon"
        @event-change="deleteIcon = $event"
        class="q-pt-sm"
      />
    </div>

    <!--2/3モーダル-->
    <div>
      <q-dialog v-model="modal.insert">
        <q-card class="q-pa-md" style="width: 500px">
          <q-section>
            <div class="text-subtitle1 row q-gutter-md">
              <div style="margin-right: auto">新規追加</div>
              <q-btn icon="close" @click="modal.insert = false" round flat />
            </div>
            <hr />
            <div class="row q-gutter-md">
              <q-input
                label="学校名"
                v-model="condition.insert"
                class="form-model"
                dense
                outlined
                stack-label
                style="width: 250px"
                clearable
              />
              <q-btn
                label="追加"
                @click.prevent="insert"
                outline
                icon="note_add"
                :loading="loading.insert"
              />
            </div>
          </q-section>
        </q-card>
      </q-dialog>
    </div>
    <div>
      <q-dialog v-model="modal.delete">
        <q-card class="q-pa-md" style="width: 500px">
          <q-section>
            <div class="text-subtitle1 row q-gutter-md">
              <div style="margin-right: auto">削除確認</div>
              <q-btn icon="close" @click="modal.delete = false" round flat />
            </div>
            <hr />

            <div>次の学校を削除してもいいかな？</div>
            <div class="q-pa-md">
              <q-card style="width: 200px">
                <q-card-section>
                  {{ condition.delete }}
                </q-card-section>
              </q-card>
            </div>
            <hr />
            <div>
              <q-btn
                @click.prevent="deleteRec()"
                label="削除する"
                color="red"
                outline
                icon="delete"
                :loading="loading.delete"
              />
            </div>
          </q-section>
        </q-card>
      </q-dialog>
    </div>

    <!--3/3テーブル-->
    <div class="q-pt-md">
      <div class="row q-gutter-md">
        <q-card v-for="r in records" :key="r">
          <q-card-section>
            {{ r }}
            <div v-if="deleteIcon == false">
              <q-btn
                icon="delete"
                outline
                color="red"
                dense
                @click.prevent="
                  condition.delete = r;
                  modal.delete = true;
                "
              />
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useSchoolListModel } from 'src/models/SchoolListModels';
import lockIcon from 'src/components/LockIcon.vue';
export default defineComponent({
  name: 'school-list',
  components: {
    'lock-icon': lockIcon,
  },
  setup() {
    const { loading, modal, condition, records, search, insert, deleteRec } =
      useSchoolListModel();
    search();
    return {
      loading,
      modal,
      condition,
      records,
      search,
      insert,
      deleteRec,
      deleteIcon: ref(true),
    };
  },
});
</script>
<style>
/*input 入力の横幅 */
.form-model {
  width: 200px;
  height: 40px;
}
/*テーブルのサイズ */
.search-table {
  max-width: 700px;
  word-break: break-word;
  max-height: 600px;
}
/*カードのサイズ */
.card-object {
  width: 100%;
  max-width: 250px;
}
</style>
