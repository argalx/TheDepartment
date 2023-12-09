import sqlite3

# Database connection
conn = sqlite3.connect('TheDepartment/td.db')

# Create cursor object
cursor = conn.cursor()

# The Department Table Creation
# employees table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
               id INTEGER PRIMARY KEY,
               full_name TEXT NOT NULL,
               department_id INTEGER

    )
''')

# departments table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
               id INTEGER PRIMARY KEY,
               department TEXT NOT NULL,
               department_manager_id INTEGER NOT NULL,
               division_id INTEGER NOT NULL
    )
''')

# divisions table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS divisions (
               id INTEGER PRIMARY KEY,
               division TEXT NOT NULL,
               division_manager_id INTEGER NOT NULL
    )
''')

# project table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
               id INTEGER PRIMARY KEY,
               project TEXT NOT NULL
    )
''')

# project_members table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS project_members (
               id INTEGER PRIMARY KEY,
               project_id INTEGER NOT NULL,
               employee_id INTEGER NOT NULL
    )
''')

# Insert Dummy Data
def insertDummyData():
    # Employees
    cursor.execute('INSERT INTO employees (full_name, department_id) VALUES (?, ?)',('Arvin Bonggal', 1,))
    cursor.execute('INSERT INTO employees (full_name, department_id) VALUES (?, ?)',('Duvall Danganan', 2,))
    cursor.execute('INSERT INTO employees (full_name) VALUES (?)',('Mark Joseph Loma',))

    # Departments
    cursor.execute('INSERT INTO departments (department, department_manager_id, division_id) VALUES (?, ?, ?)',('IT', 2, 3,))
    cursor.execute('INSERT INTO departments (department, department_manager_id, division_id) VALUES (?, ?, ?)',('HR', 1, 3,))

    # Divisions
    cursor.execute('INSERT INTO divisions (division, division_manager_id) VALUES (?, ?)',('Division 1', 1))
    cursor.execute('INSERT INTO divisions (division, division_manager_id) VALUES (?, ?)',('Division 2', 2))
    cursor.execute('INSERT INTO divisions (division, division_manager_id) VALUES (?, ?)',('Division 3', 3))

    # Projects
    cursor.execute('INSERT INTO projects (project) VALUES (?)',('Project 1',))
    cursor.execute('INSERT INTO projects (project) VALUES (?)',('Project 2',))
    cursor.execute('INSERT INTO projects (project) VALUES (?)',('Project 3',))
    cursor.execute('INSERT INTO projects (project) VALUES (?)',('Project 4',))

    # Project Members
    cursor.execute('INSERT INTO project_members (project_id, employee_id) VALUES (?, ?)',(1, 1,))
    cursor.execute('INSERT INTO project_members (project_id, employee_id) VALUES (?, ?)',(1, 2,))
    cursor.execute('INSERT INTO project_members (project_id, employee_id) VALUES (?, ?)',(1, 3,))
    cursor.execute('INSERT INTO project_members (project_id, employee_id) VALUES (?, ?)',(3, 2,))
    cursor.execute('INSERT INTO project_members (project_id, employee_id) VALUES (?, ?)',(4, 2,))
    cursor.execute('INSERT INTO project_members (project_id, employee_id) VALUES (?, ?)',(2, 1,))

    # Commit changes
    conn.commit()

# Call insertDummyData function
# insertDummyData()

# Display Employees Details
def displayEmployees():
    cursor.execute('''
                   SELECT id, full_name, COALESCE(department_id, 'Rovers')
                   FROM employees
    ''')
    employees = cursor.fetchall()

    for object in employees:
        employee = list(object)
        
        # Employee ID
        employeeId = employee[0]

        # Employee Name
        employeeName = employee[1]

        # Employee Department, Department Manager & Division, Division Manager
        if employee[2] == 'Rovers':
            employeeDepartment = 'Rovers'
            employeeDepartmentManager = 'None'
            employeeDivision = 'None'
            employeeDivisionManager = 'None'
        else:
            # Department
            cursor.execute('SELECT department, division_id, department_manager_id FROM departments WHERE id=?',(employee[2],))
            departmentDetails = cursor.fetchall()
            employeeDepartment = list(departmentDetails[0])[0]

            # Department Manager
            cursor.execute('SELECT full_name FROM employees WHERE id=?',(list(departmentDetails[0])[2],))
            employeeDetails = cursor.fetchall()
            employeeDepartmentManager = list(employeeDetails[0])[0]

            # Division
            cursor.execute('SELECT division, division_manager_id FROM divisions WHERE id=?',(list(departmentDetails[0])[1],))
            divisionDetails = cursor.fetchall()
            employeeDivision = list(divisionDetails[0])[0]

            # Division Manager
            cursor.execute('SELECT full_name FROM employees WHERE id=?',(list(divisionDetails[0])[1],))
            employeeDetails = cursor.fetchall()
            employeeDivisionManager = list(employeeDetails[0])[0]

        # Employee Projects
        employeeProjects = []
        cursor.execute('SELECT project_id FROM project_members WHERE employee_id=?',(employeeId,))
        projectDetails = cursor.fetchall()
        for object in projectDetails:
            cursor.execute('SELECT project from projects WHERE id=?',(list(object)[0],))
            project = cursor.fetchall()
            employeeProjects.append(list(project[0])[0])
        
        # Print Employee Details
        print(f'{"-"*100}\nEMPLOYEE DETAILS\n{"-"*100}\nEmployee Name: {employeeName}\nDepartment: {employeeDepartment}\nDepartment Manager: {employeeDepartmentManager}\nDivision: {employeeDivision}\nDivision Manager: {employeeDivisionManager}\nProjects: {employeeProjects}\n{"-"*100}')
        
# Call displayEmployees function
displayEmployees()

# Close Connection
conn.close()