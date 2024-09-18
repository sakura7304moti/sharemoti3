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
}

interface User {
  name: string;
  screenName: string;
  profileImage: string;
}
