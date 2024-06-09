import { ScraperAPIClient } from './ScraperBaseApi';
export class HoloMovieApi extends ScraperAPIClient {
  public memory(): Promise<HoloMemoryResponse | null> {
    const url = '/holoMovie/memory';
    const path = this.combineUrl(url);
    return this.httpGet<HoloMemoryResponse>(path);
  }
}

const api = new HoloMovieApi();
export default api;

interface HoloMemoryResponse {
  records: HoloMemory[];
}
interface HoloMemory {
  title: string;
  member: string;
  link: string;
  date: string;
  memory: string;
  detail: string;
}
