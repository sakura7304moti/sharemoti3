<template>
  <q-field label="ユーザー" dense stack-label>
    <template v-slot:control>
      <q-avatar>
        <img :src="userImageUrl" v-if="userImageUrl.length > 0" />
      </q-avatar>
      <div v-if="selectedUser.length != 0" class="q-pl-md text-subtitle1">
        {{ selectedUser[0].name }}
      </div>
      <q-btn
        flat
        icon="close"
        @click.prevent.stop="onClearUser"
        v-if="userImageUrl.length > 0"
      />
    </template>
    <template v-slot:append>
      <q-btn
        round
        dense
        flat
        icon="toc"
        @click.prevent.stop="dialogOpen = true"
      >
        <q-tooltip> ユーザーを一覧から選ぶ </q-tooltip>
      </q-btn>
    </template>
  </q-field>

  <q-dialog v-model="dialogOpen">
    <q-card
      style="width: 100%; max-width: 80vw; height: 100%; max-height: 80vh"
      class="q-pa-md"
    >
      <div class="full-width row justify-end">
        <div>
          <q-btn
            icon="close"
            flat
            color="primary"
            text-color="black"
            size="md"
            label="とじる"
            @click.prevent.stop="dialogOpen = false"
          />
        </div>
      </div>
      <q-card-section>
        <div class="text-h6 q-pb-sm">ユーザー検索</div>
        <q-table
          :rows="findUsers"
          :columns="columns"
          :filter="filter"
          row-key="name"
          separator="cell"
          :rows-per-page-options="[5, 100, 500, 1000]"
          :pagination="{ rowsPerPage: 1000 }"
          id="pixiv-hashtag-table"
          class="scroll-table"
        >
          <template v-slot:top-left>
            <q-input
              dense
              debounce="400"
              v-model="filter"
              placeholder="検索"
              class="q-pb-mr"
            >
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </template>
          <template v-slot:header="props">
            <q-tr :props="props">
              <q-th v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.label }}
              </q-th>
            </q-tr>
          </template>
          <template v-slot:body="props">
            <q-tr :props="props">
              <q-td
                v-for="col in props.cols"
                :key="col.name"
                :props="props"
                style="white-space: normal; text-align: right"
                class="cursor-pointer"
                @click="onAddUser(props.row.id)"
              >
                {{ col.value }}
              </q-td>
            </q-tr>
          </template>
        </q-table>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue';
import { PixivSearchStore } from 'src/stores/pixiv/PixivSearchStore';
import { QTableColumn } from 'quasar';
export default defineComponent({
  name: 'pixiv-user-input',
  setup() {
    const dialogOpen = ref(false);

    const store = PixivSearchStore();
    const selectedUser = computed(() => store.selectedUsers);

    watch(store.selectedUsers, (newValue,oldValue) => {
      oldValue.forEach(it => store.removeUser(it.id));
      newValue.forEach(it => store.addUser(it.id));
    })

    const userImageUrl = computed(() => store.userProfileUrl);
    const isLoading = ref(store.isLoading.user);
    const condition = ref(store.userCondition);

    const findUsers = ref(store.findUsers);

    const searchUser = async function () {
      await store.searchUsers();
    };

    const onAddUser = function (userId: number) {
      store.selectedUsers.splice(0);
      store.addUser(userId);
      dialogOpen.value = false;
    };

    const onRemoveUser = function (userId: number) {
      store.removeUser(userId);
    };

    const onClearUser = function () {
      store.clearUser();
    };

    const columns = [
      {
        name: 'id',
        label: 'id',
        field: 'id',
        sortable: true,
      },
      {
        name: 'name',
        label: 'ユーザー名',
        field: 'name',
        sortable: true,
      },
    ] as QTableColumn[];

    return {
      dialogOpen,
      userImageUrl,
      isLoading,
      condition,
      filter: ref(''),
      selectedUser,
      findUsers,
      searchUser,
      columns,
      onAddUser,
      onRemoveUser,
      onClearUser,
    };
  },
});

</script>
