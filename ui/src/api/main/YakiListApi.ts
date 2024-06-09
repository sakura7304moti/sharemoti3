import { MainAPIClient } from './MainBaseApi';

export class YakiListApi extends MainAPIClient {
  //検索
  public search(
    request: YakiListSearchRequest
  ): Promise<YakiListResponse | null> {
    const url = '/yakiList/search';
    const path = this.combineUrl(url);

    return this.httpPost<YakiListSearchRequest, YakiListResponse>(
      path,
      request
    );
  }

  //追加・更新
  public save(request: YakiListRequest): Promise<YakiListSaveResponse | null> {
    const url = '/yakiList/save';
    const path = this.combineUrl(url);

    return this.httpPost<YakiListRequest, YakiListSaveResponse>(path, request);
  }

  //削除
  public delete(
    request: YakiListRequest
  ): Promise<YakiListDeleteResponse | null> {
    const url = '/yakiList/delete';
    const path = this.combineUrl(url);

    return this.httpPost<YakiListRequest, YakiListDeleteResponse>(
      path,
      request
    );
  }
}

const api = new YakiListApi();
export default api;

/*
 *interfaces
 */
export interface YakiListSearchRequest {
  text: string | null;
}

export interface YakiListRequest {
  word: string | null;
  yaki: string | null;
}

export interface YakiListResponse {
  records: Array<WordListRec>;
}

interface WordListRec {
  word: string | null;
  yaki: string | null;
}

export interface YakiListSaveResponse {
  insert: boolean;
  update: boolean;
}

export interface YakiListDeleteResponse {
  status: boolean;
}
