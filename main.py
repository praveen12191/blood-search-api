from mongoengine.document import Document
from mongoengine import connect
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import FastAPI
import certifi
from mongoengine.fields import StringField
username = input("your_username")
password = input("your_password")
default_connection = connect(db='bloodsearch', host="mongodb+srv://{username}:{password}@cluster0.4ygvrqb.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())

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
    # val = {"places":['Tiruppur','tioe','CBE','Erode']}
    val =['TIRUPPUR','SALEM','CBE','ERODE']
    return val

@app.get('/groupDetails')
def group():
    val = ['A +ve','A -ve','B +ve','B -ve','O +ve','O -ve']
    return val 

@app.post('/postData')
def post(value : Filter):
    datas = Patients.objects.filter(place=value.place,group=value.group)
    print(datas)
    return returndata(datas)


@app.post('/check')
def check(value : Check):
    name,pin = value.id['name'],value.pin
    print(value.id)
    res = {
        "group": value.id['group'],
        "place": value.id['place']
    }
    val = Patients.objects.filter(name=name,patient_id=pin)
    if(val):
        val.delete()
        return JSONResponse(content=res,status_code=200)
    else:
        return JSONResponse(content=1,status_code=201)