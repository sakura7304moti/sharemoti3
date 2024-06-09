import axios from 'axios';
import { ScraperAPIClient } from './ScraperBaseApi';

export class HoloYoutubeApi extends ScraperAPIClient {
  public search(): Promise<HoloYoutubeResponse | null> {
    const url = '/holosong/yt';
    const path = this.combineUrl(url);

    return this.httpGet<HoloYoutubeResponse>(path);
  }

  public async download(fileName: string) {
    const url = `/holosong/yt/download?fileName=${fileName}`;
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

const api = new HoloYoutubeApi();
export default api;

export interface HoloYoutubeResponse {
  records: Array<HoloYoutubeRec>;
}

export interface HoloYoutubeRec {
  songName: string;
  member: string;
  link: string;
  fileName: string;
  date: string;
}
