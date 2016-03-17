from tornado import Server
import TemplateAPI
from random import randint
import json

def dummy():
    print "Started"


def indexPage(response):
    response.write(TemplateAPI.render('Main_Page.html', response, {}))

def randPage(response):
    response.write(str(rangen()))

def rangen():
    return randint(0, 10)
    
def inputPage(response):    
    response.write(TemplateAPI.render('input.html', response, {}))

def displayAllPage(response):
    name = response.get_field("name")
    password = response.get_field("password")
    if name == None or password == None:
        is_Valid = False
    else:
        is_Valid = get_user(name, password)
    response.write(TemplateAPI.render('Track_Database.html', response, {'name': name, 'password': password, 'is_Valid':is_Valid}))

def displayMapPage(response):
    name = response.get_field("name")
    password = response.get_field("password")
    if name == None or password == None:
        is_Valid = False
    else:
        is_Valid = get_user(name, password)
    response.write(TemplateAPI.render('Track_Map.html', response, {'name': name, 'password': password, 'is_Valid':is_Valid}))
    
def aboutPage(response):    
    response.write(TemplateAPI.render('About.html', response, {}))


def inputHandler(response):
    uuid = response.get_field("uuid")
    latitude = response.get_field("latitude")
    longitude = response.get_field("longitude")
    
    insertPositions(uuid, latitude, longitude)

def insertAssignments(response):
    uuid = response.get_field("uuid")
    pas = response.get_field("pass")
    name = response.get_field("name")
    typ = response.get_field("typ")

    cur = con.cursor()
    cur.execute("""
INSERT OR REPLACE INTO Assignments (UUID, IsVehicle, Name) 
  VALUES (  ?, 
            ?,
            ?
          );
    """, (uuid, typ == "1", name,))
    con.commit()
    cur.close()
    response.redirect("/assignments")

def showAllDebugPage(response):
    data = getLocations(100)
    response.write(TemplateAPI.render('display.html', response, {'data': data}))
    print(data)

def getAssignments():
    cur = con.cursor()
    cur.execute("SELECT UUID, IsVehicle, Name FROM Assignments ORDER BY UUID asc")
    data = cur.fetchall()
    return data


def getAssignmentsPageHandler(response):
    assignments = getAssignments()
    response.write(TemplateAPI.render('Manage_Assignments.html', response, {'assignments': assignments}))


def getLatestHandler(response):
    data = getLatestForEach()
    output = []
    for uuidData in data:
        o = list(uuidData)
        cur = con.cursor()
        cur.execute("SELECT Name, IsVehicle FROM Assignments WHERE UUID = ?", (str(uuidData[0]),))
	res = cur.fetchone()
        if res == None:
            res = ('No Assignment', False)
        cur.close()
        o.append(res[0])
        o.append(res[1])
        output.append(o)
    response.write(json.dumps(output))
    
#--------------------------------------User_Data--------------------------------------    
    
users = [line for line in open("users.txt")]  
user_dict = {}
for user in users:
    UUID = user.split(":")[0]
    Username = user.split(":")[1].split(",")[0]
    Password = user.split(":")[1].split(",")[1].strip()
    user_dict[UUID] = Username + "," + Password
    
def get_user(name, password):
    result = None
    for user in user_dict.keys():
        u_name = user_dict[user].split(",")[0]
        u_password = user_dict[user].split(",")[1]
        if str(name + " " + password) == str(u_name + " " + u_password):
            result = True
            break
    if result == None:
        return False
    else:
        return True

def make_user(input_name, input_password):
    UUID = int(len(user_dict.keys())) + 1
    user_dict[UUID] = input_name + "," + input_password
    with open("users.txt", "a") as file:
        file.write("\n" + str(UUID) + ":" + input_name + "," + input_password)
#-------------------------------------------------------------------------------------    



#--------------------------------Database Interaction--------------------------------- 
import sqlite3 as lite
import sys
import time

con = lite.connect('positions.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Positions (UUID int, Lat float, Lon float, Time timestamp)")
cur.execute("CREATE INDEX IF NOT EXISTS PositionTime ON Positions (Time)")
cur.execute("CREATE INDEX IF NOT EXISTS PositionUUID ON Positions (UUID)")
cur.execute("CREATE INDEX IF NOT EXISTS PositionCombo ON Positions (Time, UUID)")
cur.execute("CREATE TABLE IF NOT EXISTS Assignments (UUID INTEGER PRIMARY KEY, IsVehicle BOOLEAN, Name varchar(255))")

con.commit()
cur.close()


def getTime():
	raw = str(datetime.now())
	datelist = []
	datelist.append(str(raw.split(" ")[1].split(".")[0]))
	datelist.append(str(raw.split(" ")[0].split("-")[2] + "-" + raw.split(" ")[0].split("-")[1]+ "-" + raw.split(" ")[0].split("-")[0]))
	return datelist


def insertPositions(UUID, Lat, Lon):
    Time = int(time.time())
    
    cur = con.cursor()
    cur.execute("INSERT INTO Positions (UUID, Lat, Lon, Time) VALUES (?, ?, ?, ?)", (UUID, Lat, Lon, Time))
    con.commit()
    cur.close()



def queryPositions():
    cur = con.cursor()
    cur.execute("SELECT UUID, Lat, Lon, Time FROM Positions")
    data = cur.fetchall()
    print(data)

def getLocations(limit):
    cur = con.cursor()
    cur.execute("SELECT UUID, Lat, Lon, Time FROM Positions ORDER BY Time desc LIMIT ?", (str(limit),))
    data = cur.fetchall()
    cur.close()
    return data

def getLatestForEach():
    cur = con.cursor()
    cur.execute("SELECT UUID, Lat, Lon, MAX(TIME) FROM Positions GROUP BY UUID")
    data = cur.fetchall()
    cur.close()
    return data
#------------------------------------------------------------------------------------- 

    

#------------------------------Page Links---------------------------------------------
    
    
    
server = Server('0.0.0.0', 80)
server.register("/", indexPage)
server.register("/about", aboutPage)
server.register("/random", randPage)
server.register("/input", inputPage)
server.register("/all", showAllDebugPage)
server.register("/location/push", inputHandler)
server.register("/location/get/all", getLatestHandler)
server.register("/track_database", displayAllPage)
server.register("/track_map",displayMapPage)
server.register("/assignments", getAssignmentsPageHandler)
server.register("/ass/new", insertAssignments)
server.run(dummy)
