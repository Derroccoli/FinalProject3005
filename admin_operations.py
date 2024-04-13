import datetime
from database_operations import *
from trainer_operations import *

def adminFunctions(connection, user):

    while True:
        print()
        print("Admin menu")
        print("0. Quit")
        print("1. Manage room booking")
        print("2. Manage equipment maintenance")
        print("3. Manage class schedules")
        print("4. Manage bills and payments")
        print()
        

        uInput = int(input("Enter (0-4): "))

        if (uInput == 0):
            break
        elif (uInput == 1):
            roomFunctions(connection)
        elif(uInput == 2):
            equipmentFunctions(connection)
        elif(uInput == 3):
            groupClassFunctions(connection)
        elif(uInput == 4):
            billingPaymentFunctions(connection)

def roomFunctions(connection):

    while True:
        print()
        print("Room Booking Menu")
        print("0. Go back to the main admin menu")
        print("1. View rooms")
        print("2. View room bookings")
        print("3. Book a room")
        print("4. Cancel a room booking")
        print("5. Remove old room bookings")
        print()
        

        uInput = int(input("Enter (0-5): "))

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
    headers = getHeaders(connection, "rooms")
    result = executeQuery(connection, query)

    printTable(result, headers)

def viewRoomBookings(connection):
    query = "SELECT * FROM room_bookings"
    headers = getHeaders(connection, "room_bookings")
    result = executeQuery(connection, query)

    printTable(result, headers)

def bookARoom(connection):

    viewRooms(connection)

    start_time = None
    end_time = None

    room_id = int(input("Enter the room id of the room you'd like to book: "))

    while True:
        try:
            user_input = input("Enter start date and time (YYYY-MM-DD HH:MM): ")
            # Parse the user input into a datetime object
            start_time = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M")
            break
            
        except ValueError:
            print("Invalid input format. Please enter a date and time in the format YYYY-MM-DD HH:MM ")

    numTimeSlots = int(input("Enter the number of 1 hour timeslots you would like to book: "))


    end_time = start_time+ datetime.timedelta(hours=numTimeSlots)

    

    if(start_time > end_time):
        print("Start time cannot be after end time, cannot book.")
    elif(check_booking_overlap(connection, start_time, end_time, room_id)):
        print("This room is booked for that time, cannot book.")
    else:
        query = "INSERT INTO room_bookings (start_time, end_time, room_id) VALUES (%s, %s, %s)"
        queryData = (start_time, end_time, room_id)
        executeQuery(connection, query, queryData)

        viewRoomBookings(connection)

    

def cancelARoomBooking(connection):
    viewRoomBookings(connection)

    room_booking_id = int(input("Enter the room booking id of the room booking you'd like to cancel: "))

    query = f"DELETE FROM room_bookings WHERE room_booking_id = %s"

    queryData = (room_booking_id,)

    executeQuery(connection, query, queryData)

    viewRoomBookings(connection)


def removeOldRoomBookings(connection):
    query = f"DELETE FROM room_bookings WHERE end_time < CURRENT_DATE"

    executeQuery(connection, query)

    viewRoomBookings(connection)


def check_booking_overlap(connection, start_time, end_time, room_id):
    # Query to check for overlapping bookings
    query = "SELECT EXISTS (SELECT 1 FROM room_bookings WHERE room_id = %s AND ((start_time, end_time) OVERLAPS (%s, %s)))"

    queryData = (room_id, start_time, end_time)
    overlap_exists = executeQuery(connection, query, queryData, fetchOne=True)

    return overlap_exists[0]


def equipmentFunctions(connection):
    while True:
        print()
        print("Room Booking Menu")
        print("0. Go back to the main admin menu")
        print("1. View equipment status")
        print("2. Mark an equipment as maintained today")
        print("3. Mark all equipment as maintained today")
        print("4. Add new equipment")
        print("5. Remove old equipment")
        print()
        

        uInput = int(input("Enter (0-5): "))

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
    viewEquipment(connection)

    equipment_id = int(input("Enter the id of the equipment that you maintained today: "))

    query = "UPDATE equipments SET maintenance_date = CURRENT_DATE WHERE equipment_id = %s;"
    queryData = (equipment_id,)
    result = executeQuery(connection, query, queryData)

    viewEquipment(connection)

def markAllMaintained(connection):
    query = "UPDATE equipments SET maintenance_date = CURRENT_DATE;"
    result = executeQuery(connection, query)

    viewEquipment(connection)

def addNewEquipment(connection):
    equipment_type = input("What type of equipment is this new equipment: ")
    description = input("Give a short description of this equpment: ")

    query = "INSERT INTO equipments (equipment_type, description, maintenance_date) VALUES (%s, %s, CURRENT_DATE)"
    queryData = (equipment_type, description)
    result = executeQuery(connection, query, queryData)

    viewEquipment(connection)

def removeOldEquipment(connection):
    viewEquipment(connection)

    equipment_id = int(input("Enter the id of the equipment that you are getting rid of: "))

    query = f"DELETE FROM room_bookings WHERE equipment_id = %s"
    queryData = (equipment_id,)

    result = executeQuery(connection, query, queryData)

    viewEquipment(connection)

def groupClassFunctions(connection):
    while True:
        print()
        print("Class management menu")
        print("0. Go back to the main admin menu")
        print("1. View group classes")
        print("2. View members of a particular class")
        print("3. Create a group class")
        print("4. Remove a group class")
        print("5. Delete old group classes")
        print("6. Update a class schedule")
        print()
        

        uInput = int(input("Enter (0-6): "))

        if (uInput == 0):
            break
        elif (uInput == 1):
            viewGroupClasses(connection)
        elif (uInput == 2):
            viewClassMembers(connection)
        elif (uInput == 3):
            createClass(connection)
        elif (uInput == 4):
            removeClass(connection)
        elif (uInput == 5):
            deleteAllOldClasses(connection)
        elif(uInput == 6):
            updateClassSchedule(connection)

def viewGroupClasses(connection):
    query = "SELECT * FROM group_fitness"
    headers = getHeaders(connection, "group_fitness")
    result = executeQuery(connection, query)

    printTable(result, headers)


def viewClassMembers(connection):
    group_id = int(input("Enter the group id of the group you want to find the members for: "))

    query = "SELECT * FROM group_members INNER JOIN members USING (member_id) WHERE group_id = %s"
    queryData = (group_id,)

    headers = getHeaders(connection, "group_members")
    headers = headers[:-1]
    headers = headers + getHeaders(connection, "members")
    result = executeQuery(connection, query, queryData)

    printTable(result, headers)

def createClass(connection):
    query = "SELECT * FROM available_times"
    headers = getHeaders(connection, "available_times")
    result = executeQuery(connection, query)
    printTable(result, headers)

    trainer_id = int(input("Enter the trainer id of the trainer you'd like to run this class: "))
    class_name = input("Enter the name of this class: ")
    description = input("Enter a description for this class: ")
    start_time = None
    while True:
        try:
            user_input = input("Enter start date and time for this class(YYYY-MM-DD HH:MM): ")
            # Parse the user input into a datetime object
            start_time = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M")
            break
            
        except ValueError:
            print("Invalid input format. Please enter a date and time in the format YYYY-MM-DD HH:MM ")

    numTimeSlots = int(input("Enter the number of 1 hour time slots this class will go for: "))
    end_time = start_time+ datetime.timedelta(hours=numTimeSlots)


    if(bookTimeByTimeAnyone(connection, trainer_id, start_time, numTimeSlots)):
        query = "INSERT INTO group_fitness (trainer_id, class_name, description, start_time, end_time) VALUES (%s, %s, %s, %s, %s)"
        queryData = (trainer_id, class_name, description, start_time, end_time)
        executeQuery(connection, query, queryData)
    

    



def removeClass(connection):
    viewGroupClasses(connection)

    group_id = int(input("Enter the group_id of the class you'd like to remove: "))

    query = f"DELETE FROM group_members WHERE group_id = %s"
    queryData = (group_id,)
    executeQuery(connection, query, queryData)

    query = f"DELETE FROM group_fitness WHERE group_id = %s"
    queryData = (group_id,)
    executeQuery(connection, query, queryData)

    viewGroupClasses(connection)

    

def deleteAllOldClasses(connection):
    query = f"SELECT group_id FROM group_fitness WHERE end_time < CURRENT_DATE"

    results = executeQuery(connection, query)

    for result in results:
        query = f"DELETE FROM group_members WHERE group_id = %s"
        queryData = (result,)
        executeQuery(connection, query, queryData)

    query = f"DELETE FROM group_fitness WHERE end_time < CURRENT_DATE"

    executeQuery(connection, query)

    viewGroupClasses(connection)


def updateClassSchedule(connection):
    viewGroupClasses(connection)

    group_id = int(input("Enter the group_id of the class you'd like to update: "))

    query = "SELECT trainer_id FROM group_fitness WHERE group_id = %s"
    queryData = (group_id,)
    result = executeQuery(connection, query, queryData)

    trainer_id = result[0]

    query = "SELECT * FROM available_times WHERE trainer_id = %s AND booked = FALSE"
    queryData = (trainer_id,)
    headers = getHeaders(connection, "available_times")
    result = executeQuery(connection, query, queryData)
    printTable(result, headers)

    start_time = None
    while True:
        try:
            user_input = input("Enter the updated start date and time for this class(YYYY-MM-DD HH:MM): ")
            # Parse the user input into a datetime object
            start_time = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M")
            break
            
        except ValueError:
            print("Invalid input format. Please enter a date and time in the format YYYY-MM-DD HH:MM")

    numTimeSlots = int(input("Enter the number of 1 hour timeslots you would like to book: "))

    end_time = start_time+ datetime.timedelta(hours=numTimeSlots)

    query = "SELECT * FROM available_times WHERE booked = FALSE AND trainer_id = %s AND start_time <= %s AND end_time >= %s"
    queryData = (trainer_id, start_time, end_time)
    availableTime = executeQuery(connection, query, queryData, fetchOne=True)

    if(availableTime == None):
        print("There is no time slot there to set as booked")
    else:
        query = "SELECT start_time, end_time FROM group_fitness WHERE group_id = %s"
        queryData = (group_id,)
        result = executeQuery(connection, query, queryData)

        query = "UPDATE available_times SET booked = FALSE WHERE start_time = %s AND end_time = %s"
        queryData = (result[0][0], result[0][1])
        executeQuery(connection, query, queryData)

        query = "UPDATE group_fitness SET start_time = %s, end_time = %s WHERE group_id = %s"
        queryData = (start_time, end_time, group_id)
        executeQuery(connection, query, queryData)

        viewGroupClasses(connection)


    
def billingPaymentFunctions(connection):

    while True:
        print()
        print("Billing and payment menu")
        print("0. Return to main admin menu")
        print("1. View all bills")
        print("2. View bills with payments")
        print("3. Process a payment by pay_id")
        print("4. Process all unprocessed payments")
        print()
        

        uInput = int(input("Enter (0-4): "))

        if (uInput == 0):
            break
        elif (uInput == 1):
            viewAllBills(connection)
        elif(uInput == 2):
            viewAllBillsWithPayments(connection)
        elif(uInput == 3):
            processPaymentByPayId(connection)
        elif(uInput == 4):
            processAllUnprocessedPayments(connection)

def viewAllBills(connection):
    query = "SELECT * FROM bills"
    headers = getHeaders(connection, "bills")
    result = executeQuery(connection, query)
    printTable(result, headers)

def viewBillsAndPaymentsHelper(connection, uInput):
    if (uInput == 1):
        query = "SELECT * FROM bills INNER JOIN payments USING (bill_id)"
        headers = getHeaders(connection, "bills")

        paymentHeaders = getHeaders(connection, "payments")
        paymentHeaders.remove("bill_id")
        paymentHeaders.remove("amount")
        headers = headers + paymentHeaders
        result = executeQuery(connection, query)
        printTable(result, headers)

    elif(uInput == 2):
        query = "SELECT * FROM payments"
        headers = getHeaders(connection, "payments")
        result = executeQuery(connection, query)
        printTable(result, headers)



def viewAllBillsWithPayments(connection):
    while True:
        print("1. View payments with bills")
        print("2. View just payments")

        uInput = int(input("Enter (1-2): "))
        if (uInput == 1 or uInput == 2):
            viewBillsAndPaymentsHelper(connection, uInput)
            break
        

    

def processPaymentByPayId(connection):
    viewAllBillsWithPayments(connection, 1)

    pay_id = int(input("What is the pay_id of the payment you'd like to process: "))

    query = "UPDATE payments SET processed = 'processed' WHERE pay_id = %s and processed != 'processed'"
    queryData = (pay_id,)
    executeQuery(connection, query, queryData)

    viewAllBillsWithPayments(connection, 1)

def processAllUnprocessedPayments(connection):
    query = "UPDATE payments SET processed = 'processed' WHERE processed != 'processed'"
    executeQuery(connection, query)

    viewAllBillsWithPayments(connection, 2)