from database_operations import *
from trainer_operations import *
from admin_operations import *
from member_operations import *
import datetime

def main():
        connect = connect_database()

        print("Welcome to the DK fitness app")
        regOrLog = register_or_login()
        if regOrLog == "R":
                register(connect)
                personType = "MEMBER"
        else:
            personType = classify()
        
        #member signing in
        if personType == "MEMBER":
            user = signIn(connect, "MEMBER")
            memberWorkFlow(connect, user)

        elif personType == "TRAINER":
            user = signIn(connect, "TRAINER")
            trainerFunctions(connect, user)
        else:
            user = signIn(connect, "ADMIN")
            adminFunctions(connect, user)

        
             

def signIn(connection, type):
    print("Please enter your email to sign in.")
    while True:
        userEmail = input()

        if not userEmail:
             print("Please enter an email into the field")
        
        #code to fetch profile
        if type == "MEMBER":
            query = "SELECT * FROM members WHERE email = %s"
        elif type == "TRAINER":
            query = "SELECT * FROM trainers WHERE email = %s"
        else:
            query = "SELECT * FROM admin_staff WHERE email = %s"

        data = (userEmail,)
        profile = executeQuery(connection, query, data, fetchOne=True)

        if profile:
            if type == "MEMBER":
                headers = getHeaders(connection, "members")
            elif type == "TRAINER":
                headers = getHeaders(connection, "trainers")
            else:
                headers = getHeaders(connection, "admin_staff")
            
            print("Profile found: ")
            printTable(profile, headers, True)
            return profile

        else:
            print("No profile found for the provided email")



def register_or_login():
    while True:
        print("Register as a member or sign in? (type r or s): ")
        uInput = input().upper()
        if (uInput == "R" or uInput == "S"):
                return uInput

def classify():
    while True:
        uInput = input("Are you a trainer, admin, or member: ").upper()
        if (uInput == "TRAINER"):
            return "TRAINER"
        elif (uInput == "MEMBER"):
            return "MEMBER"
        elif (uInput == "ADMIN"):
            return "ADMIN"
        print("invalid, please input again")

     
                
def register(connection):
    while True:
        firstName = str(input("Please enter your first name: "))
        if firstName:
            break
        else:
            print("First name cannot be empty. Please try again.")

    while True:
        lastName = str(input("Please enter your last name: "))
        if lastName:
            break
        else:
            print("Last name cannot be empty. Please try again.")

    while True:
        email = str(input("Please enter your email: "))
        if email:
            break
        else:
            print("Email cannot be empty. Please try again.")

    while True:
        phoneNumber = str(input("Please enter your phone number: "))
        if phoneNumber:
            break
        else:
            print("Phone number cannot be empty. Please try again.")

    regDate = datetime.datetime.now()

    query = "INSERT INTO members (firstName, lastName, email, phone_number, date_registered) VALUES (%s, %s, %s, %s, %s)"
    queryData = (firstName, lastName, email, phoneNumber, regDate)
    member_id = executeQuery(connection, query, queryData, False, True)
    showAllMembers(connection)

    billQuery = "INSERT INTO bills (amount, member_id) VALUES (%s, %s)"
    billData = (100, member_id)
    paymentQuery = "INSERT INTO payments (bill_id, amount, date, processed) VALUES (%s, %s, %s, %s)"
    bill_id = executeQuery(connection, billQuery, billData, False, True)

    payData = (bill_id, 100, datetime.datetime.today(), "Not Processed")
    executeQuery(connection, paymentQuery, payData)

    print("100 dollars extracted from bank account\nWelcome to this establishment!")

    print("registration complete")




def showAllMembers(connection):
        query = "SELECT * FROM members"
        members = executeQuery(connection, query)
        headers = getHeaders(connection, "members")
        printTable(members, headers, False)





if __name__ == "__main__":
        main()