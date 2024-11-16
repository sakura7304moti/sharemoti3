import { FileAPIClient } from './FileBaseApi';

export class TopNewsApi extends FileAPIClient {
  public news(pageNo: number): Promise<TopNewsResponse | null> {
    const url = '/topNews/' + pageNo;
    const path = this.combineUrl(url);

    return this.httpGet<TopNewsResponse>(path);
  }
}

const api = new TopNewsApi();
export default api;

export interface TopNewsResponse {
  records: Array<TopNews>;
  totalCount: number;
}

interface TopNews {
  page: string;
  createdAt: string;
  total: number;
}
