document.addEventListener('DOMContentLoaded', function() {
    walkTree(document.getRootNode());
    initMutationObserver(document.getRootNode());
});

function walkTree(root) {
    const treeWalker = document.createTreeWalker(
        root, 
        window.NodeFilter.SHOW_ELEMENT, 
        { 
            acceptNode: (node) => { 
                const regex = /^https:\/\/(?:play\.google\.com|open\.spotify\.com)/;
                const accept = (node.tagName === 'A' && node.hasAttribute('href')) && regex.exec(node.getAttribute('href')) !== null;
                if (accept) {
                    return NodeFilter.FILTER_ACCEPT;
                } else {
                    return NodeFilter.FILTER_SKIP;
                }
            } 
        }, 
        false);

    let node;
    while ((node = treeWalker.nextNode())) {
		replaceLink(node);
    }
}

function initMutationObserver(root) {
    var MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach((mutation) => {
            walkTree(mutation.target);
        })
        observer.observe(root, opts);
    });
    var opts = { characterData: true, childList: true, subtree: true };
    observer.observe(root, opts);
}

function replaceLink(node) {
    node.setAttribute('href', `${beatnik_url}/music/?q=${node.getAttribute('href')}`)
}
