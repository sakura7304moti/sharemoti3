import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { MainAPIClient } from './MainBaseApi';
export class ImageListApi extends MainAPIClient {
  public search(): Promise<ImageListSearchResponse | null> {
    const url = '/imageList/search';
    const path = this.combineUrl(url);

    return this.httpGet<ImageListSearchResponse>(path);
  }

  public upload(file: File): Promise<ImageListUploadResponse | null> {
    const url = '/imageList/upload';
    const path = this.combineUrl(url);

    return this.httpUpload<ImageListUploadResponse>(path, file);
  }

  public async download(
    fileName: string,
    ext: string
  ): Promise<AxiosResponse<string, null> | null> {
    const url = `/imageList/download?fileName=${fileName}&ext=${ext}`;
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

  public insert(
    request: ImageListInsertRequest
  ): Promise<ImageListStatusResult | null> {
    const url = '/imageList/insert';
    const path = this.combineUrl(url);

    return this.httpPost<ImageListInsertRequest, ImageListStatusResult>(
      path,
      request
    );
  }

  public update(
    request: ImageListUpdateRequest
  ): Promise<ImageListStatusResult | null> {
    const url = '/imageList/update';
    const path = this.combineUrl(url);
    return this.httpPost<ImageListUpdateRequest, ImageListStatusResult>(
      path,
      request
    );
  }

  public dell(
    request: ImageListDeleteRequest
  ): Promise<ImageListStatusResult | null> {
    const url = '/imageList/delete';
    const path = this.combineUrl(url);
    return this.httpPost<ImageListDeleteRequest, ImageListStatusResult>(
      path,
      request
    );
  }
}

const api = new ImageListApi();
export default api;

/*リクエスト */
export interface ImageListInsertRequest {
  fileName: string;
  ext: string;
  title: string;
  detail: string;
}

export interface ImageListDownloadRequest {
  fileName: string;
}

export interface ImageListUpdateRequest {
  id: number;
  title: string;
  detail: string;
}

export interface ImageListDeleteRequest {
  id: number;
}

/*レスポンス */
export interface ImageListSearchResponse {
  records: searchRec[];
}

interface searchRec {
  id: number;
  fileName: string;
  ext: string;
  title: string;
  detail: string;
  createAt: string;
  updateAt: string;
}

export interface ImageListStatusResult {
  success: boolean;
  errorText: string;
}

export interface ImageListUploadResponse {
  fileName: string;
}
