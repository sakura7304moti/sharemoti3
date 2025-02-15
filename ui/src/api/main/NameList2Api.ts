import { PutResponse } from '../BaseApi';
import { MainAPIClient } from './MainBaseApi';
export class NameList2Api extends MainAPIClient {
  //検索
  public search(): Promise<DataState[] | null> {
    const url = '/nameList2/search';
    const path = this.combineUrl(url);
    return this.httpGet<DataState[]>(path);
  }

  //追加
  public insert(request: InsertRequest): Promise<PutResponse | null> {
    const url = '/nameList2/insert';
    const path = this.combineUrl(url);
    return this.httpPost<InsertRequest, PutResponse>(path, request);
  }

  //更新
  public update(request: UpdateRequest): Promise<PutResponse | null> {
    const url = '/nameList2/update';
    const path = this.combineUrl(url);
    return this.httpPost<UpdateRequest, PutResponse>(path, request);
  }

  //削除
  public dell(request: DeleteRequest): Promise<PutResponse | null> {
    const url = '/nameList2/delete';
    const path = this.combineUrl(url);
    return this.httpPost<DeleteRequest, PutResponse>(path, request);
  }
}

const api = new NameList2Api();
export default api;

/*
 *interfaces
 */
interface InsertRequest {
  name: string;
  ssbuName: string;
}
interface UpdateRequest {
  id: number;
  name: string;
  ssbuName: string;
}
interface DeleteRequest {
  id: number;
}
interface DataState {
  id: number;
  name: string;
  ssbuName: string;
  createAt: string;
  updateAt: string;
}
