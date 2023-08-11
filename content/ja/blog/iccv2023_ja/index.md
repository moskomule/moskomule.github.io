---
title: "高品質な生成画像は将来のコンピュータービジョンに悪影響を与えるのか"
date: 2023-07-15
tags: ["研究"]
---

昨今，文章から画像を生成するStableDiffusionやMidjourneyをはじめとする高品質な（text2img）生成モデルが次々に登場し，実際の画像と区別の付かないような生成画像が多量にインターネット上にアップロードされています [^openai]．
このような現象は，将来的にインターネット上から画像を収集し，データセットを作成した場合に，画像認識をはじめとするコンピュータービジョンに対してどのような影響があるのでしょうか[^question]？

本記事で紹介する，京都大学の包さん，理研AIPの荒井さんとの[研究](https://arxiv.org/abs/2211.08095)は，この疑問に対して実験的に調査を行ったもので，今年10月にフランスで開催されるコンピュータービジョン分野の国際会議であるICCVにおいて発表します．

[^openai]: https://openai.com/blog/dall-e-now-available-without-waitlist/ によれば，OpenAI社のDALL･E2は2022年9月年に1日あたり200万枚の画像を生成したという．
[^question]: 昨年の9月半ばに第2著者の包さんと伊都キャンパスから博多駅に向かうバスに乗っているときの雑談で出てきたのが，この素朴な疑問でした．

---

はじめに述べたように，この1年ほどでStableDiffusionやChatGPTといった「生成AI」が多数登場し，研究者のみならず，一般のユーザーも使うようになりました．
その結果，多数の生成データがインターネット上にアップロードされるようになり，[偽情報の補強](https://www.washingtonpost.com/technology/interactive/2022/artificial-intelligence-images-dall-e/)や[人種バイアスの拡大](https://dl.acm.org/doi/abs/10.1145/3593013.3594095)といった社会的な問題も現れてしまっています．
それに対して，本研究では，生成画像が将来的にウェブから収集した画像データセットに混入する可能性が高いと考え，このような混入が画像認識などのコンピュータービジョンに対して与える影響を実験的に調べました．

具体的には，代表的なtext2img生成モデルであるStableDiffusionを用いて，ImageNetやCOCO captionという既存のデータセットを模倣し，合計200万枚程度の画像を生成しました．
そして，生成された画像によって元のデータセットの画像を置き換えることで，生成画像が混入した状況を模擬的に再現し，画像認識モデルなどの学習データとした場合の影響を調べます．
以下の画像の左側はImageNetを真似るために，カテゴリ名を使って生成した画像（SD-ImageNet）の一部，
右側はCOCO caption（SD-COCO）の説明文から生成した画像の一部です．
少なくとも一見は「ちゃんとした」画像に見えます．

{{<figure src="datasets_wide.png" width="80%">}}

このような生成画像によってImageNetの画像を置き換えたデータセットによって画像分類モデル（ResNet-50）を訓練し，ImageNet評価データセット上で評価を行った際の正解率を以下の図（<font color="Blue">青線</font>）に示しました．
参考のために，生成画像ではなく，ImageNetと同じカテゴリの画像を別途収集したWebVisionデータセットの画像を混入させた場合の正解率を<font color="Orange">橙線</font>で示しています．
混入率（横軸）が大きくなるにつれて，生成画像の混入の方が精度（縦軸）を悪化させていることが分かります．

{{<figure src="classification-resnet50.png" width="50%">}}

SwinTransformer-SmallやConvNeXt-Tinyといった現代的なモデルでも同様の分類性能は低下し，その影響はImageNet-Aなどの分布外データに対する頑健性評価のベンチマークにも見られます．
また，このような生成画像特有の性能低下は画像説明文生成における様々な精度指標にも現れます．
さらに，生成画像の混入したデータセットを用いて画像生成モデルを訓練するタスクにおいては，生成画像の多様性が低下が観察されました．

このような生成データのもたらす悪影響の原因として，実際の画像と比較して，生成画像の多様性が低いことが挙げられます[^webimages]．
実際に，[precition-recallという生成モデルの品質尺度](https://proceedings.neurips.cc/paper_files/paper/2019/hash/0234c510bc6d908b28c70ff313743079-Abstract.html)によりSD-ImageNetの画像分布がImageNetの画像分布の一部領域にほぼ含まれていることが分かっています．

{{<figure src="precision-recall.png" width="50%">}}

キャプションを工夫したSD-ImageNetの派生の画像も，ImageNetの画像と比べて多様性が乏しいことがわかっています．
このような多様性の低下は，[Shumailov et al. 2023](https://arxiv.org/abs/2305.17493)でも指摘されているように，生成画像を含んだデータセットから生成モデルが作られるループが繰り返されることで加速していく可能性があります．

[^webimages]: もちろんインターネット上から収集可能な画像も，「撮影しよう」「投稿しよう」という人の意思フィルターがかかるため，実世界にあり得る画像に比べれば多様性には乏しいはずです．

最新の生成モデルによる高品質な生成画像が厄介なのは，簡易な検出が難しく，巨大なデータセットから効率的に取り除けない点です．
例えば[実画像と生成画像の周波数成分の違いに着目した検出](https://proceedings.neurips.cc/paper/2020/hash/1f8d87e1161af68b81bace188a1ec624-Abstract.html)はあまり使えなさそうです．
さらに，多くの場合，人の目でも識別は困難です．
幸いにもStableDiffusionやDALL･Eなどは「透かし」を入れているので検出は可能ですが，今後も生成モデル開発者には生成画像の検出を可能にする透かしの導入が求められるでしょう．
同時に，生成画像の高速な検出方法の開発も望まれます．


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

この研究で生成したSD-ImageNetおよびSD-COCOは https://dmsgrdm.riken.jp:5000/c24kn/ からダウンロードできます．