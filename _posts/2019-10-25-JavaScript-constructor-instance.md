---
layout: post
title: JavaScript - constructor, instance
date: 2019-10-25
---


> Object는 Object instance를  생성하는 '생성자(constructor)'입니다.  
> Function은 Function instance를 생성하는 '생성자(constructor)'입니다.

이 문장의 뜻을 살펴보자. 인스턴스(instance)는 '객체'로 봐도 무방하다. 생성자가 객체를 만들 때, 그 시점의 객체를 인스턴스라고 하기 때문이다. 결국 맥락의 차이이기 때문에 특별히 다른 것으로 '억지로' 생각하지 않아도 된다.

그렇다면 생성자는 무엇일까? 생성자는 인스턴스를 만드는 객체 혹은 함수를 말하는데, 함수 인스턴스를 생성하는 생성자를 '**Function**' 객체 인스턴스를 생성하는 생성자를 '**Object**'라고 한다.  우리는 자바스크립트에서 함수가 객체라는 것을 알고 있다. 그렇다면 두 생성자 **Function**과 **Object**는 어떤 관계가 있을까?

자바스크립트에서 모든 객체를 생성할 때 생성자 Object가 존재한다. 그리고 Object는 자신의 prototype에 객체들이 공유할만한 property들을 가지고 있다. 객체 원형이라 불리는 이 Object는 함수 객체인데, 이것이 바로 Function의 instance다. 정리하면 자바스크립트에서 **Object는 Function의 instance**, **Object 객체는 Object의 instance**이며 결국 모든 객체가 Function(함수)에서 파생된 함수 객체다.

공유하기

게시글 관리

**관성을 이기는 데이터**