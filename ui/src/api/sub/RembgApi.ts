import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { SubAPIClient } from './SubBaseApi';
export class RembgApi extends SubAPIClient {
  public async upload(file: File): Promise<string | null> {
    const url = '/rembg';
    const path = this.combineUrl(url);

    return this.httpUpload<string>(path, file);
  }

  public async uploadAnime(file: File): Promise<string | null> {
    const url = '/rembg/anime';
    const path = this.combineUrl(url);

    return this.httpUpload<string>(path, file);
  }

  public async download(
    fileName: string
  ): Promise<AxiosResponse<string, null> | null> {
    const url = `/rembg/download?fileName=${fileName}`;
    const config = {
      headers: {
        'Content-Type': 'image/png',
      },
    } as AxiosRequestConfig;
    try {
      const res: AxiosResponse<string> = await axios.get(url, config);
      return res;
    } catch {
      return null;
    }
  }
}
