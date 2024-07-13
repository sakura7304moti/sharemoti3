<template>
  <div class="pixiv-search-area-desktop">
    <div class="row q-gutter-sm">
      <div>
        <q-input
          dense
          v-model="condition.text"
          label="検索欄"
          outlined
          stack-label
          @keydown.enter="onSearchClick"
          style="width: 300px"
        >
          <template v-slot:append>
            <q-btn flat icon="search" color="primary" @click="onSearchClick">
            </q-btn>
          </template>
          <template v-slot:after>
            <q-btn
              icon="settings"
              flat
              text-color="gray"
              @click="dialogView = true"
            ></q-btn>
          </template>
        </q-input>
      </div>
    </div>
    <div class="q-pt-md">
      <q-pagination
        v-model="condition.pageNo"
        :max="pageState.pageCount"
        :max-pages="10"
        direction-links
        boundary-links
        icon-first="skip_previous"
        icon-last="skip_next"
        icon-prev="fast_rewind"
        icon-next="fast_forward"
        @update:model-value="onPageClick"
        v-if="pageState.records.length > 0"
      />
    </div>
  </div>
  <div class="pixiv-search-area-mobile"></div>
  <q-dialog v-model="dialogView">
    <q-card class="q-pa-md">
      <q-card-section class="q-pa-md">
        <div class="q-pa-md">
          <q-input
            dense
            v-model="condition.text"
            label="検索欄"
            outlined
            stack-label
            style="width: 300px"
          >
            <template v-slot:append>
              <q-btn flat icon="search" color="primary" @click="onSearchClick">
                <q-tooltip :delay="1000">検索する</q-tooltip>
              </q-btn>
            </template>
          </q-input>
        </div>
        <div>
          <div class="q-pa-md">
            <hashtag-input />
          </div>
          <div class="q-pa-md">
            <user-input />
          </div>
          <div class="q-pa-md">
            <holo-name-select />
          </div>
          <div class="q-pa-md" style="display: none">
            <q-select
              v-model="condition.minTotalBookmarks"
              :options="[0, 5000, 10000, 20000, 50000]"
              label="ブックマーク数"
              type="number"
              dense
              style="width: 300px"
            />
          </div>
          <div class="q-pa-md">
            <q-select
              v-model="condition.minTotalView"
              :options="[0, 10000, 20000, 50000, 100000, 200000, 500000]"
              label="閲覧数"
              type="number"
              dense
              style="width: 300px"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue';
import PixivHoloNameSelect from '../selects/PixivHoloNameSelect.vue';
import PixivHashtagInput from './PixivHashtagInput.vue';
import PixivUserInput from './PixivUserInput.vue';
import { PixivSearchStore } from 'src/stores/pixiv/PixivSearchStore';
import { useRoute, useRouter } from 'vue-router';
export default defineComponent({
  name: 'pixiv-search-area',
  components: {
    'holo-name-select': PixivHoloNameSelect,
    'hashtag-input': PixivHashtagInput,
    'user-input': PixivUserInput,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();

    const dialogView = ref(false);
    const store = PixivSearchStore();
    const condition = ref(store.condition);
    const holoname = ref(store.selectedHoloName);

    watch(holoname, (newValue, oldValue) => {
      store.removeHashtag(oldValue);
      if (newValue?.length > 0) {
        store.addHashtag(newValue);
      }
    });

    const onSearchClick = function () {
      dialogView.value = false;
      condition.value.pageNo = 1;
      store.searchIllust();
      replaceUrl(1);
    };

    const onPageClick = function () {
      dialogView.value = false;
      store.searchIllust();
      replaceUrl(condition.value.pageNo);
    };

    store.searchHashtags();
    store.searchUsers();

    const pageState = computed(() => store.pageState);

    const handleProps = function () {
      console.log('query', route.query);
      if (route.query.text) {
        store.condition.text = route.query.text.toString();
      }
      if (route.query.tags) {
        if (route.query.tags instanceof String) {
          store.condition.hashtags.push(route.query.tags.toString());
        }
      }
      if (route.query.user) {
        if (route.query.user instanceof String) {
          store.condition.userIds.push(Number(route.query.user));
        }
      }
      if (route.query.minbookmark) {
        store.condition.minTotalBookmarks = Number(route.query.minbookmark);
      }
      if (route.query.mintotal) {
        store.condition.minTotalView = Number(route.query.mintotal);
      }
      if (route.query.page) {
        store.condition.pageNo = Number(route.query.page);
      }
      if (route.query.fetch) {
        store.searchIllust();
      }
    };

    handleProps();

    const replaceUrl = function (page: number) {
      router.push({
        query: {
          text: store.condition.text,
          tags: store.condition.hashtags,
          user: store.condition.userIds,
          minbookmark: store.condition.minTotalBookmarks,
          minview: store.condition.minTotalView,
          page: page,
          fetch: 'true',
        },
      });
    };

    return {
      condition,
      pageState,
      holoname,
      onSearchClick,
      onPageClick,
      dialogView,
    };
  },
});
interface ConditionState {
  hashtags: string[];
  userIds: number[];
  minTotalBookmarks: number;
  minTotalView: number;
}
</script>
<style>
@media only screen and(max-width:800px) {
  #pixiv-search-area-desktop {
    display: none;
  }
}
@media only screen and(min-width:800px) {
  #pixiv-search-area-mobile {
    display: none;
  }
}
</style>
