---
layout: post
title: pythonanywhere - 장고 서버 구축
date: 2020-05-17
---


웹으로 모델을 서빙해야 하는 상황이 자주 생긴다. pythonanywhere로 간단한 개인 서버를 띄워보고 싶다면, 딱 3가지만 생각하면 된다.

1. 로컬에서 개발하고
2. Github에 원격으로 올리고
3. 외부 호스팅 업체를 사용한다.

1. 로컬 개발하고

머신러닝 모델 배포나 일반 웹서비스를 위해 html 페이지를 로컬 서버에 띄워봤을 수 있다. 주소창에 localhost : ~ / ~ 3000  이런 식으로 나타나는데 이것이 로컬 서버다. 외부에서는 접속할 수 없다.

2. Github에 원격으로 올리고

내 컴퓨터에서 작성한 코드를 clone, post 와 같은 명령어로 github에서 가져오기도 하고 repositories로 올릴 수도 있다. 다른 사람들과 코드를 공유하고, 내 코드가 변경을 하다가 이전 버전으로 돌아가고 싶은 경우 모든 기록이 github에 남아있기 때문에 쉽게 복구할 수도 있다.

3. 외부 호스팅 업체를 사용한다.

AWS와 같이 서버를 임대해주는 서비스들이다. pythonanywhere의 경우 test 서버를 잠깐 사용해보기 위한 환경을 무료로 제공한다. 실제로 서버를 운영하게 되면, 일반적으로 트래픽 발생량에 따라 빌려쓴 서버 회사는 우리에게 비용을 청구한다. 이 3가지 과정은 항상 같이 움직인다. 그리고 실력이 늘고 더 고도화된 웹을 개발한다 하더라도 크게 다르지 않다. 

생각해보자. 로컬 서버에서 여러가지 테스트를 하며 웹에 이것 저것 띄우고 만들어본다. 3일 밤낮을 새면서 만든 코드가 갑자기 사라지면 큰일나니 만드는 과정에서 깃에 add 해주고, github에 올려둔다. 그러다보니 멋진 웹이 탄생했고, pythonanywhere과 같은 호스팅 업체를 통해 외부 서버에 띄워서 다른 사람들도 이용할 수 있도록 했다. 이렇게 배포한 뒤에 트래픽 관리가 어려운 경우도 당연히 생길 수 있다. 이왕 비용을 더 지불할 겸, 더 안정적인 aws로 호스팅 업체를 바꾼다. 

앗, 그런데 사용자들이 내 웹 페이지에 에러를 발견해서 알려줬다. 이럴때에는 코드를 수정해야하는데 무작정 바꿔버릴 수는 없다. 로컬 환경에서 테스트를 거치고 문제가 없다면 다시 깃허브를 거쳐 외부 서버에 올려 새로운 웹을 보여준다.

그럼 이제 pythonanywhere 사이트를 사용해보자. 먼저 회원가입을 할 때, beginner로 설정해야 과금이 되지 않는다. 가입하면 이렇게 Dashboard를 볼 수 있다. Consoles에서 bash를 선택해서 git을 사용할 수 있게 열어준다.

![](/assets/images/posts/43-0.webp)

Bash를 열었으면, github에 원격으로 띄운 repository url을 복사해서 git clone 명령어를 통해 호스팅하는 서버에 repository를 생성한다.

$ tree my-first-blog

명령어를 통해 로컬환경과 구조를 비교해볼 수 있다. 코드는 '로컬 -> 깃허브 -> pythonanywhere' 로 거쳐왔다는 것을 다시 기억하자.

![](/assets/images/posts/43-1.webp)

현재 호스팅 서버에 내 로컬에 있던 코드를 복사해왔으니, 개발을 위한 가상환경도 만들어주자. 로컬에서의 과정과 다르지 않다.

$ cd my-first-blog

- my-first-blog 폴더로 들어간다.

$ vertualenv --python=python3.6 myenv

-여기서 'myenv'라는 이름의 가상환경을 만들어준다.

![](/assets/images/posts/43-2.webp)

$ source myenv/bin/activate

-가상환경 myenv를 실행한다.

그럼 코드 앞에 (myenv)가 표시된다.(가상환경에 잘 들어온 것이다.)

$ pip install django~=2.0

- 익숙한 장고를 설치해본다.

![](/assets/images/posts/43-3.webp)

장고가 설치되었다면 DB를 초기화한다.

$ python manage.py migrate 

![](/assets/images/posts/43-4.webp)

이어서 관리자계정을 만들어준다.

![](/assets/images/posts/43-5.webp)

계정 설정을 완료했다면 다시 pythonanywhere 사이트 Web 탭으로 들어가 Web app을 생성해준다.

![](/assets/images/posts/43-6.webp)

Next를 누르면 파이썬 버전과 프레임워크를 설정하는 부분이 나온다. Django를 선택하지 말고 manual configuration(수동 설정)을 선택한다. 파이썬은 우리가 계속 가상환경으로 세팅한 것처럼 3.6으로 지정한다.

![](/assets/images/posts/43-7.webp)

그럼 이렇게 성공적으로 Web app이 생성된 것을 확인할 수 있다. 이제 가상환경과 WSGI 파일을 설정해주도록 한다. 아래에 Virtualenv는 가상환경 경로를 설정해주는 부분이다. 앞서 bash에서 만든 가상환경 myenv의 경로를 작성해주면 된다.

/home/&lt;계정&gt;/my-first-blog/myenv 같은 형식이었다.

![](/assets/images/posts/43-8.webp)

다음으로 WSGI 파일에 코드를 작성해준다. 가상환경 바로 위 설정인 Code 항목에서 WSGI configuration file: (링크).py 파일을 클릭한다.

![](/assets/images/posts/43-9.webp)

아래와 같이 코드를 작성해주면 된다. 참고로 sw930601은 개인 계정 ID이므로 코드 항목(위 이미지)에서 Working directory가 어떤 이름으로 되어 있는지 각자 확인해야 한다.

![](/assets/images/posts/43-10.webp)

&nbsp;&nbsp;

이제 저장하고, 가장 상단의 사이트 주소를 클릭하고 웹을 구경해본다.

![](/assets/images/posts/43-11.webp)

로컬 환경에서 띄웠던 웹이 똑같이 나온다. 휴대폰을 들고 적힌 주소로 들어가보면 동일한 사이트가 나타난다. 이제 Rest api 등 통신 방식을 활용해 서버측 모델을 사용자에게 랜더링해주면 된다.

공유하기

게시글 관리

**관성을 이기는 데이터**