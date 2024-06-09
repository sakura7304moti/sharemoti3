import axios from 'axios';
import { FileAPIClient } from './FileBaseApi';

export class MovieListApi extends FileAPIClient {
  public search(): Promise<MovieListResponse | null> {
    const url = '/movieList/search';
    const path = this.combineUrl(url);
    return this.httpGet<MovieListResponse>(path);
  }

  public async download(fileName: string, poster: string) {
    const url = `/movieList/download?fileName=${fileName}&poster=${poster}`;
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

const api = new MovieListApi();
export default api;

export interface MovieListResponse {
  records: Array<MovieListRec>;
}

export interface MovieListRec {
  id: number;
  fileName: string;
  poster: string;
}
