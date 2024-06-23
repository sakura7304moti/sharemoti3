import { PageResult } from '../BaseApi';
import { ScraperAPIClient } from './ScraperBaseApi';

export class TwitterApi extends ScraperAPIClient {
  public search(
    request: TwitterRequest
  ): Promise<PageResult<TwitterResponse> | null> {
    const url = '/twitter/search'; //twitter/search
    const path = this.combineUrl(url);

    return this.httpPost<TwitterRequest, PageResult<TwitterResponse>>(
      path,
      request
    );
  }

  public holoList(): Promise<HoloNameResponse | null> {
    const url = '/twitter/hololist'; //twitter/hololist
    const path = this.combineUrl(url);

    return this.httpGet<HoloNameResponse>(path);
  }
}

const api = new TwitterApi();
export default api;

/*
 *interfaces
 */
export interface TwitterRequest {
  page_no: number | null;
  page_size: number | null;
  hashtag: string | null;
  start_date: string | null;
  end_date: string | null;
  user_name: string | null;
  mode: string | null;
  min_like: number | null;
  max_like: number | null;
}
export interface TwitterResponse {
  hashtag: string;
  mode: string;
  url: string;
  date: string;
  images: Array<string>;
  userId: string;
  userName: string;
  likeCount: number;
}
interface HoloNameResponse {
  records: HoloName[];
}

interface HoloName {
  hashtag: string;
  url: string;
}
