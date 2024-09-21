import axios from 'axios';
import { ScraperAPIClient } from './ScraperBaseApi';
export class HolotwitterApi extends ScraperAPIClient {
  public searchTweet(request: SearchRequest): Promise<SearchResponse | null> {
    const url = '/holotwitter/search';
    const path = this.combineUrl(url);
    return this.httpPost<SearchRequest, SearchResponse>(path, request);
  }

  public getAcount(): Promise<Array<User> | null> {
    const url = '/holotwitter/acount';
    const path = this.combineUrl(url);
    return this.httpGet<Array<User>>(path);
  }

  public getMedia(id: number): Promise<Array<Media> | null> {
    const url = '/holotwitter/media/' + id;
    const path = this.combineUrl(url);
    return this.httpGet<Array<Media>>(path);
  }

  public async movieDownload(movieUrl: string) {
    const url = `/holotiwtter/movie?url=${movieUrl}`;
    const path = this.combineUrl(url);

    await axios({
      url: path,
      method: 'GET',
      responseType: 'blob',
    }).then((response) => {
      if (response) {
        console.log('download', response);
        return response;
      }
    });
  }
}

const api = new HolotwitterApi();
export default api;

interface SearchRequest {
  text: string;
  acountName: string;
  startDate: string;
  pageNo: number;
}

interface SearchResponse {
  records: Tweet[];
  totalCount: number;
}

interface Tweet {
  id: number;
  text: string;
  createdAt: string;
  userScreenName: string;
  userName: string;
  profileImage: string;
  medias: Media[];
}

interface User {
  name: string;
  screenName: string;
  profileImage: string;
}

interface Media {
  type: string;
  url: string;
  mediaUrl: string;
  metaImageUrl: string;
}
