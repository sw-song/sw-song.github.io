---
layout: post
title: JavaScript - 콜백
date: 2019-11-05
categories: ["1. 기술", "웹, 자바스크립트"]

---


### What is "callback hell"?

Asynchronous JavaScript, or JavaScript that uses callbacks, is hard to get right intuitively. A lot of code ends up looking like this:

```
fs.readdir(source, function (err, files) {
  if (err) {
    console.log('Error finding files: ' + err)
  } else {
    files.forEach(function (filename, fileIndex) {
      console.log(filename)
      gm(source + filename).size(function (err, values) {
        if (err) {
          console.log('Error identifying file size: ' + err)
        } else {
          console.log(filename + ' : ' + values)
          aspect = (values.width / values.height)
          widths.forEach(function (width, widthIndex) {
            height = Math.round(width / aspect)
            console.log('resizing ' + filename + 'to ' + height + 'x' + height)
            this.resize(width, height).write(dest + 'w' + width + '_' + filename, function(err) {
              if (err) console.log('Error writing file: ' + err)
            })
          }.bind(this))
        }
      })
    })
  }
})
```

<http://callbackhell.com/>

위 코드는 자바스크립트에서 가장 악명 높은 콜백 지옥을 구현한 것이다. 코드를 작성할 때 비동기 처리를 해야할 경우가 자주 생기게 되는데, 이 때 작성자의 의식의 흐름대로 연속적으로 콜백 함수를 사용하다보면 이렇게 알아보기 힘들 정도로 코드가 복잡해진다. 이러한 시각적 복잡성을 해결하기 위해 es6부터 Promise라는 개념이 도입되었다.

```
let p1 = new Promise(function(resolve, reject){ //true->resolve, false->reject
  setTimeout(function() {
    console.log('hello p1');
    resolve();   // ..............................성공했을 때,
  }, 1500);
});

let p2 = new Promise(function(resolve, reject){
  setTimeout(function() {
    console.log('hello p2');
    reject();    // ..................................실패했을 때
  }, 2300);
});

Promise.all([p1, p2]).then(function() {
  console.log('pass') // ..........둘 다 성공해야 출력
}).catch(function() {
  console.log('failed')  // ......실패가 있으면 출력
});
```

코드의 흐름은 다음과 같다.

**1. new를 통해 Promise를 생성해준다.**

**2. Promise는 매개변수 resolve, reject를 갖는다**

**3. 생성자 선언과 동시에 비동기 콜백이 각각 실행된다.**

**4. 코드가 실행되면 1.5초 뒤 'hello p1', 2.3초 뒤 'hello p2'가 실행되며 'hello p2'는 reject일 때 실행된 것이므로 Promise.all- 에서는 catch 메소드가 실행된다.**

만약 resolve가 실행될 시간이 더 늦도록 다음과 같이 코드를 수정한다면 어떻게 출력될까?

```
let p1 = new Promise(function(resolve, reject){ //true->resolve, false->reject
  setTimeout(function() {
    console.log('hello p1');
    resolve();   // ..............................성공했을 때,
  }, 3300);
});

let p2 = new Promise(function(resolve, reject){
  setTimeout(function() {
    console.log('hello p2');
    reject();    // ..................................실패했을 때
  }, 2300);
});

Promise.all([p1, p2]).then(function() {
  console.log('pass') // ..........둘 다 성공해야 출력
}).catch(function() {
  console.log('failed')  // ......실패가 있으면 출력
});
```

그렇다면 콘솔은

**1. hello p2**

**2. failed**

**3. hello p1**

순서로 보여주는데, Promise.all- 에서 catch 메소드는 reject가 나오는 순간 바로 동작하기 때문이다. 이렇게 Promise는 상대적으로 콜백 지옥을 읽기가 수월한 형태로 보여준다. \*비동기처리 뿐만 아니라  코드 작성 시점에서는 각각의 단위가 언제 확정될지 모르는 상황에서도  promise를 응용해서 다양하게 사용이 가능하다는 장점이 있다. 앞서 본 코드에서 볼 수 있듯이 Promise를 사용해도 콜백 함수가 그대로 노출되어 있기 때문에 함수로 둘러싼 형태는 여전히 존재하며 기존의 복잡한 코드를 문단으로 나눈 것 같은 효과에 그치게 된다.



**관성을 이기는 데이터**