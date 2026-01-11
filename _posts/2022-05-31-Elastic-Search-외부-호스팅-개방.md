---
layout: post
title: Elastic Search - 외부 호스팅 개방
date: 2022-05-31
categories: ["1. 기술", "서버, 데이터, 클라우드"]

---


외부에서 엘라스틱서치 클러스터에 접속하기 위해서는 config/elasticsearch.yml 파일에서 network.host: “\_stie\_” (혹은 internet-ip) 를 입력해줘야 한다.

**그런데, 이렇게 수정하고 실행하면 부트스트랩 에러가 발생한다.**

![](/assets/images/posts/74-0.webp)
![](/assets/images/posts/74-1.webp)

**이 부분을 해결하려면 /etc/security/limits.conf 파일과 /etc/sysctl.conf 파일 수정 통해 리소스 제한을 영구적으로 풀어줘야한다.**

**수정 내용은 아래 이미지 참고)**

![](/assets/images/posts/74-2.webp)
![](/assets/images/posts/74-3.webp)

수정했다면, 리눅스 시스템을 다시 올린다.

**$sudo shutdown -r**

![](/assets/images/posts/74-4.webp)

추가로, config 파일에 discovery.seed\_hosts로 호스트 설정도 해줘야 한다.

![](/assets/images/posts/74-5.webp)

**이렇게 외부 호스트를 열고 실행시, 내부에서는 이제 localhost로는 접속이 안되고, 내부 IP로 접속해하는데, 만약 localhost로도 접속하고싶으면 아래와 같이 배열로  “\_local\_” 추가한다.**

![](/assets/images/posts/74-6.webp)

curl 명령어로 호출해보면 정상적으로 연결이 된다.

![](/assets/images/posts/74-7.webp)

**내부가 아닌 외부에서는 당연하게도 외부 IP로 접속해야하며 이를 위해 방화벽을 열어준다.**

![](/assets/images/posts/74-8.webp)

**좌- 내부접속, 우-외부접속**

![](/assets/images/posts/74-9.webp)



**관성을 이기는 데이터**

[저작자표시
(새창열림)](https://creativecommons.org/licenses/by/4.0/deed.ko)