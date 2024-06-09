<template>
  <q-layout>
    <q-header elevated class="bg-secondary">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          <a @click.prevent="router.replace('/scraper/')" class="text-white"
            >Scraper</a
          >
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" class="q-pa-md bg-grey-4" bordered>
      <q-item-label header> Pages</q-item-label>
      <q-list>
        <template v-for="(menuItem, index) in menuList" :key="index">
          <q-item
            clickable
            :active="menuItem.label === 'Outbox'"
            v-ripple
            @click="router.replace(menuItem.link)"
          >
            <q-item-section avatar>
              <q-icon :name="menuItem.icon" :color="menuItem.iconColor" />
            </q-item-section>
            <q-item-section class="text-h6">
              {{ menuItem.label }}
            </q-item-section>
          </q-item>
          <q-separator :key="'sep' + index" v-if="menuItem.separator" />
        </template>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view class="q-pa-md" />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'MainLayout',

  setup() {
    const leftDrawerOpen = ref(false);
    const menuList = [
      {
        label: 'Twitter',
        icon: 'image',
        iconColor: 'primary',
        link: '/scraper/twitter',
      },
      {
        label: 'Hololewd',
        icon: 'image',
        iconColor: 'red-6',
        link: '/scraper/hololewd',
      },
    ] as MenuItem[];
    const router = useRouter();
    return {
      leftDrawerOpen,
      menuList,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
      router,
    };
  },
});
interface MenuItem {
  icon: string;
  iconColor: string;
  label: string;
  separator: string;
  link: string;
}
</script>
