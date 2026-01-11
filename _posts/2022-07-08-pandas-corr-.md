---
layout: post
title: pandas - corr()
date: 2022-07-08
categories: ["1. 기술", "통계, 시계열"]

---


df.corr(method='s')
-------------------

### reference

1. [document : pandas.DataFrame.corr](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html)
2. [비선형 상관관계 : 스피어만 상관계수, 켄달타우](https://ekdud7667.tistory.com/entry/%EB%B9%84%EC%84%A0%ED%98%95-%EC%83%81%EA%B4%80%EA%B4%80%EA%B3%84-%EC%8A%A4%ED%94%BC%EC%96%B4%EB%A7%8C-%EC%83%81%EA%B4%80%EA%B3%84%EC%88%98-%EC%BC%84%EB%8B%AC%ED%83%80%EC%9A%B0)

---

pandas 데이터프레임 객체에 대해 corr()함수를 사용할 수 있다.

corr()은 누락값을 제외하고 전체(dataframe) 컬럼들 간의 상관도를 계산한다.

계산에 사용되는 상관계수의 default값은 pearson 상관계수로, 모든 변수가 연속형이고 정규분포를 띄는 경우 사용할 수 있다.

만약 정규분포를 따르지 않는 변수가 포함되어 있다면 보편적으로 spearman 상관계수를 사용한다.

spearman 상관계수는 비모수적 방법 (모수를 특정 분포로 가정하여 접근하는 방법론) 으로써 값에 순위를 매기고 순위에 대해 상관계수를 구하는 방식이다. 따라서 분석에 모수와 정규분포 가정이 필요하지 않다.

비모수적 방법으로는 kendall Tau 상관계수도 있으며 spearman과 적용 대상은 대체로 유사하다.

상관계수를 가장 대표적인 pearson으로 사용한다면 별도의 인자를 주지 않아도 되고,

```
df.corr()
```

pearson이 아닌 다른 상관계수를 사용하는 경우 파이썬 코드는 아래와 같이 작성할 수 있다.

```
df.corr(method='spearman')
```



**관성을 이기는 데이터**

[저작자표시
(새창열림)](https://creativecommons.org/licenses/by/4.0/deed.ko)