import axios from 'axios';

export function useYoutubeSupport() {
  const getThumbnailUrl = function (url: string) {
    const param = new URL(url).searchParams;
    const v = param.get('v');
    const maxUrl = `https://img.youtube.com/vi/${v}/maxresdefault.jpg`;
    let returnUrl = '';
    axios
      .get(maxUrl)
      .then((response) => {
        if (response) {
          return maxUrl;
        } else {
          const mediumUrl = `http://img.youtube.com/vi/${v}/sddefault.jpg`;
          returnUrl = mediumUrl;
        }
      })
      .catch((e) => {
        const mediumUrl = `http://img.youtube.com/vi/${v}/sddefault.jpg`;
        returnUrl = mediumUrl;
      });
    return returnUrl;
  };
  return { getThumbnailUrl };
}
