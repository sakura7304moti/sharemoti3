<template>
  <q-card id="holo-archive-search-box">
    <q-card-section>
      <div class="row q-gutter-md">
        <!--タイトル-->
        <div class="q-mb-sm">
          <q-input
            v-model="filter.title"
            dense
            label="テキスト"
            stack-label
            style="width: 200px"
            :disable="isLoading"
          />
        </div>

        <!--チャンネル-->
        <div>
          <holo-channel-select v-model="filter.channelId" label="チャンネル" />
        </div>

        <!--動画のタイプ-->
        <div>
          <q-select
            v-model="filter.movieType"
            :options="movieTypeOptions"
            option-value="value"
            option-label="label"
            emit-value
            map-options
            dense
            style="width: 120px"
            label="種類"
            stack-label
            clearable
            :disable="isLoading"
          />
        </div>
      </div>
      <div class="q-pt-md row q-gutter-md">
        <!--fromDate-->
        <div class="holo-archive-date-select">
          <div
            class="text-caption"
            :class="{
              'text-primary': view.fromDate,
              'text-grey': !view.fromDate,
            }"
          >
            開始日
          </div>
          <div class="row q-gutter-sm">
            <div>
              <q-btn
                icon="today"
                @click="
                  view.fromDate = !view.fromDate;
                  view.toDate = false;
                "
                dense
                :text-color="fromDateSelected"
              />
            </div>
          </div>

          <div class="text-caption row q-gutter-xs">
            <div>
              {{ filter.fromDate }}
            </div>

            <div v-if="filter.fromDate != ''">
              <q-btn
                icon="clear"
                @click="
                  filter.fromDate = '';
                  view.fromDate = false;
                "
                text-color="grey"
                dense
                round
                size="xs"
              />
            </div>
          </div>
        </div>

        <!--toDate-->
        <div class="holo-archive-date-select">
          <div
            class="text-caption"
            :class="{ 'text-primary': view.toDate, 'text-grey': !view.toDate }"
          >
            終了日
          </div>
          <div class="row q-gutter-sm">
            <div>
              <q-btn
                icon="today"
                @click="
                  view.toDate = !view.toDate;
                  view.fromDate = false;
                "
                dense
                :text-color="toDateSelected"
              />
            </div>
          </div>

          <div class="text-caption row q-gutter-xs">
            <div>
              {{ filter.toDate }}
            </div>

            <div v-if="filter.toDate != ''">
              <q-btn
                icon="clear"
                @click="
                  filter.toDate = '';
                  view.toDate = false;
                "
                text-color="grey"
                dense
                round
                size="xs"
              />
            </div>
          </div>
        </div>

        <div class="q-pt-md">
          <q-btn
            icon="search"
            @click.prevent="search"
            :loading="isLoading"
            color="primary"
          />
        </div>
      </div>

      <!--Page-->
      <div class="q-pt-md">
        <q-pagination
          v-if="page.pageCount > 0"
          v-model="page.pageNo"
          :max="page.pageCount"
          max-pages="3"
          input
          direction-links
          @click="search"
        />
      </div>
      <!--toDate select-->
      <div>
        <q-date
          v-if="view.toDate"
          v-model="filter.toDate"
          title="toDate"
          mask="YYYY-MM-DD"
          @update:model-value="view.toDate = false"
          minimal
        />
      </div>

      <!--fromDate select-->
      <div>
        <q-date
          v-if="view.fromDate"
          v-model="filter.fromDate"
          title="fromDate"
          mask="YYYY-MM-DD"
          @update:model-value="view.fromDate = false"
          minimal
        />
      </div>
    </q-card-section>
  </q-card>
</template>
<script lang="ts">
import { computed, defineComponent, ref, SetupContext } from 'vue';
import HoloChannelList from '../selects/HoloChannelList.vue';
import { useHoloArchiveStore } from 'src/stores/HoloArchiveStore';
export default defineComponent({
  name: 'holo-archive',
  components: {
    'holo-channel-select': HoloChannelList,
  },
  setup(_, context: SetupContext) {
    const store = useHoloArchiveStore();
    store.getMovies();
    const filter = ref(store.filter);
    const page = ref(store.page);
    const isLoading = computed(() => store.loading);

    const movieTypeOptions = [
      {
        label: '動画',
        value: 'movie',
      },
      {
        label: 'ライブ',
        value: 'live',
      },
      {
        label: 'ショート',
        value: 'short',
      },
    ] as movieTypeOption[];

    const view = ref({
      toDate: false,
      fromDate: false,
    } as viewState);

    const fromDateSelected = computed(() =>
      view.value.fromDate ? 'primary' : 'black'
    );

    const toDateSelected = computed(() =>
      view.value.toDate ? 'primary' : 'black'
    );

    const search = function () {
      context.emit('search-start'); //検索開始したことを知らせる

      store.getMovies();

      const element = document.getElementById('holo-archive-cards');
      element?.scroll({ top: 0 });
      context.emit('search-end'); //検索完了したことを知らせる
    };

    return {
      isLoading,
      filter,
      page,
      movieTypeOptions,
      view,
      fromDateSelected,
      toDateSelected,
      search,
    };
  },
});
interface movieTypeOption {
  label: string;
  value: string;
}
interface viewState {
  toDate: boolean;
  fromDate: boolean;
}
</script>
<style>
#holo-archive-search-box {
  height: 330px;
  width: 380px;
}
.holo-archive-date-select {
  width: 100px;
  height: 62px;
  max-height: 62px;
}
</style>
