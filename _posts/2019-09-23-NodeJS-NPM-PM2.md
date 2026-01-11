---
layout: post
title: NodeJS - NPM, PM2
date: 2019-09-23
categories: ["Web/JavaScript"]

---


Pm2는 NodeJS의 Package Manager인 'NPM'을 통해 설치할 수 있는 Package 중 하나로 단순 반복 작업을 도와주면서 에러를 실시간으로 감시하게 해주는 고마운 모듈이다. 생활코딩으로 유명하신 '이고잉'님의 말을 빌리면 NPM은 **NodeJS계의 앱스토어**다. 

주 기능은 **NodeJS를 사용하는 서버 측 관리자에게 편의를 제공하는 것**이다.

NodeJS로 구동하는 서버가 무너지지 않게 유지해주고, 코드를 리로드 하고 잘 동작하는지 확인하는 과정을 전체를 편리하게 해주면서 전체 프로세스 과정에서 매번 발생하는 로그를 실시간으로 보여준다. 

![](/assets/images/posts/4-0.webp)

pm2 monit

왼쪽은 현재 구동하고 있는 스크립트, 오른쪽은 전역에서 발생하는 로그를 보여준다. 강제로, 혹은 실수로 서버가 다운된다면

오른쪽에서 그러한 내용을 보여주면서 다시 서버를 살려놓는다.

사용 방법은 아래와 같다.

우선 npm을 통해 전역에 pm2를 설치해준다.

```
npm install pm2 -g
```

다음으로 pm2를 실행하고 모니터링을 시작한다.

```
pm2 start main.js --watch
```

아래 이미지는 pm2가 실시간으로 모니터링하는 모습니다.

![](/assets/images/posts/4-1.webp)

pm2 start main(main.js) --watch

여기서 pm2 start main 혹은 main.js 까지만 타이핑해도 실행이 되지만 **--watch** 까지 작성해주는 것이 좋다.

**"코드를 리로드 하고 잘 동작하는지 확인하는 과정을 전체를 편리하게 해 준다"** 라는 pm2의 두 번째 기능을 잘 활용하기 위해서다.

```
pm2 start main --watch
```

이를 통해 위 vscode 캡쳐화면서에서 드래그된 20번째 라인을 수정함과 동시에 nodejs를 재시작하지 않고도 페이지가 변하는 모습을 볼 수 있다.

![](/assets/images/posts/4-2.webp)

웹 동작 화면

코드를 작성하고 제대로 동작하는지 확인하기 위해서는 웹브라우저 화면뿐만 아니라 코드에 문제가 없는지 지속적으로 추적하고

콘솔을 확인해야한다. 즉, 모든 동작마다 실행되는 log들을 한 번에 볼 필요가 생긴다.

![](/assets/images/posts/4-3.webp)

여기 붉은 박스(Global logs)에서 동작 및 에러를 실시간으로 감시할 수 있지만 좀 더 가볍게, 로그만 뽑아서 보고싶다면

```
pm2 logs
```

를 사용하면 된다.

![](/assets/images/posts/4-4.webp)

pm2 logs (log)



**관성을 이기는 데이터**