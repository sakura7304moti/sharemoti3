<template>
  <q-page class="">
    <div class="text-h6">イチローの国立美術館</div>
    <!--ヘッダー-->
    <div class="row q-gutter-xs q-pl-md">
      <q-card>
        <q-card-section>
          <div class="row q-gutter-md">
            <div>
              <uploader :uploaded="uploaded" @research="reSearch" />
            </div>
            <div>
              <q-btn
                round
                dense
                icon="loop"
                textColor="black"
                @click="search"
              />
            </div>
            <a
              href="#"
              class="q-pt-sm image-list-button-text q-pr-md"
              @click.prevent="search"
              style="text-decoration: none"
              >再検索</a
            >
            <div class="q-pl-md">
              <q-toggle v-model="deleteLock" icon="delete" color="negative" />
            </div>
            <a
              href="#"
              class="q-pt-sm image-list-button-text q-pr-md"
              @click.prevent="deleteLock = !deleteLock"
              style="text-decoration: none"
              >削除アイコン表示</a
            >
          </div>
        </q-card-section>
      </q-card>

      <q-card>
        <q-card-section>
          <div class="row q-gutter-md">
            <div>
              <div class="text-grey text-subtitle1">検索</div>
              <q-input v-model="filter" filled dense />
            </div>
            <div>
              <div class="text-grey text-subtitle1">表示方法</div>
              <div class="row q-gutter-xs text-grey-6">
                <q-radio
                  v-model="cardSize"
                  val="lg"
                  label="大"
                  color="primary"
                  keep-color
                  size="sm"
                  dense
                />
                <q-radio
                  v-model="cardSize"
                  val="md"
                  label="中"
                  color="primary"
                  keep-color
                  size="sm"
                  dense
                />
                <q-radio
                  v-model="cardSize"
                  val="sm"
                  label="小"
                  color="primary"
                  keep-color
                  size="sm"
                  dense
                />
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>

    <!--カード一覧-->
    <div style="display: flex; width: 100%; flex-wrap: wrap">
      <div v-for="rec in filteringData" :key="rec.id" class="q-pa-md">
        <imageCard
          :dataState="rec"
          :deleteDisplay="deleteLock"
          :size="cardSize"
          @deleted="reSearch"
        />
      </div>
    </div>
  </q-page>
</template>
<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import api from 'src/api/main/ImageListApi';
import ImageUploader from 'src/components/imagelist/ImageUploader.vue';
import ImageCard from 'src/components/imagelist/ImageCard.vue';
import { useViewSupport } from 'src/utils/viewSupport';
export default defineComponent({
  name: 'image-list-page',
  components: {
    uploader: ImageUploader,
    imageCard: ImageCard,
  },
  setup() {
    const { displayDate } = useViewSupport();
    const filter = ref('');
    const records = ref([] as DataState[]);
    const uploaded = ref(false);
    const deleteLock = ref(false);
    const cardSize = ref('lg');

    const filteringData = computed(() =>
      records.value.filter(
        (it) =>
          it.title.includes(filter.value) || it.detail.includes(filter.value)
      )
    );

    const search = async function () {
      records.value.splice(0);

      await api.search().then((res) => {
        if (res) {
          console.log('search', res);
          res.records.forEach((it) =>
            records.value.push({
              id: it.id,
              fileName: it.fileName,
              ext: it.ext,
              title: it.title,
              detail: it.detail,
              createAt: displayDate(it.createAt),
              updateAt: displayDate(it.updateAt),
            })
          );
          records.value.reverse(); //とりあえず追加順
        }
      });
    };
    search();

    const reSearch = function () {
      search();
      console.log('research called');
    };

    return {
      records,
      uploaded,
      search,
      deleteLock,
      reSearch,
      cardSize,
      filter,
      filteringData,
    };
  },
});
interface DataState {
  id: number;
  fileName: string;
  ext: string;
  title: string;
  detail: string;
  createAt: string;
  updateAt: string;
}
</script>
<style lang="scss">
.image-list-button-text {
  color: $grey-6;
}
</style>
