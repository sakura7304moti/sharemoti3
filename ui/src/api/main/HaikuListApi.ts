import { MainAPIClient } from './MainBaseApi';
import { PutResponse } from '../BaseApi';

export class HaikuListApi extends MainAPIClient {
  public search(): Promise<DataState[] | null> {
    const url = '/haikuList/search';
    const path = this.combineUrl(url);

    return this.httpGet<DataState[]>(path);
  }

  public insert(request: HaikuListInsertRequest): Promise<PutResponse | null> {
    const url = '/haikuList/insert';
    const path = this.combineUrl(url);

    return this.httpPost<HaikuListInsertRequest, PutResponse>(path, request);
  }

  public update(request: HaikuListUpdateReqeust): Promise<PutResponse | null> {
    const url = '/haikuList/update';
    const path = this.combineUrl(url);

    return this.httpPost<HaikuListUpdateReqeust, PutResponse>(path, request);
  }

  public delete(id: number): Promise<PutResponse | null> {
    const url = '/haikuList/delete';
    const path = this.combineUrl(url);
    const request = { id: id } as HaikuListDeleteRequest;

    return this.httpPost<HaikuListDeleteRequest, PutResponse>(path, request);
  }
}

const api = new HaikuListApi();
export default api;

/*
 * request
 */
export interface HaikuListSearchRequest {
  id: number;
  haikuText: string;
  poster: string;
  detail: string;
}

export interface HaikuListInsertRequest {
  first: string;
  second: string;
  third: string;
  poster: string;
  detail: string;
}

export interface HaikuListUpdateReqeust {
  id: number;
  first: string;
  second: string;
  third: string;
  poster: string;
  detail: string;
}

export interface HaikuListDeleteRequest {
  id: number;
}

/*
 *response
 */

export interface HaikuListSearchResponse {
  records: DataState[];
}

interface DataState {
  id: number;
  first: string;
  second: string;
  third: string;
  poster: string;
  detail: string;
  createAt: string;
  updateAt: string;
}

export interface HaikuListStatusResponse {
  success: boolean;
  errorText: string;
}
