<template>
  <!--SUB 1/3 上に表示する検索、追加等詳細な操作画面-->
  <div class="q-pb-md">
    <q-card style="max-width: 400px" class="q-pa-sm" v-if="tableView == false">
      <q-card-section>
        <div class="text-h6">{{ listName }}</div>
        <div
          class="haiku-upper"
          v-if="displayCondition.upper && tableView == false"
        >
          <div>
            <q-select
              label="俳人"
              :options="posterItems"
              v-model="selectPoster"
              clearable
            />
          </div>
          <div class="row q-pt-md">
            <div class="col">
              <q-toggle
                v-model="detailDisplay"
                label="解説を表示"
                color="primary"
              />
            </div>
            <div class="col">
              <q-toggle
                v-model="displaySort"
                label="新しい順"
                color="primary"
              />
            </div>
          </div>
          <div class="q-pt-md row justify-between">
            <!--新規追加ボタン-->
            <div class="q-pt-sm">
              <q-btn
                label="ここで一句"
                icon-right="note_add"
                color="primary"
                @click="insertClick"
              />
            </div>

            <!--編集ロックアイコン-->
            <div>
              <lock-icon
                v-model="lockIconCondition"
                @event-change="lockIconCondition = $event"
                class="q-pt-md"
              />
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
  <div
    v-for="rec in viewRecords"
    :key="rec.id"
    class="row q-gutter-md q-pa-md wrap"
  >
    <div class="haiku-box">
      <div
        style="
          writing-mode: vertical-rl;
          font-family: haiku;
          font-size: 32px;
          margin-left: auto;
          height: 280px;
        "
      >
        <div style="margin-right: 50px; height: 320px">
          {{ rec.first }}
        </div>
        <div style="margin-right: 20px; height: 320px">
          {{ rec.second }}
        </div>
        <div style="margin-right: 20px; height: 320px">
          {{ rec.third }}
        </div>
        <div style="margin-right: 20px; height: 320px" class="text-right">
          {{ rec.poster }}
        </div>
      </div>
      <div
        class="bg-light-green-1"
        style="height: 50px"
        v-if="lockIconCondition == false"
      >
        <hr />
        <div class="row" style="width: 270px">
          <div class="col text-left">
            <q-btn
              color="primary"
              label="編集する"
              @click.prevent="updateClick(rec)"
              icon="edit"
              dense
            />
          </div>
          <div class="col text-right">
            <q-btn
              color="negative"
              label="削除する"
              @click.prevent="deleteClick(rec)"
              icon="delete"
              dense
            />
          </div>
        </div>
      </div>
    </div>
    <div>
      <div class="box28 bg-white" v-if="detailDisplay">
        <span class="box-title">解説</span>
        <p
          style="text-align: left; white-space: pre-wrap; word-wrap: break-word"
        >
          {{ rec.detail }}
        </p>
      </div>
    </div>
  </div>

  <!--SUB 3/3 モーダル一覧-->
  <div>
    <q-dialog v-model="displayCondition.insert">
      <q-card class="q-pa-md" style="max-width: 700px">
        <q-section>
          <div style="font-family: HinaMincho-Regular" class="text-h6">
            <div class="row justify-between">
              <div>王将マンの俳句審査</div>
              <div>
                <q-btn
                  @click="displayCondition.insert = false"
                  icon="close"
                  text-color="grey"
                  label="閉じる"
                  dense
                />
              </div>
            </div>
            <q-checkbox
              class="text-subtitle1 text-weight-medium"
              v-model="insertHaikuOmake"
              label="みちゃやーよ"
            />
          </div>
          <hr />
          <div class="row q-gutter-md" style="width: 700px">
            <!--inputs-->
            <div style="width: 350px">
              <q-input
                v-model="insertCondition.poster"
                label="投稿者名"
                stack-label
                style="width: 200px"
                outlined
                dense
                class="q-pb-lg"
                filled
              />
              <q-input
                v-model="insertCondition.first"
                outlined
                class="q-pb-md"
                style="width: 200px"
                label="5"
                stack-label
              />
              <q-input
                v-model="insertCondition.second"
                outlined
                class="q-pb-md"
                style="width: 300px"
                label="7"
                stack-label
              />
              <q-input
                v-model="insertCondition.third"
                outlined
                class="q-pb-md"
                style="width: 200px"
                label="5"
                stack-label
              />
            </div>
            <div>
              <q-input
                style="
                  width: 250px;
                  text-align: left;
                  white-space: pre-wrap;
                  word-wrap: break-word;
                "
                rows="12"
                type="textarea"
                v-model="insertCondition.detail"
                outlined
                stack-label
                label="解説(省略可)"
              />
            </div>
            <!--作品イメージ-->
            <div style="width: 250px" v-if="insertHaikuOmake">
              <div>
                <div>作品イメージ</div>
                <!--セリフ-->
                <div class="haiku-box">
                  <div
                    style="
                      writing-mode: vertical-rl;
                      font-family: haiku;
                      font-size: 32px;
                      margin-left: auto;
                    "
                  >
                    <div style="margin-right: 50px">
                      {{ insertCondition.first }}
                    </div>
                    <div style="margin-right: 20px">
                      {{ insertCondition.second }}
                    </div>
                    <div style="margin-right: 20px">
                      {{ insertCondition.third }}
                    </div>
                    <div style="margin-right: 20px">
                      {{ insertCondition.poster }}
                    </div>
                  </div>
                </div>
                <img src="../assets/senno_rikyu.png" width="200" />
                <div>そこにわびさびはあるんか?</div>
              </div>
            </div>
          </div>

          <hr />
          <div>
            <q-btn
              label="追加する"
              color="primary"
              class="text-weight-bold"
              :disable="
                insertCondition.first == '' ||
                insertCondition.second == '' ||
                insertCondition.third == ''
              "
              style="margin-right: auto"
              @click="insert"
              :loading="LoadingCondition.insert"
            />
          </div>
        </q-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="displayCondition.update">
      <q-card class="q-pa-md" style="max-width: 1200px">
        <q-section>
          <div class="row justify-between">
            <div class="text-h6">俳句の編集</div>
            <div>
              <q-btn
                @click="displayCondition.update = false"
                icon="close"
                text-color="grey"
                label="閉じる"
                dense
              />
            </div>
          </div>
          <hr />
          <div class="row q-gutter-md">
            <!--編集後-->
            <div>
              <div class="row q-gutter-xs">
                <!--inputs-->
                <div style="width: 320px">
                  <q-input
                    v-model="updateCondition.poster"
                    label="投稿者名"
                    stack-label
                    style="width: 200px"
                    outlined
                    dense
                    class="q-pb-lg"
                    filled
                  />
                  <q-input
                    v-model="updateCondition.first"
                    outlined
                    class="q-pb-md"
                    style="width: 200px"
                    label="5"
                    stack-label
                  />
                  <q-input
                    v-model="updateCondition.second"
                    outlined
                    class="q-pb-md"
                    style="width: 300px"
                    label="7"
                    stack-label
                  />
                  <q-input
                    v-model="updateCondition.third"
                    outlined
                    class="q-pb-md"
                    style="width: 200px"
                    label="5"
                    stack-label
                  />
                </div>
                <div>
                  <q-input
                    style="
                      width: 250px;
                      text-align: left;
                      white-space: pre-wrap;
                      word-wrap: break-word;
                    "
                    rows="12"
                    type="textarea"
                    v-model="updateCondition.detail"
                    outlined
                    stack-label
                    label="解説(省略可)"
                  />
                </div>
              </div>
            </div>
            <!--編集前-->
            <div style="width: 300px">
              <div>
                <div class="text-subtitle1">編集前の俳句</div>
                <div class="haiku-box">
                  <div
                    style="
                      writing-mode: vertical-rl;
                      font-family: haiku;
                      font-size: 32px;
                      margin-left: auto;
                    "
                  >
                    <div style="margin-right: 50px">
                      {{ updateSelectedCondition.first }}
                    </div>
                    <div style="margin-right: 20px">
                      {{ updateSelectedCondition.second }}
                    </div>
                    <div style="margin-right: 20px">
                      {{ updateSelectedCondition.third }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div>
            <hr />
            <q-btn
              label="更新"
              @click="update"
              color="primary"
              :loading="LoadingCondition.update"
            />
          </div>
        </q-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="displayCondition.delete">
      <q-card class="q-pa-md" style="width: 700px">
        <q-section>
          <div class="text-h6 row q-gutter-md">
            <div>俳句の削除確認</div>
            <div style="margin-left: auto">
              <a
                href="#"
                class="text-grey"
                @click.prevent="displayCondition.delete = false"
                ><q-icon name="close"
                  ><q-tooltip class="bg-white text-primary"
                    >Close</q-tooltip
                  ></q-icon
                ></a
              >
            </div>
          </div>
          <hr />
          <div>次の俳句を削除してもいいかな？</div>

          <div
            style="
              writing-mode: vertical-rl;
              font-family: haiku;
              font-size: 32px;
              height: 270px;
            "
          >
            <div style="margin-right: 50px">
              {{ updateSelectedCondition.first }}
            </div>
            <div style="margin-right: 20px">
              {{ updateSelectedCondition.second }}
            </div>
            <div style="margin-right: 20px">
              {{ updateSelectedCondition.third }}
            </div>
            <div style="margin-right: 20px" class="text-right">
              {{ updateSelectedCondition.poster }}
            </div>
          </div>
          <hr />
          <q-btn
            label="削除"
            color="negative"
            @click="deleteRecord"
            :loading="LoadingCondition.delete"
          />
        </q-section>
      </q-card>
    </q-dialog>
  </div>
</template>
<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue';
import { useHaikuListModel } from 'src/models/HaikuListModels';
import lockIcon from 'src/components/LockIcon.vue';
export default defineComponent({
  name: 'haiku-list',
  props: {
    modelValue: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: false,
      default: '俳句王決定戦',
    },
  },
  components: {
    'lock-icon': lockIcon,
  },
  setup(props) {
    const {
      lockIconCondition,
      displayCondition,
      condition,
      insertCondition,
      updateCondition,
      updateSelectedCondition,
      LoadingCondition,
      records,
      tableView,
      columns,
      rows,
      search,
      insertClick,
      insert,
      updateClick,
      update,
      deleteClick,
      deleteRecord,
      rangeChange,
      displaySort,
    } = useHaikuListModel();
    search();

    const detailDisplay = ref(false);

    watch(detailDisplay, () => {
      if (detailDisplay.value) {
        records.value.forEach((it) => (it.detailDisplay = false));
      } else {
        records.value.forEach((it) => (it.detailDisplay = true));
      }
    });

    watch(displaySort, () => {
      rangeChange();
    });

    const viewRecords = computed(() => {
      if (selectPoster.value == null || selectPoster.value == '') {
        return records.value;
      } else {
        return records.value.filter((it) => it.poster == selectPoster.value);
      }
    });
    const selectPoster = ref('' as string | null);
    const posterItems = computed(() =>
      [...new Set(records.value.map((it) => it.poster))].sort()
    );

    return {
      filter: ref(props.modelValue),
      listName: ref(props.label),
      //Models
      lockIconCondition,
      displayCondition,
      condition,
      insertCondition,
      updateCondition,
      updateSelectedCondition,
      LoadingCondition,
      records,
      tableView,
      columns,
      rows,
      search,
      insertClick,
      insert,
      updateClick,
      update,
      deleteClick,
      deleteRecord,
      insertHaikuOmake: ref(false),
      detailDisplay,
      rangeChange,
      displaySort,
      // filter
      viewRecords,
      selectPoster,
      posterItems,
    };
  },
});
</script>
<style>
@font-face {
  font-family: 'haiku';
  src: url(src/fonts/haiku2.ttf) format('truetype');
}
@font-face {
  font-family: 'HinaMincho-Regular';
  src: url(src/fonts/HinaMincho-Regular.ttf) format('truetype');
}
/*input 入力の横幅 */
.form-model {
  width: 200px;
  height: 40px;
}
/*俳句の外枠 */
.haiku-box {
  width: 300px;
  height: 350px;
  margin: 1em 0;
  position: relative;
  padding: 0.5em 1em;
  border-top: solid 2px black;
  border-bottom: solid 2px black;
}
.haiku-box:before,
.haiku-box:after {
  content: '';
  position: absolute;
  top: -10px;
  width: 2px;
  height: -webkit-calc(100% + 20px);
  height: calc(100% + 20px);
  background-color: black;
}
.haiku-box:before {
  left: 10px;
}
.haiku-box:after {
  right: 10px;
}
.haiku-box div {
  margin: 0;
  padding: 0;
}
/*解説の外枠 */
.box28 {
  position: relative;
  margin: 2em 0;
  padding: 25px 10px 7px;
  border: solid 2px #28b315;
  height: 300px;
  width: 300px;
}
.box28 .box-title {
  position: absolute;
  display: inline-block;
  top: -2px;
  left: -2px;
  padding: 0 9px;
  height: 25px;
  line-height: 25px;
  font-size: 17px;
  background: #28b315;
  color: #ffffff;
  font-weight: bold;
}
.box28 p {
  margin: 0;
  padding: 0;
}
</style>
