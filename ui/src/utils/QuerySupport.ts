import { LocationQueryValue } from 'vue-router';

export function useQuerySupport(){
  const decodeQueryString = function(query:LocationQueryValue | LocationQueryValue[]){
    const text = query?.toString() ?? '';
    if((text) != ''){
      return text;
    }
  }

  const decodeQueryNumber = function(query:LocationQueryValue | LocationQueryValue[]){
    const text = query?.toString() ?? '';
    if(!isNaN(Number(text))){
      return Number(query)
    }
  }

  const decodeQueryStringArray = function(query:LocationQueryValue | LocationQueryValue[]){
    const text = query?.toString() ?? '';
    if(text.includes(',')){
      return text.split(',').map(it => it);
    }
    else{
      const oneQuery = query?.toString() ?? '';
      if(oneQuery != ''){
        return [oneQuery] as string[];
      }
    }
  }

  const decodeQueryNumberArray = function(query:LocationQueryValue | LocationQueryValue[]){
    const text = query?.toString() ?? '';
    if(text.includes(',')){
      // ,で分割 -> 数値に変換 -> 数値のみに抽出
      return text.split(',').map(it => Number(it)).filter(it => !isNaN(it));
    }
    else{
      const oneQuery = Number(text);
      if(!isNaN(oneQuery)){
        return [oneQuery] as number[];
      }
    }
  }

  const decodeQueryBoolean = function(query:LocationQueryValue | LocationQueryValue[]){
    const text = query?.toString() ?? '';
    if(text == 'true'){
      return true;
    }
    if(text == 'false'){
      return false;
    }
  }
  return{
    decodeQueryString,
    decodeQueryNumber,
    decodeQueryStringArray,
    decodeQueryNumberArray,
    decodeQueryBoolean
  }
}
