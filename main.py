
# # from pymongo.mongo_client import MongoClient
# # from pymongo.server_api import ServerApi
# # from fastapi import FastAPI
# # import certifi
# # from mongoengine import Document, StringField, IntField
# # from pydantic import BaseModel

# # app = FastAPI()

# # # from sqlalchemy import create_engine

# # # CONNSTR = 'postgresql://praveen.rcse2020:X6ZQj2uhJCKH@ep-dry-glade-690954.us-east-2.aws.neon.tech/bloodsearch'
# # # try:
# # #     engine = create_engine(CONNSTR)
# # # except Exception as e :
# # #     print("Exception: ",e)
# # uri = "mongodb+srv://praveen:qwerty1234@cluster0.4ygvrqb.mongodb.net/?retryWrites=true&w=majority"

# # # Create a new client and connect to the server 
# # client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())

# # # Send a ping to confirm a successful connection
# # try:
# #     client.admin.command('ping')
# #     print("Pinged your deployment. You successfully connected to MongoDB!")
# # except Exception as e:
# #     print(e)
# # class Add(Document):
# #     name = StringField(required=True)

# # class Added(BaseModel):
# #     name: str

# # @app.post('/add')
# # async def add(value: Added):
# #     obj = Add(name=value.name)
# #     obj.save()
# #     return
# from mongoengine import connect
# from mongoengine.document import Document
# from mongoengine.fields import StringField
# from pydantic import BaseModel
# from fastapi import FastAPI
# import certifi

# # Establish a default connection
# default_connection = connect(db='bloodsearch', host="mongodb+srv://praveen:qwerty1234@cluster0.4ygvrqb.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())

# class Add(Document):
#     name = StringField(required=True)

# class Added(BaseModel):
#     name: str

# app = FastAPI()

# @app.post('/add')
# async def add(value: Added):
#     obj = Add(name=value.name)
#     obj.save()
#     return







from mongoengine.document import Document
from mongoengine import connect
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import FastAPI
import certifi
from mongoengine.fields import StringField

# Establish a default connection
default_connection = connect(db='bloodsearch', host="mongodb+srv://praveen:qwerty1234@cluster0.4ygvrqb.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Patients(Document):
    name = StringField(required=True)
    age = StringField(required=True)
    group = StringField(required=True)
    place = StringField(required=True)
    phone = StringField(required=True)
    patient_id = StringField(required=True)

class PatientsDetails(BaseModel):
    name: str
    age : str
    group : str 
    place : str 
    phone : str 
    id : str 

class Filter(BaseModel):
    place : str 
    group : str 

class Check(BaseModel):
    id  : object
    pin : str 


detail=[]
class Fun(Document):
    name : StringField(required=True)

class Funed(BaseModel):
    name : str 

@app.post('/pos')
def funn(val:Funed):
    obj = Fun(name=val.name)
    obj.save()
    return 

@app.get('/place')
def place():
    val = {'Tiruppur':'tioe','CBE':'Erode'}
    return val


@app.post('/post')
def details(patient: PatientsDetails):
    new_patient = Patients(
        name=patient.name,
        age=patient.age,
        group=patient.group,
        place=patient.place,
        phone=patient.phone,
        patient_id=patient.id,
    )
    new_patient.save()

    val = dict()
    for j in patient:
        val[j[0]] = j[1]
    detail.append(val)
    return detail
def returndata(datas):
    val = []
    for i in datas:
        val.append({'name':i.name,'age':i.age,'group':i.group,'place':i.place,'phone':i.phone,'id':i.patient_id})
    print(val)
    return val

@app.get('/getData')
def returnData():
    datas = Patients.objects.all()
    return returndata(datas)

@app.get('/placeDetails')
def place():
    place = []
    for i in detail:
        if(i['place'] not in place):
            place.append(i['place'])
    return place

@app.post('/postData')
def post(value : Filter):
    datas = Patients.objects.filter(place=value.place,group=value.group)
    return returndata(datas)


@app.post('/check')
def check(value : Check):
    name,pin = value.id['name'],value.pin
    val = Patients.objects.filter(name=name,patient_id=pin)
    if(val):
        val.delete()
        return JSONResponse(content=1,status_code=200)
    else:
        return JSONResponse(content=1,status_code=201)
