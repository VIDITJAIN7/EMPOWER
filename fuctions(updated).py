from mysql.connector import *

try:
    con1 = connect(host='localhost', user='root', password='viditjain', database='empower')
    cur1 = con1.cursor()

    def db_empower():
        # Create empmaster table
        cur1.execute('''
            CREATE TABLE IF NOT EXISTS empmaster (
                empid INT PRIMARY KEY,
                name VARCHAR(50),
                gender CHAR(1),
                doj DATE,
                aadhar INT,
                deptid INT,
                desgn VARCHAR(40),
                salary NUMERIC(7, 2),
                contact INT
            );
        ''')
        # Create sal_structure table
        cur1.execute('''
            CREATE TABLE IF NOT EXISTS sal_structure (
                empid INT,
                basic_sal NUMERIC(7, 2),
                allowances NUMERIC(7, 2),
                provident_fund NUMERIC(7, 2),
                tds NUMERIC(7, 2),
                FOREIGN KEY (empid) REFERENCES empmaster(empid)
            );
        ''')
        # Create dept table
        cur1.execute('''
            CREATE TABLE IF NOT EXISTS dept (
                deptid INT PRIMARY KEY,
                dept_name VARCHAR(40),
                dept_head INT,
                FOREIGN KEY (dept_head) REFERENCES empmaster(empid)
            );
        ''')
        # Add foreign key constraint to empmaster for edeptid
        cur1.execute('''
            ALTER TABLE empmaster
            ADD CONSTRAINT FOREIGN KEY (edeptid) REFERENCES dept(deptid);
        ''')
        # Add departments to the dept table
        department_data = [
            (0, 'admin',0001 ),
            (1, 'HR',0002),
            (2, 'sales',0003),
            (3, 'IT',0004),
            (4, 'unassigned',None)
        ]

        cur1.executemany('INSERT INTO dept (deptid, dept_name, dept_head) VALUES (%s, %s, %s)', department_data)
        
        con1.commit()

    db_empower()

except Error as e:
    print(e)

def addrec_empmaster():
    a = input('enter employee ID >>')
    b = input('enter employee name >>')
    c = input('enter gender (M/F/O) >>')
    d = input('enter Date of Joining as YYYY-MM-DD >>')
    e = input('enter Aadhar Card No. >>')
    f = input('enter department ID >>')
    g = input('enter current designation >>')
    h = input('enter current salary >>')
    i = input('enter contact no. >>')

    cur1.execute("INSERT INTO empmaster VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (a, b, c, d, e, f, g, h, i))

    con1.commit()

def delrec_empmaster():
    a = input('enter employee id of record to be deleted >>')
    cur1.execute('DELETE FROM empmaster WHERE empid = %s', (a,))
    b = input('Do you wish to make the changes permanent (Y/N)? >>')
    if b in 'Yy':
        con1.commit()
    elif b in 'Nn':
        cur1.execute('ROLLBACK;')

def search_emp():
    a = input('enter field to filter by (empid, name, gender, doj, aadhar, deptid, desgn, salary, or contact): ')
    b = input('enter term to search: ')
    search = 'SELECT * FROM empmaster WHERE {} = %s'.format(a)
    cur1.execute(search, (b,))
    r = cur1.fetchall()
    if r:
        for row in r:
            print(row)
    else:
        print("No results found.")
