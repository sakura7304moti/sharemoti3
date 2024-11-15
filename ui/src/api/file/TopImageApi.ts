import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { FileAPIClient } from './FileBaseApi';
export class TopImageApi extends FileAPIClient {
  public async imageSingle(): Promise<AxiosResponse<string, null> | null> {
    const url = '/topImage/image';
    const config = {
      headers: {
        'Content-Type': 'image/jpeg',
      },
    } as AxiosRequestConfig;
    try {
      const res: AxiosResponse<string> = await axios.get(url, config);
      return res;
    } catch {
      return null;
    }
  }

  public singleImageUrl(): string {
    return this.combineUrl('/topImage/image');
  }
}

const api = new TopImageApi();
export default api;
