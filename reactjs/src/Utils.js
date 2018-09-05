class Utils {
  static getQueryParams(url) {
    if(!url) url = window.location.href;

    const matches = url.match(/[^?]*\?(?:([^=]+)=([^&]+))+/).slice(1);

    let returnMatches = {};
    for (var i = 0; i < matches.length; i += 2) {
      const key = matches[i];
      const value = matches[i+1];

      returnMatches[key] = value;
    }

    return returnMatches;
  }

}

export default Utils;
