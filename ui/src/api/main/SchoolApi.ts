import { MainAPIClient } from './MainBaseApi';

export class SchoolApi extends MainAPIClient{
  public school():Promise<Array<SchoolState> | null>{
    /**
     * 学校の一覧を取得
     */
    const url = '/school/list';
    const path = this.combineUrl(url);
    return this.httpGet<Array<SchoolState>>(path);
  }

  public comment(id:number):Promise<Array<SchoolCommentState> | null >{
    /**
     * コメントの一覧を取得
     */
    const url = '/school/comment/' + id;
    const path = this.combineUrl(url);
    return this.httpGet<Array<SchoolCommentState>>(path)
  }

  public createSchool(request:School):Promise<PutResponse | null>{
    /**
     * 学校を設立
     */
    const url = '/school/create/school'
    const path = this.combineUrl(url);
    return this.httpPost<School , PutResponse>(path, request)
  }

  public createComment(request:Comment):Promise<PutResponse | null>{
    /**
     * コメントを作成
     */
    const url = '/school/create/comment'
    const path = this.combineUrl(url);
    return this.httpPost<Comment , PutResponse>(path, request)
  }

  public editSchool(request:School):Promise<PutResponse | null>{
    /**
     * 学校を編集
     */
    const url = '/school/edit/school'
    const path = this.combineUrl(url);
    return this.httpPost<School , PutResponse>(path, request)
  }

  public editComment(request:Comment):Promise<PutResponse | null>{
    /**
     * コメントを編集
     */
    const url = '/school/edit/comment'
    const path = this.combineUrl(url);
    return this.httpPost<Comment , PutResponse>(path, request)
  }

  public deleteSchool(id:number):Promise<PutResponse | null>{
    /**
     * 学校を取り壊し
     */
    const url = '/school/delete/school/' + id;
    const path = this.combineUrl(url);
    return this.httpDelete<PutResponse>(path);
  }

  public deleteComment(id:number):Promise<PutResponse | null>{
    /**
     * コメントを削除
     */
    const url = '/school/delete/comment/' + id;
    const path = this.combineUrl(url);
    return this.httpDelete<PutResponse>(path);
  }
}

interface SchoolState extends School{
  create_at:string;
  update_at:string;
}

interface School{
  id:number;
  schoolName:string;
  principal:string;
  detail:string;
  slogan:string;
}

interface SchoolCommentState extends SchoolComment{
  create_at:string;
  update_at:string;
}

interface SchoolComment{
  id:number;
  schoolId:number;
  star:number;
  title:string;
  comment:string;
  postPerson:string;
}

interface PutResponse{
  status:string;
}
