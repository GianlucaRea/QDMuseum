from flask import Flask, request, jsonify
import requests
from queue import Queue
from threading import Thread
import random
import datetime
import time

DataVisitor = {
}

DataMuseum = {
"1":{
    "ID":"1",
    "SizeXmax":300,
    "SizeYmax":300,
    "SizeXmin":0,
    "SizeYmin":0,
    "Floors":1,
    "StartX":100,
    "StartY":150
}
}
DataArtwork = {
"1":{
    "ID":"1",
    "Museum":"1",
    "PosX":100,
    "PosY":150,
    "Floor":"1",
    "Room":"1"
},
"2":{
    "ID":"2",
    "Museum":"1",
    "PosX":90,
    "PosY":90,
    "Floor":"1",
    "Room":"1"
},
"3":
{
    "ID":"3",
    "Museum":"1",
    "PosX":30,
    "PosY":120,
    "Floor":"1",
    "Room":"1"
},
"4":{
    "ID":"4",
    "Museum":"1",
    "PosX":50,
    "PosY":20,
    "Floor":"1",
    "Room":"2"
},
"5":{
    "ID":"5",
    "Museum":"1",
    "PosX":150,
    "PosY":20,
    "Floor":"1",
    "Room":"2"
},
"6":
{
    "ID":"6",
    "Museum":"1",
    "PosX":20,
    "PosY":60,
    "Floor":"1",
    "Room":"2"
}
}

'''
Model used
-Visitor
    +ID
    +Museum [Key]
    +PosX [INT]
    +PosY [INT]
    +Floor [INT]

-Artwork
    +ID
    +Museum [Key]
    +PosX [INT]
    +PosY [INT]
    +Floor [INT]

-Museum
    +ID
    +SizeX [INT]
    +SizeY [INT]
    +Floors [INT]
'''

# DATA CRUD


def AddArtwork (art_id, museum_id, posX, posY, fl):
    global DataArtwork
    DataArtwork[art_id] = {"ID":art_id, "Museum":museum_id, "PosX":posX, "PosY":posY, "Floor":fl}


def RemoveArtwork (art_id):
    global DataArtwork
    DataArtwork.pop(art_id)


def AddMuseum (museum_id, s_x, s_y, st_x, st_y, fl):
    global DataMuseum
    DataMuseum[museum_id] = {"ID":museum_id, "SizeX":s_x, "SizeY":s_y, "StartX":st_x, "StartY":st_y, "Floors":fl }


def RemoveMuseum (museum_id):
    global DataMuseum
    DataMuseum.pop(museum_id)


def AddVisitor (user_id, museum_id, start_time):
    global DataVisitor
    DataVisitor[user_id] = {"ID":user_id, "Museum":museum_id, "PosX":DataMuseum[museum_id].get("StartX"), "PosY":DataMuseum[museum_id].get("StartY"), "Floor":"1", "Room":"1", "NearArt":[], "start_time": start_time}


def RemoveVisitor (user_id):
    global DataVisitor
    DataVisitor.pop(user_id)


def Distance(x, y):
    if x >= y:
        result = x - y
    else:
        result = y - x
    return result


def Main():
    global DataVisitor, DataArtwork, DataMuseum, ExitFlag, q
    random.seed(datetime.datetime.now())
    dict_artwork = {}
    while ExitFlag:
        # CORE PART [CYCLED]
        try:
            while not q.empty():
                data = q.get().split("|")
                if data[0] == "track":
                    start_time = time.time()
                    AddVisitor(data[1], data[2], start_time)
                elif data[0] == "untrack":
                    visit_time = int(time.time() - DataVisitor[data[1]]["start_time"])
                    param = {'time': visit_time, 'museum': DataVisitor[data[1]]["Museum"]}
                    response = requests.post(url="http://127.0.0.1:8000/museum/reg_visit", data=param)
                    print(response)
                    RemoveVisitor(data[1])
        except:
            print("No data received")


        for target in DataVisitor:
            # check if previous art near the visitor is still there
            if len(DataVisitor[target]["NearArt"]) > 0:
                for art in DataVisitor[target]["NearArt"]:
                    if DataArtwork[art]["Museum"] == DataVisitor[target]["Museum"] and DataArtwork[art]["Floor"] == DataVisitor[target]["Floor"] and DataArtwork[art]["Room"] == DataVisitor[target]["Room"]:
                        if Distance(DataArtwork[art]["PosX"], DataVisitor[target]["PosX"]) >= 40 or Distance(DataArtwork[art]["PosY"], DataVisitor[target]["PosY"]) >= 40:
                            DataVisitor[target]["NearArt"].remove(art)
                            if dict_artwork[art]["Visitor"] > 2:
                                dict_artwork[art]["Visitor"] = dict_artwork[art]["Visitor"] - 1
                            else:
                                param = {'time': time.time() - dict_artwork[art]['Time'], 'artwork': art}
                                response = requests.post(url="http://127.0.0.1:8000/museum/reg_art_visit", data=param)
                                dict_artwork.pop(art, None)
                    else:
                        print("Prova3")
                        DataVisitor[target]["NearArt"].remove(art)
                        if dict_artwork[art]["Visitor"] > 2:
                            dict_artwork[art]["Visitor"] = dict_artwork[art]["Visitor"] - 1
                        else:
                            param = {'time': time.time() - dict_artwork[art]['Time'], 'artwork': art}
                            response = requests.post(url="http://127.0.0.1:8000/museum/reg_art_visit", data=param)
                            dict_artwork.pop(art, None)

            # check if there is new art near the visitor
            for art in DataArtwork:
                if DataArtwork[art]["Museum"] == DataVisitor[target]["Museum"] and DataArtwork[art]["Floor"] == DataVisitor[target]["Floor"] and DataArtwork[art]["Room"] == DataVisitor[target]["Room"]:
                    if Distance(DataArtwork[art]["PosX"], DataVisitor[target]["PosX"]) <= 40 and Distance(DataArtwork[art]["PosY"], DataVisitor[target]["PosY"]) <= 40:
                        print(art)
                        print(DataVisitor[target]["NearArt"])
                        if not(art in DataVisitor[target]["NearArt"]):
                            print("Test4")
                            DataVisitor[target]["NearArt"].append(art)
                            print(DataVisitor[target]["NearArt"])
                            if (art in dict_artwork):
                                dict_artwork[art]["Visitor"] = dict_artwork[art]["Visitor"] + 1
                            else:
                                dict_artwork[art] = {"Time": time.time(), "Visitor": 1}
            
            # if there is at least one art near the visitor, the movement is slowed
            if len(DataVisitor[target]["NearArt"]) > 0:
                movSpd = 5
            else:
                movSpd = 3

            # make the visitor's movement
            targetMoved = False
            MuseumID = DataVisitor[target]["Museum"]
            direction = random.randint(0, 3)
            while not targetMoved:
                if direction == 0:
                    if DataMuseum[MuseumID]["SizeXmax"] >= DataVisitor[target]["PosX"] + movSpd:
                        DataVisitor[target]["PosX"] += movSpd
                        targetMoved = True
                elif direction == 1:
                    if DataMuseum[MuseumID]["SizeXmax"] >= DataVisitor[target]["PosY"] + movSpd:
                        DataVisitor[target]["PosY"] += movSpd
                        targetMoved = True
                elif direction == 2:
                    if DataMuseum[MuseumID]["SizeXmin"] <= DataVisitor[target]["PosX"] - movSpd:
                        DataVisitor[target]["PosX"] += -movSpd
                        targetMoved = True
                elif direction == 3:
                    if DataMuseum[MuseumID]["SizeXmin"] <= DataVisitor[target]["PosY"] - movSpd:
                        DataVisitor[target]["PosY"] += -movSpd
                        targetMoved = True
                direction = (direction + 1) % 4
            
            direction = random.randint(0, 100)
            if direction > 99:
                DataVisitor[target]["Room"] = str((int(DataVisitor[target]["Room"]) + 1) % 3)
                if DataVisitor[target]["Room"] == "0":
                    DataVisitor[target]["Room"] = "1"
            

        # print("-------------------------------------------------------")
        time.sleep(1)

app = Flask(__name__)
q = Queue()
locService = Thread(target = Main)
ExitFlag = True


@app.route('/userMngtPostman', methods=['POST'])
def visitorManagerPost():
    # Check the request and do on MainFrame
    req_opr = request.form.get('operation')
    req_trg = request.form.get('target')
    req_mus = request.form.get('museum')
    q.put(req_opr + "|" + req_trg + "|" + req_mus)
    return "Visitor Tracked"


@app.route('/userMngt', methods=['POST'])
def visitorManager():
    # Check the request and do on MainFram
    req_opr = request.json['operation']
    req_trg = str(request.json['target'])
    if req_opr == "track":
        req_mus = request.json['museum']
        q.put(req_opr + "|" + req_trg + "|" + req_mus)
    else:
        print(req_opr)
        q.put(req_opr + "|" + req_trg)
    return "Visitor Tracked"


@app.route('/userPos', methods=['POST'])
def visitorPosition():
    global DataVisitor
    DataCollection = []
    # Check the request and do on MainFrame
    req_target = request.json['target']
    print (req_target)
    print (DataVisitor)
    if req_target == "ALL":
        req_floor = request.json['floor']
        req_museum = request.json['museum']
        for target in DataVisitor:
            if DataVisitor[target]["Museum"] == req_museum and DataVisitor[target]["Floor"] == req_floor:
                DataCollection.append({"ID":DataVisitor[target]["ID"], "PosX":DataVisitor[target]["PosX"], "PosY":DataVisitor[target]["PosY"], "Floor":DataVisitor[target]["Floor"],"Room":DataVisitor[target]["Room"], "NearArt":DataVisitor[target]["NearArt"]})
    else:
        DataCollection = DataVisitor[str(req_target)]
    return jsonify(DataCollection)


@app.route('/start', methods=['GET'])
def StartService():
    global locService, ExitFlag
    ExitFlag = True
    locService = Thread(target = Main)
    locService.start()
    return "Service Started"


@app.route('/stop', methods=['GET'])
def StopService():
    global locService, ExitFlag
    ExitFlag = False
    locService.join()
    return "Service Stopped"
  

if __name__ == '__main__':
    ExitFlag = True
    locService = Thread(target=Main)
    locService.start()
    app.run(port=5050, debug=False)