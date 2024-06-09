import { ScraperAPIClient } from './ScraperBaseApi';

export class HololewdApi extends ScraperAPIClient {
  public search(request: HololewdRequest): Promise<HololewdResponse | null> {
    const url = '/hololewd/search';
    const path = this.combineUrl(url);

    return this.httpPost<HololewdRequest, HololewdResponse>(path, request);
  }

  public holoList(): Promise<Array<string> | null> {
    const url = '/hololewd/hololist';
    const path = this.combineUrl(url);

    return this.httpGet<Array<string>>(path);
  }
}

const api = new HololewdApi();
export default api;

/*
 *interfaces
 */
export interface HololewdRequest {
  pageNo: number;
  pageSize: number;
  flairText: string;
  minScore: number;
}
export interface HololewdResponse {
  records: HololewdRec[];
  totalPages: number;
}
export interface HololewdRec {
  flairText: string;
  url: string;
  date: string;
  score: number;
}
