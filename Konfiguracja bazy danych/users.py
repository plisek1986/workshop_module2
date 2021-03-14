import argparse
from models import User
from psycopg2.errors import UniqueViolation
from utils import check_password
from psycopg2 import connect, OperationalError

#preparing logic for parsing information provided by the user in the console
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password (min 8 characters)')
parser.add_argument('-n', '--new_pass', help='new_password')
parser.add_argument('-l', '--list', help='list of users', action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()

# function for listing users
def list_users(cursor):
    users = User.load_all_users(cursor)
    for user in users:
        print(user.username)

#function for creating a new user
def new_user(cursor, username, password):
    user = User.load_user_by_username(cursor, username)
    try:
        if not user:
            if len(password) >= 8:
                user = User(username=username, hashed_password=password)
                user.save_to_db(cursor)
                print('User has been created')
            else:
                print('Provided password is too short, please try again!')
    except UniqueViolation as e:
        print('User already exists, please try another username!', e)

#function for amending user's password
def password_edit(cursor, username, password, new_pass):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print('User does not exist!')
    elif check_password(password, user.hashed_password):
        if len(new_pass) >= 8:
            user.hashed_password = new_pass
            user.save_to_db(cursor)
            print('Password has been changed!')
        else:
            print('Provided password is too short, please try again!')
    else:
        print('Provided password is incorrect!')

#function for deleting a user
def delete_user(cursor, username, password):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print('User does not exist!')
    elif check_password(password, user.hashed_password):
        user.delete(cursor)
        print('User has been deleted!')
    else:
        print('Provided password is incorrect!')

#main function for establishing connection with the database and parsing information
#provided by the user in the console
if __name__ == '__main__':
    try:
        con = connect(user='postgres', host='localhost', password='coderslab', database='workshops_module2')
        con.autocommit = True
        cursor = con.cursor()

        if args.username and args.password and args.edit and args.new_pass:
            password_edit(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            new_user(cursor, args.username, args.password)
        elif args.list:
            list_users(cursor)
        else:
            parser.print_help()
        con.close()
    except OperationalError as e:
        print('Connection failed!', e)




