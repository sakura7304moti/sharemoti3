<template>
  <div class="row full-width cursor-pointer pixiv-user-icon" @click="onUserClick(findUser?.id ?? -1)">
      <div>
        <q-avatar size="md" v-if="userProfileUrl">
          <img :src="userProfileUrl" />
        </q-avatar>
      </div>
      <div class="q-pl-sm q-pt-xs text-grey text-caption" v-if="findUser">
        <div v-if="shortView">
          {{ findUser.name.substring(0, 8) }}
        </div>
        <div v-else>
          {{ findUser.name }}
        </div>

        <span v-if="findUser.name.length > 8 && shortView">...</span>
      </div>
    </div>
</template>

<script lang="ts">
import { useQuasar } from 'quasar';
import { PixivSearchStore } from 'src/stores/pixiv/PixivSearchStore';
import {defineComponent, onMounted, ref, watch} from 'vue';
import { useRoute, useRouter } from 'vue-router';
export default defineComponent({
  name:'pixiv-user-area',
  props:{
    userId:{
      type: Number,
      required: true
    },
      shortView:{
        type:Boolean,
        required:false,
        default:true
      }

  },
  setup(props){
    const store = PixivSearchStore();
    const quasar = useQuasar();
    const route = useRoute();
    const router = useRouter();
    const userProfileUrl = ref('');
    const findUser = ref(null as null | User);

    const getUserUrl = function(){
      const user = store.getUserbyId(props.userId);
      if(user){
        findUser.value = user;
        const baseUrl = store.findUserImageUrl(user);
        userProfileUrl.value = store.getImageUrl(baseUrl);
      }
    }

    const onUserClick = function(userId:number){
      if(userId == -1){
        return;
      }
      store.resetCondition();
      const beforePath = route.path.toString();
      router.push({
        path: '/pixiv',
        query: {
          user:userId,
          minview:10000,
          fetch:'true'
        },
      });

      console.log('beforePath',beforePath);
      if(beforePath == '/pixiv'){
        store.addUser(userId);
        store.searchIllust();
      }
      quasar.notify({
          color: 'secondary',
          position: 'top',
          message: 'ユーザー名で検索',
        });
    }

    // 初回起動時
    onMounted(() => {
      getUserUrl();
    })

    // 変更検知
    watch(props,() => {
      getUserUrl();
    })

    return {
      findUser,
      userProfileUrl,
      onUserClick,
    }
  }
})
interface User {
  id: number;
  name: string;
  account: string;
  profileImageUrlSquareMedium: string;
  profileImageUrlMedium: string;
  profileImageUrlLarge: string;
}
</script>
