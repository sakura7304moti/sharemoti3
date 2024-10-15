import { PutResponse } from '../BaseApi';
import { MainAPIClient } from './MainBaseApi';

export class WordList2Api extends MainAPIClient {
  // 検索
  public search(request: SearchRequest): Promise<Array<DataState> | null> {
    const url = '/wordList/search';
    const path = this.combineUrl(url);

    return this.httpPost<SearchRequest, Array<DataState>>(path, request);
  }

  // 追加
  public insert(request: InsertRequest): Promise<PutResponse | null> {
    const url = '/wordList/insert';
    const path = this.combineUrl(url);

    return this.httpPost<InsertRequest, PutResponse>(path, request);
  }

  // 更新
  public update(request: UpdateRequest): Promise<PutResponse | null> {
    const url = '/wordList/update';
    const path = this.combineUrl(url);

    return this.httpPost<UpdateRequest, PutResponse>(path, request);
  }

  // 削除
  public delete(request: DeleteRequest): Promise<PutResponse | null> {
    const url = '/wordList/delete';
    const path = this.combineUrl(url);

    return this.httpPost<DeleteRequest, PutResponse>(path, request);
  }
}

const api = new WordList2Api();
export default api;

/*
 *interfaces
 */
interface SearchRequest {
  text: string;
}

interface InsertRequest {
  word: string;
  detail: string | null;
}

interface UpdateRequest {
  id: number;
  word: string;
  detail: string | null;
}

interface DeleteRequest {
  id: number;
}

interface DataState {
  id: number;
  word: string;
  detail: string | null;
  createAt: string;
  updateAt: string;
}
