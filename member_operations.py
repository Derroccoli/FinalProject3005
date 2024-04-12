from database_operations import *
from main import *

def memberWorkFlow(connect, user):
    while True:
        memberMenu()
        choices = ["1", "2", "3"]
        menuChoice = input("Please type in (1, 2, or 3): ")
        print()
        
        if menuChoice not in choices:
            print("invalid option")
            continue

        if menuChoice == "1":
            while True:
                headers = getHeaders(connect, "members")
                profileMenu()
                profileValues = ["1","2","3","4"]
                profileChoice = input("Please type in (1 - 4): ")

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
                
                else:
                    updateRoutine(connect, user)
        
        elif menuChoice == "2":
            while True:
                displayMenu()
                displayChoice = input("Please input your decision (1 - 3): ")

                if displayChoice not in ["1", "2", "3"]:
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

                else:
                    break


        else:
            break

def updateProfile(connection, user):
     print("Above is your profile, what would you like to change?")
     while True:
        print("1. Email")
        print("2. Phone Number")
        print("B. backout")
        profileInput = input("Input 1 or 2: ")

        if profileInput.upper() not in ["1","2","B"]:
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
        
        if profileInput == "2":
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

        if profileInput.upper() == "B":
            break

def updateFitnessGoals(connection, user):
    #code to fetch user's fitness goals
    
    while True:
        query = "SELECT * FROM fitness_goals WHERE member_id = %s"
        data = (user[0],)
        fitnessGoals = executeQuery(connection, query, data, True)
        headers = getHeaders(connection, "fitness_goals")
        printTable(fitnessGoals, headers)

        print("Would you like to add, remove or complete a fitness goals?")
        userChoice = input("Please type in (add, remove or complete)").upper()

        if userChoice not in ["ADD", "REMOVE", "COMPLETE"]:
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
            data = (user[0], goal, "No")
            executeQuery(connection, query, data)
            print("goal successfully added")

        elif userChoice == "REMOVE":
            while True:
                printTable(fitnessGoals, headers)
                print("Please enter the fitness ID for the goal you would like to Delete")
                idInput = input("ID: ")
                for elements in fitnessGoals:
                    if idInput == elements[0]:
                        deleteQuery = "DELETE FROM fitness_goals WHERE fitness_id = %s"
                        data = (elements[0])
                        executeQuery(connection, deleteQuery, data)
                        break
                    
                print("invalid ID entered")

        else:
            while True:
                printTable(fitnessGoals, headers)
                print("Please enter the fitness ID for the goal you would like to complete")
                idInput = input("ID: ")
                for elements in fitnessGoals:
                    if idInput == elements[0]:
                        #add an achievement and delete the goal
                        addQuery = "INSERT INTO achievements (member_id, date_of_accomplishment, feat) VALUES (%s,%s,%s)"
                        addData = (user[0], datetime.datetime.today(), elements[2])
                        executeQuery(connection, addQuery, addData)

                        deleteQuery  = "DELETE FROM fitness_goals WHERE fitness_id = %s"
                        deleteData = (elements[0])
                        executeQuery(connection, deleteQuery, deleteData)
                        print("congratulation on completing the goal, it has been moved to your achievements")
                        break
                print("invalid ID entered")
                

def updateHealthMetric(connection, user):
    while True:
        query = "SELECT * FROM health_metrics WHERE member_id = %s"
        data = (user[0],)
        healthMetrics = executeQuery(connection, query, data, True)
        headers = getHeaders(connection, "health_metrics")
        printTable(healthMetrics, headers)

        print("Would you like to add or remove a health metric")
        userChoice = input("Please type in (add or remove)").upper()

        if userChoice not in ["ADD", "REMOVE"]:
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

        else:
            while True:
                printTable(healthMetrics, headers)
                print("Please enter the metric ID for the health metric you would like to Delete")
                idInput = input("ID: ")
                for elements in healthMetrics:
                    if idInput == elements[0]:
                        deleteQuery = "DELETE FROM health_metrics WHERE metric_id = %s"
                        data = (elements[0])
                        executeQuery(connection, deleteQuery, data)
                        break
                    
                print("invalid ID entered")


def updateRoutine(connection, user):
    while True:
        query = "SELECT * FROM exercises WHERE member_id = %s"
        data = (user[0],)
        exercises = executeQuery(connection, query, data, True)
        headers = getHeaders(connection, "exercises")
        printTable(exercises, headers)

        print("Would you like to add or remove an exercise routine")
        userChoice = input("Please type in (add or remove)").upper()

        if userChoice not in ["ADD", "REMOVE"]:
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

                if not sets:
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

                if not sets:
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

def displayHealth(connection, user):
    query = "SELECT * FROM health_metrics WHERE member_id = %s"
    data = (user[0],)
    healthMetrics = executeQuery(connection, query, data, True)
    headers = getHeaders(connection, "health_metrics")
    printTable(healthMetrics, headers)


def displayExercise(connection, user):
    query = "SELECT * FROM exercises WHERE member_id = %s"
    data = (user[0],)
    exercises = executeQuery(connection, query, data, True)
    headers = getHeaders(connection, "exercises")
    printTable(exercises, headers)


def displayAchievements(connection, user):
    query = "SELECT * FROM achievements WHERE member_id = %s"
    data = (user[0],)
    achievements = executeQuery(connection, query, data, True)
    headers = getHeaders(connection, "achievments")
    printTable(achievements, headers)


def memberMenu():
     print("What would you like to do?")
     print("1. Update Personal and exercise information")
     print("2. Check exercise routines, fitness achievements and health statistics")
     print("3. Book personal or group training sessions")
     print("Q. Exit\n")

def profileMenu():
     print("What would you like to update?")
     print("1. Profile")
     print("2. Fitness goals")
     print("3. Health metrics")
     print("4. Exercise routine")

def displayMenu():
    print("What would you like to check?")
    print("1. Health statistics?")
    print("2. Exercise routines?")
    print("3. Achievements")

