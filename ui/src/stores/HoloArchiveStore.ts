import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from 'src/api/scraper/HoloArchiveApi';
export const useHoloArchiveStore = defineStore('holo-archive', {
  state: () => {
    return {
      records: ref([] as Movie[]),
      playMovie: ref(''),
      filter: ref({
        channelId: '',
        fromDate: '',
        toDate: '',
        movieType: '',
        title: '',
      } as FilterState),
      beforeFilter: ref({
        channelId: '',
        fromDate: '',
        toDate: '',
        movieType: '',
        title: '',
      } as FilterState),
      page: ref({
        pageNo: 1,
        pageCount: 0,
        pageSize: 40,
      } as PageState),
      channels: ref([] as Channel[]),
      loading: ref(false),
    };
  },
  getters: {
    isPageReset: function () {
      if (
        this.filter.channelId != this.beforeFilter.channelId ||
        this.filter.fromDate != this.beforeFilter.fromDate ||
        this.filter.toDate != this.beforeFilter.toDate ||
        this.filter.title != this.beforeFilter.title ||
        this.filter.movieType != this.beforeFilter.movieType
      ) {
        return true;
      } else {
        return false;
      }
    },
  },
  actions: {
    getMovies: async function () {
      /**
       * アーカイブを取得
       */
      this.loading = true;
      this.records.splice(0);
      this.argmentQuery();

      if (this.isPageReset) {
        this.page.pageNo = 1;
      }
      await api
        .SearchMovie({
          title: this.filter.title,
          fromDate: this.filter.fromDate,
          toDate: this.filter.toDate,
          channelId: this.filter.channelId,
          movieType: this.filter.movieType,
          pageNo: this.page.pageNo,
          pageSize: this.page.pageSize,
        })
        .then((response) => {
          if (response) {
            console.log('response', response);
            response.records.forEach((it) => {
              this.records.push({
                id: it.id,
                url: it.url,
                title: it.title,
                date: new Date(it.date.split(' ')[0]),
                channelId: it.channelId,
                avatarUrl: this.channels.filter(
                  (c) => c.channelId == it.channelId
                )[0].avatarUrl,
                viewCount: it.viewCount,
                thumbnailUrl: it.thumbnailUrl.replace(
                  'maxresdefault',
                  'mqdefault'
                ),
                movieType: it.movieType,
              });
            });
            this.page.pageCount = response.totalPages;
          }
        });
      this.setBeforeQuery();
      this.loading = false;
    },
    getChannels: function () {
      /**
       * チャンネルを取得
       */
      this.channels.splice(0);
      api.GetChannel().then((response) => {
        if (response) {
          response.records.forEach((it) => this.channels.push(it));
        }
      });
    },

    setPlayMovie: function (url: string) {
      console.log('play', url);
      this.playMovie = url;
    },

    setBeforeQuery: function () {
      this.beforeFilter.title = this.filter.title;
      this.beforeFilter.fromDate = this.filter.fromDate;
      this.beforeFilter.toDate = this.filter.toDate;
      this.beforeFilter.channelId = this.filter.channelId;
      this.beforeFilter.movieType = this.filter.movieType;
    },
    argmentQuery: function () {
      if (this.filter.movieType == undefined) this.filter.movieType = '';
    },
  },
});
interface Movie {
  id: string;
  url: string;
  title: string;
  date: Date;
  channelId: string;
  avatarUrl: string;
  viewCount: number;
  thumbnailUrl: string;
  movieType: 'movie' | 'live' | 'short';
}
interface FilterState {
  channelId: string;
  fromDate: string;
  toDate: string;
  movieType: string;
  title: string;
}
interface PageState {
  pageNo: number;
  pageCount: number;
  pageSize: number;
}
interface Channel {
  channelId: string;
  channelName: string;
  description: string;
  headerUrl: string;
  avatarUrl: string;
}
/**
 * State
 * 検索データ
 * ページング済み検索データ
 * ページデータ
 * 検索条件
 *
 *
 *
 *
 *
 */
