## Postgres JSONB Queries

### 1. Simple table with JSONB column
```sql
create table profiles
(
	id int not null,
	profile jsonb not null
);
```
### 2. Insert dummy data into the table

```sql
insert into profiles  values (1, '{"name":"Linus Torvalds","experience":[{"title":"Fellow at Linux Foundation","company":"Linux Foundation","startMonth":"July","startYear":"2003","endMonth":"","endYear":"","projects":["Linux Kernel"]},{"title":"Fellow","company":"Open Source Development Labs","startMonth":"July","startYear":"2003","endMonth":"Dec","endYear":"2006","projects":["Linux Kernel"]},{"title":"Fellow","company":"Transmeta Corp","startMonth":"March","startYear":"1997","endMonth":"June","endYear":"2003","projects":["Linux Kernel"]}],"education":[{"degree":"Msc Computer Science","university":"University of Helsinki"}]}' );
```

```sql
insert into profiles values (2, '{"name":"Jeff Dean","experience":[{"title":"SVP of Google Research and Health","company":"Google","startMonth":"Aug","startYear":"2009","endMonth":"","endYear":"","projects":["Map Reduce","BigTable","Spanner"]}],"education":[{"degree":"Ph.D Computer Science","university":"University of Washington"}]}');
```

### 3. Get JSON documents matching a fragment. 
```sql
select * from profiles where profile @> '{"name":"Jeff Dean"}';
```

|id|profile|
|--|-------|
|2|{"name": "Jeff Dean", "location": {"city": "Palo Alto", "state": "California", "country": "United States"}, "education": [{"degree": "Ph.D Computer Science", "university": "University of Washington"}], "experience": [{"title": "SVP of Google Research and Health", "company": "Google", "endYear": "", "endMonth": "", "projects": ["Map Reduce", "BigTable", "Spanner"], "startYear": "2009", "startMonth": "Aug"}]}|


### 4. GET JSON documents matching a fragment within an array.
```sql
select * from profiles where profile @> '{"experience":[{"company": "Linux Foundation"}]}';
```


|id|profile|
|--|-------|
|1|{"name": "Linus Torvalds", "education": [{"degree": "Msc Computer Science", "university": "University of Helsinki"}], "experience": [{"title": "Fellow at Linux Foundation", "company": "Linux Foundation", "endYear": "", "endMonth": "", "projects": ["Linux Kernel"], "startYear": "2003", "startMonth": "July"}, {"title": "Fellow", "company": "Open Source Development Labs", "endYear": "2006", "endMonth": "Dec", "projects": ["Linux Kernel"], "startYear": "2003", "startMonth": "July"}, {"title": "Fellow", "company": "Transmeta Corp", "endYear": "2003", "endMonth": "June", "projects": ["Linux Kernel"], "startYear": "1997", "startMonth": "March"}]}|


### 5. Update works as usual. Full update
```sql
update profiles set profile = '{"name":"Jeff Dean","experience":[{"title":"SVP of Google Research and Health","company":"Google","startMonth":"Aug","startYear":"2009","endMonth":"","endYear":"","projects":["Map Reduce","BigTable","Spanner"]}],"education":[{"degree":"Ph.D Computer Science","university":"University of Washington"}],"location":{"city":"Palo Alto","state":"California","country":"United States"}}' where id =2;
```

### 6. Partial update (append a fragment)
```sql
update profiles set profile = profile || '{"location":{"city":"Portland","state":"Oregon","country":"United States"}}' where id=1
```

### 7. Partial update (delete a fragment)
```sql
update profiles set profile = profile - 'location' where id =1;
```

### 8. Get JSON documents where key matches a value.
```sql
select * from profiles where profile ->> 'name' = 'Linus Torvalds';
```

### 9. Get JSON documents where nested key matches a value.
```sql
select * from profiles where profile -> 'location' ->> 'state'  = 'California';
```

## Windowing

### 1. Simple table with employee,role and salary
```sql
create table emp_role_salary
(
	emp_id int not null,
	emp_role text,
	emp_salary float
);

```
### 2. Insert dummy data into the table.

```sql
insert into emp_role_salary values (1, 'developer', 100);
insert into emp_role_salary values (2, 'developer', 200);
insert into emp_role_salary values (3, 'developer', 150);
insert into emp_role_salary values (4, 'developer', 350);

insert into emp_role_salary values (5, 'manager', 500);
insert into emp_role_salary values (6, 'manager', 700);

insert into emp_role_salary values (7, 'senior-manager', 1000);
insert into emp_role_salary values (8, 'senior-manager', 1500);

insert into emp_role_salary values (9, 'principal-engineer', 1200);
insert into emp_role_salary values (8, 'principal-engineer', 1300);

```

### 3. Average salary per employee
```sql
select avg(emp_salary) as average_employee_salary from emp_role_salary;
```

|average_employee_salary|
|-----------------------|
|700.0|

### 4. Average salary per role
```sql
select emp_role, avg(emp_salary) as average_employee_salary_by_role from emp_role_salary 
group by emp_role order by average_employee_salary_by_role desc; 
```

|emp_role|average_employee_salary_by_role|
|--------|-------------------------------|
|senior-manager|1250.0|
|principal-engineer|1250.0|
|manager|600.0|
|developer|200.0|

### 4. Which roles fall into high paying category? 

```sql
select emp_role, avg(emp_salary) as average_employee_salary_by_role from emp_role_salary 
group by emp_role 
having avg(emp_salary) > 1000

```

|emp_role|average_employee_salary_by_role|
|--------|-------------------------------|
|senior-manager|1250.0|
|principal-engineer|1250.0|

### 5. How does an employee fare with respect to peers in the same role?

```sql
select emp_id,emp_role,emp_salary, avg(emp_salary) over (partition by emp_role) from emp_role_salary;

```

|emp_id|emp_role|emp_salary|avg|
|------|--------|----------|---|
|2|developer|200.0|200.0|
|1|developer|100.0|200.0|
|3|developer|150.0|200.0|
|4|developer|350.0|200.0|
|6|manager|700.0|600.0|
|5|manager|500.0|600.0|
|9|principal-engineer|1200.0|1250.0|
|8|principal-engineer|1300.0|1250.0|
|7|senior-manager|1000.0|1250.0|
|8|senior-manager|1500.0|1250.0|

- Use copy command for large data inserts.

```sql

select name from employees;

select name from employees order by name asc;

select name from employees where name='John Doe';

select avg(age) from employees;

-- Where clause is for filtering rows.
-- Having clause is for filtering rows after an aggregation is run.
-- Views allow client code to be abstracted from specific column names.

create table employees(
	id int primary key not null,
	name text not null,
	designation text not null,
	salary float not null check(salary>0)	
)



insert into employees values (1, 'D1', 'Developer', 10 );
insert into employees values (2, 'D2', 'Developer', 11 );
insert into employees values (3, 'D3', 'Developer', 15 );
insert into employees values (4, 'M1', 'Manager', 15 );
insert into employees values (5, 'M2', 'Manager', 20 );

select id,name,designation, salary, avg(salary) over (partition by designation) from employees ;

select id,name,designation, salary, rank() over (partition by designation order by salary desc) from employees ;

-- Transactions are ACID compliant. Ability to rollback transactions midway to a safe point if necessary.

begin;
	
insert into employees values (6, 'M3', 'Manager', 30);
savepoint initial_state;

insert into employees values (7, 'M4', 'Manager', 40);
rollback to initial_state;
	
commit;

-- Postgres also supports inheritance.
create table developers
(
	tech_stack text not null
)inherits(employees);

```
