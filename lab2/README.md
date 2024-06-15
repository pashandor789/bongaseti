Реализован поиск минимального MTU в канале между локальным пользователем и хостом
Скрипт проверен на macos и на ubuntu

```
$ docker build . -t seti
$ docker run -i -t seti
Checking MTU for host: brazzers.com
MTU 750 is bad
MTU 375 is ok
MTU 562 is bad
MTU 468 is ok
MTU 515 is bad
MTU 491 is bad
MTU 479 is ok
MTU 485 is bad
MTU 482 is ok
MTU 483 is ok
MTU 484 is bad
Minimal MTU for brazzers.com = 483
```