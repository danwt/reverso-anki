const got = require("got");
import cheerio from "cheerio";
import { page as example } from "./exampleReversoPage";

console.log("got", got);
console.log("cheerio", cheerio);

function exampleWithoutMakingRequest() {
  return example;
}

async function fetchPage(url: string) {
  //TODO: make the return value structure better
  try {
    const response = await got(url);
    return [response.body, null];
  } catch (error) {
    return [null, error.response.body];
  }
}

function createReversoUrl(from: string, to: string, word: string) {
  // example url: 'https://context.reverso.net/translation/german-english/vertraue';
  const fromLower = from.toLowerCase();
  const toLower = to.toLowerCase();
  const wordLower = word.toLowerCase();
  return (
    "https://context.reverso.net/translation/" +
    fromLower +
    "-" +
    toLower +
    "/" +
    wordLower
  );
}

function getTranslationsFromHTMLString(stringRep: string) {
  //Create the sentence pairs from a string representing a Reverso html page
  const $ = cheerio.load(stringRep);

  function extractTextToArray(arr: string[]) {
    return function (i: any, e: any) {
      arr.push($(e).text().trim());
    };
  }

  function extractTextFromInsideClassTag(htmlClass: string): string[] {
    const arr: string[] = [];
    $(htmlClass).find(".text").each(extractTextToArray(arr));
    return arr;
  }

  const fromLang: string[] = extractTextFromInsideClassTag(".src.ltr");
  const toLang: string[] = extractTextFromInsideClassTag(".trg.ltr");

  function zipLangs(from: string[], to: string[]): [string, string][] {
    //TODO: add assertion that arrays are same length
    const ret: [string, string][] = [];
    from.map((e, i) => {
      ret.push([e, to[i]]);
    });
    return ret;
  }

  return zipLangs(fromLang, toLang);
}

export default async function getSentencePairs(
  from: string,
  to: string,
  word: string,
  useLocal?: boolean
) {
  useLocal = true; //TODO: unblock if necessary

  let stringHTML;
  if (useLocal) {
    stringHTML = exampleWithoutMakingRequest();
  } else {
    const url = createReversoUrl(from, to, word);
    const [result, err] = await fetchPage(url);

    if (!result) {
      console.log("Could not make request to reverso");
      console.log(err);
      return [];
    } else {
      stringHTML = result;
    }
  }

  return getTranslationsFromHTMLString(stringHTML);
}

console.log("try", getSentencePairs("german", "italian", "vertraue"));
