---
layout: post
title: Python Django - blog, admin
date: 2020-05-17
categories: ["Technology"]

---


> [장고걸스 튜토리얼](https://tutorial.djangogirls.org/ko/django_start_project/)을 참고했습니다.

manage.py 가 있는 파일 경로로 들어가서 아래 명령어를 실행한다.

% python manage.py startapp blog

- manage.py 파일이 있는 경로에서 blog 파일을 생성한다.

![](/assets/images/posts/41-0.webp)

그럼 이렇게 blog라는 이름의 폴더가 생성되고,

![](/assets/images/posts/41-1.webp)

apps.py 파일, migrations 폴더를 포함해 여러 가지 항목들이 패키지로 설치된 것을 확인할 수 있다.

![](/assets/images/posts/41-2.webp)

> (\*참고) 장고 걸스에서 가져온 현재 디렉터리 모습

![](/assets/images/posts/41-3.webp)

blog 모델을 생성했다면 이 App이 설치되었다고 알려줘야한다. mysite에서 다시 settings.py를 실행한다.

![](/assets/images/posts/41-4.webp)

INSTALLED\_APPS를 찾아서 'blog'를 추가해준다.

![](/assets/images/posts/41-5.webp)

이렇게 'blog' 앱이 설치된 것을 인식시켜줬다면, 다음으로 blog에 대해서 어떤 모습으로 구현할 것인지 상세 코드를 작성해줘야한다.

blog에서 models.py를 연다.

![](/assets/images/posts/41-6.webp)

장고 걸스에서 표준으로 공유한 코드를 넣어준다. 아래 코드는 블로그로서 필요한 기능들을 넣는 동작을 수행한다.

![](/assets/images/posts/41-7.webp)

이제, 우리가 만든(models.py) blog에 대해 migration을 해주면,

![](/assets/images/posts/41-8.webp)

Post라는 새로운 모델이 생성된다.

% python manage.py migrate blog

- 데이터베이스에 모델을 추가해준다.

![](/assets/images/posts/41-9.webp)

정상적으로 잘 반영이 되었고 생성된 Post모델을 불러와 admin에 등록한다. 관리자 페이지를 만드는 과정이다.

![](/assets/images/posts/41-10.webp)

이제 % python manage.py runserver를 입력해서 서버를 구동시켜본다.

![](/assets/images/posts/41-11.webp)

기존 서버 주소에 /admin/을 붙여주면 관리자 페이지로 이동한다.

 <http://127.0.0.1:8000/admin/> 

![](/assets/images/posts/41-12.webp)
![](/assets/images/posts/41-13.webp)

우리는 아직 아이디/비밀번호가 없기 때문에 superuser(관리자)를 생성해줘야 한다.

잠깐 서버를 종료하고

% python manage.py createsuperuser

를 실행하면 계정을 생성하는 명령어들이 순차적으로 나온다.

![](/assets/images/posts/41-14.webp)

생성된 계정을 입력하면 아래와 같이 관리자 화면으로 넘어간다.

![](/assets/images/posts/41-15.webp)

Blog니까 글도 한번 써보자.

![](/assets/images/posts/41-16.webp)
![](/assets/images/posts/41-17.webp)

포스팅까지 정상적으로 잘된다.



**관성을 이기는 데이터**