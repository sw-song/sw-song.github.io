---
layout: post
title: HTML element, CSS
date: 2019-09-24
categories: ["Web/JavaScript"]

---


HTML은 다양한 요소(element)들로 구성되어 있다.

요소란, '&lt;태그&gt; 내용 &lt;/태그&gt;' 에서 밑줄 친 전체를 뜻한다. 즉, 태그를 포함해 태그로 감싼 내용까지 모두 '요소'라고 한다. 그리고 요소는 어떤 형태를 만들어내는데, 그 형태를 기준으로 블록 요소와 인라인 요소로 나눌 수 있다.

그렇게 요소를 이루는 태그 중 <div> 태그와 <span> 태그를 살펴볼텐데, <div>와 <span> 태그는 그 자체만으로 특별한 기능을 갖고 있지 않아서 다방면으로 사용될 수 있다. 그래서 무분별하게 사용될 수 있다.

아래 이미지는 블록 요소와 인라인 요소에 css로 배경색을 넣었을 때 어떻게 표현되는지 보여준다.

![](/assets/images/posts/7-0.webp)

codepen.io

'hello block'은 화면 끝까지, 'hello inline'은 글자가 끝날 때까지만 색칠이 되었다. 그렇다. '<div>~' 는 블록 요소, '<span>~' 은 인라인 요소다. 그리고 '<div>~' 요소의 영역이 해당 줄 전체를 포함하기 때문에 **줄 바꿈**이 일어난다는 것을 알 수 있다.

아래 이미지는 블록 요소와 인라인 요소에 css로 사이즈를 변경했을 때 어떻게 표현되는지 보여준다.

![](/assets/images/posts/7-1.webp)

codepen.io

인라인 요소인 '<span>~' 은 heigh, width 값을 가지지 않기 때문에 텍스트에만 배경색이 칠해진다. 반면 '<div>~' 는 '박스'의 모습으로 아주 예쁘게 만들어졌다.

그러나 인라인 요소도 박스처럼 그릴 수 있다. '<span>~'은 '<div>~'처럼 padding 속성을 가지고 있기 때문에 이를 이용하면 된다.

![](/assets/images/posts/7-2.webp)

codepen.io

그러나 padding을 잘 못 다루면 다른 영역도 침범하게 돼서 전체 디자인이 망가질 수 있다.

이럴때는, **display:block;** 을 넣어주면 되겠다.

![](/assets/images/posts/7-3.webp)

codepen.io

인라인 요소를 다룰 때 또 주의해야 할 점은 블록 요소를 포함할 수 없다는 것이다. 아래 이미지는 블록 요소인 <h1> 태그를 인라인 요소 <span>으로 감쌌을 때 해당 요소에 css 적용이 안되는 것을 보여준다.

![](/assets/images/posts/7-4.webp)

codepen.io

제목 태그인 <h1>~<h6>는 모두 '블록 요소'이므로 인라인 요소가 아니라 **블록 요소에 직접 접근해서 css를 적용**해야 한다.

![](/assets/images/posts/7-5.webp)

codepen.io



**관성을 이기는 데이터**