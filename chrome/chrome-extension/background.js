function createObjectRepresentation(word, sentenceArr) {
  return {
    sentences: sentenceArr.map((sentence) => {
      return { front: sentence[0], back: sentence[1], word };
    }),
  };
}

function getFileName(languages, word, numSentences) {
  return "reverso_" + languages + "/reverso_downloader_" + word + "_" +
    numSentences + ".json";
}

function createBlob(obj) {
  const str = JSON.stringify(obj);
  const bytes = new TextEncoder().encode(str);
  const blob = new Blob([bytes], {
    type: "application/json;charset=utf-8",
  });
  return blob;
}

function downloadBlob(blob, filename) {
  var url = URL.createObjectURL(blob);
  chrome.downloads.download({
    url: url, // The object URL can be used as download URL,
    filename: filename,
    //...
  });
}

async function getUrl() {
  return await new Promise((resolve, reject) => {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
      let url = tabs[0].url;
      // use `url` here inside the callback because it's asynchronous!
      resolve(url);
    });
  });
}

function parseUrl(url) {
  const split = url.split("/");
  const languages = split[4];
  return languages;
}

async function processAndDownloadParsedPage(pageParseResult) {
  pageParseResult = pageParseResult[0]; //unpack 1 level of nesting (flatten)
  word = pageParseResult[0];
  sentences = pageParseResult[1];
  let numSentences = sentences.length.toString();

  const url = await getUrl();
  const languages = parseUrl(url);
  const filename = getFileName(languages, word, numSentences);
  const obj = createObjectRepresentation(word, sentences);
  const blob = createBlob(obj);
  downloadBlob(blob, filename);
}

chrome.browserAction.onClicked.addListener(function (tab) {
  chrome.tabs.executeScript(
    tab.id,
    {
      file: "content.js",
    },
    processAndDownloadParsedPage,
  );
});
