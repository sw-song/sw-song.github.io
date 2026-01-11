---
layout: post
title: '[Dolt + Python + MySQL] 금융 분석을 위한 재무제표 데이터베이스 구축과 실행'
date: 2025-05-09
---


재무제표 데이터를 확보할 때 yfinance를 많이 사용하며, 긴 시계열에 대해서는 공시자료를 스크래핑하여 필요한 table 영역만 적절히 포멧팅할 수도 있다. 가장 좋은 건 yfinance 같은 무료 api를 활용해 적정 주기마다 데이터를 가져와 적재해 두는 것인데, 상장된 모든 주가 재무정보를 개인 PC나 클라우드 서버에 저장해 두는 건 개인으로서 여간 부담되는 일이 아니다.

이때, 약소하게나마 대안으로 사용해 볼 수 있는 것이 다른 사람들이 공개해 둔 DB인데, DropBox나 DoltHub가 대표적이다. 코드가 익숙하다면 DoltHub에서 매우 쉽고 빠르게 DB 전체를 Pull 할 수 있으며 아래 예시로 사용한 1.26 GB짜리 재무데이터를 수 초 내에 모두 다운로드 가능하다.

DoltHub는 코드 버전관리를 위해 Git을 사용하는 것처럼, SQL DB의 버전관리 목적으로 이용할 수 있다. fork, clone, branch, merge, push, pull 등 git command를 그대로 차용하기 때문에 git에 익숙하다면 어렵지 않게 적응이 가능하다. Open Source라 [Github에도 코드베이스가 공개되어 있으며](https://github.com/dolthub/dolt) 여타 Open Source가 그런 것처럼 Enterprise Support 등에 대해 별도의 가격 플랜은 존재한다.

![](/assets/images/posts/156-0.webp)

예시 저장소는 미국 기업을 대상으로 하며, 상장된 모든 기업은 아니지만 상당히 많은 기업의 10년 이상 적재된 raw data를 받아볼 수 있다.

![](/assets/images/posts/156-1.webp)

post-no-preference / earnings

사용법은 Github이나 Dolt Document에서 간단히 살펴볼 수 있으니 각 명령어에 대한 설명은 공식 문서를 참고하길 바라며, 본문에서는 필요한 데이터를 추출하는 프로세스만 가볍게 다뤄보겠다.

먼저 Dolt는 Git과 같은 버전관리 도구이므로, 버전관리 대상 폴더를 지정하여 init 시키는 것이 선행되어야 한다. 만약, Dolt를 현재 작업 중인 PC에서 처음 사용한다면 DoltHub에 가입하고 가입 정보를 global config로 설정해줘야 한다. Git의 Remote 저장소를 GitHub로 설정하기 위한 작업과 동일하다.

![](/assets/images/posts/156-2.webp)

user.email, user.name 뒤에는 각자 계정 정보를 입력한다.

dolt init 명령어를 수행하면 .dolt 폴더와 함께 버전관리에 필요한 파일들이 생성되고 작업 폴더에서 SQL DB의 변경된 버전을 저장하고, 원격 저장소에 밀어 넣는 등의 작업을 수행할 수 있다.

그러나 우리는 필요한 데이터를 가져오기만 하면 되기 때문에 dolt clone 명령어와 함께 필요한 repository를 지정해주면, 현재 경로 하위에 earnings라는 폴더가 생성되고, 해당 폴더 내 .dolt 폴더 역시 확인할 수 있다.

![](/assets/images/posts/156-3.webp)

위 예시에서는 명령어 실행을 위해 임시 폴더를 사용하였음

데이터가 잘 가져왔다면 dolt를 활용해 쿼리를 실행해본다. mysql이 설치되어 있다면 기본적으로 mysql, information\_schema 2개의 database는 보일 것이고, 추가된 earnings database와 그 하위 table을 확인할 수 있다.

![](/assets/images/posts/156-4.webp)
![](/assets/images/posts/156-5.webp)

아래는 데이터를 일부 추출한 예시다.

![](/assets/images/posts/156-6.webp)

우리는 sql 서버를 dolt로 띄우고, 띄운 서버를 python으로 접근해 데이터를 쿼리 할 것이다. dolt sql-server 명령어를 수행하면 sql 로컬 서버를 기본 포트 3306번으로 띄울 수 있다.

![](/assets/images/posts/156-7.webp)

python에서는 mysql-connector-python 패키지를 설치한 다음 아래와 같이 명령어를 수행하면 SQL 서버에 진입 가능하고, pandas read\_sql 함수를 통해 쿼리가 동일하게 실행되어야 한다.

![](/assets/images/posts/156-8.webp)
![](/assets/images/posts/156-9.webp)

이제 자유롭게 필요한 데이터를 가공해 분석에 활용할 수 있는 상태다. 위와 같이 DoltHub로 기반 DB를 clone 해서 사용할 수도 있고, yfinance 등 다른 api를 통해 주기적으로 필요한 데이터만 가공, 적재할 수도 있다.

어떤 방식이든 결국 원하는 재무제표 정보를 전기간 내 손실 없이 자체 관리하는 것이 필요해진다. 금융 분석을 위한 데이터를 온전히 외부에 의존하기에는 어떤 api든 높은 비용이 발생하게 되므로 Local Server에 데이터를 적재하고 후처리 하는 일련의 데이터 파이프라인 구축 작업을 고려해야 한다. 이때, DoltHub를 사용해 보면 어떤 구조로 ERD를 구성하고 데이터를 관리해야 하는지 감을 잡을 수 있으니 첫 선택지로 좋은 옵션이다.

공유하기

게시글 관리

**관성을 이기는 데이터**

[저작자표시
(새창열림)](https://creativecommons.org/licenses/by/4.0/deed.ko)