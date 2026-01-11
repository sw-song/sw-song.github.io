---
layout: post
title: Scheduling
date: 2022-06-23
categories: ["1. 기술", "통계, 시계열"]

---


Reference :

1. [스케줄링 - 배치처리, 시분할시스템, 멀티테스킹, 멀티 프로그래밍](https://velog.io/@kim-jaemin420/%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81-%EB%B0%B0%EC%B9%98-%EC%B2%98%EB%A6%AC-%EC%8B%9C%EB%B6%84%ED%95%A0-%EC%8B%9C%EC%8A%A4%ED%85%9C-%EB%A9%80%ED%8B%B0-%ED%83%9C%EC%8A%A4%ED%82%B9-%EB%A9%80%ED%8B%B0-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D)
2. [운영체제의 발전사 - 배치 처리 시스템, 시분할 시스템, 멀티 테스킹](https://libertegrace.tistory.com/entry/%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C-%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EC%9D%98-%EB%B0%9C%EC%A0%84%EC%82%AC%EB%B0%B0%EC%B9%98-%EC%B2%98%EB%A6%AC-%EC%8B%9C%EC%8A%A4%ED%85%9C-%EC%8B%9C%EB%B6%84%ED%95%A0-%EC%8B%9C%EC%8A%A4%ED%85%9C-%EB%A9%80%ED%8B%B0-%ED%83%9C%EC%8A%A4%ED%82%B9)
3. [운영체제 - 스케줄링 (배치 처리, 시분할 시스템, 멀티 프로그래밍)](https://analysis-flood.tistory.com/131)

Scheduling
==========

서버의 실시간 시스템이 일관된 처리 속도를 갖추도록 하는 최적화 알고리즘

### Batch

시스템 개발자의 설계에 따라 프로그램 흐름을 결정

* First In, Fist Out
* 순차적 실행 방식 (&lt;-&gt;병렬 처리)

### Event-Driven

이벤트 발생시 프로그램 흐름 결정

### Time Sharing

동시에 다중 사용자 지원을 위해 컴퓨터 응답 시간을 최소화 하여 동시에 여러 사용자를 수용할 수 있도록 하는 방식

### Multi-tasking

단일 CPU에서 여러 응용 프로그램이 동시에 실행되는 것처럼 보이는 방식으로, 실제로는 10~20ms 단위로 응용 프로그램이 변경되며 실행됨.



**관성을 이기는 데이터**

[저작자표시
(새창열림)](https://creativecommons.org/licenses/by/4.0/deed.ko)