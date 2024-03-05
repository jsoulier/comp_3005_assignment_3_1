from argparse import ArgumentParser
from students import Students

def main():

    # create parser
    parser = ArgumentParser(description='comp_3005_assignment_3_1')
    parser.add_argument('--get-all-students', action='store_true', help='show all students')
    parser.add_argument('--add-student', nargs=4, metavar=('first_name', 'last_name', 'email', 'enrollment_date'), help='create new student')
    parser.add_argument('--update-student-email', nargs=2, metavar=('student_id', 'email'), help='update student email')
    parser.add_argument('--delete-student', metavar='student_id', help='delete student')
    args = parser.parse_args()

    # forward arguments to students
    try:
        students = Students()
        if args.get_all_students:
            pass
        elif args.add_student:
            students.add_student(*args.add_student)
        elif args.update_student_email:
            students.update_student_email(*args.update_student_email)
        elif args.delete_student:
            students.delete_student(args.delete_student)
        else:
            return parser.print_help()
        students.get_all_students()

    # handle errors
    except Exception as e:
        print(e)
    finally:
        students.close()

if __name__ == '__main__':
    main()
