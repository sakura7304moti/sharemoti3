import { MainAPIClient } from './MainBaseApi';

export class NameListApi extends MainAPIClient {
  //検索
  public search(request: NameListRequest): Promise<NameListResponse | null> {
    const url = '/nameList/search';
    const path = this.combineUrl(url);

    return this.httpPost<NameListRequest, NameListResponse>(path, request);
  }

  //追加・更新
  public insert(
    request: NameListRequest
  ): Promise<NameListSaveResponse | null> {
    const url = '/nameList/insert';
    const path = this.combineUrl(url);

    return this.httpPost<NameListRequest, NameListSaveResponse>(path, request);
  }

  public update(
    request: NameListUpdateRequest
  ): Promise<NameListSaveResponse | null> {
    const url = '/nameList/update';
    const path = this.combineUrl(url);

    return this.httpPost<NameListUpdateRequest, NameListSaveResponse>(
      path,
      request
    );
  }

  //削除
  public delete(
    request: NameListRequest
  ): Promise<NameListDeleteResponse | null> {
    const url = '/nameList/delete';
    const path = this.combineUrl(url);

    return this.httpPost<NameListRequest, NameListDeleteResponse>(
      path,
      request
    );
  }

  //初期update
  public init(): Promise<null> {
    const url = '/nameList/init';
    const path = this.combineUrl(url);
    return this.httpGet<null>(path);
  }

  //スマブラのキャラ名一覧
  public ssbu_names(): Promise<SsbuName | null> {
    const url = '/nameList/names';
    const path = this.combineUrl(url);
    return this.httpGet(path);
  }
}

const api = new NameListApi();
export default api;

/*
 *interfaces
 */
interface SsbuName {
  records: SsbuNameResponse[];
}

interface SsbuNameResponse {
  name: string;
  url: string;
  icon: string;
}

export interface NameListRequest {
  key: string | null;
  val: string | null;
}

export interface NameListUpdateRequest {
  bkey: string | null;
  bval: string | null;
  key: string | null;
  val: string | null;
}

export interface NameListResponse {
  records: Array<NameListRec>;
}

interface NameListRec {
  key: string | null;
  val: string | null;
}

export interface NameListSaveResponse {
  insert: boolean;
  update: boolean;
}

export interface NameListDeleteResponse {
  status: boolean;
}
