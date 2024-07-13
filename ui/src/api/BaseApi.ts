import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { useRoute } from 'vue-router';
//API呼び出しのためのクラス
export class APIClient {
  public route = useRoute();

  public apiEndpoint = function () {
    if (location.origin.includes('sakura0moti')) {
      return 'http://api.sakura0moti.com';
    } else {
      const originUrl = new URL(window.location.origin);
      originUrl.port = '5000';
      return originUrl.toString();
    }
  };
  public config = {
    headers: {
      'Content-Type': 'application/json',
    },
  } as AxiosRequestConfig;

  public uploadConfig = {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  } as AxiosRequestConfig;

  //URL結合
  public combineUrl(endpoint: string): string {
    return this.apiEndpoint() + endpoint;
  }
  //http post
  public async httpPost<T, U>(url: string, request: T): Promise<U | null> {
    try {
      const res: AxiosResponse<string> = await axios.post<
        T,
        AxiosResponse<string>
      >(url, request, this.config);
      const r = JSON.parse(res.data);
      return r;
    } catch (e) {
      console.log('parse err', e);
      return null;
    }
  }

  //http get
  public async httpGet<T>(url: string): Promise<T | null> {
    try {
      const res: AxiosResponse<string> = await axios.get<
        T,
        AxiosResponse<string>
      >(url);
      const r = JSON.parse(res.data);
      return r;
    } catch {
      return null;
    }
  }

  //file upload
  public async httpUpload<T>(url: string, file: File): Promise<T | null> {
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res: AxiosResponse<string> = await axios.post<
        T,
        AxiosResponse<string>
      >(url, formData, this.uploadConfig);
      const jsonText = JSON.stringify(res.data);
      const r = JSON.parse(jsonText);
      return r;
    } catch (e) {
      console.log('upload err', e);
      return null;
    }
  }
}

export interface PageResult<T> {
  records: Array<T>;
  totalPages: number;
}
