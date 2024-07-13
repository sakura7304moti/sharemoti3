import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { ScraperAPIClient } from './ScraperBaseApi';

export class PixivApi extends ScraperAPIClient {
  public search_illust(
    request: IllustSearchRequest
  ): Promise<Array<Illust> | null> {
    const url = '/pixiv/search/illust';
    const path = this.combineUrl(url);

    return this.httpPost<IllustSearchRequest, Array<Illust>>(path, request);
  }

  public search_illust_count(
    request: IllustSearchRequest
  ): Promise<number | null> {
    const url = '/pixiv/search/illust/count';
    const path = this.combineUrl(url);

    return this.httpPost<IllustSearchRequest, number>(path, request);
  }

  public get_illust(id: number): Promise<IllustImage | null> {
    const url = '/pixiv/illust/' + id;
    const path = this.combineUrl(url);

    return this.httpGet<IllustImage>(path);
  }

  public get_images(id: number): Promise<Array<Image> | null> {
    const url = '/pixiv/images?id=' + id;
    const path = this.combineUrl(url);
    return this.httpGet<Array<Image>>(path);
  }

  public async download(url: string): Promise<AxiosResponse<string> | null> {
    const config = {
      headers: {
        'Content-Type': 'image/jpeg',
      },
    } as AxiosRequestConfig;
    if (url.includes('png')) {
      config.headers = {
        'Content-Type': 'image/png',
      };
    }
    try {
      const res: AxiosResponse<string> = await axios.get(url, config);
      return res;
    } catch {
      return null;
    }
  }

  public search_hashtags(name: string): Promise<Array<Hashtag> | null> {
    const url = '/pixiv/search/hashtags?name=' + name;
    const path = this.combineUrl(url);
    return this.httpGet<Array<Hashtag>>(path);
  }

  public search_users(name: string): Promise<Array<User> | null> {
    const url = '/pixiv/search/users?name=' + name;
    const path = this.combineUrl(url);
    return this.httpGet<Array<User>>(path);
  }

  public holoname(): Promise<Array<HoloName> | null> {
    const url = '/pixiv/option/holoname';
    const path = this.combineUrl(url);
    return this.httpGet<Array<HoloName>>(path);
  }
}

const api = new PixivApi();
export default api;

interface IllustSearchRequest {
  text: string;
  hashtags: string[];
  userIds: number[];
  minTotalBookmarks: number;
  minTotalView: number;
  pageNo: number;
  pageSize: number;
}

interface Illust {
  id: number;
  title: string;
  type: string;
  userId: number;
  createDate: string;
  pageCount: number;
  width: number;
  height: number;
  sanityLevel: number;
  totalView: number;
  totalBookmarks: number;
  illustAiType: number;
}

interface IllustImage extends Illust {
  images: Image[];
}

interface Image {
  id: number;
  line: number;
  imageUrlSquareMedium: string | null;
  imageUrlMedium: string | null;
  imageUrlLarge: string | null;
  originalImageUrl: string | null;
}

interface Hashtag {
  name: string;
  translatedName: string;
}

interface User {
  id: number;
  name: string;
  account: string;
  profileImageUrlSquareMedium: string;
  profileImageUrlMedium: string;
  profileImageUrlLarge: string;
}

interface HoloName {
  name: string;
  hashtag: string;
  url: string;
}
