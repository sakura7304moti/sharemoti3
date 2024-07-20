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
        @update:model-value="onPageClick"
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
      condition.value.pageNo = 1;
      store.isR18 = isR18.value;
      store.searchIllust();
      replaceUrl(1);
    };

    const onPageClick = function () {
      dialogView.value = false;
      store.searchIllust();
      replaceUrl(condition.value.pageNo);
    };

    const onResetConditionclick = function () {
      store.resetCondition();
    };

    store.searchHashtags();
    store.searchUsers();

    const pageState = computed(() => store.pageState);

    const handleProps = function () {
      console.log('query', route.query);
      if (route.query.text) {
        store.condition.text = route.query.text.toString();
      }
      if (route.query.hashtag) {
        const tags = route.query.hashtag.toString();
        if(tags.includes(',')){
          tags.split(',').forEach((tag) => {
          if (tags.length > 0 && !store.condition.hashtags.includes(tag)) {
            store.condition.hashtags.push(tag);
          }
        });
        }
        else{
          if(!store.condition.hashtags.includes(tags) && tags.length > 0){
            store.condition.hashtags.push(tags);
          }
        }
      }
      if(store.condition.hashtags.includes('')){
        const findIndex = store.condition.hashtags.findIndex(() => '');
        if(findIndex > -1){
          store.condition.hashtags.splice(findIndex);
        }
      }
      if (route.query.user) {
        const users = route.query.user.toString();
        if(users.includes(',')){
          users.split(',').forEach((us) => {
            if (Number(us) > 0) {
              store.addUser(Number(us));
            }
          })
        }
        else{
          if(Number(users) > 0){
            store.addUser(Number(users));
          }
        }

      }
      if (route.query.minbookmark) {
        store.condition.minTotalBookmarks = Number(route.query.minbookmark);
      }
      if (route.query.minview) {
        store.condition.minTotalView = Number(route.query.minview);
      }
      if (route.query.r18) {
        store.isR18 = route.query.r18.toString() == 'true';
      }
      if (route.query.page) {
        store.condition.pageNo = Number(route.query.page);
      }
      if (route.query.fetch) {
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

    return {
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
