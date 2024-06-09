import axios from 'axios';
import { FileAPIClient } from './FileBaseApi';

export class VoiceListApi extends FileAPIClient {
  public search(): Promise<VoiceListResponse | null> {
    const url = '/voice/search';
    const path = this.combineUrl(url);

    return this.httpGet<VoiceListResponse>(path);
  }

  public async download(id: number) {
    const url = `/voice/download?id=${id}`;
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

const api = new VoiceListApi();
export default api;

export interface VoiceListResponse {
  records: Array<VoiceListRec>;
}

export interface VoiceListRec {
  id: number;
  fileName: string;
}
