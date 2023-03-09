# SQL의 장단점

#### **장점**

- 사용하기 쉽고 시간이 지남에 따라
  - SQL은 원래 70년대 초 IBM에서 개발되었습니다.
  - 구조화된 데이터 작업에 가장 적합한 언어(관계형 데이터베이스)
    - 데이터는 레코드(행) 및 필드(유형이 있는 열)가 있는 테이블(구조화)에 저장됩니다.
  - 두 부분으로 구성되어 있습니다.
    - DDL: 데이터 정의 언어
      - CREATE TABLE, DROP TABLE, ALTER TABLE
    - DML: 데이터 조작 언어
      - SELECT, INSERT INTO
  - 2000년대 중반에는 새로운 빅 데이터 기술이 등장하면서 인기가 떨어졌지만 결국에는 모두 일부 SQL 형식(Hive, Presto)을 지원했습니다.

#### **단점**

- 비구조화 된 데이터를 처리하지 못한다. -> Spark 을 쓰는 것이 좋겠음
  - 비정형 데이터 처리에 정규식과 JSON을 어느 정도 사용할 수 있음
  - Redshift는 플랫 구조만 처리할 수 있습니다(중첩되지 않음).
    - Big Query는 중첩 구조를 지원합니다(매우 강력함).
- 스타 스키마가 항상 좋은 것은 아닙니다. 비정규화된 스키마
- 표준 구문이 없습니다(다양한 SQL 언어). - 대체로 비슷하지만
- 반정형 또는 비정형 데이터를 유연하게 처리하지 못함:
  - 보다 유연한 대규모 비정형 데이터 처리에는 다른 프레임워크가 필요함
  - **Spark, Hadoop**(MapReduce -> Hive) 등

cf) **Spark**

- df 을 모티브로 large scale unstructured data를 처리하게끔 만들어짐.

# SQL DDL과 DML

#### 일을 할 때...

- 깨끗한 데이터란 존재하지 않는다. 항상 데이터를 의심할 것.
- 데이터 품질을 의심하고 체크하는 버릇이 필요
  - 중복된 레코드들 체크하기
  - 최근 데이터의 존재 여부 체크하기
  - Primary key unuqueness가 지켜지는지 체크하기
  - 값이 비어있는 컬럼들이 있는지 체크하기
  - 위의 체크는 unit test 형태로 만들어 매번 쉽게 체크해볼 수 있음.
- 어느 시점이 되면 너무 많은 테이블들이 존재하게됨 -> Data Discovery 문제들이 생김
  - 무슨 테이블에 내가 원하고 신뢰할 수 있는 정보가 들어있나?
  - 테이블에 대해 질문을 하고 싶은데 누구에게 질문을 해야하나?
- 이 문제 해결을 위해 다양한 오픈소스와 서비스 출현
  - DataHub, Amundsen, ...
  - Select Star, DataFrame, ...

#### **DDL**

CREATE TABLE

- Primary key 속성을 지정할 수 있으나 무시됨. (Bigdata dataware house는 속도를 위해 primary key 체크를 하지 않음)

```
CREATE TABLE raw_data.user_session_channel (
	userid int,
	sessionid varchar(32) primary key,
	channel varchar(32)
);
and then INSERT

// 통으로 결과 테이블 작성 가능
CREATE TABLE schema_name.table_name AS SELECT ( )
```

DROP TABLE

```
DROP TABLE schema_name.table_nmae;

// 없는 테이블이어도 에러 안남
DROP TABLE IF EXISTS table_name;
```

- DELETE FROM : delete record

ALTER TABLE

```
// 새로운 컬럼 추가
ALTER TABLE table_name ADD COLUMN field_name field_type

// 기존 컬럼 이름 변경
ALTER TABLE table_name RENAME field_name to new_field_name

// 기존 ㅋ러럼 제거
ALTER TABLE table_name DROP COLUMN field_name

// 테이블 이름 변경
ALTER TABLE table_name RENAME TO new_table_name
```

#### **DML**

SELECT
UPDATE FROM
DELETE FROM

- vs TRUNCATE

# BASIC SQL

#### SELECT

- WHERE

```
# IN
WHERE channel in (‘Google’, ‘Youtube’)
WHERE channel = ‘Google’ OR channel = ‘Youtube’ ○ NOTIN

# LIKE : a case sensitive string match.
# ILIKE : a case-insensitive string match
WHERE channel LIKE ‘G%’ -> ‘G*’
WHERE channel LIKE ‘%o%’ -> ‘*o*’
NOT LIKE or NOT ILIKE

# BETWEEN : Used for date range matching
```

- STRING FUNCTION

```
LEFT(str, N)
REPLACE(str, exp1, exp2)
UPPER(str)
LOWER(str)
LEN(str)
LPAD, RPAD
SUBSTRING
```

- ORDER BY

```
# Ordering by multiple columns
RDER BY 1 DESC, 2, 3
```

```
# NULL value ordering
# By default, NULL values are ordered the last for ascending order
# By default, NULL values are ordered the first for descending order
# You can change this with
# NULLS FIRST | NULLS LAST

ORDER BY 1 DESC; -- NULL값이 가장 앞에 옴
ORDER BY 1 DESC NULLS LAST; -- NULL값이 맨뒤로 이동
```

#### INSERT INTO vs COPY

- INSERT INTO is slower than COPU
- INSERT INTO table_name SELECT \* FROM ...
  - This is better than CTAS(CREATE TABLE .. AS SELECT ) if you want to control the type of the fields
  - But matching varchar length can be challenging
  - Snowflack and BigQuery support String type(no need to worry about string length)

#### Type Cast and Conversion

- DATE Conversion

```
CONVERT_TIMEZONE('America/Los_Angeles', ts)
DATE, TRUNCATE
DATE_TRUNC
EXTRACT or DATE_PART
DATEDIFF, DATEADD, GET_CURRENT, ...
```

- Type Casting
  - cast or :: operator

```
category::int
cast(category as int)
```

- TO_CHAR, TO_TIMESTAMP

#### NULL

- 값이 존재하지 않음
- IS NULL, IS NOT NULL
- LEFT JOIN시 매칭되는 것이 있는지 확인하는데 아주 유용
- NULL 값을 다른 값으로 변환하고 싶다면?
  - COALESCE
  - NULLF

#### JOIN

- 조인시 고려해야할 점
  - 스타 스키마에서는 항상 필요
  - 중복레코드가 없고 Primary Key의 uniqueness가 보장됨을 체크
  - 조인하는 테이블들간의 관계를 명확하게 정의
    - one to one, one to many, many to many

#### WHERE

- LIKE : case sensitive string match
- ILIKE case insensitive string match

# Advanced SQL

#### UNION

- 여러개의 테이블들이나 SELECT 결과를 하나의 결과로 합쳐줌
- UNION은 중복을 제거해줌, UNION ALL은 그냥 합침

#### EXCEPT

- (차집합) 하나의 SELECT 결과에서 다른 SELECT 결과를 빼주는 것이 가능

#### INTERSECT(교집합)

- 여러 개 SELECT문에서 같은 레코드들만 찾아줌

#### COALESCE(Expression1, Expression2, ... ):

- 첫번째 Expression부터 값이 NULL이 아닌 것이 나오면 그 값을 리턴하고 모두 NULL이면 NULL을 리턴한다.
- NULL값을 다른 값으로 바꾸고 싶을 때 사용한다.

#### NULLIF(Expression1, Expression2):

- Expression1과 Expression2의 값이 같으면 NULL을 리턴한다.

#### DELETE FROM table_name

- 테이블에서 모든 레코드를 삭제
- WHERE 사용해 특정 레코드만 삭제 가능
  - DELETE FROM table_schema.table_name WHERE ''

#### TRUNCATE table

- 테이블에서 모든 레코드 삭제, 전체 삭제시에 유리
- DELETE FROM은 속도가 느림
- 하지만 단점
  - WHERE 지원하지 않음
  - Transaction을 지원하지 않음

#### WINDOW

```
function(expression) OVER ( [ PARTITION BY expression] [ ORDER BY expression ] )
```

- useful functions:
  - ROW_NUMBER, FIRST_VALUE, LAST_VALUE
  - Math functions: AVG, SUM, COUNT, MAX, MIN, MEDIAN, NTH_VALUE

#### SUB QUERY(CTE)

- 임시 테이블 생성함

```
WITH channel AS (
	SELECT * FROM
	WHERE ...
), user AS (
	SELECT * FROM
	WHERE ...
)

SELECT * FROM
user ...
```

#### JSON Parsing Function

```
SELECT JSON_EXTRACT_PATH_TEXT('{"f2":{"f3":1},"f4":{"f5":99,"f6":"star"}}','f4', 'f6');
```
