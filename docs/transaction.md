# Transaction

여러 SQL이 하나의 동작처럼 되어야할 때, begin-end 문 사용한다. end가 나오기 전까지는 commit 이 안됨.

- DELETE FROM table WHERE 가능, WHERE 없으면 전체 레코드 삭제
- TRUNCATE 전체 레코드 삭제, 조건 불가능, 훨씬 빠름

**트랜잭션이란?**

- Atomic하게 실행되어야 하는 SQL들을 묶어서 하나의 작업처럼 처리하는 방법
- BEGIN과 END 혹은 BEGIN과 COMMIT 사이에 해당 SQL들을 사용
- ROLLBACK

**트랜잭션 구현방법**

- 두 가지 종류의 트랜잭션이 존재

  - 레코드 변경을 바로 반영하는지 여부. autocommit이라는 파라미터로 조절가능

- autocommit=True

  - 기본적으로 모든 SQL statement가 바로 커밋됨
  - 이를 바꾸고 싶다면 BEGIN;END; 혹은 BEGIN;COMMIT을 사용 (혹은 ROLLBACK)

- autocommit=False

  - 기본적으로 모든 SQL statement가 커밋되지 않음
  - 커넥션 객체의 .commit()과 .rollback()함수로 커밋할지 말지 결정
    -> 같은 세션에서는 데이터가 보임. 작업하며 내가 원하는대로 데이터가 저장되었는지 확인하고 commit하여 db에 최종 반영할 수 있음.

- 무엇을 사용할지는 개인 취향
  - python try/catch 와 같이 사용하는 것이 일반적
    - try/catch 로 에러가 나면 rollback을 명시적으로 실행, 에러가 안 나면 commit을 실행
  - try/except 사용시 유의할 점
    - except에서 raise를 호출하면 발생한 원래 exception이 위로 전파됨
    - cur.execute("ROLLBACK;") 뒤에 raise를 호출해주는 것이 좋음
