import { FileAPIClient } from './FileBaseApi';

export class SsbuClipToukeiApi extends FileAPIClient {
  public async rank(text: string): Promise<Rank[] | null> {
    const url = '/ssbu_clip/toukei/count/' + text;
    const path = this.combineUrl(url);
    return this.httpGet<Rank[]>(path);
  }

  public async first(text: string): Promise<First[] | null> {
    const url = '/ssbu_clip/toukei/first/' + text;
    const path = this.combineUrl(url);
    return this.httpGet<First[]>(path);
  }
}

const api = new SsbuClipToukeiApi();
export default api;

interface Rank {
  name: string;
  total: number;
  rank: number;
}

interface First {
  name: string;
  date: string;
}
