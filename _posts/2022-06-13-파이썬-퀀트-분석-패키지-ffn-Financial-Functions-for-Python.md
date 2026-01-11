---
layout: post
title: 파이썬 퀀트 분석 패키지 - ffn(Financial Functions for Python)
date: 2022-06-13
categories: ["Quantitative Investment"]

---


<https://github.com/pmorissette/ffn>

[GitHub - pmorissette/ffn: ffn - a financial function library for Python

ffn - a financial function library for Python. Contribute to pmorissette/ffn development by creating an account on GitHub.

github.com](https://github.com/pmorissette/ffn)

Python ffn 패키지는 퀀트 분석을 편하게 하도록 작성된 라이브러리다. 유용한 함수들을 많이 제공하고 있는데, 그중에서도 어렵지 않게 써먹을만한 함수들을 빠르게 익혀보자.

#### **Step 1. 데이터 추출**

기본적으로 야후 파이낸스를 통해 데이터를 가져오게 되어있고, 데이터 로드 속도도 빠른 편이다.

![](/assets/images/posts/119-0.webp)

#### **Step 2. 기준일 스케일링**

자산 등락을 확인할 때 4개의 자산 가격의 기준일을 맞춰서 그래프를 그려보게 되는데, 여기서는 이러한 스케일링 작업을 rebase() 함수로 제공한다.

![](/assets/images/posts/119-1.webp)
![](/assets/images/posts/119-2.webp)

#### **Step 3. 수익률**

굳이 있어야 하나? 싶은 함수도 있다. 아래의 경우 일간 변화율(수익률)을 구하는 함수인데, pct\_change()와 함수명만 다르고 동작은 동일하다.

![](/assets/images/posts/119-3.webp)
![](/assets/images/posts/119-4.webp)

#### **Step 4. 기술 통계**

이 패키지에서 제공하는 가장 유용한 부분은 기술통계다. 기본적인 기술 분석에 필요한 내용들은 calc\_stats() 함수를 사용하면 빠르게 확인할 수 있다.

![](/assets/images/posts/119-5.webp)
![](/assets/images/posts/119-6.webp)
![](/assets/images/posts/119-7.webp)

기간별 수익률과 샤프지수, 최대 낙폭, 연간 승률 등 유용한 데이터를 제공하고 있다. 기본적이면서 중요하고, 반복적이라 귀찮은 작업들을 대신해주는 고마운 녀석이다.

#### **Step 5. 손실률**

손실률을 따로 볼 수도 있다. 수익이 난 구간은 0으로 대체하고 나머지 구간은 백분율을 비율로 풀어서(나누기 100) 보여준다.

![](/assets/images/posts/119-8.webp)

손실률을 그래프로 그리고, 가장 큰 손실을 MDD로 체크해볼 수 있다.

![](/assets/images/posts/119-9.webp)

#### **Step 6. 기간별 증감 추이**

display\_lookback\_returns() 함수는 각 기간(월초, 3개월 전, 6개월 전, 연초, 1년 전.. , 최초 관찰일) 대비 증감률을 간단히 보여준다.

![](/assets/images/posts/119-10.webp)

#### **Step  7. stats 객체**

stats 객체(ffn.core.PerformanceStats)는 판다스 각 변수(자산 데이터)에 대해 데이터 프레임처럼 인덱싱하게 해준다. 특정 자산의 월간 수익률을 다음과 같이 확인할 수 있다.

![](/assets/images/posts/119-11.webp)

객체로 히스토그램을 그릴 수도 있는데, 커스텀이 불편해 잘 사용하지는 않을 것 같다.

![](/assets/images/posts/119-12.webp)



**관성을 이기는 데이터**

[저작자표시
(새창열림)](https://creativecommons.org/licenses/by/4.0/deed.ko)