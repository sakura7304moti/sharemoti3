import { ScraperAPIClient } from "./ScraperBaseApi";
export class HoloSongApi extends ScraperAPIClient {
  public search(): Promise<HoloSongResponse | null> {
    const url = '/holoSong/search';
    const path = this.combineUrl(url);

    return this.httpGet<HoloSongResponse>(path);
  }
  public ori(): Promise<HoloSongResponse | null> {
    const url = '/holoSong/ori';
    const path = this.combineUrl(url);

    return this.httpGet<HoloSongResponse>(path);
  }
  public holoList(): Promise<Array<string> | null> {
    const url = '/holoSong/hololist';
    const path = this.combineUrl(url);

    return this.httpGet<Array<string>>(path);
  }
}

const api = new HoloSongApi();
export default api;
export interface HoloSongResponse {
  records: Array<HoloSongDataState>;
}

interface HoloSongDataState {
  date: string;
  member: string;
  link: string;
  songName: string;
  detail: string;
}
