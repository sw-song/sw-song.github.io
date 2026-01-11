---
layout: post
title: JavaScript - 가변인자, 클래스, 배열 순회
date: 2019-11-02
categories: ["1. 기술", "웹, 자바스크립트"]

---


자바스크립트의 높은 자유도는 협업을 하거나 에러를 수정할 때 불편함으로 다가온다. 따라서 고의적으로 명시적 코드를 작성해줄 필요가 있다. 처음 입문하더라도 명시적인 코드와 관련해 대표적인 3가지 유형을 알고 넘어가면 좋다. **'가변 인자'**, **'클래스'** 그리고 **'배열 순회'**에 대해 알아보자.

#### 1. 가변 인자

자바스크립트의 함수는 인자를 적게 받거나 다른 타입으로 받더라도 오류가 발생하지 않는다. 매개변수를 지정하지 않고 변할 수 있는 인자, 즉 가변 인자를 받을 수 있도록 되어 있기 때문이다.

```
function sum() {
    let res = 0;
    for (let i = 0; i &lt; arguments.length; i++) {
        res += arguments[i]; // 선언하지 않은 arguments를 사용하고 있다. 
    }
    return res;
}
```

arguments는 함수 내부적으로 가지고 있으며 우리가 선언하지 않았음에도 동작한다. arguments는 무엇일까?

```
function sum() {
    let res = 0;
    for (let i = 0; i < arguments.length; i++) {
        res += arguments[i]; // 선언하지 않은 arguments를 사용하고 있다. 
    }
    console.log(arguments);
    return res;
}

sum(1,2,3,4)
```

코드를 실행하면 아래와 같이 출력된다.

```
[Arguments] {'0':1, '1':2, '2':3, '3':4}
```

arguments는 객체다. 이러한 형태의 객체를 유사 배열이라고도 한다. parameter가 정의되어 있지 않다는 점과 유사 배열로 동작한다는 점은 직관적이지 않고 불편하다. 유사배열이 아니라 우리에게 익숙한 (오리지날?)배열을 돌려받기 위해 같은 함수를 다른 방식으로 작성해보자.

```
function sum(...args) {
    let res = 0;
    for (let i = 0; i < args.length; i++) {
        res += args[i]; // 선언하지 않은 arguments를 사용하고 있다. 
    }
    console.log(args);
    return res;
}

sum(1,2,3,4)
```

이렇게 작성하면, **...args**라는 parameter로 가변 인자가 들어온다는 것을 명시적으로 확인할 수 있다. 출력하면 아래와 같이 배열을 반환해준다.

```
[1,2,3,4]
```

마음이 편안하다.

#### 2. 클래스

자바스크립트에서 클래스라는 문법이 생겨 클래스에서 constructor 명시할 수 있게 되었다. 또한 클래스는 new 연산자로 호출하지 않으면  즉시 에러가 난다는 점에서 명시적 코드를 요구한다.

함수는 new 연산자 사용을 강제할 수 없지만 class는 반드시 new로 인스턴스를 생성해야만 동작한다. 함수 형태의 코드를 보자.

```
function Car(make, model, year){
	 this.make = make;
  	 this.model = model;
   	 this.year = year;
}

// descriptiveCar 메소드는 상속받는 모든 객체에 필요하지 않기 때문에 prototype에 따로 저장한다.
Car.prototype.descriptiveCar = function(){
    return `
    make : ${this.make} 
    model : ${this.model} 
    year : ${this.year}
    `;
}
```

위 함수와 동일한 기능을 하도록 클래스로 구현해보자.

```
class Car {
    constructor(make, model, year) {
            this.make = make;
            this.model = model;
            this.year = year;
        } // 생성자에 바로 저장되는 부분
        
    descriptiveCar() {
        return `
            make : ${this.make} 
            model : ${this.model} 
            year : ${this.year}
            `; 
    } // 프로토타입에 저장되는 부분
}
```

Car 클래스는 생성자다. 비유적으로 표현하면 붕어빵이라는 객체를 생성해내는 붕어빵 틀이다. Car라는 객체 생성 공장(생성자)을 통해 새로운 객체를 만들어보자.

```
class fistCar extends Car {
	constructor(make, model, year) {
    	super(make, model, year);
    }
} // firstCar만 따로 가지는 속성이 없기 때문에 constructor를 작성해주지 않아도 되지만 명시하는 것이 권장된다.

class secondCar extends Car {
	constructor(make, model, year) {
    	super(make, model, year);
    }
    	descriptiveCar() {
    		return 'this is my second Car'
    } // descriptiveCar 메소드를 오버라이딩. 하위 스코프에서 새로 메소드를 지정해주면 상위 스코프는 참조하지 않는다.
}

// secondCar는 descriptiveCar() 메소드를 직접 내장하고 있지 않고 프로토타입을 참조하므로 다음과 같이 호출해야 한다.
console.log(secondCar.prototype.descriptiveCar())
```

생성자를 constructor로 명시하고 상속관계를 만들어줘서 기존의 \_\_proto\_\_와 prototype으로 작성된 코드를 개선했다. 이렇게 클래스를 활용해 코드를 짜면 extends라는 키워드로 상속 관계를 좀 더 분명하게 확인할 수 있게 되고, 파이썬과 같은 다른 객체 지향 언어에서 사용하는 super()를 통해 부모 클래스에 대해 코드로 명시할 수 있어서 더 직관적이고 편리하다.

기존에 함수로 상속을 구현할 때 상위 함수의 prototype을 직접 연결해줘야 했지만 자바스크립트에 class가 도입되면서 extends를 활용하면 이렇게 편하게 상속 관계를 만들 수 있다. 물론 자바스크립트의 class는 다른 객체 지향 언어의 개념과는 차이가 있기 때문에 \_\_proto\_\_ 그리고 prototype에 대한 이해를 필요로 한다.

#### 3. 배열 순회

ES5부터 등장한 배열 순회 메소드는 다음과 같다.

&gt; forEach   
> map,   
> filter,  
> sort,  
> reduce,   
> every/some,   
> indexOf,   
> …

이 중 자주 비교가 되는 forEach와 map을 다뤄보자.

기존 자바스크립트는 배열의 데이터를 활용하고자 할 때 주로 for문과 같이 반복문을 사용했다. 하지만 조건문과 반복문처럼 조건에 값(데이터)이 들어가는 형태는 에러가 발생할 경우 종종 디버깅을 어렵게 한다. 값을 잘못 입력하거나 값이 저장된 변수가 변하면 코드는 동작하지만 잘못된 결과가 나올 수 있기 때문이다. (에러를 확인하기 어렵다는 뜻이다.)

따라서 항상 코드를 작성할 때에는 최대한 값(데이터)을 분리시키는 것이 필요하다. 예시 코드를 보자.

```
let car = [
  {make : 'audi', model : 'a4'},
  {make : 'bmw', model : 'm4'},
  {make : 'kia', model : 'k5'}
];

for(let i=0; i<car.length; i++) {
  console.log(`${i+1}. make : ${car[i].make} / model : ${car[i].model}`)
}
```

```
1. make : audi / model : a4
2. make : bmw / model : m4
3. make : kia / model : k5
```

이러한 코드 형태를 '**명령형 패러다임**'이라고 한다. 조건을 매번 확인하고 실행하는 식으로, 변수 i가 1씩 증가하며 계속 교체된다. 이 방식은 인덱스를 잘못 잡거나 변수에 초기값이 잘못 들어가는 경우 초과 인덱스와 같은 형식으로 에러가 난다면 다행이지만 더 복잡한 코드에서는문제를 확인하기 어렵다.

forEach()는 이런 문제를 해결한다.

```
let car = [
  {make : 'audi', model : 'a4'},
  {make : 'bmw', model : 'm4'},
  {make : 'kia', model : 'k5'}
];

/*
for(let i=0; i<car.length; i++) {
  console.log(`${i+1}. make : ${car[i].make} / model : ${car[i].model}`)
}
*/

car.forEach(function(eachCar, idx) {
  console.log(`${idx+1}. make : ${eachCar.make} / model : ${eachCar.model}`);
});
```

forEach()는 전달인자로 함수를 받는다. 이 함수의 경우 콜백 함수로 세 인자를 받아 호출된다.

첫번째 인자로 배열 원소의 값(currentValue)을, 두번째 인자로 각 원소의 인덱스(index)를, 세번째 인자로 배열(array) 자체를 받는다.

보통 데이터인 배열 원소에 접근하고자 하므로 첫번째 인자만 기재하는 경우가 많다. 여기서는 인덱스까지 넣어주었다. forEach는 각 요소에 접근할 때마다 콜백함수를 호출하기 때문에 여기서는 콜백함수를 총 세번 호출했다.

콘솔을 확인해보면 이전 코드와 동일한 결과값이 나온다.

```
1. make : audi / model : a4
2. make : bmw / model : m4
3. make : kia / model : k5
```

그렇다면 map은 어떻게 동작할까? map은 forEach와 같이 첫번째 전달인자로 함수를 받고, 그 함수 역시 동일하게 currentValue, index, array 순서로 인자를 가지고 호출되는 콜백 함수다. 차이점은 콜백함수의 결과(return)값들로 구성된 새로운 배열을 반환한다는 것이다.

역시 코드를 보자.

```
let car = [
  {make : 'audi', model : 'a4'},
  {make : 'bmw', model : 'm4'},
  {make : 'kia', model : 'k5'}
];

/*
for(let i=0; i<car.length; i++) {
    console.log(`${i+1}. make : ${car[i].make} / model : ${car[i].model}`)
}
*/

/*
car.forEach(function(eachCar, idx) {
    console.log(`${idx+1}. make : ${eachCar.make} / model : ${eachCar.model}`);
});
*/

cars = car.map(function(eachCar, idx){
    return `${idx+1}. make : ${eachCar.make} / model : ${eachCar.model}`;
})

console.log(cars)
```

forEach를 사용할 때와 형태는 비슷하다. 눈에 띄는 차이가 있다면 forEach는 console.log를 바로 찍은 반면, map은 return을 해줬다는 점이다. 앞서  언급했듯 map의 기능은 return된 값들로 새로 배열을 만든다. 따라서 콘솔창을 확인해보면 하나의 배열로 묶여있다.

```
[1. make : audi / model : a4
 2. make : bmw / model : m4
 3. make : kia / model : k5]
```



**관성을 이기는 데이터**