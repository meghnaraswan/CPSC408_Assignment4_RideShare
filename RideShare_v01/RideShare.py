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

    userID = int(userID)

    isDriver = set_is_driver(userID, isDriver)

    # selectIsDriver = "SELECT IsDriver FROM Users WHERE UserID = '" + str(userID) + "';"
    # isDriver = cur_obj.execute(selectIsDriver)

    if isDriver == 1:
        new_driver_choice(userID)
    else:
        create_rider(userID)
        new_rider_choice(userID)

def old_user_info():
    return
    
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
        (userID, isActive),
        ]
        cur_obj.executemany(insertDriversQuery, driversValues)
        conn.commit()

        # updateActive = "UPDATE Drivers SET IsActive = 1 WHERE DriverID = '" + str(userID) + "';"
        # cur_obj.execute(updateActive)
        # conn.commit()

    elif choice == 2:

        insertDriversQuery = '''
        INSERT INTO Drivers (DriverID, IsActive)
        VALUES(%s, %s);
        '''
        driversValues = [
        (userID, isNotActive),
        ]
        cur_obj.executemany(insertDriversQuery, driversValues)
        conn.commit()

        # updateNotActive = "UPDATE Drivers SET IsActive = 0 WHERE DriverID = '" + str(userID) + "';"
        # cur_obj.execute(updateNotActive)
        # conn.commit()

def create_rider(userID):
    insertRidersQuery = '''
    INSERT INTO Riders (RiderID)
    VALUES(%s, %s);
    '''
    ridersValues = [
    (userID, 'NULL'),
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
        print("call ride")
        new_user_call_ride(userID)
    elif choice == 2:
        print("exit")
        # rate_My_Driver(userID)

def new_user_call_ride(userID):
    pickUpLoc = input("Please type your Pick Up Location")
    dropOffLoc = input("Please type your Drop Off Location")
    # sql2 = "UPDATE Rides SET PickUpAddress = " + pickUpLoc + ", DropOffAddress = " + dropOffLoc + " WHERE RiderID = '" + str(riderID) + "';"

def returning_rider_choice():
    print('''
    Hi Rider! What would you like to do? \n 
    1) Call a ride \n
    2) Rate my driver \n
    ''') 
    choice = get_choice([1, 2])
    if choice == 1:
        print("choice 1")
        # call_Ride(userID)
    elif choice == 2:
        print("choice 2")
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
    # drop_all_tables()
    conn.close()
    print("end main program")
