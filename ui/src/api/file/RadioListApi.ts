import axios from 'axios';
import { FileAPIClient } from './FileBaseApi';

export class RadioListApi extends FileAPIClient {
  public search(): Promise<RadioListResponse | null> {
    const url = '/radio/search';
    const path = this.combineUrl(url);

    return this.httpGet<RadioListResponse>(path);
  }

  public async download(id: number) {
    const url = `/radio/download?id=${id}`;
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

const api = new RadioListApi();
export default api;

export interface RadioListResponse {
  records: Array<RadioListRec>;
}

export interface RadioListRec {
  id: number;
  fileName: string;
  date: string;
}
