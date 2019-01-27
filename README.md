# ベイズ分類器

## 実装

https://github.com/ttezel/bayes/blob/master/lib/naive_bayes.js を参考に、てきとうに実装


## データセット

```
curl "https://ja.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext&titles=木村拓哉" | jq -r '.query.pages|.[]|.extract' >smap1
curl "https://ja.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext&titles=香取慎吾" | jq -r '.query.pages|.[]|.extract' >smap2
curl "https://ja.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext&titles=稲垣吾郎" | jq -r '.query.pages|.[]|.extract' >smap3
curl "https://ja.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext&titles=中居正広" | jq -r '.query.pages|.[]|.extract' >smap4

curl "https://ja.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext&titles=城島茂" | jq -r '.query.pages|.[]|.extract' >tokio1
curl "https://ja.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext&titles=国分太一" | jq -r '.query.pages|.[]|.extract' >tokio2
curl "https://ja.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext&titles=松岡昌宏" | jq -r '.query.pages|.[]|.extract' >tokio3
curl "https://ja.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext&titles=長瀬智也" | jq -r '.query.pages|.[]|.extract' >tokio4

curl "https://ja.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext&titles=山口達也" | jq -r '.query.pages|.[]|.extract' >test
```

## 実行例

```
$ python play.py
Learning ./smap1
Learning ./smap2
Learning ./smap3
Learning ./smap4
Learning ./tokio1
Learning ./tokio2
Learning ./tokio3
Learning ./tokio4
SMAP => -3889.192823
TOKIO => -3681.215206
```

```
$ python play.janome.py 
Learning ./smap1
Learning ./smap2
Learning ./smap3
Learning ./smap4
Learning ./tokio1
Learning ./tokio2
Learning ./tokio3
Learning ./tokio4
SMAP => -3994.242037
TOKIO => -3788.365390
```

無事に？山口達也はSMAPではなくTOKIOっぽいと分類された。
janomeとmecab-pythonで微妙に結果が違うのは、まぁこういうもんなんだろう...。

### Node.js の bayse を使うと...

```
$ node play.js
./smap1
./smap2
./smap3
./smap4
./tokio1
./tokio2
./tokio3
./tokio4
{ SMAP: -3913.9842620870786, TOKIO: -3704.4482315353903 }
```

どうも形態素解析のパース結果で、語数カウントが微妙に違うらしく、Pythonのやつとは数字は異なる。
けど、やはりTOKIOに分類されているところは変わりなし。