<template>
  <q-page class="">
    <!--トップメッセージ-->
    <div class="q-mb-md">
      <q-chat-message
        name="オム子"
        avatar="/src/assets/omuko_icon2.jpg"
        bg-color="white"
      >
        <div
          class="top-message__text"
          style="white-space: pre-wrap; word-wrap: break-word"
        >
          <div>ここは韓国のおばあちゃんち。</div>
          <div>あの時の名言やあだ名、スマブラの切り抜きなど...</div>
          <div>たくさんの思い出があるわ。ゆっくりしていってね。</div>
        </div>
      </q-chat-message>
    </div>

    <!--おしらせ-->
    <div style="margin: 32px 0; text-align: center">
      <div>
        <span
          ><img
            src="/src/assets/lief-left.png"
            style="width: 40px; height: 20px; object-fit: contain"
        /></span>
        <span class="top-title">お知らせ</span>
        <span
          ><img
            src="/src/assets/lief-right.png"
            style="width: 40px; height: 40px; object-fit: contain"
        /></span>
      </div>
      <div class="q-mt-md top-news-container">
        <hr />
        <div
          v-for="(rec, idx) in newsDataState.records"
          :key="idx"
          class="top-news-card"
        >
          <div class="top-news-card-child">
            <div
              style="
                text-align: left;
                padding-left: 16px;
                width: 100px;
                font-family: EB Garamond;
              "
            >
              {{ rec.createdAt }}
            </div>
            <div style="font-family: Noto Sans JP; padding-left: 16px">
              <span class="top-news-card-url" @click="onPageClick(rec.url)"
                ><q-tooltip transition-show="scale" transition-hide="scale"
                  >{{ rec.page }}にジャンプする</q-tooltip
                >{{ rec.page }}</span
              >に新しいデータが追加されたよ！
            </div>
          </div>
          <hr />
        </div>
        <div
          style="
            display: flex;
            justify-content: center; /* 中央揃え */
            align-items: center; /* 垂直方向のセンタリング（必要に応じて） */
            margin-top: 8px; /* 上下の余白を調整 */
          "
        >
          <q-pagination
            v-model="newsCondition"
            :max="newsDataState.totalCount"
            color="teal-6"
            @update:model-value="getNews"
            class="q-mt-sm"
          />
        </div>
      </div>
    </div>

    <!--トップ画像-->
    <div class="top-image-container zoomIn" style="margin: 32px 0">
      <div
        style="
          margin-left: 16px;
          margin-bottom: 8px;
          font-size: 32px;
          font-family: serif;
        "
      >
        <span
          ><img
            src="../assets/lief-left.png"
            style="width: 40px; height: 20px; object-fit: contain"
        /></span>
        <span class="top-title">今日の一枚</span>
        <span
          ><img
            src="../assets/lief-right.png"
            style="width: 40px; height: 40px; object-fit: contain"
        /></span>
      </div>
      <div
        style="
          text-align: left;
          max-width: 100vw;
          width: 100%;
          padding-bottom: 16px;
        "
      >
        <img :src="imageUrl" class="top-image" />
      </div>
    </div>

    <!--スペシャルサンクス-->
    <div style="margin: 32px 0; text-align: center">
      <div>
        <span
          ><img
            src="../assets/lief-left.png"
            style="width: 40px; height: 20px; object-fit: contain"
        /></span>
        <span class="top-title">Special Thanks</span>
        <span
          ><img
            src="../assets/lief-right.png"
            style="width: 40px; height: 40px; object-fit: contain"
        /></span>
      </div>
      <div class="text-left">
        <span class="top-sp-subtitle" @click="onLinkClick('/namelist')"
          >学校<q-tooltip transition-show="scale" transition-hide="scale"
            >学校のページにジャンプする</q-tooltip
          ></span
        >
      </div>
      <div class="row q-mb-md">
        <div
          class="wrap top-sp-content-school"
          v-for="sc in schoolNames"
          :key="sc.id"
          @click="onClickSchoolName(sc.id)"
        >
          {{ sc.schoolName }}
        </div>
      </div>
      <div class="text-left">
        <span class="top-sp-subtitle" @click="onLinkClick('/namelist')"
          >お友達<q-tooltip transition-show="scale" transition-hide="scale"
            >あだ名のページにジャンプする</q-tooltip
          ></span
        >
      </div>
      <div class="row">
        <div
          class="wrap top-sp-content-member"
          v-for="staff in members"
          :key="staff"
        >
          {{ staff }}
        </div>
      </div>
    </div>

    <!--フッター-->
    <div style="margin: 32px 0; text-align: center">
      <div style="font-family: EB Garamond">
        © 韓国のおばあちゃんち製作委員会
        <span>
          <img
            src="/src/assets/kimutaku.png"
            style="
              position: relative;
              top: 10px;
              height: 40px;
              width: 40px;
              object-fit: contain;
            "
          />
        </span>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import { TopImageApi } from 'src/api/file/TopImageApi';
import { TopNewsApi } from 'src/api/file/TopNewsApi';
import { SchoolApi } from 'src/api/main/SchoolApi';
import { NameList2Api } from 'src/api/main/NameList2Api';
import { useQuasar } from 'quasar';
export default defineComponent({
  name: 'IndexPage',
  setup() {
    const quasar = useQuasar();
    // API
    const topImageApi = new TopImageApi();
    const newsApi = new TopNewsApi();
    const schoolApi = new SchoolApi();
    const nameApi = new NameList2Api();

    // STATES
    const schoolNames = ref([] as School[]);
    const members = ref([] as string[]);
    const router = useRouter();
    const onPageClick = function (url: string) {
      router.push(url);
    };
    const imageUrl = computed(() => topImageApi.singleImageUrl());
    const isTopNewsLoading = ref(false);
    const newsCondition = ref(1);
    const newsDataState = ref({
      records: [],
      totalCount: 0,
    } as NewsDataState);

    // API CALL
    const getNews = async function () {
      isTopNewsLoading.value = true;
      await newsApi
        .news(newsCondition.value)
        .then((response) => {
          if (response) {
            console.log('news', response);
            newsDataState.value.totalCount = response.totalCount;
            newsDataState.value.records = response.records;
          }
        })
        .catch((err) => {
          console.log('schol err', err);
          quasar.notify({
            color: 'red',
            position: 'top',
            message: 'お知らせの取得でエラーになった...',
          });
        });
      isTopNewsLoading.value = false;
    };
    const getSchoolNames = async function () {
      await schoolApi.school().then((response) => {
        if (response) {
          console.log('school', response);
          schoolNames.value = response;
        }
      });
    };
    const onClickSchoolName = function (id: number) {
      router.push('/school/' + id);
    };

    const getMemberNames = async function () {
      await nameApi.search().then((response) => {
        if (response) {
          console.log('names', response);
          members.value = response.reverse().map((it) => it.name);
        }
      });
    };

    const onLinkClick = function (url: string) {
      router.push(url);
    };

    // 初期化処理
    getNews();
    getSchoolNames();
    getMemberNames();
    return {
      imageUrl,
      isTopNewsLoading,
      newsCondition,
      newsDataState,
      schoolNames,
      members,
      getNews,
      onPageClick,
      onClickSchoolName,
      onLinkClick,
    };
  },
});
interface NewsDataState {
  records: Array<TopNews>;
  totalCount: number;
}

interface TopNews {
  page: string;
  createdAt: string;
  total: number;
  url: string;
}
interface School {
  id: number;
  schoolName: string;
  principal: string;
  detail: string;
  slogan: string;
  avgStar: null | number;
}
</script>
<style>
/*画像 */
.top-image {
  max-width: 100vw;
  width: 100%;
  max-height: 50vh;
  height: 100%;
  display: inline-block;
  object-fit: contain;
  padding-left: 16px;
  padding-right: 16px;
}
.top-image-container {
  max-width: 100vw;
  border-radius: 20px;
  box-shadow: 10px;
  text-align: center;
}
/*ニュース */
.top-news-card {
  max-width: 800px;
  font-size: 12px;
  line-height: 20px;
}
.top-news-container {
  max-width: 60%;
  width: 100%;
  margin-right: auto;
  margin-left: auto;
}
.top-news-card-child {
  padding: 16px 0;
  display: flex;
}
@media (max-width: 650px) {
  .top-news-container {
    max-width: 90%;
  }
  .top-news-card-child {
    display: block;
    padding: 4px 0;
  }
}
.top-news-card-url {
  color: rgb(0, 167, 137);
  cursor: pointer;
}
.top-news-card-url:hover {
  opacity: 0.5;
  transition: 0.3s;
}
/*トップメッセージ */
.top-message__text {
  font-family: 'Noto Serif JP', serif;
  font-size: 18px;
  line-height: 2.3;
}
.top-title {
  font-size: 32px;
  font-family: serif;
  margin-left: 16px;
  margin-right: 16px;
}
/*sp */
.top-sp-subtitle {
  text-align: left;
  color: #18bfa0;
  margin-left: 16px;
  margin-bottom: 8px;
  font-size: 32px;
  font-family: serif;
  cursor: pointer;
}
.top-sp-subtitle:hover {
  opacity: 0.5;
  transition: 0.3s;
}
.top-sp-content-school {
  margin-right: 16px;
  padding-bottom: 8px;
  font-family: serif;
  cursor: pointer;
}
.top-sp-content-school:hover {
  opacity: 0.5;
  transition: 0.3s;
}
.top-sp-content-member {
  margin-right: 16px;
  padding-bottom: 8px;
  font-family: serif;
}
@media (max-width: 800px) {
  .top-message__text {
    font-size: 16px;
    line-height: 1.5;
  }
  .top-title {
    font-size: 20px;
  }
  .top-sp-subtitle {
    font-size: 20px;
  }
}
</style>
