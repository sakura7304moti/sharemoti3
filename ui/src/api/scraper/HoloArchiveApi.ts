import { ScraperAPIClient } from './ScraperBaseApi';
export class HoloArchiveApi extends ScraperAPIClient {
  public SearchMovie(request: MovieSearchState): Promise<MovieState | null> {
    const url = '/holoArchive/search/movie';
    const path = this.combineUrl(url);
    return this.httpPost<MovieSearchState, MovieState>(path, request);
  }

  public GetChannel(): Promise<ChannelState | null> {
    const url = '/holoArchive/search/channel';
    const path = this.combineUrl(url);
    return this.httpGet<ChannelState>(path);
  }
}
const api = new HoloArchiveApi();
export default api;

interface ChannelState {
  records: Array<Channel>;
}

interface MovieSearchState {
  title: string;
  fromDate: string;
  toDate: string;
  channelId: string;
  movieType: string;
  pageNo: number;
  pageSize: number;
}

interface MovieState {
  records: Array<Movie>;
  totalPages: number;
}

interface Movie {
  id: string;
  url: string;
  title: string;
  date: string;
  channelId: string;
  viewCount: number;
  thumbnailUrl: string;
  movieType: 'movie' | 'live' | 'short';
}

interface Channel {
  channelId: string;
  channelName: string;
  description: string;
  headerUrl: string;
  avatarUrl: string;
}
