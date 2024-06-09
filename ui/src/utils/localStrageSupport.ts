export class LocalStrageObject {
  public setterValue = function <T>(key: string, value: T) {
    const text = JSON.stringify(value);
    localStorage.setItem(key, text);
  };
  public getterValue = function <T>(key: string) {
    try {
      const objText = localStorage.getItem(key);
      if (objText) {
        return JSON.parse(objText) as T;
      } else {
        return null;
      }
    } catch (err) {
      console.log('localstrage error', err);
      return null;
    }
  };
  public deleteValue = function (key: string) {
    try {
      localStorage.removeItem(key);
    } catch (err) {
      console.log('localstrage error', err);
    }
  };
}
