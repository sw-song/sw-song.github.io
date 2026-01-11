---
layout: post
title: JavaScript - '객체 참조', assign()
date: 2019-11-10
categories: ["Web/JavaScript"]

---


자바스크립트에서 객체는 복사되지 않고, 참조된다. 이러한 이유에서 예상하지 못했던 값의 변화로 에러를 경험하곤 한다.

사람은 현실에서든, 코드에서든 원본이 변하는 것을 좋아하지 않는다. 원본은 유일해야 하며 필요에 따라 수정할 경우 복사본을 이용하는 것이 좋다. 이런 점에서 객체를 참조하고, 원본을 수정할 수 있는 자바스크립트의 특성은**취약점**이다.

자바스크립트는 **prototype**을 통해 얼마든지 객체 원본을 변형할 수 있다. ES2015부터 이 **취약점**을 해결하기 위해 assign()이라는 메서드를 제공하고 있다. 특정 객체를 전달할 때 원본을 참조하는 것이 아니라 새로 만들어서(복사) 전달하자는 컨셉이다.

사실 assign() 메서드가 등장하기 전까지는 주로 json을 활용했다. 객체를 json 형태로 변환시키고 다시 변환된 json을 새로운 객체로 저장하면서 같은 내용의 서로 다른 객체를 만드는 방식이다. 

```
let car = {
    color:'red',
    price:500,
    fe:9
    }
  
let carJson = JSON.stringify(car)   //obj를 json 문자열로 변환
let newCar = JSON.parse(carJson) // json 문자열을 객체로 변환

console.log(newCar) // { color: 'red', price: 500, fe: 9 }
```

그러나 json변환을 거치는 것은 코드가 길어지고 객체의 복사가 잦은 코드일수록 매우 피곤한 작업이 된다. 새로 등장한 assign() 메서드는 이에 비해 편리하고 간결한 문법을 제공한다.

```
let car = {
    color:'red',
    price:500,
    fe:9
    }

let newCar = Object.assign({}, car) // 새로운 객체 {}를 만들고 car 객체 복사

console.log(newCar) // { color: 'red', price: 500, fe: 9 }
```

> The Object.assign() method is used to copy the values of all enumerable own properties   
> from one or more source objects to a target object. It will return the target object.  
> -mozilla.org

문법의 명세 **Object.assign(target, ...sources)**에서 assign은 다수의 parameters를 전달받는데, 첫 번째는 만들고자 하는 target object, 그 외에는 모두 복사하고자 하는 source objects다. 즉 위의 코드에서 newCar로 새로이 만들고자 하는 객체 {}를 target으로 설정해주고, source object로서 car 객체를 이용했다고 할 수 있다. 

assign() 메서드를 사용할 때에 있어서 주의할 점은 '객체 병합' 현상이다. 만들고자 하는 target object를 빈 객체로 두지 않고 먼저 내용을 담은 경우 source object에 같은 속성이 포함되어 있다면 '덮어쓰기'를 한 것처럼 병합이 이루어진다.

![](/assets/images/posts/30-0.webp)

새로운 객체를 담을 변수 returnedTarget은 target object로 만들어진다. 그렇다는 것은 target(객체)은 returnedTarget과 내용이 동일하다는 것을 의미한다. assign() 메서드에서 객체를 만들고 그 객체를 returnedTarget에 반환한 것이므로 target을 확인해보면 **{ a : 1, b : 2}**가 아닌 **{ a : 1, b : 4, c : 5 }**로 출력되는 것이다.

따라서 객체의 원본이 변하지 않도록 하기 위해서는 아래와 같이 target object는 빈 객체로 만들어주고 source objects를 넣어주는 방식으로 코드를 작성하는 것이 좋다.

![](/assets/images/posts/30-1.webp)

이렇게 assign() 메서드를 활용하면 객체의 원본을 유지하고 참조 관계를 완전히 단절시킬 수 있다.

정리하면, 변수의 상태가 변하면 에러가 발생할 가능성이 증가하는데 특히 **원본이 저장된 변수의 상태가 변하는 것은****코드에 치명적인 문제를 야기할 수 있다.**따라서 객체가 다른 변수에 넘겨질 때 "참조가 아닌 복사가 되도록"하기 위해 assign()을 적극적으로 사용할 필요가 있다.



**관성을 이기는 데이터**