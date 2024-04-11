from database_operations import *
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
             print(user)
        
             

def signIn(connection, type):
    print("Please enter your email to sign in.")
    while True:
        userEmail = input()

        if not userEmail:
             print("Please enter an email into the field")
        
        #code to fetch profile
        if type == "MEMBER":
            query = "SELECT * FROM members WHERE email = %s"

        data = (userEmail,)
        profile = executeQuery(connection, query, data, fetchOne=True)
        if profile:
            print("Profile found: ", profile)
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
    print("Are you a trainer, administator, or member")
    while True:
        uInput = input().upper()
        if (uInput == "TRAINER"):
            return "TRAINER"
        elif (uInput == "MEMBER"):
            return "MEMBER"
        elif (uInput == "ADMIN"):
            return "ADMIN"

     
                
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
    executeQuery(connection, query, queryData)
    showAllMembers(connection)
    print("registration complete")




def showAllMembers(connection):
        query = "SELECT * FROM members"
        members = executeQuery(connection, query)
        print(members)


def memberMenu():
     print("What would you like to do?")
     print("1. Update Personal information")
     print("2. ")


if __name__ == "__main__":
        main()