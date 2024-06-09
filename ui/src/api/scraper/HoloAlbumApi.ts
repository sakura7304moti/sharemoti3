import { ScraperAPIClient } from './ScraperBaseApi';
export class HoloSongApi extends ScraperAPIClient {
  public searchAlbum(): Promise<AlbumRecord | null> {
    const url = '/holosong/album';
    const path = this.combineUrl(url);
    return this.httpGet<AlbumRecord>(path);
  }

  public searchMusic(): Promise<MusicRecored | null> {
    const url = '/holosong/album/music';
    const path = this.combineUrl(url);
    return this.httpGet<MusicRecored>(path);
  }
}
const api = new HoloSongApi();
export default api;

interface AlbumRecord {
  records: Array<Album>;
}

interface MusicRecored {
  records: Array<Music>;
}

interface Album {
  albumName: string;
  artist: string;
  playlistLink: string;
  date: string;
  imageLink: string;
}
interface Music {
  musicName: string;
  artist: string;
  musicLink: string;
  playlistLink: string;
  imageLink: string;
}
