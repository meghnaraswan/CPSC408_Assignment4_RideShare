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
        RiderID INT NOT NULL PRIMARY KEY
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

def insert_users_data():
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

def insert_riders_data():
    insertRidersQuery = '''
    INSERT INTO Riders (RiderID)
    VALUES(%s);
    '''
    ridersValues = [
    (1),
    (3)
    ]
    cur_obj.executemany(insertRidersQuery, ridersValues)
    conn.commit()

def insert_drivers_data():
    insertDriversQuery = '''
    INSERT INTO Drivers (DriverID, Rating, IsActive)
    VALUES(%s, %s, %s);
    '''
    driversValues = [
    (2, 4.8, 1),
    (4, 1.7, 0),
    (5, 3.5, 1),
    ]
    cur_obj.executemany(insertDriversQuery, driversValues)
    conn.commit()

def insert_rides_data():
    insertRidesQuery = '''
    INSERT INTO Rides (RideID, RiderID, DriverID, PickUpLoc, DropOffLoc)
    VALUES(%s, %s, %s, %s, %s);
    '''
    ridesValues = [
    (1, 1, 2, 'Chapman University', 'UCLA'),
    (3, 3, 5, 'Angels Stadium', 'Irvine Spectrum'),
    ]
    cur_obj.executemany(insertRidesQuery, ridesValues)
    conn.commit()

def insert_data():
    #insert data
    insertUsersQuery = '''
    INSERT INTO Users
    VALUES(%s, %s);
    '''
    usersValues = [
    (1, 'false'),
    (2, 'true'),
    (3, 'false'),
    (4, 'true'),
    (5, 'true'),
    ]

    insertRidersQuery = '''
    INSERT INTO Riders
    VALUES(%s);
    '''
    ridersValues = [
    (1),
    (3),
    ]

    insertDriversQuery = '''
    INSERT INTO Drivers
    VALUES(%s, %s, %s);
    '''
    driversValues = [
    (2, 4.8, 'true'),
    (4, 1.7, 'false'),
    (5, 3.5, 'true'),
    ]

    insertRidesQuery = '''
    INSERT INTO Rides
    VALUES(%s, %s, %s, %s, %s);
    '''
    ridesValues = [
    (1, 1, 2, 'Chapman University', 'UCLA'),
    (3, 3, 5, 'Angels Stadium', 'Irvine Spectrum'),
    ]

    cur_obj.executemany(insertUsersQuery, usersValues)
    conn.commit()
    cur_obj.executemany(insertRidersQuery, ridersValues)
    conn.commit()
    cur_obj.executemany(insertDriversQuery, driversValues)
    conn.commit()
    cur_obj.executemany(insertRidesQuery, ridesValues)
    conn.commit()

#main program
if __name__ == "__main__":
    print("start main program")
    # initial_create()
    # print_to_verify()
    # create()
    # insert_data()
    # insert_users_data()
    # insert_riders_data()
    # insert_drivers_data()
    # insert_rides_data()
    print("end main program")
