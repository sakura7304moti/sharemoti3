import { MainAPIClient } from './MainBaseApi';
export class NameList2Api extends MainAPIClient {
  //検索
  public search(): Promise<SearchResponse | null> {
    const url = '/nameList2/search';
    const path = this.combineUrl(url);
    return this.httpGet<SearchResponse>(path);
  }

  //追加
  public insert(request: InsertRequest): Promise<DbResult | null> {
    const url = '/nameList2/insert';
    const path = this.combineUrl(url);
    return this.httpPost<InsertRequest, DbResult>(path, request);
  }

  //更新
  public update(request: UpdateRequest): Promise<DbResult | null> {
    const url = '/nameList2/update';
    const path = this.combineUrl(url);
    return this.httpPost<UpdateRequest, DbResult>(path, request);
  }

  //削除
  public dell(request: DeleteRequest): Promise<DbResult | null> {
    const url = '/nameList2/delete';
    const path = this.combineUrl(url);
    return this.httpPost<DeleteRequest, DbResult>(path, request);
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
interface SearchResponse {
  records: DataState[];
}
interface DataState {
  id: number;
  name: string;
  ssbuName: string;
  createAt: string;
  updateAt: string;
}
interface DbResult {
  success: boolean;
  errorText: string;
}
