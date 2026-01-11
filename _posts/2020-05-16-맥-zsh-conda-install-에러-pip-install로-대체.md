---
layout: post
title: 맥 zsh - conda install 에러, pip install로 대체
date: 2020-05-16
---


이번에 새로 산 맥에 장고를 설치하려다가 conda install 관련 에러가 있어 내용을 기록한다.

우선, 사용자폴더에서 새롭게 sw\_python이라는 폴더를 생성하고, 가상환경도 만들어 줬다. 가상환경 이름은 재미없지만 django\_venv이다.

![](/assets/images/posts/39-0.webp)

가상환경은 잘 생성되었다. conda activate django\_venv 명령어로 가상환경을 실행한다.

![](/assets/images/posts/39-1.webp)

이어서 conda install 명령어를 통해 django를 설치해줬다.

![](/assets/images/posts/39-2.webp)

그리고, 장고를 실행하기 위한 mysite와 하위 파일들을 생성하려고 시도해보았으나 No module named 'django' 메시지가 뜨면서 실행되지 않는다. 이어서 django --version 으로 설치가 되었는지 확인해보니 command not found: django 라고 알려준다. 아래 이미지에서 **문제 상황**을 볼 수 있다.

![](/assets/images/posts/39-3.webp)

혹시나해서 conda list 를 통해 django 가 설치되지 않았는지 다시 확인해보았다.

![](/assets/images/posts/39-4.webp)

django는 설치가 되어 있는데 인식을 못하는 것 같다. 이렇게 conda로 설치했을때 모듈을 찾지 못한다는 에러가 나오면 아나콘다 경로 문제일 수 있다. 복잡하니 그냥 pip로 설치해주자.

![](/assets/images/posts/39-5.webp)

잘 동작한다. mysite 폴더도 멀쩡하게 생성되었다.

![](/assets/images/posts/39-6.webp)

공유하기

게시글 관리

**관성을 이기는 데이터**