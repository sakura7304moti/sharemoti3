import { MainAPIClient } from './MainBaseApi';

export class SchoolListApi extends MainAPIClient {
  //検索
  public search(
    request: SchoolListSearchRequest
  ): Promise<SchoolListResponse | null> {
    const url = '/schoolList/search';
    const path = this.combineUrl(url);

    return this.httpPost<SchoolListSearchRequest, SchoolListResponse>(
      path,
      request
    );
  }

  //追加・更新
  public save(
    request: SchoolListRequest
  ): Promise<SchoolListSaveResponse | null> {
    const url = '/schoolList/save';
    const path = this.combineUrl(url);

    return this.httpPost<SchoolListRequest, SchoolListSaveResponse>(
      path,
      request
    );
  }

  //削除
  public delete(
    request: SchoolListRequest
  ): Promise<SchoolListDeleteResponse | null> {
    const url = '/schoolList/delete';
    const path = this.combineUrl(url);

    return this.httpPost<SchoolListRequest, SchoolListDeleteResponse>(
      path,
      request
    );
  }
}

const api = new SchoolListApi();
export default api;

/*
 *interfaces
 */
export interface SchoolListSearchRequest {
  word: string | null;
}

export interface SchoolListRequest {
  word: string | null;
}

export interface SchoolListResponse {
  records: Array<WordListRec>;
}

interface WordListRec {
  word: string | null;
}

export interface SchoolListSaveResponse {
  insert: boolean;
  update: boolean;
}

export interface SchoolListDeleteResponse {
  status: boolean;
}
