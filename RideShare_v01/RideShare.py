#import MySQL
import mysql.connector
import uuid

#Make Connection
conn = mysql.connector.connect(host="localhost",
    user="root",
    password="cpsc408!",
    auth_plugin='mysql_native_password',
    database="RideShare")

#create cursor object
cur_obj = conn.cursor()

def initial_create():
    #create database schema
    cur_obj.execute("CREATE SCHEMA RideShare;")

    #confirm execution worked by printing result
    cur_obj.execute("SHOW DATABASES;")
    for row in cur_obj:
        print(row)

    #Print out connection to verify and close
    print(conn)
    conn.close()

def print_to_verify():
    #Print out connection to verify and close
    print(conn)
    conn.close()

def create():
    #create tables
    users_table = ('''
        CREATE TABLE Users(
        UserID INT NOT NULL PRIMARY KEY,
        IsDriver BOOLEAN
        );
    ''')
    riders_table = ('''
        CREATE TABLE Riders(
        RiderID INT NOT NULL PRIMARY KEY,
        RideID VARCHAR(10)
        );
    ''')
    drivers_table = ('''
        CREATE TABLE Drivers(
        DriverID INT NOT NULL PRIMARY KEY,
        Rating DOUBLE,
        IsActive BOOLEAN
        );
    ''')
    rides_table = ('''
        CREATE TABLE Rides(
        RideID INT NOT NULL PRIMARY KEY,
        RiderID INT,
        DriverID INT,
        PickUpLoc VARCHAR(100),
        DropOffLoc VARCHAR(100)
        );
    ''')

    cur_obj.execute(users_table)
    cur_obj.execute(riders_table)
    cur_obj.execute(drivers_table)
    cur_obj.execute(rides_table)

def insert_data():
    insertUsersQuery = '''
    INSERT INTO Users (UserID, IsDriver)
    VALUES(%s, %s);
    '''
    usersValues = [
    (1, 0),
    (2, 1),
    (3, 0),
    (4, 1),
    (5, 1)
    ]
    cur_obj.executemany(insertUsersQuery, usersValues)
    conn.commit()

    insertRidersQuery = '''
    INSERT INTO Riders (RiderID, RideID)
    VALUES(%s, %s);
    '''
    ridersValues = [
    (1, 'NULL'),
    (3, 'NULL')
    ]
    cur_obj.executemany(insertRidersQuery, ridersValues)
    conn.commit()

    insertDriversQuery = '''
    INSERT INTO Drivers (DriverID, Rating, IsActive)
    VALUES(%s, %s, %s);
    '''
    driversValues = [
    (2, 4.8, 0),
    (4, 1.7, 1),
    (5, 3.5, 0)
    ]
    cur_obj.executemany(insertDriversQuery, driversValues)
    conn.commit()

    insertRidesQuery = '''
    INSERT INTO Rides (RideID, RiderID, DriverID, PickUpLoc, DropOffLoc)
    VALUES(%s, %s, %s, %s, %s);
    '''
    ridesValues = [
    (1, 1, 2, 'Chapman University', 'UCLA'),
    (2, 3, 5, 'Angels Stadium', 'Irvine Spectrum')
    ]
    cur_obj.executemany(insertRidesQuery, ridesValues)
    conn.commit()

def new_or_returning():
    print('''
    Hello! Are you a new or returning user? \n 
    1) New User \n
    2) Returning User \n
    ''') 
    choice = get_choice([1, 2])
    if choice == 1:
        new_user_info()
    elif choice == 2:
        old_user_info()

def new_user_info():
    userID = ""
    isDriver = None

    userID = input("Please enter your ID: ")
    while userID.isdigit() == False:
        userID = input("Invalid ID. Please enter your ID again: ")

    print("Your User ID is: " + userID)

    comparisonUserID = find_user_id_in_table(userID)

    while(int(userID) == comparisonUserID):
        userID = input("This ID already exists. Please enter your ID again: ")
        comparisonUserID = find_user_id_in_table(userID)

    isDriver = set_is_driver(userID, isDriver)

    if isDriver == 1:
        new_driver_choice(userID)
    else:
        create_rider(userID)
        new_rider_choice(userID)

def old_user_info():
    userID = ""
    isDriver = None

    userID = input("Please enter your ID: ")
    while userID.isdigit() == False:
        userID = input("Invalid ID. Please enter your ID again: ")

    print("Your User ID is: " + userID)

    comparisonUserID = find_user_id_in_table(userID)

    while(int(userID) != comparisonUserID):
        userID = input("This ID does not exist. Please enter your ID again: ")
        comparisonUserID = find_user_id_in_table(userID)
    
    selectIsDriver = "SELECT IsDriver FROM Users WHERE UserID = '" + str(userID) + "';"
    cur_obj.execute(selectIsDriver)
    result = cur_obj.fetchall()
    # print(result)
    for row in result:
        isDriver = int(row[0])
        # print(isDriver)
    if isDriver == 1:
        old_driver_choice(userID)
    else:
        old_rider_choice(userID)

def old_driver_choice(userID):
    print('''
    Hello Driver, Welcome Back! Please choose the following: \n 
    1) View my rating \n
    2) View my rides \n
    3) Change my Active Driver mode \n
    ''') 
    choice = get_choice([1, 2, 3])
    if choice == 1:
        view_rating(userID)
    elif choice == 2:
        view_driver_rides(userID)
    elif choice == 3:
        modify_is_driver_active(userID)

def old_rider_choice(userID):
    print('''
    Hello Rider, Welcome Back! Please choose the following: \n 
    1) View my rides \n
    2) Find a driver and start a ride \n
    3) Rate my last driver \n
    ''') 
    choice = get_choice([1, 2, 3])
    if choice == 1:
        view_rider_rides(userID)
    elif choice == 2:
        new_rider_choice(userID)
    elif choice == 3:
        get_last_driver_id(userID)

def get_last_driver_id(userID):
    driverID = 0
    selectLastDriver = "SELECT DriverID FROM Rides WHERE RiderID = '" + str(userID) + "' ORDER BY RideID DESC LIMIT 1;"
    cur_obj.execute(selectLastDriver)
    result = cur_obj.fetchall()
    print(result)
    for row in result:
        driverID = int(row[0])
    print("The Driver ID is: " + str(driverID))
    print('''
    Is this the correct Driver that you would like to rate? \n 
    1) Yes \n
    2) No \n
    ''') 
    choice = get_choice([1, 2])
    if choice == 1:
        rate_driver(driverID)
    elif choice == 2:
        change_driver(userID)
    return driverID

def get_correct_ride(userID):
    driverID = get_last_driver_id(userID)
    print("The Driver ID is: " + str(driverID))
    print('''
    Is this the correct Driver that you would like to rate? \n 
    1) Yes \n
    2) No \n
    ''') 
    choice = get_choice([1, 2])
    if choice == 1:
        rate_driver(driverID)
    if choice == 2:
        change_driver(userID)

def change_driver(userID):
    rideID = input("Enter the Ride ID for the Driver you would like to rate: ")
    selectRide = "SELECT * FROM Rides WHERE RideID = '" + str(rideID) + "';"
    cur_obj.execute(selectRide)
    result = cur_obj.fetchall()
    print(result)
    print('''
    Is this the correct Ride? \n 
    1) Yes \n
    2) No \n
    ''') 
    choice = get_choice([1, 2])
    while(choice == 2):
        change_driver(userID)
    selectDriver = "SELECT DriverID FROM Rides WHERE RideID = '" + str(rideID) + "';"
    cur_obj.execute(selectDriver)
    result = cur_obj.fetchall()
    for row in result:
        driverID = int(row[0])
        # print(driverID)
    rate_driver(driverID)
    
def rate_driver(driverID):
    currRating = 0
    rating = input("What would you like to rate the driver: ")
    selectRating = "SELECT Rating FROM Drivers WHERE DriverID = '" + str(driverID) + "';"
    cur_obj.execute(selectRating)
    result = cur_obj.fetchall()
    
    for row in result:
        try:
            currRating = float(row[0])
            # print(currRating)
            newRating = float((currRating + float(rating)) / 2)
        except:
            newRating = float(rating)
    
    updateDriversQuery = "UPDATE Drivers SET Rating = '" + str(newRating) + "' WHERE DriverID = '" + str(driverID) + "';"
    cur_obj.execute(updateDriversQuery)
    conn.commit()
    print("The Driver's new rating is " + str(newRating))
    
def view_rating(userID):
    selectRating = "SELECT Rating FROM Drivers WHERE DriverID = '" + str(userID) + "';"
    cur_obj.execute(selectRating)
    result = cur_obj.fetchall()
    print(result)
    print("Here is your rating: \n")
    for row in result:
        try:
            viewRating = float(row[0])
            # print(viewRating)
        except:
            print("You do not have a rating :( \n")

def view_rider_rides(userID):
    selectRides = "SELECT * FROM Rides WHERE RiderID = '" + str(userID) + "';"
    cur_obj.execute(selectRides)
    result = cur_obj.fetchall()
    print("Here are all of your rides: \n")
    for row in result:
        print(row)

def view_driver_rides(userID):
    selectRides = "SELECT * FROM Rides WHERE DriverID = '" + str(userID) + "';"
    cur_obj.execute(selectRides)
    result = cur_obj.fetchall()
    print("Here are all of your rides: \n")
    for row in result:
        print(row)

def set_is_driver(userID, isDriver):
    print('''
    Hello! Are you a Rider or a Driver? \n 
    1) Rider \n
    2) Driver \n
    ''') 
    choice = get_choice([1, 2])
    if choice == 1:
        isDriver = 0
        insertUsersQuery = '''
        INSERT INTO Users (UserID, IsDriver)
        VALUES(%s, %s);
        '''
        usersValue = [
        (userID, isDriver)
        ]
        cur_obj.executemany(insertUsersQuery, usersValue)
        conn.commit()
        return isDriver
    elif choice == 2:
        isDriver = 1
        insertUsersQuery = '''
        INSERT INTO Users (UserID, IsDriver)
        VALUES(%s, %s);
        '''
        usersValue = [
        (userID, isDriver)
        ]
        cur_obj.executemany(insertUsersQuery, usersValue)
        conn.commit()
        return isDriver

def new_driver_choice(userID):
    set_is_driver_active(userID)
    return

def set_is_driver_active(userID):
    print('''
    Hi Driver! Are you active currently? \n 
    1) Yes, I am active \n
    2) No, I am not active \n
    ''') 

    isActive = 1
    isNotActive = 0

    choice = get_choice([1, 2])
    if choice == 1:
        insertDriversQuery = '''
        INSERT INTO Drivers (DriverID, IsActive)
        VALUES(%s, %s);
        '''
        driversValues = [
        (userID, isActive)
        ]
        cur_obj.executemany(insertDriversQuery, driversValues)
        conn.commit()

    elif choice == 2:
        insertDriversQuery = '''
        INSERT INTO Drivers (DriverID, IsActive)
        VALUES(%s, %s);
        '''
        driversValues = [
        (userID, isNotActive)
        ]
        cur_obj.executemany(insertDriversQuery, driversValues)
        conn.commit()

def modify_is_driver_active(userID):
    print('''
    Hi Driver! Would you like to change you Active Status? \n 
    1) Yes \n
    2) No \n
    ''') 

    isActive = None
    selectIsActive = "SELECT IsActive FROM Drivers WHERE DriverID = '" + str(userID) + "';"
    cur_obj.execute(selectIsActive)
    result = cur_obj.fetchall()
    for row in result:
        isActive = int(row[0])
        # print(isDriver)
    if(isActive == 0):
        print("You're status is: not active")
    elif(isActive == 1):
        print("You're status is: active")

    choice = get_choice([1, 2])
    if choice == 1:
        if(isActive == 0):
            updateDriversQuery = "UPDATE Drivers SET IsActive = 1 WHERE DriverID = '" + str(userID) + "';"
            cur_obj.execute(updateDriversQuery)
            conn.commit()
            print("You're status is now active")

        elif(isActive == 1):
            updateDriversQuery = "UPDATE Drivers SET IsActive = 0 WHERE DriverID = '" + str(userID) + "';"
            cur_obj.execute(updateDriversQuery)
            conn.commit()
            print("You're status is now active")
    
    if choice == 2:
        return

def create_rider(userID):
    insertRidersQuery = '''
    INSERT INTO Riders (RiderID, RideID)
    VALUES(%s, %s);
    '''
    ridersValues = [
    (userID, 'NULL')
    ]
    cur_obj.executemany(insertRidersQuery, ridersValues)
    conn.commit()

def new_rider_choice(userID):
    print('''
    Hi Rider! Would you like to call a ride? \n 
    1) Yes \n
    2) No \n
    ''') 
    choice = get_choice([1, 2])
    if choice == 1:
        print("Calling Ride \n")
        new_user_call_ride(userID)
    elif choice == 2:
        print("Exit \n")
        # rate_My_Driver(userID)

def new_user_call_ride(userID):
    rideCountOutput = 0

    pickUpLoc = input("Please type your Pick Up Location: ")
    dropOffLoc = input("Please type your Drop Off Location: ")

    rideCount = '''
    SELECT COUNT(*)
    FROM Rides
    '''

    cur_obj.execute(rideCount)
    result = cur_obj.fetchall()
    # print(result)
    for row in result:
        rideCountOutput = int(row[0])
        # print(rideCountOutput)

    rideID = rideCountOutput + 1

    driverID = find_driver()
    
    insertRidesQuery = '''
    INSERT INTO Rides (RideID, RiderID, DriverID, PickUpLoc, DropOffLoc)
    VALUES(%s, %s, %s, %s, %s);
    '''
    ridesValues = [
    (rideID, userID, driverID, pickUpLoc, dropOffLoc),
    ]
    cur_obj.executemany(insertRidesQuery, ridesValues)
    conn.commit()

    print("Your Ride ID is: " + str(rideID))
    print("Your Driver's ID is: " + str(driverID))

    old_rider_choice(userID)

def find_driver():
    selectDriver = '''SELECT UserID 
                    FROM Users u INNER JOIN Drivers d 
                    ON u.UserID = d.DriverID
                    WHERE d.IsActive = 1
                    ORDER BY RAND()
                    LIMIT 1;
                    '''
    cur_obj.execute(selectDriver)
    result = cur_obj.fetchall()
    # print(result)
    for row in result:
        driverID = int(row[0])
        # print(driverID)
    return driverID

def find_user_id_in_table(userID):
    comparisonUserID = 0
    selectDriver = "SELECT UserID FROM Users WHERE UserID = '" + str(userID) + "';"
    cur_obj.execute(selectDriver)
    result = cur_obj.fetchall()
    # print(result)
    for row in result:
        comparisonUserID = int(row[0])
        # print(comparisonUserID)
    return comparisonUserID

def returning_rider_choice():
    print('''
    Hi Rider! What would you like to do? \n 
    1) Call a ride \n
    2) Rate my driver \n
    ''') 
    choice = get_choice([1, 2])
    if choice == 1:
        print("Calling Ride \n")
        # call_Ride(userID)
    elif choice == 2:
        print("Rate the Driver \n")
        # rate_My_Driver(userID)

# from helper function in Assignment 4
def get_choice(lst):
    choice = input("Enter choice number: ")
    while choice.isdigit() == False:
        print("Incorrect option. Try again")
        choice = input("Enter choice number: ")

    while int(choice) not in lst:
        print("Incorrect option. Try again")
        choice = input("Enter choice number: ")
    return int(choice)

def drop_all_tables():
    # drop table
    dropUsers = "DROP TABLE Users"
    dropRiders = "DROP TABLE Riders"
    dropDrivers = "DROP TABLE Drivers"
    dropRides = "DROP TABLE Rides"
    cur_obj.execute(dropUsers)
    cur_obj.execute(dropRiders)
    cur_obj.execute(dropDrivers)
    cur_obj.execute(dropRides)
    conn.commit()

#main program
if __name__ == "__main__":
    print("start main program")
    # initial_create()
    # print_to_verify()
    # create()
    # insert_data()
    # user_info()
    new_or_returning()
    # find_driver()
    # new_user_call_ride()
    # find_user_id_in_table(20)
    # drop_all_tables()
    conn.close()
    print("")
    print("end main program")
