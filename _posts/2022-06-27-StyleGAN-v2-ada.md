---
layout: post
title: StyleGAN v2-ada
date: 2022-06-27
---


StyleGAN v2-ada - Basic Concept
===============================

reference :

1. [StyleGAN2를 이용한 성격 유형별 얼굴 생성 모델 연구 개발 과정 공개!](https://www.sphinfo.com/stylegan2/)
2. [[StyleGan2-ada 실습] AFHQ 데이터 셋 이용해서 stylegan2-ada 학습하기 2](https://study-grow.tistory.com/entry/StyleGan2-ada-%EC%8B%A4%EC%8A%B5-AFHQ-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%85%8B-%EC%9D%B4%EC%9A%A9%ED%95%B4%EC%84%9C-stylegan2-ada-%ED%95%99%EC%8A%B5%ED%95%98%EA%B8%B0-2)
3. [[Paper review]StyleGAN2](https://iamseungjun.tistory.com/6)
4. [github/NVlabs/stylegan2-ada-pytorch](https://github.com/NVlabs/stylegan2-ada-pytorch)

styleGAN2-ada는 기존 styleGAN의 일명 '물방울 현상'을 발생시키는 AdaIN(Adaptive Instance Normalization)을 정규화부분을 수정하고(StyleGAN2) ADA(Adaptive Discriminator Augmentation, 데이터 증강기법)을 추가로 활용하여 데이터가 부족한 상황에서도 좋은 성능을 낼 수 있도록 개선되었다.

추가로, latent code(style)를 얻기 위해 별도의 네트워크를 구성할 필요 없이 자체적으로 구현된 projection method를 활용할 수 있도록 하였으며, pretrained model로 test해 볼 수 있다.

```
python projector.py --outdir=out \
                    --target=~/mytargetimg.png \
                    --network=https://nvlabs-fi-cdn.nvidia.com/stylegan2-ada-pytorch/pretrained/ffhq.pkl
```



**관성을 이기는 데이터**

[저작자표시
(새창열림)](https://creativecommons.org/licenses/by/4.0/deed.ko)