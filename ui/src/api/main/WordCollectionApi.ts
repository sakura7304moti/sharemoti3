import { MainAPIClient } from './MainBaseApi';

export class WordCollectionApi extends MainAPIClient {
  // 検索
  public searchWord(request: SearchRequest): Promise<Array<WordState> | null> {
    const url = '/wordCollection/search';
    const path = this.combineUrl(url);

    return this.httpPost<SearchRequest, Array<WordState>>(path, request);
  }

  // 記念の件数リスト
  public getKinens(): Promise<Array<number> | null> {
    const url = '/wordCollection/kinen';
    const path = this.combineUrl(url);

    return this.httpGet<Array<number>>(path);
  }

  // 年のリスト
  public getYears(): Promise<Array<number> | null> {
    const url = '/wordCollection/year';
    const path = this.combineUrl(url);

    return this.httpGet<Array<number>>(path);
  }
}

interface SearchRequest {
  keyword: string | null;
  dateOrder: string | null;
  textOrder: string | null;
  kinen: number | null;
  year: number | null;
}
interface WordState {
  id: number;
  word: string;
  detail: string;
  wordRank: number;
  createAt: string;
  updateAt: string;
}
