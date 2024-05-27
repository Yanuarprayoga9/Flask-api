# Technical Test On Software Developer (Backend) team in Agile Technica. 

## Setup 
instal package
```bash
pip install Flask Flask-Caching
```


## Start Development Server On http://localhost:5000/
Start Dev

```bash
phyton main.py
```


- Task 1 complete 
![alt text](image.png)
- Task 2 complete 
![alt text](image-1.png)
- Task 3 complete 
![alt text](image-2.png)
- Task 4 complete 
- Task 5 complete 
- Task Bonus Complete
- Task Bonus 2 Complete
![alt text](image-3.png)

## ENDPOINT http://localhost:5000/api
- GET /employees_with_domains
![alt text](image-5.png)
- GET /companies_with_employees
![alt text](image-4.png) 

<!-- (BONUS) CREATE API FOR EMPLOYEE CRUD IMPLEMENTATION -->
- POST /create_employee
request body:
``` json
{
  "name": "EMP-0004",
  "first_name": "Mike",
  "last_name": "Sernine",
  "full_name": "Mike Sernine",
  "company": "Company 3"
}
```
![alt text](image-6.png)


- PUT /update_employee
request body:
``` json
{
    "name": "EMP-0003",
  "company": "Company 3"
}
```
![alt text](image-7.png)


- DELETE /delete_employee/"EMP-0001"
![alt text](image-8.png)
