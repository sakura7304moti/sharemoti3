<template>
  <q-btn icon="settings" @click.prevent="dialogView = true" round />
  <q-dialog v-model="dialogView" position="top">
    <q-card>
      <q-card-section>
        <div class="text-h5 text-weight-light row q-gutter-md q-pa-md">
          ページ設定
          <div style="margin: 0 0 0 auto">
            <q-btn
              label="閉じる"
              @click.prevent="dialogView = false"
              flat
              text-color="primary"
            />
          </div>
        </div>
        <div class="q-pa-md">
          <div class="row q-gutter-md">
            <div class="setting-radio-text-left">ページ一覧の表示方法</div>
            <div class="setting-radio-text-right">
              <div>
                <q-radio
                  val="default"
                  label="画像で表示(初期値)"
                  v-model="setting.indexType"
                />
              </div>
              <div>
                <q-radio
                  val="light"
                  label="軽量版で表示"
                  v-model="setting.indexType"
                />
              </div>
            </div>
          </div>
          <div class="row q-gutter-md q-pt-md">
            <div class="setting-radio-text-left">drawerの表示方法</div>
            <div class="setting-radio-text-right">
              <div>
                <q-radio
                  val="default"
                  label="画像で表示(初期値)"
                  v-model="setting.drawerType"
                />
              </div>
              <div>
                <q-radio
                  val="light"
                  label="軽量版で表示"
                  v-model="setting.drawerType"
                />
              </div>
            </div>
          </div>
          <div style="margin: 0 0 0 auto" v-if="checkReset">
            <q-btn
              label="初期値に戻す"
              @click.prevent="onResetClick"
              text-color="grey"
              icon="restart_alt"
              flat
            />
          </div>
          <div v-else style="height: 36px"></div>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script lang="ts">
import { SetupContext, computed, defineComponent, ref, watch } from 'vue';
import { LocalStrageObject } from 'src/utils/localStrageSupport';
export default defineComponent({
  name: 'page-setting',
  setup(_, context: SetupContext) {
    const dialogView = ref(false);

    //ローカルストレージのキーと値
    const settingKey = 'page-setting';
    const defaultSetting = ref({
      indexType: 'default',
      drawerType: 'default',
    } as Setting);
    const setting = ref({
      indexType: 'default',
      drawerType: 'default',
    } as Setting);

    //ローカルストレージの初期化
    const model = new LocalStrageObject();
    const getValue = model.getterValue<Setting>(settingKey);
    if (getValue) {
      setting.value = getValue;
    } else {
      model.setterValue(settingKey, defaultSetting.value);
    }

    //保存と初期化ボタン
    const updated = ref(false);
    const onSaveClick = function () {
      model.setterValue<Setting>(settingKey, setting.value);
      context.emit('update');
      updated.value = true;
    };
    const onResetClick = function () {
      setting.value.indexType = defaultSetting.value.indexType;
      setting.value.drawerType = defaultSetting.value.drawerType;
    };
    const checkReset = computed(
      () =>
        defaultSetting.value.indexType != setting.value.indexType ||
        defaultSetting.value.drawerType != setting.value.drawerType
    );
    watch(setting.value, () => {
      onSaveClick();
    });
    watch(dialogView, () => {
      if (dialogView.value == false && updated.value == true) {
        location.reload();
      }
    });
    return {
      dialogView,
      setting,
      model,
      onSaveClick,
      onResetClick,
      checkReset,
    };
  },
});
export interface Setting {
  indexType: 'default' | 'light';
  drawerType: 'default' | 'light';
}
</script>
<style>
.setting-radio-text-left {
  padding-right: 32px;
  width: 200px;
}
.setting-radio-text-right {
  color: grey;
}
</style>
