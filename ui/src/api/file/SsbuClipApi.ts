import axios from 'axios';
import { FileAPIClient } from './FileBaseApi';

export class SsbuClipApi extends FileAPIClient {
  public search(request: SearchRequest): Promise<SearchResponse | null> {
    const url = '/ssbu_clip/search';
    const path = this.combineUrl(url);
    return this.httpPost<SearchRequest, SearchResponse>(path, request);
  }

  public date(): Promise<Array<string> | null> {
    const url = 'ssbu_clip/date';
    const path = this.combineUrl(url);
    return this.httpGet<Array<string>>(path);
  }

  public category(): Promise<Array<string> | null> {
    const url = 'ssbu_clip/category';
    const path = this.combineUrl(url);
    return this.httpGet<Array<string>>(path);
  }

  public async movie(dir_name: string, file_name: string) {
    const url = `ssbu_clip/movie?dir_name=${dir_name}&file_name=${file_name}`;
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

  public updateTable() {
    const url = 'ssbu_clip/update';
    const path = this.combineUrl(url);

    return this.httpGet<StatusResponse>(path);
  }

  public static MovieUrl(dir_name: string, file_name: string) {
    const url = `ssbu_clip/movie?dir_name=${dir_name}&file_name=${file_name}`;

    const baseApi = new FileAPIClient();
    const path = baseApi.combineUrl(url);
    return path;
  }
}

const api = new SsbuClipApi();
export default api;

interface SearchRequest {
  text: string;
  charName: string;
  ssbuName: string;
  date: string;
  cate: string;
  pageNo: number;
}

interface SearchResponse {
  records: SsbuClip[];
  totalCount: number;
}

interface SsbuClip {
  id: number;
  title: string;
  fileName: string;
  dirName: string;
  charName: string;
  ssbuName: string;
  date: string;
  fullIcon: string;
  smallIcon: string;
}

interface StatusResponse {
  statu: string;
}
