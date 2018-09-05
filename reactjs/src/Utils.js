class Utils {
  static getQueryParams(url) {
    if(!url) url = window.location.href;

    const matches = url.match(/[^?]*\?(?:([^=]+)=([^&]+))+/)
      
    const groups = matches ? matches.slice(1) : {};

    let params = {};
    for (var i = 0; i < groups.length; i += 2) {
      const key = groups[i];
      const value = groups[i+1];

      params[key] = value;
    }

    return params;
  }

}

export default Utils;
