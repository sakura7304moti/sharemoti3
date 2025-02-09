import axios from 'axios';
import { FileAPIClient } from './FileBaseApi';
import { PutResponse } from '../BaseApi';

export class MovieApi extends FileAPIClient {
  public async upload(file: File): Promise<MovieUploadResponse | null> {
    const path = this.uploadUrl();

    return this.httpUpload<MovieUploadResponse>(path, file);
  }

  public async createMovie(request: CreateMovie): Promise<PutResponse | null> {
    const url = '/movie';
    const path = this.combineUrl(url);
    return this.httpPut<CreateMovie, PutResponse>(path, request);
  }

  public uploadUrl() {
    const url = '/movie/upload';
    const path = this.combineUrl(url);
    return path;
  }

  public async updateMovie(request: Movie): Promise<PutResponse | null> {
    const url = '/movie';
    const path = this.combineUrl(url);
    return this.httpPut<Movie, PutResponse>(path, request);
  }

  public async downloadMovie(fileName: string) {
    const url = '/movie/' + fileName;
    const path = this.combineUrl(url);

    await axios({
      url: path,
      method: 'GET',
      responseType: 'blob',
    }).then((response) => {
      if (response) {
        console.log('download', response);
        return response;
      }
    });
  }

  public async getThumbNailImage(fileName: string) {
    const url = '/movie/thumbnail/' + fileName;
    const path = this.combineUrl(url);

    await axios({
      url: path,
      method: 'GET',
      responseType: 'blob',
    }).then((response) => {
      if (response) {
        console.log('download', response);
        return response;
      }
    });
  }

  public thumbnailLink(fileName: string) {
    const url = '/movie/thumbnail/' + fileName;
    const path = this.combineUrl(url);
    return path;
  }

  public downloadLink(fileName: string) {
    const url = '/movie/' + fileName;
    const path = this.combineUrl(url);
    return path;
  }

  public async deleteMovie(fileName: string): Promise<PutResponse | null> {
    const url = '/movie/' + fileName;
    const path = this.combineUrl(url);

    return this.httpDelete<PutResponse>(path);
  }

  public async hashtagList(): Promise<MovieHashtag[] | null> {
    const url = '/movie/hashtag';
    const path = this.combineUrl(url);

    return this.httpGet<MovieHashtag[]>(path);
  }

  public async searchMovie(
    keyword: string | null,
    hashtag: string | null,
    displayMode: number | null,
    pageNo: number
  ): Promise<SearchMovieResponse | null> {
    let url = '/movie?a=1';
    if (keyword) {
      url += `&keyword=${keyword}`;
    }
    if (hashtag) {
      url += `&hashtag=${hashtag}`;
    }
    if (displayMode != null) {
      url += `&mode=${displayMode}`;
    }
    url += `&page=${pageNo}`;
    const path = this.combineUrl(url);

    return this.httpGet<SearchMovieResponse>(path);
  }
}

const api = new MovieApi();
export default api;

interface CreateMovie {
  title: string;
  detail: string;
  fileName: string;
  thumbnailFlg: number;
  staffCd: number;
  hashtags: string[];
}

interface Movie extends CreateMovie {
  id: number;
}

interface MovieUploadResponse {
  fileName: string;
}

interface MovieHashtag {
  name: string;
  isGroup: number;
}

interface SearchMovieResponse {
  records: Movie[];
  totalCount: number;
}
