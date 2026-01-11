---
layout: post
title: 블록체인 개념적 구현(javascript)
date: 2019-09-26
categories: ["1. 기술", "웹, 자바스크립트"]

---


블록체인은 데이터를 여러 블록으로 이어붙이며 저장하고, 저장하는 과정에서 Hash(문자열과 같은 특정 데이터를 해시 함수를 통해 일정한 길이의 데이터로 변환한 값)변환을 수행하기 때문에 양자 연산이 아닌 이상 해독하는 것은 어렵다.

5분안에 블록체인을 만들어보자. 물론 우리가 만들 블록체인은 누군가와 거래를 하거나 장부에 거래 내용을 기록하거나 하는 서비스용 네트워크는 아다. 혼자 가지고 놀 LEGO를 조립하는 수준이다. 하지만 블록체인이 도대체 어떻게 생겨먹었는지 알기 위해 딱 좋은 난이도라 생각한다.

전체 코드는 아래와 같다.

```
const crypto = require('crypto');

let blockchain = [];

const genesisBlock = {
    index: blockchain.length,
    timestamp: Date(),
    data: "1stblock",
    dataHash: crypto.createHash('sha256').update("firstblock").digest('hex'),
    previousHash: '',
    headerHash: crypto.createHash('sha256').update("firstblockheader").digest('hex')
}

let createBlock = function(data){
    let block = {
        index : blockchain.length,
        timestamp : Date(),
        data : data,
        dataHash : crypto.createHash('sha256').update(data).digest('hex'),
        previousHash : blockchain[blockchain.length-1].headerHash,
        headerHash : crypto.createHash('sha256').update(
            data + genesisBlock.previousHash).digest('hex')
    }
    blockchain.push(block);
}

blockchain.push(genesisBlock);

createBlock('2ndblock');
createBlock('3rdblock');
createBlock('4thblock');
createBlock('5thblock');

console.log(blockchain);
```

코드를 실행하면 아래 이미지의 우측 화면과 같이 **각 블록 안에 담긴 내용물**을 확인할 수 있다.

![](/assets/images/posts/9-0.webp)

Visual Studio Code

먼저 위 코드는 세 영역으로 구성된다.

![](/assets/images/posts/9-1.webp)

Visual Studio Code

1. **해시 함수 사용을 위해 'crypto' 모듈을 호출하고, 블록체인 배열을 담을 변수를 생성한다.**
2. **제네시스(생성자, init 같은 역할) 블록을 생성하고, 그 뒤로 블록을 이어 붙이는 함수를 작성한다.**
3. **함수를 실행해서 블록체인을 구성하고 콘솔을 통해 실행한다.**

그렇게 실행된 오른쪽 콘솔 화면은 제네시스 블록부터 시작해서 총 5개의 블록을 보여주고 있다.

![](/assets/images/posts/9-2.webp)

Visual Studio Code

내용물을 살펴보자. 각각의 블록을 대표하는 headerHash는 모두 그다음 블록의 previousHash와 같은 값을 가지고 있다. 즉 모든 블록이 headerHash와 previousHash로 연결이 되어있는 구조다.

만약, 특정 블록의 데이터를 고의로 변경한다면 해당 블록의 headerHash가 변경되고 변경된 headerHash는 그 다음 블록의 previousHash와 일치하지 않기 때문에 블록체인 내부에서 변경된 블록을 포함한 일련의 과정은 모두 무효로 처리된다. 물론 이러한 프로세스는 현재 코드에는 구현되어 있지 않다.

**무작위(인간의 수준에서)로 나열된 hash는  어떻게 만들어진 것일까?**

![](/assets/images/posts/9-3.webp)

Visual Studio Code

여기서는 편의상 'crypto' 라는 모듈을 호출해서 이미 구현된 'SHA256'이라는 해시 함수를 사용했다.

> 'SHA'는 Secure Hash Algorithm이라는 뜻에서 NSA에서 설계한 표준 암호 알고리즘이다.

update()는 암호화하고자 하는 데이터를, digest()는 보여주고자 하는 방식을 입력받는다. 여기서는 'firstblock'이라는 데이터를 SHA256 함수로 암호화하고 'hex' 방식을 통해 Hash값을 얻었다.

그리고 Timestamp라는 변수를 볼 수 있는데, 비트코인의 Timestamp와 조금 다르다. 비트코인에서 Timestamp는 유닉스 시간으로 1970년 1월 1일 00:00:00시부터 현재까지 경과한 시간을 초로 환산하여 저장하고 있지만 여기서는 이해를 돕기 위해 date() 함수를 통해 현재 시간을 그대로 입력받고 있다.

![](/assets/images/posts/9-4.webp)

Visual Studio Code

시간순으로 기록한다는 점이 블록체인의 핵심이고, 각 블록은 그 순서대로 고유 번호를 부여받는다. 이러한 특성을 구현하기 위해 index라는 변수를 두고 blockchain.length를 통해 블록체인의 길이를 저장하는 방식으로 구현했다. 그리고 createBlock()이라는 함수는 argument로 'data'를 입력받는데 여기서는 블록 순서를 네이밍 해서 입력해주었지만 거래 내역 혹은 기록할 정보들을 문자열 그대로 입력할 수도 있다.

참고로, 블록을 만드는 과정에서 해시 함수를 사용할 때 주의할 점은 전역 변수로 지정하지 않은 'headerHash' 변수를 그대로 사용할 수는 없다는 것이다. 전역 변수는 프로그래밍할 때 스코프를 고려하지 못해 나타나는 에러로, 블록체인을 구현할 때 특히 헷갈릴 수 있다.

![](/assets/images/posts/9-5.webp)

Visual Studio Code

이렇게 우리는 'previousHash'와 'headerHash'를 연결하는 것을 통해 미니 블록체인을 구현해보았다. 이번 실습으로 블록체인에서 해시함수가 담당하는 '위변조를 방지하는 역할'에 대해 이해했다면 이제는 이를 기반으로 로직을 한 층씩 더 쌓아나가며 더 큰 블록체인을 만들어갈 수 있다.



**관성을 이기는 데이터**