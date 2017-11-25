window.addEventListener("load", replaceLinks, false);

function replaceLinks(event) {
    const link_regex = /https:\/\/l\.messenger\.com\/l\.php\?u=([A-z\.\%0-9]+)&h=.+$/;
    const regex = /https?:\/\/(?:play\.google\.com\/music\/m\/[A-z0-9]+(?:\?t=.*)?|open\.spotify\.com\/(?:track|album)\/[A-z0-9]+)/;

    let anchors = document.getElementsByTagName('a');

    for (let i = 0; i < anchors.length; i++) {
        let result = link_regex.exec(anchors[i].href);

        if (result) {
            let href = decodeURIComponent(result[1]);

            if (regex.exec(href)) {
                new_href = `http://127.0.0.1:8000/music/?q=${href}`;
                anchors[i].href = new_href;
            }
        }
    }
}
