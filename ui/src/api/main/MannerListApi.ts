import { MainAPIClient } from './MainBaseApi';

export class MannerListApi extends MainAPIClient {
  //検索
  public search(
    request: MannerListSearchRequest
  ): Promise<MannerListResponse | null> {
    const url = '/mannerList/search';
    const path = this.combineUrl(url);

    return this.httpPost<MannerListSearchRequest, MannerListResponse>(
      path,
      request
    );
  }

  //追加・更新
  public save(
    request: MannerListRequest
  ): Promise<MannerListSaveResponse | null> {
    const url = '/mannerList/save';
    const path = this.combineUrl(url);

    return this.httpPost<MannerListRequest, MannerListSaveResponse>(
      path,
      request
    );
  }

  //削除
  public delete(
    request: MannerListRequest
  ): Promise<MannerListDeleteResponse | null> {
    const url = '/mannerList/delete';
    const path = this.combineUrl(url);

    return this.httpPost<MannerListRequest, MannerListDeleteResponse>(
      path,
      request
    );
  }
}

const api = new MannerListApi();
export default api;

/*
 *interfaces
 */
export interface MannerListSearchRequest {
  word: string | null;
}

export interface MannerListRequest {
  word: string | null;
}

export interface MannerListResponse {
  records: Array<WordListRec>;
}

interface WordListRec {
  word: string | null;
}

export interface MannerListSaveResponse {
  insert: boolean;
  update: boolean;
}

export interface MannerListDeleteResponse {
  status: boolean;
}
