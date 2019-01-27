let fs = require('fs');
let glob = require('glob');
let bayes = require('bayes');
const Mecab = require('mecab-lite');
let mecab = new Mecab();

let classifier = bayes({
  tokenizer: (text) => {
    var arr = mecab.parseSync(text);
    arr.pop(); // EOS を除く
    arr.pop(); // EOS を除く
    return mecab.parseSync(text).filter((item) => {
        return item[1] == '名詞' && (item[2] == '固有名詞' || item[2] == '一般');
    }).map((item) => {
        return item[0];
    })
  }
});

glob.sync("./smap*").forEach((filename) => {
    console.log(filename)
    let text = fs.readFileSync(filename, "utf-8");
    classifier.learn(text, "SMAP")
});
glob.sync("./tokio*").forEach((filename) => {
    console.log(filename)
    let text = fs.readFileSync(filename, "utf-8");
    classifier.learn(text, "TOKIO")
});

let text = fs.readFileSync("test", "utf-8");
console.log(classifier.categorize(text))
