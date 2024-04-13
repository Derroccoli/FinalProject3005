import datetime
from database_operations import *

def trainerFunctions(connection, user):
    print("What would you like to do:")

    while True:
        print("Trainer menu")
        print("0. Quit")
        print("1. View members")
        print("2. Manage your schedule availability")
        

        uInput = int(input())

        if (uInput == 0):
            break
        elif (uInput == 1):
            viewMemberFunctions(connection)
        elif(uInput == 2):
            availablilityFunctions(connection, user)

def viewMemberFunctions(connection):
    print("What would you like to do:")

    while True:
        print("View members menu")
        print("0. Return back to main trainer menu")
        print("1. View all members")
        print("2. Find member by member id")
        print("3. Find member(s) by first name")
        

        uInput = int(input())

        if (uInput == 0):
            break
        elif (uInput == 1):
            viewAllMembers(connection)
        elif(uInput == 2):
            findByMemberId(connection)
        elif(uInput == 3):
            findByFirstName(connection)

def viewAllMembers(connection):
    query = "SELECT * FROM members"
    members = executeQuery(connection, query)
    headers = getHeaders(connection, "members")
    printTable(members, headers, False)

def findByMemberId(connection):
    member_id = int(input("What is the member id of the member you'd like to find"))
    query = "SELECT * FROM members WHERE member_id = %s"


    data = (member_id,)
    profile = executeQuery(connection, query, data, fetchOne=True)
    if profile:
        headers = getHeaders(connection, "members")
        print("Profile found: ")
        printTable(profile, headers, True)
    else:
        print("No profile found for the provided member id")

def findByFirstName(connection):
    firstName = input("What is the first name of the member you'd like to find")
    query = "SELECT * FROM members WHERE firstName = %s"

    data = (firstName,)
    profile = executeQuery(connection, query, data)
    print(profile)
    if profile:
        headers = getHeaders(connection, "members")
        print("Profile found: ")
        printTable(profile, headers)
    else:
        print("No profile found for the provided first name")


def availablilityFunctions(connection, user):
    print("What would you like to do:")

    while True:
        print("Schedule management functions")
        print("0. Return back to main trainer menu")
        print("1. View your schedule")
        print("2. Add an available time to your schedule")
        print("3. Set a timeslot as booked by availability id")
        print("4. Set a timeslot as booked by time")
        

        uInput = int(input())

        if (uInput == 0):
            break
        elif (uInput == 1):
            viewYourSchedule(connection, user)
        elif(uInput == 2):
            addAvailableTime(connection, user)
        elif(uInput == 3):
            bookTimebyAvailabilityId(connection)
        elif(uInput == 4):
            bookTimeByTime(connection, user)

def viewYourSchedule(connection, user):
    query = "SELECT * FROM available_times WHERE trainer_id = %s"
    queryData = (user[0],)

    result = executeQuery(connection, query, queryData)
    headers = getHeaders(connection, "available_times")
    printTable(result, headers)



def addAvailableTime(connection, user):
    start_time = None
    end_time = None

    while True:
        try:
            user_input = input("Enter start date and time (YYYY-MM-DD HH:MM): ")
            # Parse the user input into a datetime object
            start_time = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M")
            break
            
        except ValueError:
            print("Invalid input format. Please enter a date and time in the format YYYY-MM-DD HH:MM")

    numTimeSlots = int(input("Enter the number of 1 hour timeslots you would like to set yourself available for after the start time."))

    end_time = start_time+ datetime.timedelta(hours=numTimeSlots)

    trainer_id = user[0]

    query = "INSERT INTO available_times (start_time, end_time, trainer_id, booked) VALUES (%s, %s, %s, FALSE)"

    queryData = (start_time, end_time, trainer_id)

    executeQuery(connection, query, queryData)


def bookTimebyAvailabilityId(connection):
    availability_id = int(input("What is the availability id of the time slot you would like to set as booked"))

    query = "UPDATE available_times SET booked = TRUE WHERE availability_id = %s"

    queryData = (availability_id,)

    executeQuery(connection, query, queryData)

def bookTimeByTime(connection, user):
    start_time = None
    end_time = None

    while True:
        try:
            user_input = input("Enter start date and time of the time you would like to book(YYYY-MM-DD HH:MM): ")
            # Parse the user input into a datetime object
            start_time = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M")
            break
            
        except ValueError:
            print("Invalid input format. Please enter a date and time in the format YYYY-MM-DD HH:MM")

    numTimeSlots = int(input("How many hours would you like to set as booked"))

    end_time = start_time+ datetime.timedelta(hours=numTimeSlots)

    trainer_id = user[0]

    query = "SELECT * FROM available_times WHERE booked = FALSE AND trainer_id = %s AND start_time <= %s AND end_time >= %s"
    queryData = (trainer_id, start_time, end_time)
    availableTime = executeQuery(connection, query, queryData, fetchOne=True)

    if(availableTime == None):
        print("There is no time slot there to set as booked")
    else:
        if(availableTime[1] == start_time and availableTime[2] == end_time):
            query = "UPDATE available_times SET booked = TRUE WHERE availability_id = %s"
            queryData = (availableTime[0],)
            executeQuery(connection, query, queryData)
        elif(availableTime[1] == start_time):
            query = "UPDATE available_times SET booked = TRUE, end_time = %s WHERE availability_id = %s"
            queryData = (end_time, availableTime[0])
            executeQuery(connection, query, queryData)

            query = "INSERT INTO available_times (start_time, end_time, trainer_id, booked) VALUES (%s, %s, %s, FALSE)"
            queryData = (end_time, availableTime[2], user[0])
            executeQuery(connection, query, queryData)

        elif(availableTime[2] == end_time):
            query = "UPDATE available_times SET booked = TRUE, start_time = %s WHERE availability_id = %s"
            queryData = (start_time, availableTime[0])
            executeQuery(connection, query, queryData)

            query = "INSERT INTO available_times (start_time, end_time, trainer_id, booked) VALUES (%s, %s, %s, FALSE)"
            queryData = (availableTime[1], start_time, user[0])
            executeQuery(connection, query, queryData)
        else:
            query = f"DELETE FROM available_times WHERE availability_id = %s"
            queryData = (availableTime[0],)
            executeQuery(connection, query, queryData)

            query = "INSERT INTO available_times (start_time, end_time, trainer_id, booked) VALUES (%s, %s, %s, FALSE)"
            queryData = (availableTime[1], start_time, user[0])
            executeQuery(connection, query, queryData)

            query = "INSERT INTO available_times (start_time, end_time, trainer_id, booked) VALUES (%s, %s, %s, TRUE)"
            queryData = (start_time, end_time, user[0])
            executeQuery(connection, query, queryData)

            query = "INSERT INTO available_times (start_time, end_time, trainer_id, booked) VALUES (%s, %s, %s, FALSE)"
            queryData = (end_time, availableTime[2], user[0])
            executeQuery(connection, query, queryData)




