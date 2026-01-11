---
layout: post
title: GCP - firestore
date: 2022-06-05
---


firestore를 사용하기 위해 먼저 구글 클라우드 플랫폼의 IAM 관리자에서 서비스 계정을 하나 만들어준다(이미 있으면 pass)

![](/assets/images/posts/115-0.webp)

서비스계정을 만들면 자동으로 인증키 json 파일이 다운로드 된다. 해당 파일을 가지고  나의 firebase\_admin을 초기화해주면 설정 완료.

설정(키 인식)이 끝났다면, 데이터를 넣어본다. 만약 doc\_ref 변수로 지정한 collection과 document가 없다면 알아서 생성된다.

\*데이터 구조: 컬렉션 > 문서 > 필드 > 데이터 

![](/assets/images/posts/115-1.webp)

기존에 가지고 있던 collection, document가 있다면, 해당 경로에 데이터가 추가된다

![](/assets/images/posts/115-2.webp)

문서 아래에는 하위 컬랙션을 추가할 수도 있다.

![](/assets/images/posts/115-3.webp)

해당 컬랙션에는 message 정보를 담아보자

![](/assets/images/posts/115-4.webp)

만약, 데이터프레임 형태의 데이터를 가지고 있다면 딕셔너리 타입으로 변경해서 넘겨주면 된다.

![](/assets/images/posts/115-5.webp)

그동안 사용한 set 명령어는 문서 전체를 덮어쓰게 된다. 따라서 일부 값만 수정하고 싶으면 update를 사용한다.

![](/assets/images/posts/115-6.webp)

 update 명령어를 통해 특정 필드와 필드에 해당하는 값만 삭제할 수도 있다.

![](/assets/images/posts/115-7.webp)

get()을 사용하면 단일 문서의 내용을 가져올 수 있다.

![](/assets/images/posts/115-8.webp)

만약 한 컬랙션 내의 모든 문서를 조회하고 싶다면,  컬렉션 객체에 대해 stream()함수를 사용하면 된다 단, 이 때 하위 컬렉션은 함께 조회되지 않는다.

![](/assets/images/posts/115-9.webp)

컬랙션 내 문서 조회 시 쿼리를 적용할 수도 있다.

![](/assets/images/posts/115-10.webp)

정렬 쿼리는 아래와 같이 사용한다.

![](/assets/images/posts/115-11.webp)

공유하기

게시글 관리

**관성을 이기는 데이터**

[저작자표시
(새창열림)](https://creativecommons.org/licenses/by/4.0/deed.ko)