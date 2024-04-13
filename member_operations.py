from database_operations import *
from main import *
from trainer_operations import *

def memberWorkFlow(connect, user):
    while True:
        memberMenu()
        choices = ["1", "2", "3", "0"]
        menuChoice = input("Please type in (0-3): ")
        print()
        
        if menuChoice not in choices:
            print("invalid option")
            continue

        if menuChoice == "1":
            while True:
                headers = getHeaders(connect, "members")
                profileMenu()
                profileValues = ["1","2","3","4","0"]
                profileChoice = input("Please type in (0 - 4): ").upper()

                if profileChoice not in profileValues:
                    print("invalid option")
                    continue
                
                if profileChoice == "1":
                    printTable(user, headers, True)
                    updateProfile(connect, user)
                
                elif profileChoice == "2":
                    updateFitnessGoals(connect, user)
                
                elif profileChoice == "3":
                    updateHealthMetric(connect, user)
                
                elif profileChoice == "4":
                    updateRoutine(connect, user)

                else:
                    break

        elif menuChoice == "2":
            while True:
                displayMenu()
                displayChoice = input("Please input your decision (0 - 3): ")

                if displayChoice not in ["1", "2", "3", "0"]:
                    print("invalid option")
                    continue

                if displayChoice == "1":
                    print("Here are you health statistics!\n")
                    displayHealth(connect, user)
                    print("What else would like to see? \n")

                elif displayChoice == "2":
                    print("Here are you exercise routines\n")
                    displayExercise(connect, user)
                    print("What else would like to see? \n")

                elif displayChoice == "3":
                    print("Here are your Achievements!")
                    displayAchievements(connect, user)
                    print("What else would like to see? \n")
                
                else:
                    break

        elif menuChoice == "3":
            while True:
                schedulingMenu()
                scheduleChoice = input("Please input (0-6)")

                if scheduleChoice not in ["1", "2", "3", "4", "5", "6", "0"]:
                    print("invalid option")
                    continue

                if scheduleChoice == "1":
                    schedulePersonalSession(connect, user)
                elif scheduleChoice == "2":
                    reschedulePersonalSession(connect, user)
                elif scheduleChoice == "3":
                    cancelPersonalSession(connect, user)
                elif scheduleChoice == "4":
                    viewYourPersonalSessions(connect, user)
                elif scheduleChoice == "5":
                    scheduleClass(connect, user)
                elif scheduleChoice == "6":
                    viewYourClasses(connect, user)
                
                else:
                    break


        else:
            break

def updateProfile(connection, user):
     print("Above is your profile, what would you like to change?")
     while True:
        print("0. backout")
        print("1. Email")
        print("2. Phone Number")
        
        profileInput = input("Input (0-2): ")

        if profileInput.upper() not in ["1","2","0"]:
             print("invalid option")
             continue
        
        if profileInput == "1":
             while True:
                newEmail = input("Please input your new email: ")

                if not newEmail:
                    print("invalid, please input an email")
                    continue

                query = "UPDATE members SET email = %s WHERE member_id = %s"
                data = (newEmail, user[0])
                executeQuery(connection, query, data)
                print("email successfully changed.")
                break
        
        elif profileInput == "2":
            while True:
                newPhoneNumber = input("Please input your new phone number: ")

                if not newPhoneNumber:
                    print("invalid, please input a phone number")
                    continue

                query = "UPDATE members SET phone_number = %s WHERE member_id = %s"
                data = (newPhoneNumber, user[0])
                executeQuery(connection, query, data)
                print("phone number successfully changed.")
                break

        else:
            break

def updateFitnessGoals(connection, user):
    #code to fetch user's fitness goals
    query = "SELECT * FROM fitness_goals WHERE member_id = %s"
    data = (user[0],)
    fitnessGoals = executeQuery(connection, query, data)
    headers = getHeaders(connection, "fitness_goals")
    printTable(fitnessGoals, headers, False)
    
    while True:
        print("Would you like to add, remove or complete a fitness goals?\nYou can also input B to backtrack")
        userChoice = input("Please type in (add, remove or complete)").upper()

        if userChoice not in ["ADD", "REMOVE", "COMPLETE", "B"]:
            print("Invalid choice")
            continue

        if userChoice == "ADD":
            while True:
                goal = input("What goal do you want to add: ")

                if not goal:
                    print("please add a valid goal")
                    continue
                
                break

            query = "INSERT INTO fitness_goals (member_id, description, completed) VALUES (%s, %s, %s)"
            data = (user[0], goal, "Incomplete")
            print(data)
            executeQuery(connection, query, data)
            print("goal successfully added")

        elif userChoice == "REMOVE":
            while True:
                printTable(fitnessGoals, headers)
                print("Please enter the fitness ID for the goal you would like to Delete")
                idInput = input("ID: ")
                for elements in fitnessGoals:
                    if idInput == str(elements[0]):
                        print("proc")
                        deleteQuery = "DELETE FROM fitness_goals WHERE fitness_id = %s"
                        data = (elements[0],)
                        executeQuery(connection, deleteQuery, data)
                        break
                    
                print("invalid ID entered")

        elif userChoice == "COMPLETE":
            while True:
                printTable(fitnessGoals, headers)
                print("Please enter the fitness ID for the goal you would like to complete")
                idInput = input("ID: ")
                for elements in fitnessGoals:
                    if idInput == str(elements[0]):
                        #add an achievement and delete the goal
                        addQuery = "INSERT INTO achievements (member_id, date_of_accomplishment, feat) VALUES (%s,%s,%s)"
                        addData = (user[0], datetime.datetime.today(), elements[2])
                        executeQuery(connection, addQuery, addData)

                        deleteQuery  = "DELETE FROM fitness_goals WHERE fitness_id = %s"
                        deleteData = (elements[0],)
                        executeQuery(connection, deleteQuery, deleteData)
                        print("congratulation on completing the goal, it has been moved to your achievements")
                        break
                print("invalid ID entered")
        else:
            break
                

def updateHealthMetric(connection, user):
    while True:
        query = "SELECT * FROM health_metrics WHERE member_id = %s"
        data = (user[0],)
        healthMetrics = executeQuery(connection, query, data)
        headers = getHeaders(connection, "health_metrics")
        printTable(healthMetrics, headers, False)

        print("Would you like to add or remove a health metric\nYou can also input B to backtrack")
        userChoice = input("Please type in (add or remove)").upper()

        if userChoice not in ["ADD", "REMOVE", "B"]:
            print("Invalid option")
            continue

        if userChoice == "ADD":
            while True:
                metric = input("What health metric do you want to add: ")

                if not metric:
                    print("please add a valid metric")
                    continue
                
                break

            while True:
                metricValue = input("What is the value of this metric: ")

                if not metricValue:
                    print("please add a valid value")
                    continue
                
                break

            query = "INSERT INTO health_metrics (member_id, recorded_date, metric_type, value) VALUES (%s, %s, %s, %s)"
            data = (user[0], datetime.datetime.today(), metric, metricValue)
            executeQuery(connection, query, data)
            print("metric successfully added")

        elif userChoice == "REMOVE":
            while True:
                printTable(healthMetrics, headers)
                print("Please enter the metric ID for the health metric you would like to Delete")
                idInput = input("ID: ")
                if not idInput:
                    print("invalid input")
                    continue

                for elements in healthMetrics:
                    if idInput == str(elements[0]):
                        deleteQuery = "DELETE FROM health_metrics WHERE metric_id = %s"
                        data = (elements[0],)
                        executeQuery(connection, deleteQuery, data)
                        finishedRemoving = True
                        
                if finishedRemoving:
                    break
                    
        else:
            break


def updateRoutine(connection, user):
    while True:
        query = "SELECT * FROM exercises WHERE member_id = %s"
        data = (user[0],)
        exercises = executeQuery(connection, query, data)
        headers = getHeaders(connection, "exercises")
        printTable(exercises, headers, False)

        print("Would you like to add or remove an exercise routine\nYou can also input B to backtrack")
        userChoice = input("Please type in (add or remove)").upper()

        if userChoice not in ["ADD", "REMOVE", "B"]:
            print("Invalid option")
            continue
        
        if userChoice == "ADD":
            while True:
                print("Please note that it is okay to enter 0 when prompted for duration\nif your exercise was not time gated")
                exercise = input("What exercise did you do: ")

                if not exercise:
                    print("please add a valid exercise")
                    continue
                
                break

            while True:
                sets = input("How many sets: ")

                if not sets:
                    print("please add a valid value")
                    continue
                
                if sets.isdigit():
                    break

                else:
                    print("Not a numerical value")
                    continue

            while True:
                reps = input("How many reps: ")

                if not reps:
                    print("please add a valid value")
                    continue
                
                #check if is int
                if reps.isdigit():
                    break

                else:
                    print("Not a numerical value")
                    continue

            while True:
                duration = input("what is the duration: ")

                if not duration:
                    print("please add a valid value")
                    continue
                
                if duration.isdigit():
                    break

                else:
                    print("Not a numerical value")
                    continue

            query = "INSERT INTO exercises (member_id, date_of_routine, exercise, sets, reps, duration) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (user[0], datetime.datetime.today(), exercise, sets, reps, duration)
            executeQuery(connection, query, data)
            print("exercise successfully added")

        elif userChoice == "REMOVE":
            while True:
                printTable(exercises, headers)
                print("Please enter the exercise ID for the exercise you would like to remove from your routine")
                idInput = input("ID: ")
                if not idInput:
                    print("invalid input")
                    continue

                for elements in exercises:
                    if idInput == str(elements[0]):
                        deleteQuery = "DELETE FROM exercises WHERE routine_id = %s"
                        data = (elements[0],)
                        executeQuery(connection, deleteQuery, data)
                        finishedRemoving = True
                        
                if finishedRemoving:
                    break

        else:
            break

def displayHealth(connection, user):
    query = "SELECT recorded_date, metric_type, value FROM health_metrics WHERE member_id = %s"
    data = (user[0],)
    headerData = ("recorded_date", "metric_type", "value")
    healthMetrics = executeQuery(connection, query, data)
    headers = getHeaders(connection, "health_metrics", headerData)
    printTable(healthMetrics, headers)


def displayExercise(connection, user):
    query = "SELECT date_of_routine, exercise, sets, reps, duration FROM exercises WHERE member_id = %s"
    data = (user[0],)
    headerData = ("date_of_routine", "exercise", "sets", "reps", "duration")
    exercises = executeQuery(connection, query, data)
    headers = getHeaders(connection, "exercises", headerData)
    printTable(exercises, headers)


def displayAchievements(connection, user):
    query = "SELECT date_of_accomplishment, feat FROM achievements WHERE member_id = %s"
    data = (user[0],)
    headerData = ("date_of_accomplishment", "feat")
    achievements = executeQuery(connection, query, data)
    headers = getHeaders(connection, "achievements", headerData)
    printTable(achievements, headers)


def schedulePersonalSession(connection, user):
    while True:
        print("Here are the trainers: ")
        trainerQuery = "SELECT * FROM trainers"
        trainerHeader = getHeaders(connection, "trainers")
        trainers = executeQuery(connection, trainerQuery)
        printTable(trainers, trainerHeader)
        print()
        print("Here's the schedule")
        query = "SELECT * FROM available_times"
        availableTimes = executeQuery(connection, query)
        headers = getHeaders(connection, "available_times")
        printTable(availableTimes, headers)

        while True:
            trainerId = int(input("Input the trainer Id of the trainer you would like to book with: "))

            for trainer in trainers:
                if trainerId == trainer[0]:
                    isTrainer = True
                
            if isTrainer:
                break
        
        while True:
            try:
                user_input = input("Enter start date and time of the time you would like to book(YYYY-MM-DD HH:MM): ")
                # Parse the user input into a datetime object
                start_time = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M")
                break

            except ValueError:
                print("Invalid input format. Please enter a date and time in the format YYYY-MM-DD HH:MM")

        while True:
            numTimeSlots = int(input("How many hours would you like to set as booked: "))

            if not numTimeSlots:
                print("invalid value")
                continue

            break
                
            
        booked = bookTimeByTimeAnyone(connection, trainerId, start_time, numTimeSlots)
        
        print(trainerId, start_time, numTimeSlots)

        if booked == False:
            print("invalid number of hours")
            continue

        else:
            while True:
                #get parameters for session, create a bill, ask the user to pay the bill, if the bill is payed create a payment and then, create the session
                sessionType = input("What kind of session is this (ex: cardio, weights, etc.): ")

                if not sessionType:
                    print("Must input a value")
                    continue
                
                break
            
            #create bill
            end_time = start_time+ datetime.timedelta(hours=numTimeSlots)
            price = numTimeSlots * 30

            billQuery = "INSERT INTO bills (amount, member_id) VALUES (%s, %s)"
            billData = (price, user[0])
            bill_id = executeQuery(connection, billQuery, billData, True, True)


            print("Here is your bill: ")
            billQuery = "SELECT * FROM bills WHERE bill_id = (SELECT MAX(bill_id) FROM bills)"
            billHeader = getHeaders(connection, "bills")
            bills = executeQuery(connection, billQuery)
            printTable(bills, billHeader)

    
            

            print("Bill created, it will be %i dollars", price)
            
            while True:
                pay = input("Would you like to pay?(Y or N): ").upper()

                if pay not in ["Y", "N"]:
                    print("invalid input please try again")
                    continue
                
                break
            
            if pay == "Y":
                #create payment
                paymentQuery = "INSERT INTO payments (bill_id, amount, date, processed) VALUES (%s, %s, %s, %s)"
                payData = (bill_id, price, datetime.datetime.today(), "Not Processed")
                executeQuery(connection, paymentQuery, payData)

                query = "INSERT INTO pt_session (member_id, trainer_id, session_type, start_time, end_time) VALUES (%s, %s, %s, %s, %s)"
                data = (user[0], trainerId, sessionType, start_time, end_time)
                executeQuery(connection, query, data)
                print(" Session successfully created")


                query = "SELECT * FROM pt_session WHERE member_id = %s and session_id = (SELECT MAX(session_id) from pt_session)"
                queryData = (user[0],)

                session = executeQuery(connection, query, queryData, fetchOne=True)

                headers = getHeaders(connection, "pt_session")
                printTable(session, headers, one=True)

                break

                


            else:
                print("Scheduling cancelled")
                query = "UPDATE available_times SET booked = FALSE WHERE start_time = %s AND end_time = %s"
                queryData = (start_time, end_time)
                executeQuery(connection, query, queryData)
                break
            
def reschedulePersonalSession(connection, user):
    viewYourPersonalSessions(connection, user)
    session_id = int(input("What is the session_id of the personal training session you would like to reschedule: "))
    query = "SELECT * FROM pt_session WHERE member_id = %s and session_id = %s"
    queryData = (user[0], session_id)

    session = executeQuery(connection, query, queryData, fetchOne=True)

    if(session != None):
        headers = getHeaders(connection, "pt_session")
        printTable(session, headers, one=True)

        trainer_id = session[2]
        print(trainer_id)

        print("Here are the times your trainer is available for")
        query = "SELECT * FROM available_times WHERE trainer_id = %s"
        queryData = (trainer_id,)
        availableTimes = executeQuery(connection, query, queryData)
        headers = getHeaders(connection, "available_times")
        printTable(availableTimes, headers)

        start_time = None
        while True:
            try:
                user_input = input("Enter start date and time of the time you would like to book(YYYY-MM-DD HH:MM): ")
                # Parse the user input into a datetime object
                start_time = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M")
                break

            except ValueError:
                print("Invalid input format. Please enter a date and time in the format YYYY-MM-DD HH:MM")

        numTimeSlots = int(input("How many hours would you like to set as booked: "))

        
        end_time = start_time+ datetime.timedelta(hours=numTimeSlots)

        query = "SELECT * FROM available_times WHERE booked = FALSE AND trainer_id = %s AND start_time <= %s AND end_time >= %s"
        queryData = (trainer_id, start_time, end_time)
        availableTime = executeQuery(connection, query, queryData, fetchOne=True)

        if(availableTime == None):
            print("There is no time slot there to set as booked")
        else:
            query = "SELECT start_time, end_time FROM pt_session WHERE session_id = %s"
            queryData = (session_id,)
            result = executeQuery(connection, query, queryData)

            query = "UPDATE available_times SET booked = FALSE WHERE start_time = %s AND end_time = %s"
            queryData = (result[0][0], result[0][1])
            executeQuery(connection, query, queryData)

            query = "UPDATE pt_session SET start_time = %s, end_time = %s WHERE session_id = %s"
            queryData = (start_time, end_time, session_id)
            executeQuery(connection, query, queryData)

            query = "SELECT * FROM pt_session WHERE member_id = %s and session_id = %s"
            queryData = (user[0], session_id)

            session = executeQuery(connection, query, queryData, fetchOne=True)

            headers = getHeaders(connection, "pt_session")
            printTable(session, headers, one=True)

            print("Your session has been updated.")

    else:
        print("There is no session of yours that matches")
    
def cancelPersonalSession(connection, user):
    viewYourPersonalSessions(connection, user)
    print("There are no refunds")
    session_id = int(input("What is the session_id of the personal training session you would like to cancel: "))

    query = "DELETE FROM pt_session WHERE member_id = %s and session_id = %s"
    queryData = (user[0], session_id)

    executeQuery(connection, query, queryData)

    query = "SELECT start_time, end_time FROM pt_session WHERE session_id = %s"
    queryData = (session_id,)
    result = executeQuery(connection, query, queryData)
    query = "UPDATE available_times SET booked = FALSE WHERE start_time = %s AND end_time = %s"
    queryData = (result[0][0], result[0][1])
    executeQuery(connection, query, queryData)

    viewYourPersonalSessions(connection, user)

def viewYourPersonalSessions(connection, user):
    print("Your personal sessions: ")
    query = "SELECT * FROM pt_session WHERE member_id = %s"
    queryData = (user[0],)
    result = executeQuery(connection, query, queryData)
    headers = getHeaders(connection, "pt_session")
    printTable(result, headers)


def scheduleClass(connection, user):
    while True:
        print("Here are the Classes: ")
        query = "SELECT * FROM group_fitness"
        classHeader = getHeaders(connection, "group_fitness")
        classes = executeQuery(connection, query)
        printTable(classes, classHeader)

        while True:
            groupId = int(input("Please enter the group id for the class you would like to join: "))

            if not groupId:
                print("invalid value")
                continue
            
            for id in classes:
                if groupId == id[0]:
                    isValidGroup = True
            
            if isValidGroup:
                break

        
        billQuery = "INSERT INTO bills (amount, member_id) VALUES (%s, %s)"
        billData = (50, user[0])
        bill_id = executeQuery(connection, billQuery, billData, False, True)

        print("Bill created, it will be 50 dollars")
            
        while True:
            pay = input("Would you like to pay?(Y or N): ").upper()

            if pay not in ["Y", "N"]:
                print("invalid input please try again")
                continue
            
            break
        
        if pay == "Y":
            #create payment
            paymentQuery = "INSERT INTO payments (bill_id, amount, date, processed) VALUES (%s, %s, %s, %s)"
            payData = (bill_id, 50, datetime.datetime.today(), "Not Processed")
            executeQuery(connection, paymentQuery, payData)

            query = "INSERT INTO group_members (group_id, member_id) VALUES (%s, %s)"
            data = (groupId, user[0])
            executeQuery(connection, query, data)
            print("Added to Class")

            viewYourClasses(connection, user)
            break

        else:
            print("Scheduling cancelled")
            break
            
        
def viewYourClasses(connection, user):
    print("Your personal sessions: ")
    query = "SELECT gf.* FROM group_fitness gf JOIN group_members gm ON gf.group_id = gm.group_id WHERE gm.member_id = %s"
    queryData = (user[0],)
    result = executeQuery(connection, query, queryData)
    headers = getHeaders(connection, "group_fitness")
    printTable(result, headers)
        

def memberMenu():
     print("What would you like to do?")
     print("0. Exit App\n")
     print("1. Update Personal and exercise information")
     print("2. Check exercise routines, fitness achievements and health statistics")
     print("3. Book personal or group training sessions")
     

def profileMenu():
     print("What would you like to update?")
     print("0. BackTrack\n")
     print("1. Profile")
     print("2. Fitness goals")
     print("3. Health metrics")
     print("4. Exercise routine")
     

def displayMenu():
    print("What would you like to check?")
    print("0. BackTrack\n")
    print("1. Health statistics?")
    print("2. Exercise routines?")
    print("3. Achievements")
    

def schedulingMenu():
    print("Welcome to the scheduling zone")
    print("What would you like to do?")
    print("0. BackTrack\n")
    print("1. Schedule a personal training session")
    print("2. Reschedule a personal training session")
    print("3. Cancel a personal training session")
    print("4. View your personal training sessions")
    print("5. Register for a group class")
    print("6. View your group classes")

