import { PutResponse } from '../BaseApi';
import { MainAPIClient } from './MainBaseApi';
export class YakiList2Api extends MainAPIClient {
  //検索
  public search(): Promise<DataState[] | null> {
    const url = '/yakiList/search';
    const path = this.combineUrl(url);
    return this.httpGet<DataState[]>(path);
  }

  //追加
  public insert(request: InsertRequest): Promise<PutResponse | null> {
    const url = '/yakiList/insert';
    const path = this.combineUrl(url);
    return this.httpPost<InsertRequest, PutResponse>(path, request);
  }

  //更新
  public update(request: UpdateRequest): Promise<PutResponse | null> {
    const url = '/yakiList/update';
    const path = this.combineUrl(url);
    return this.httpPost<UpdateRequest, PutResponse>(path, request);
  }

  //削除
  public dell(request: DeleteRequest): Promise<PutResponse | null> {
    const url = '/yakiList/delete';
    const path = this.combineUrl(url);
    return this.httpPost<DeleteRequest, PutResponse>(path, request);
  }
}

const api = new YakiList2Api();
export default api;

/*
 *interfaces
 */
interface InsertRequest {
  word: string;
  yaki: string;
}
interface UpdateRequest {
  id: number;
  word: string;
  yaki: string;
}
interface DeleteRequest {
  id: number;
}
interface SearchResponse {
  records: DataState[];
}
interface DataState {
  id: number;
  word: string;
  yaki: string;
  createAt: string;
  updateAt: string;
}
interface DbResult {
  success: boolean;
  errorText: string;
}
