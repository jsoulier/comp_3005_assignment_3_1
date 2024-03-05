import json
import os
import psycopg

class Students:
    def __init__(self):
        ''' create database connections and ensure students exists '''

        # force root directory and load config
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        with open('config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # create database connection
        self.connection = psycopg.connect(
            'dbname=' + data['database'] + ' '
            'user=' + data['username'] + ' '
            'password=' + data['password'] + ' '
        )
        self.cursor = self.connection.cursor()

        # check if table already exists
        self.cursor.execute(
            'SELECT EXISTS ('
            '    SELECT 1 '
            '    FROM   information_schema.tables '
            '    WHERE  table_schema = %s '
            '    AND    table_name = %s '
            ') ', ('public', 'students')
        )
        if self.cursor.fetchone()[0]:
            return

        # create empty table
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS Students ( '
            '    student_id SERIAL PRIMARY KEY, '
            '    first_name TEXT NOT NULL, '
            '    last_name TEXT NOT NULL, '
            '    email TEXT UNIQUE NOT NULL, '
            '    enrollment_date DATE '
            ') '
        )

        # fill with initial data
        self.add_student('John', 'Doe', 'john.doe@example.com', '2023-09-01')
        self.add_student('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01')
        self.add_student('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02')

    def close(self):
        ''' commit database and close connections '''
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def get_all_students(self):
        ''' print all students from database '''
        self.cursor.execute('SELECT * FROM Students')
        students = self.cursor.fetchall()
        print('student_id first_name last_name email enrollment_date')
        print('-----------------------------------------------------')
        for student_id, first_name, last_name, email, enrollment_date in students:
            string = ''
            string += str(student_id)
            string += ' '
            string += first_name
            string += ' '
            string += last_name
            string += ' '
            string += email
            string += ' '
            string += str(enrollment_date)
            print(string)

    def add_student(self, first_name, last_name, email, enrollment_date):
        ''' add student to database '''
        self.cursor.execute(
            'INSERT INTO Students (first_name, last_name, email, enrollment_date) '
            'VALUES (%s, %s, %s, %s) ',
            (first_name, last_name, email, enrollment_date)
        )

    def update_student_email(self, student_id, email):
        ''' update student email in database '''
        self.cursor.execute(
            'UPDATE Students '
            'SET email = %s '
            'WHERE student_id = %s ',
            (email, student_id)
        )

    def delete_student(self, student_id):
        ''' delete student from database '''
        self.cursor.execute(
            'DELETE FROM Students '
            'WHERE student_id = %s ',
            (student_id, )
        )
