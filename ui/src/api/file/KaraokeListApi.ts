import axios from 'axios';
import { FileAPIClient } from './FileBaseApi';

export class KaraokeListApi extends FileAPIClient {
  public search(): Promise<KaraokeListResponse | null> {
    const url = '/karaoke/search';
    const path = this.combineUrl(url);

    return this.httpGet<KaraokeListResponse>(path);
  }

  public async download(id: number) {
    const url = `/karaoke/download?id=${id}`;
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

const api = new KaraokeListApi();
export default api;

export interface KaraokeListResponse {
  records: Array<KaraokeListRec>;
}

export interface KaraokeListRec {
  id: number;
  fileName: string;
  date: string;
}
