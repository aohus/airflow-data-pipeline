# What is data engineering?

Different Roles

- Managing Data Warehouse
- Writing and Managing Data Pipelines
  - Data Pipeline == ETL (Extract, Transform and Load) == Data Job == DAG
- Types of Data Pipelines
  - Batch Processing vs. Realtime Processing
    - Realtime Processing은 보통 kafka+spark streaming 이용(이번 강의에는 포함되지 않음)
  - Summary Data Generation (DBT - Analytics Engineer)
- Event Collection
  - User’s behavioral data

# Data Warehouse

**a seperate SQL database**

- SQL은 구조화된 데이터를 다루기에 아직 가장 중요하다. 테이블 구조를 잘 구성하는 것이 중요하다.
- production db는 처리 속도가 중요하다. production db를 관리하는 사람은 주로 backend engineer. data warehouse는 사용하는 사람들이 내부 직원들이고, 처리 속도보다는 scalability가 훨씬 중요하다.
- OLAP(OnLine Analytical Processing) vs OLTP(OnLine Transaction Processing)

**Central Data Storage of your**

- Create summary tables out of the raw data
  - this is more ELT than ETL
- Fixed Cost option vs Variable Cost Option
