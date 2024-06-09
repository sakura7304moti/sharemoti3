import { FileAPIClient } from './FileBaseApi';

export class ObaRadioApi extends FileAPIClient {
  public search(): Promise<Array<string> | null> {
    const url = '/obaRadioList/';
    const path = this.combineUrl(url);

    return this.httpGet<Array<string>>(path);
  }
}
const api = new ObaRadioApi();
export default api;
