import { MainAPIClient } from './MainBaseApi';
export class YakiList2Api extends MainAPIClient {
  //検索
  public search(): Promise<SearchResponse | null> {
    const url = '/yakiList2/search';
    const path = this.combineUrl(url);
    return this.httpGet<SearchResponse>(path);
  }

  //追加
  public insert(request: InsertRequest): Promise<DbResult | null> {
    const url = '/yakiList2/insert';
    const path = this.combineUrl(url);
    return this.httpPost<InsertRequest, DbResult>(path, request);
  }

  //更新
  public update(request: UpdateRequest): Promise<DbResult | null> {
    const url = '/yakiList2/update';
    const path = this.combineUrl(url);
    return this.httpPost<UpdateRequest, DbResult>(path, request);
  }

  //削除
  public dell(request: DeleteRequest): Promise<DbResult | null> {
    const url = '/yakiList2/delete';
    const path = this.combineUrl(url);
    return this.httpPost<DeleteRequest, DbResult>(path, request);
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
