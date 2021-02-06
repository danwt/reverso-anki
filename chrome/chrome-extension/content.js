/*
Parse the reverso contect webpage for examples and the searched word.
*/

function parseTextContainer(tc) {
  return tc.outerText;
}

function parseExample(ex) {
  let children = ex.children;
  return [children[0], children[1]].map(parseTextContainer);
}

var eles = document.getElementsByClassName("example");

/* Get the from language word */
var searchword_ele = document.getElementById("search-input");
var searchword = searchword_ele.children[0].value;

// prettier-ignore
if (eles != null) {
  /* Return the word, and the example pairs */
  [searchword,
   Array.prototype.map.call(eles, parseExample)]  // eslint-disable-line
} else {
  []
}
