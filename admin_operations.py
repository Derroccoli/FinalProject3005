import datetime
from database_operations import *

def adminFunctions(connection):
    print("What would you like to do:")

    while True:
        print("Admin menu")
        print("0. Quit")
        print("1. Manage room booking")
        print("2. Manage equipment maintenance")
        

        uInput = int(input())

        if (uInput == 0):
            break
        elif (uInput == 1):
            roomFunctions(connection)
        elif(uInput == 2):
            equipmentFunctions(connection)

def roomFunctions(connection):
    print("What would you like to do:")

    while True:
        print("Room Booking Menu")
        print("0. Go back to the main admin menu")
        print("1. View rooms")
        print("2. View room bookings")
        print("3. Book a room")
        print("4. Cancel a room booking")
        print("5. Remove old room bookings")
        

        uInput = int(input())

        if (uInput == 0):
            break
        elif (uInput == 1):
            viewRooms(connection)
        elif (uInput == 2):
            viewRoomBookings(connection)
        elif (uInput == 3):
            bookARoom(connection)
        elif (uInput == 4):
            cancelARoomBooking(connection)
        elif (uInput == 5):
            removeOldRoomBookings(connection)

def viewRooms(connection):
    query = "SELECT * FROM rooms"
    headers = getHeaders(connection, "room")
    result = executeQuery(connection, query)

    printTable(result, headers)

def viewRoomBookings(connection):
    query = "SELECT * FROM room_bookings"
    headers = getHeaders(connection, "room_bookings")
    result = executeQuery(connection, query)

    printTable(result, headers)

def bookARoom(connection):

    start_time = None
    end_time = None

    while True:
        try:
            user_input = input("Enter start date and time (YYYY-MM-DD HH:MM:SS): ")
            # Parse the user input into a datetime object
            start_time = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M:%S")
            break
            
        except ValueError:
            print("Invalid input format. Please enter a date and time in the format YYYY-MM-DD HH:MM:SS")


    while True:
        try:
            user_input = input("Enter end and time (YYYY-MM-DD HH:MM:SS): ")
            # Parse the user input into a datetime object
            end_time = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M:%S")
            break
            
        except ValueError:
            print("Invalid input format. Please enter a date and time in the format YYYY-MM-DD HH:MM:SS")

    room_id = int(input("Enter the room id of the room you'd like to book:"))

    query = "INSERT INTO room_bookings (start_time, end_time, room_id) VALUES (%s, %s, %s)"
    queryData = (start_time, end_time, room_id)
    executeQuery(connection, query, queryData)

def cancelARoomBooking(connection):
    room_booking_id = int(input("Enter the room booking id of the room booking you'd like to cancel"))

    query = f"DELETE FROM room_bookings WHERE room_booking_id = %s"

    queryData = (room_booking_id,)

    executeQuery(connection, query, queryData)


def removeOldRoomBookings(connection):
    query = f"DELETE FROM room_bookings WHERE end_time < CURRENT_DATE"

    executeQuery(connection, query)



def equipmentFunctions(connection):
    while True:
        print("Room Booking Menu")
        print("0. Go back to the main admin menu")
        print("1. View equipment status")
        print("2. Mark an equipment as maintained")
        print("3. Mark all equipment as maintained")
        print("4. Add new equipment")
        print("5. Remove old equipment")
        

        uInput = int(input())

        if (uInput == 0):
            break
        elif (uInput == 1):
            viewEquipment(connection)
        elif (uInput == 2):
            markMaintained(connection)
        elif (uInput == 3):
            markAllMaintained(connection)
        elif (uInput == 4):
            addNewEquipment(connection)
        elif (uInput == 5):
            removeOldEquipment(connection)


def viewEquipment(connection):
    query = "SELECT * FROM equipments"
    headers = getHeaders(connection, "equipments")
    result = executeQuery(connection, query)

    printTable(result, headers)


def markMaintained(connection):
    equipment_id = int(input("Enter the id of the equipment that you maintained today"))

    query = "UPDATE equipments SET maintenance_date = CURRENT_DATE WHERE equipment_id = %s;"
    queryData = (equipment_id,)
    result = executeQuery(connection, query, queryData)

def markAllMaintained(connection):
    query = "UPDATE equipments SET maintenance_date = CURRENT_DATE;"
    result = executeQuery(connection, query)

def addNewEquipment(connection):
    equipment_type = input("What type of equipment is this new equipment: ")
    description = input("Give a short description of this equpment: ")

    query = "INSERT INTO room_bookings (equipment_type, description, maintenance_date) VALUES (%s, %s, CURRENT_DATE)"
    queryData = (equipment_type, description)
    result = executeQuery(connection, query, queryData)

def removeOldEquipment(connection):
    equipment_id = int(input("Enter the id of the equipment that you are getting rid of"))

    query = f"DELETE FROM room_bookings WHERE equipment_id = %s"
    queryData = (equipment_id,)

    result = executeQuery(connection, query, queryData)

