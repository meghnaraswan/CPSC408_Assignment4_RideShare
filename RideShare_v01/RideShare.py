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
    Hello! Are you a new or returningr? \n 
    1) New User \n
    2) Returning User \n
    ''') 
    choice = get_choice([1, 2])
    if choice == 1:
        new_user_info()
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

def new_user_info():
    userID = ""
    isDriver = None

    userID = input("Please enter your ID: ")
    while userID.isdigit() == False:
        userID = input("Invalid ID. Please enter your ID again: ")

    isDriver = set_is_driver(userID, isDriver)

    # selectIsDriver = "SELECT IsDriver FROM Users WHERE UserID = '" + str(userID) + "';"
    # isDriver = cur_obj.execute(selectIsDriver)

    if isDriver == 1:
        set_is_driver_active(userID)
    else:
        rider_choice(userID)
    
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

def set_is_driver_active(userID):
    print('''
    Hi Driver! Are you active currently? \n 
    1) Yes, I am active \n
    2) No, I am not active \n
    ''') 
    choice = get_choice([1, 2])
    if choice == 1:
        updateActive = "UPDATE Drivers SET IsActive = 1 WHERE DriverID = '" + str(userID) + "';"
        cur_obj.execute(updateActive)
        conn.commit()
    elif choice == 2:
        updateNotActive = "UPDATE Drivers SET IsActive = 0 WHERE DriverID = '" + str(userID) + "';"
        cur_obj.execute(updateNotActive)
        conn.commit()

def rider_choice(userID):
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
    user_info()
    # drop_all_tables()
    conn.close()
    print("end main program")
