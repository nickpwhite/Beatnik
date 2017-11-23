const beatnik_regex = /^http:\/\/127\.0\.0\.1:8000\/.*$/

const url = document.URL;

if (beatnik_regex.exec(url)) {
    console.log("Hello Beatnik user!");
} else {
    const regex = /https?:\/\/(?:play\.google\.com\/music\/m\/[A-z0-9]+(?:\?t=.*)?|open\.spotify\.com\/(?:track|album)\/[A-z0-9]+)/;

    let anchors = document.getElementsByTagName('a');

    for (let i = 0; i < anchors.length; i++) {
        let href = anchors[i].href;

        if (regex.exec(href)) {
            new_href = `http://127.0.0.1:8000/music/?q=${href}`;
            console.log(new_href);
            anchors[i].href = new_href;
        } else {
            console.log(href);
        }
    }
}
