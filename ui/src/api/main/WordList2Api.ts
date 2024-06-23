import { MainAPIClient } from './MainBaseApi';

export class WordList2Api extends MainAPIClient {
  //検索
  public search(
    request: WordList2SearchRequest
  ): Promise<WordList2Response | null> {
    const url = '/wordList/search';
    const path = this.combineUrl(url);

    return this.httpPost<WordList2SearchRequest, WordList2Response>(
      path,
      request
    );
  }

  //追加・更新
  public save(
    request: WordList2Request
  ): Promise<WordList2SaveResponse | null> {
    const url = '/wordList/save';
    const path = this.combineUrl(url);

    return this.httpPost<WordList2Request, WordList2SaveResponse>(
      path,
      request
    );
  }

  //削除
  public delete(
    request: WordList2Request
  ): Promise<WordList2DeleteResponse | null> {
    const url = '/wordList/delete';
    const path = this.combineUrl(url);

    return this.httpPost<WordList2Request, WordList2DeleteResponse>(
      path,
      request
    );
  }
}

const api = new WordList2Api();
export default api;

/*
 *interfaces
 */
export interface WordList2SearchRequest {
  text: string | null;
}

export interface WordList2Request {
  word: string | null;
  desc: string | null;
}

export interface WordList2Response {
  records: Array<WordList2Rec>;
}

interface WordList2Rec {
  word: string | null;
  desc: string | null;
  createAt: string | null;
  updateAt: string | null;
}

export interface WordList2SaveResponse {
  insert: boolean;
  update: boolean;
}

export interface WordList2DeleteResponse {
  status: boolean;
}
