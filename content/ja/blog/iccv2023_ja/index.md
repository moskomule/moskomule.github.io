---
title: "高品質な生成画像は将来のコンピュータービジョンに悪影響を与えるのか"
date: 2023-07-15
tags: ["研究"]
---

昨今，文章から画像を生成するStableDiffusionやMidjourneyをはじめとする高品質な（text2img）生成モデルが次々に登場し，実際の画像と区別の付かないような生成画像が多量にインターネット上にアップロードされています [^openai]．
このような現象は，将来的にインターネット上から画像を収集し，データセットを作成した場合にコンピュータービジョンに対してどのような影響があるのでしょうか[^question]？
本記事で紹介する，京都大学の包さん，理研AIPの荒井さんとの[研究](https://arxiv.org/abs/2211.08095)は，この疑問に対して実験的に調査を行ったもので，今年10月にフランスで開催されるコンピュータービジョン分野の国際会議であるICCVにおいて発表します．


[^openai]: https://openai.com/blog/dall-e-now-available-without-waitlist/ によれば，OpenAI社のDALL･E2は2022年9月年に1日あたり200万枚の画像を生成したという．
[^question]: 昨年の9月半ばに第2著者の包さんと伊都キャンパスから博多駅に向かうバスに乗っているときの雑談で出てきたのが，この素朴な疑問でした．

---

はじめに述べたように，この1年ほどでStableDiffusionやChatGPTといった「生成AI」が多数登場し，研究者のみならず，一般のユーザーも使うようになりました．
その結果，多数の生成データがインターネット上にアップロードされるようになり，[偽情報の生産](https://www.washingtonpost.com/technology/interactive/2022/artificial-intelligence-images-dall-e/)や[人種バイアスの拡大](https://dl.acm.org/doi/abs/10.1145/3593013.3594095)といった社会的な問題も現れています．
本研究では，将来的にウェブから収集した画像データセットに生成画像が混入した場合に，コンピュータービジョンに対してどのような影響があるのかを実験的に調べました．

具体的には，代表的なtext2img生成モデルであるStableDiffusionを用いて，ImageNetやCOCO captionといった既存のデータセットを模倣して，200万枚程度の画像を生成しました．そして，生成された画像で元のデータセットの画像を置き換えることによって，生成画像が混入した状況を模倣し，画像認識モデルなどの学習データとした場合の影響を調べます．

{{<figure src="datasets_wide.png" width="80%">}}



---

論文の情報は以下の通りです．

```bibtex
@inproceedings{hataya2023will,
    author = {Ryuichiro Hataya and Han Bao and Hiromi Arai},
    title = {{Will Large-scale Generative Models Corrupt Future Datasets?}},
    booktitle = {ICCV},
    year = {2023},
}
```
