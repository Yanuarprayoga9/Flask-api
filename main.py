from flask import Flask, jsonify, request
from flask_caching import Cache

app = Flask(__name__)

# Configure cache
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

# Existing data and functions from the prompt
company_name_list = [{'name': 'Company 1'}, {'name': 'Company 2'}, {'name': 'Company 3'}]

employee_name_list = [{'name': 'John Doe'}, {'name': 'Tom Smith'}, {'name': 'Andrew Sebastian'}]

company_detail_list = {
    'Company 1': {'name': 'Company 1', 'domain': 'Retail'},
    'Company 2': {'name': 'Company 2', 'domain': 'Construction'},
    'Company 3': {'name': 'Company 3', 'domain': 'Healthcare'}
}

employee_detail_list = {
    'John Doe': {'name': 'EMP-0001', 'first_name': 'John', 'last_name': 'Doe', 'full_name': 'John Doe', 'company': 'Company 1'},
    'Tom Smith': {'name': 'EMP-0002', 'first_name': 'Tom', 'last_name': 'Smith', 'full_name': 'Tom Smith', 'company': 'Company 2'},
    'Andrew Sebastian': {'name': 'EMP-0003', 'first_name': 'Andrew', 'last_name': 'Sebastian', 'full_name': 'Andrew Sebastian', 'company': 'Company 2'}
}

attendance_list = []

# Functions
def get_list_company():
    return company_name_list

def get_company_detail(company_name):
    return company_detail_list[company_name]

def get_list_employee():
    return employee_name_list

def get_employee_detail(employee_name):
    return employee_detail_list[employee_name]


# CRUD UNIT
def create_new_company(company_dict):
    assert 'name' in company_dict
    assert 'domain' in company_dict

    company_detail_list[company_dict['name']] = {
        'name': company_dict['name'],
        'domain': company_dict['domain']
    }
    company_name_list.append({'name': company_dict['name']})

def delete_company(company_name):
    assert company_name in company_detail_list
    company_detail_list.pop(company_name, None)
    global company_name_list
    company_name_list = [x for x in get_list_company() if x['name'] != company_name]



def update_employee(employee_dict):
    assert 'name' in employee_dict
    employee_name = None
    for emp in employee_detail_list.values():
        if emp['name'] == employee_dict['name']:
            employee_name = emp['full_name']
            break
    if employee_name:
        employee_detail_list[employee_name].update(employee_dict)

def delete_employee(employee_name):
    if employee_name in employee_detail_list:
        employee_detail_list.pop(employee_name)
        global employee_name_list
        employee_name_list = [emp for emp in employee_name_list if emp['name'] != employee_name]

def get_list_attendance():
    return attendance_list

def create_new_attendance(attendance_dict):
    assert 'name' in attendance_dict
    assert 'employee' in attendance_dict
    assert 'attendance_date' in attendance_dict
    assert 'company' in attendance_dict
    assert 'status' in attendance_dict

    attendance_list.append(attendance_dict)

def delete_attendance(attendance_name):
    global attendance_list
    attendance_list = [att for att in attendance_list if att['name'] != attendance_name]

def get_employees_with_domains():
    employees = get_list_employee()
    result = []
    for emp in employees:
        emp_detail = get_employee_detail(emp['name'])
        company_detail = get_company_detail(emp_detail['company'])
        result.append({
            "full_name": emp_detail['full_name'],
            "company": emp_detail['company'],
            "domain": company_detail['domain']
        })
    return result
# ///////////////////////////////////// SOLUTION STARTED /////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////

# Task 1 Get the list of all companies and sort by company name in reverse order.
def task_1():
    company_list = get_list_company()
    sorted_company_list = sorted(company_list, key=lambda x: x['name'], reverse=True)
    return sorted_company_list

# Call the function and print the result
task_1_result = task_1()
print(task_1_result)



# Task 2
# Print all domain values in every company.
def task_2():
    company_list = get_list_company()
    for company in company_list:
        company_name = company['name']
        company_detail = get_company_detail(company_name)
        print(f"{company_name}: {company_detail['domain']}")

# Call the function
task_2()




# Task 3
# List all employees working in Company 2.
def task_3():
    employees = get_list_employee()
    company_2_employees = [emp['name'] for emp in employees if get_employee_detail(emp['name'])['company'] == 'Company 2']
    return company_2_employees

# Call the function and print the result
task_3_result = task_3()
print(task_3_result)



# Task 4 API
@app.route('/api/employees_with_domains', methods=['GET'])
@cache.cached(timeout=60)
def employees_with_domains():
    employees = get_list_employee()
    result = []
    for emp in employees:
        emp_detail = get_employee_detail(emp['name'])
        company_detail = get_company_detail(emp_detail['company'])
        result.append({
            "full_name": emp_detail['full_name'],
            "company": emp_detail['company'],
            "domain": company_detail['domain']
        })
    return jsonify(employees_with_domains())

# Task 5 API
@app.route('/api/companies_with_employees', methods=['GET'])
@cache.cached(timeout=60)
def companies_with_employees():
    companies = get_list_company()
    result = []
    for company in companies:
        company_name = company['name']
        employees = get_list_employee()
        employee_list = [emp['name'] for emp in employees if get_employee_detail(emp['name'])['company'] == company_name]
        result.append({
            "company": company_name,
            "employees": employee_list
        })
    return jsonify(result)

# Bonus Task 1: Employee CRUD Operations
@app.route('/api/create_employee', methods=['POST'])
def create_employee():
    employee_data = request.json

    def create_new_employee(employee_dict):
        assert 'name' in employee_dict
        assert 'first_name' in employee_dict
        assert 'last_name' in employee_dict
        assert 'full_name' in employee_dict
        assert 'company' in employee_dict

        employee_name_list.append({'name': employee_dict['full_name']})
        employee_detail_list[employee_dict['full_name']] = {
            'name': employee_dict['name'],
            'first_name': employee_dict['first_name'],
            'last_name': employee_dict['last_name'],
            'full_name': employee_dict['full_name'],
            'company': employee_dict['company']
        }
       
    create_new_employee(employee_data)
    all_employees_list = get_employees_with_domains()
    return jsonify({"message": "Employee created successfully","employees": all_employees_list}), 201

@app.route('/api/update_employee', methods=['PUT'])
def update_employee_api():
    employee_data = request.json
    update_employee(employee_data)
    all_employees_list = get_list_employee()
    return jsonify({"message": "Employee Updated successfully","employees": all_employees_list}), 201

@app.route('/api/delete_employee/<string:employee_name>', methods=['DELETE'])
def delete_employee_api(employee_name):
    delete_employee(employee_name)
    return jsonify({"message": "Employee deleted successfully"}), 200

# Bonus Task 2: Employee Attendance CRUD Operations
@app.route('/api/create_attendance', methods=['POST'])
def create_attendance():
    attendance_data = request.json
    create_new_attendance(attendance_data)
    return jsonify({"message": "Attendance created successfully"}), 201

@app.route('/api/delete_attendance/<string:attendance_name>', methods=['DELETE'])
def delete_attendance_api(attendance_name):
    delete_attendance(attendance_name)
    return jsonify({"message": "Attendance deleted successfully"}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
