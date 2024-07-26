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
          @keypress.enter="onSearchClick"
          style="width: 300px"
        >
          <template v-slot:append>
            <q-btn flat icon="search" color="primary" @click="onSearchClick" />
          </template>
          <template v-slot:after>
            <q-btn
              icon="settings"
              flat
              @click="dialogView = true"
            />
          </template>
        </q-input>
        </div>

    </div>
    <div class="q-pt-md">
      <q-pagination
        v-model="condition.pageNo"
        :max="pageState.pageCount"
        :max-pages="10"
        input
        v-if="pageState.records.length > 0"
      />
    </div>
  </div>
  <div class="pixiv-search-area-mobile"></div>
  <q-dialog v-model="dialogView">
    <q-card class="q-pa-md">
      <q-card-section class="q-pa-md">

        <div class="q-pa-md flex">
          <q-input
            dense
            v-model="condition.text"
            label="検索欄"
            outlined
            stack-label
            style="width: 220px"
          >
            <template v-slot:append>
              <q-btn flat icon="search" color="primary" @click="onSearchClick">
                <q-tooltip :delay="1000">検索する</q-tooltip>
              </q-btn>
            </template>
          </q-input>
          <q-checkbox v-model="isR18" label="R18" style="width: 40px">
          </q-checkbox>
        </div>
        <div>
          <div class="q-pa-md">
            <holo-name-select />
          </div>
          <div class="q-pa-md">
            <hashtag-input />
          </div>
          <div class="q-pa-md">
            <user-input />
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
import { computed, defineComponent, ref, watch ,PropType} from 'vue';
import PixivHoloNameSelect from '../selects/PixivHoloNameSelect.vue';
import PixivHashtagInput from './PixivHashtagInput.vue';
import PixivUserInput from './PixivUserInput.vue';
import { PixivSearchStore } from 'src/stores/pixiv/PixivSearchStore';
import { useRoute, useRouter } from 'vue-router';
import { useQuerySupport } from 'src/utils/QuerySupport';
const {decodeQueryString,
  decodeQueryNumber,
  decodeQueryStringArray,
  decodeQueryNumberArray,
  decodeQueryBoolean} = useQuerySupport();
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
    const loading = ref(store.isLoading.illust);
    const condition = ref(store.condition);
    const isConditionDefault = computed(() => store.isConditionDefault());
    const isR18 = ref(store.isR18);
    const holoname = ref(store.selectedHoloName);

    watch(holoname, (newValue, oldValue) => {
      store.removeHashtag(oldValue);
      if (newValue?.length > 0) {
        store.addHashtag(newValue);
      }
    });

    const onSearchClick = function () {
      dialogView.value = false;
      store.condition.pageNo = 1;
      store.isR18 = isR18.value;
      store.searchIllust();
      replaceUrl(1);
    };

    const onPageClick = function () {
      dialogView.value = false;
      store.searchIllust();
      replaceUrl(store.condition.pageNo);
    };

    const onResetConditionclick = function () {
      store.resetCondition();
    };

    store.searchHashtags();
    store.searchUsers();

    const pageState = computed(() => store.pageState);

    const handleProps = function () {
      console.log('props',route.query)
      const queryText = decodeQueryString(route.query.text);
      if (queryText) {
        store.condition.text = queryText;
      }

      const queryHashtags = decodeQueryStringArray(route.query.hashtag)
      if (queryHashtags) {
        store.condition.hashtags = queryHashtags;
      }

      const queryUserIds = decodeQueryNumberArray(route.query.user);
      if (queryUserIds) {
        queryUserIds.forEach(it => it > 0 ? store.addUser(it) : null);
      }

      const queryMinBookmarks = decodeQueryNumber(route.query.minbookmark)
      if (queryMinBookmarks) {
        store.condition.minTotalBookmarks = queryMinBookmarks;
      }

      const queryMinTotalView = decodeQueryNumber(route.query.minview);
      if (queryMinTotalView) {
        store.condition.minTotalView = queryMinTotalView;
      }

      const queryR18 = decodeQueryBoolean(route.query.r18);
      if (queryR18 != undefined) {
        store.isR18 = queryR18;
      }

      const queryPage = decodeQueryNumber(route.query.page);
      if (queryPage) {
        store.condition.pageNo = queryPage;
      }
      if (decodeQueryBoolean(route.query.fetch)) {
        console.log('condition', condition.value);
        store.searchIllust();
      }
    };

    handleProps();

    const replaceUrl = function (page: number) {
      router.push({
        query: {},
      });

      router.push({
        path: '/pixiv',
        query: {
          text: store.condition.text,
          hashtag: store.condition.hashtags,
          user: store.condition.userIds,
          minbookmark: store.condition.minTotalBookmarks,
          minview: store.condition.minTotalView,
          r18: isR18.value ? 'true' : 'false',
          page: page,
          fetch: 'true',
        },
      });
    };

    watch(() => condition.value.pageNo,(newCondition, oldCondition) => {
      if(newCondition != oldCondition){
        onPageClick();
      }
    })

    return {
      loading,
      condition,
      isConditionDefault,
      isR18,
      pageState,
      holoname,
      onSearchClick,
      onPageClick,
      onResetConditionclick,
      dialogView,
    };
  },
});
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
