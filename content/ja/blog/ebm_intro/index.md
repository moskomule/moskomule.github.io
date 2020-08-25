---
title: "深層EBM概論"
date: 2020-06-14T16:10:12+09:00
draft: true
---

$$
    \newcommand{\R}{\mathbb{R}}
    \newcommand{\E}{\mathbb{E}}
    \newcommand{\vx}{\boldsymbol{x}}
    \newcommand{\vtheta}{\boldsymbol{\theta}}
$$

この記事では最近の生成モデルで熱いDeep Energy-based Models（深層EBM）についてサーベイしてみました．EBMは非常に大きな枠組みで，GANのような（画像）生成から自己教示あり学習まで幅広い対象を扱えます．深層学習三枚目のLeCun先生も大好きです．

EBMはデータ$\vx\in\R$が存在する領域に低いエネルギーを，存在しない領域に高いエネルギーを割り当てるようなエネルギー函数$E:\R^D\to\R$に対して，密度函数をボルツマン分布（またの名をギブス分布，カノニカル分布など）

\begin{equation}
    p(\vx)=\frac{\exp(-E(\vx))}{Z},~~Z=\int\mathrm{d}\vx\exp(-E(\vx)) \label{eq:ebm}
\end{equation}


によって表現します．このように表現可能なモデルとしてはボルツマンマシンなどが有名です．EBMはエネルギー函数$E$に事前知識を入れた設計を行える点が利点で，たとえばデータの背景にあるグラフ構造をつかってエネルギーを定義することが可能です．正規化を担う$Z$は計算困難ですが，EBMでは基本的に求める必要がありません．

{{< figure src="energy_based_1.png" caption="偉大なEBM概論([LeCun+06]より)" width="50%">}}

なお，EBMの応用は必ずしも教師なし学習に限る必要はなく，教師あり学習でも利用できます．たとえば上の図では入力と教師ラベルの対を入力としています．

{{< figure src="energy_based_2.png" caption="偉大なEBM概論([LeCun+06]より)" width="50%">}}

EBMの学習は$\vtheta$でパラメタづけられたモデル$p_{\vtheta}$の対数尤度の勾配を

\begin{equation}
    \frac{\partial \log p_\vtheta(\vx')}{\partial \vtheta}=\E_{p_\vtheta}[\frac{\partial E_{\vtheta}(\vx')}{\partial \vtheta}]-\frac{\partial E_\vtheta(\vx)}{\partial \vtheta} \label{eq:gradient}
\end{equation}

によって得ることによって行います．

式\eqref{eq:gradient}右辺第1項の期待値は$p_\theta$についてとる必要があるので，MCMCなどによって推定するのが一般的です．たとえばEBMの一種である制限付きボルツマンマシンはギブスサンプラーを使っていますが，深層学習モデルのようにデータの次元数$D$が大きくなると難易度が増してきます．そこで，深層EBMでは1.サンプリングの工夫や2.サンプリングによらないスコアマッチングなどを行います．

## サンプリングの工夫

多くの研究[Nijkamp+19, Du & Mordatch 19]はMCMCの一種である，Stochastic Graitedient Langevin dynamics (SGLD) [Welling & Teh 11]によるサンプリングが利用しています．

\begin{equation}
    \vx_0 \sim p_0(\vx), ~\vx_{t+1}=\vx_t-\frac{\alpha}{2}\frac{\partial E_\vtheta(\vx_t)}{\partial \vx_t}+\epsilon, ~\epsilon\sim\mathcal{N}(0, \alpha)
\end{equation}

$p_0$はデータ空間での一様分布などで，$\alpha$が十分に小さければ十分に長い時間の後，$p_\vtheta$からサンプリングすることが可能になります．SGLDは他のMCMCと比較して，エネルギー函数の勾配が得られる場合に，ランダムな初期値からでも効率的にサンプリングを行うことが可能です．

{{< figure src="energy_based_3.png" caption="[Nijkamp+19a]より，一様分布から画像を更新し生成する例" width="50%">}}

Persistent Contrastive Divergenceのように



## スコアマッチング

## Self-supervised Learning as EBM

いかがでしたか？深層EBMについてまとめてみました．多くの可能性がある深層EBMからは今後も目を離せませんね！