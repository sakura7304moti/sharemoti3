import axios from 'axios';
import { FileAPIClient } from './FileBaseApi';

export class SsbuListApi extends FileAPIClient {
  public search(): Promise<SsbuListResponse | null> {
    const url = '/ssbu/search';
    const path = this.combineUrl(url);

    return this.httpGet<SsbuListResponse>(path);
  }

  public async download(filePath: string) {
    const url = `/ssbu/download?path=${filePath}`;
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

const api = new SsbuListApi();
export default api;

export interface SsbuListResponse {
  records: Array<SsbuListRec>;
}

export interface SsbuListRec {
  id: number;
  fileName: string;
  date: string;
  year: string;
  path:string;
}
