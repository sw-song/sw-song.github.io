---
layout: post
title: JavaScript - DOM(Document Object Model) 제어
date: 2019-10-20
---


> DOM(Document Object Model)

DOM은 브라우저가 제공하는 객체(BOM-Browser Object Model) 중 하나로 BOM의 가장 상위 객체인 Window의 하위 객체라고 볼 수 있다. 넓은 의미로 DOM은 웹브라우저가  HTML 문서를 인식하는 방식을 말하며 객체 참조를 통해 이루어진다. DOM이 제공하는 기능은 **C(create), R(read), U(update), D(delete)** 4가지다.

DOM을 사용해보자.

```html
&lt;html&gt;
  &lt;head&gt;
  &lt;/head&gt;
  &lt;body&gt;
    &lt;div id='el'&gt;&lt;/div&gt;
  &lt;/body&gt;
&lt;/html&gt;
```

javaScript로 Html을 조작하기 위해 DOM을 사용해서 접근할 수 있다.

```
let elmts = document.getElementsByTagName('div');
```

이렇게 **getElements**라는 복수 형태를 사용하면 변수 elements는 배열 형태로 div를 가진다.

따라서 현재 코드에는 단 하나의 div만 존재하지만 div가 여러개 있다고 가정하면, 첫 번째 div에 접근하기 위해서는 elements[0]으로 불러내면 된다.

만약 배열 인덱스를 이용하고 싶지 않다면 단수 형태로 변수를 만들어준다.

```
let elmt = document.getElementById('el')
```

이렇게 **getElementById** 메소드를 사용하면 **id**값으로 접근할 수 있고, 하나의 element만 특정해서 접근이 가능하다. 그러나 getElement는 Id를 지정해주지 않는 이상 클래스를 포함해 모든 태그를 복수형으로 받아와야 한다는 불편함이 있다.

따라서 가장 첫 번째 요소만 가져오기를 원한다면, **querySelector** 를 사용해주는 것이 편하다.

```
let elmt = document.querySelector('div');
```

이렇게 해주면 가장 첫 번째 div element를 입력받게 된다. 뿐만아니라 querySelector를 사용하면 **띄어쓰기(엘리먼트 하위), >(자식 태그), 아이디 선택자(#),****클래스 선택자(.)**를  통해 원하는 태그에 접근할 수 있다.

따라서 **querySelector**는 태그명이 유일한 사용자 정의 태그에 접근하거나 특정 깊이의 위치에 있는 하나의 태그에 접근하기에 매우 효율적이다. 만약 **getElementsByTagName**을 사용한 것처럼 리스트로 돌려받고 싶다면 '**querySelectorAll**'을 사용하면 된다.

웹이 점점 발전하면서 그저 HTML 문서를 보여주는 것이 아닌 사용자가 입력하고 브라우저가 반응하는 형태(반응형이 아니라 이벤트를 설명하고 있다.)의 UI가 필요해졌다. 그러나 순수한 자바스크립트만으로는 그저 작성된 그대로 시간 순서대로 한 줄씩 읽어나갈 뿐 사용자의 입력을 기다리는 식의 동작은 불가능하다. 대신 브라우저는 자체적으로 'Event'(사건, 이벤트)를 제공한다. 팝업을 띄우거나 입력을 받고 페이지를 전환하는 등의 기능을 말한다. 이것이 바로 DOM 객체의 역할이며 이러한 이벤트를 동작시킬 수 있는 메소드를 지닌다. 

**자바스크립트는 DOM 객체를 통해 브라우저가 제공하는 이벤트를 제어할 수 있다.**

```html
&lt;div&gt;
  &lt;form id="js_obj"&gt;
    &lt;button type='isevent'&gt;
      &lt;span&gt;Click&lt;/span&gt;
    &lt;/button&gt;
  &lt;/form&gt;
&lt;/div&gt;
```

위 코드는 아래 캡쳐 화면과 같이 사용자가 클릭할 수 있는 버튼을 만들어낸다.

![](/assets/images/posts/22-0.webp)

Click 버튼을 누르게 되면 브라우저는 'isevent'라는 이벤트를 발생시킨다. 이때 DOM은 'isevent' 이벤트를 제어할 수 있도록 기능을 제공한다.

```
form = document.querySelector('#js_obj');

function popAlert(event){
  event.preventDefault()
  alert('hi')
};

form.addEventListener('isevent',popAlert);
```

먼저 아이디 선택자(#js\_obs)를 이용해 HTML의 버튼 form을 가져왔다. 그리고 **form.addEventListener** 메소드를 이용해 'isevent' 이벤트를 동작시키면 이벤트를 기다리던 브라우저는 'hi'라는 메시지를 띄워준다.

![](/assets/images/posts/22-1.webp)

공유하기

게시글 관리

**관성을 이기는 데이터**