import uvicorn
import pymongo
import sys
import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime, time, timedelta
from bson import ObjectId
from typing import Optional, List
import boto3
import json

import motor.motor_asyncio

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://pragma:pragma123@copapragmadb.cluster-cpoxrljke2qk.us-east-1.docdb.amazonaws.com:27017/?retryWrites=false")
db = client.mapa_crecimiento

def enviar_mensaje_sqs(Message={}):
    sqs = boto3.resource("sqs", region_name="us-east-1")
    data = json.dumps(Message)
    response = sqs.queue.send_message(MessageBody=data)
    return response

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class chapterModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    id_chapter: str 
    nombre: str
    descripcion: str
    knowledge_center: str 

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id_chapter" : "14", 
                "nombre" : "Frontend", 
                "descripcion" : "Desarrollo Frontend", 
                "knowledge_center" : "Ciencias de la Computación"
            }
        }

class learnresourceModel(BaseModel):
    #id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    id_pragma_power: int
    nombre: str
    descripcion: str
    valor: float
    recurso: str
    plataforma: str
    link : str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id_pragma_power": 330,
                "nombre": "Protocolos",
                "descripcion": "Es capaz de consumir un servicio utilizando protocolos tcp",
                "valor": 3.0,
                "recurso": "REST API Automation:REST Assured,Serenity BDD Framework",
                "plataforma":"Udemy",
                "link":"https://www.udemy.com/course/rest-api-automation-with-rest-assuredserenity-bdd-framework/" 
                
            }
        }

class pragmapowersModel(BaseModel):
    #id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    id: int
    nombre: str
    descripcion: str
    valor: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
            "id": 250,
            "nombre": "Metodologias Desarrollo",
            "descripcion": "Tiene comprensión conceptual y aplica estrategías de desarrollo BDD o TDD",
            "valor": 4                 
            }
        }

class pragmalevelModel(BaseModel):
    #id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    id_seniority: int
    seniority: str
    nivel: str
    score_total: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {                
                "id_seniority": 30,
                "seniority": "Advanced",
                "nivel": "L3",
                "score_total": 3.5                             
            }
        }
        

class recommendationModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    id_pragmatico: EmailStr
    id_plan_carrera: str
    id_valoracion: str
    fecha_creacion: str
    creado_por: str
    fecha_modificacion:str
    modificado_por:str   
    descripcion_plan: str
    recursos_aprendizaje : List[learnresourceModel]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id_pragmatico":"pragma@pragma.com.co",
                "id_plan_carrera":1000,
                "id_valoracion":"V000014581",
                "fecha_creacion":"datetime.datetime.now()",
                "creado_por":"pepe.gomez@pragma.com.co",
                "recursos_aprendizaje":[
                {
                    "id_pragma_power":330,
                    "nombre":"Protocolos",
                    "descripcion":"Es capaz de consumir un servicio utilizando REST y un protocolo de aplicacion adicional (STOMP, RSocket, gRPC o SOAP), entendiendo las caracteristicas del protocolo, estructura de los mensajes y modelo de procesado.",
                    "valor":3,
                    "recurso":"REST API Automation:REST Assured,Serenity BDD Framework",
                    "plataforma":"Udemy",
                    "link":"https://www.udemy.com/course/rest-api-automation-with-rest-assuredserenity-bdd-framework/"
                },
                {
                    "id_pragma_power":210,
                    "nombre":"Frameworks",
                    "descripcion":"Conoce en profundidad 1 Framework sobre su lenguaje de programacion primario, lo que le permite escribir codigo mas claro y menor boilerplate. (Seguridad, ORM y Programacion Orientada a Aspectos)",
                    "valor":3,
                    "recurso":"Universidad Spring - Spring Framework y Spring Boot!",
                    "plataforma":"Udemy",
                    "link":"https://www.udemy.com/course/universidad-spring-framework-springboot-java-security-rest-webservices/"
                }
            ]
        }
    }

class valorationModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")    
    id_valoracion: str
    fecha: str
    id_pragmatico: str
    id_rol: int
    rol: str
    pragma_powers: List[pragmapowersModel] 
    pragma_level:pragmalevelModel

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id_valoracion": "V000014581",
                "fecha": "10/01/2023 09:12:45",
                "id_pragmatico": "xxxx@pragma.com.co",
                "id_rol": 1000,
                "rol": "Backend",
                "pragma_powers": [
                    {
                        "id": 330,
                        "nombre": "Protocolos",
                        "descripcion": "Es capaz de consumir un servicio utilizando REST y un protocolo de aplicacion adicional (STOMP, RSocket, gRPC o SOAP), entendiendo las caracteristicas del protocolo, estructura de los mensajes y modelo de procesado.",
                        "valor": 3
                    },
                    {
                        "id": 210,
                        "nombre": "Frameworks",
                        "descripcion": "Conoce en profundidad 1 Framework sobre su lenguaje de programacion primario, lo que le permite escribir codigo mas claro y menor boilerplate. (Seguridad, ORM y Programacion Orientada a Aspectos)",
                        "valor": 3
                    },
                    {
                        "id": 40,
                        "nombre": "Bases de Datos",
                        "descripcion": "Puede realizar cualquier operacion de SQL usando DML, TCL, DQL, DDL en bases de datos relacionales",
                        "valor": 5
                    },
                    {
                        "id": 260,
                        "nombre": "No SQL",
                        "descripcion": "Conoce las principales caracteristicas de las bases de datos NoSQL y sabe cuando usar SQL o No SQL.",
                        "valor": 3
                    },
                    {
                        "id": 250,
                        "nombre": "Metodologias Desarrollo",
                        "descripcion": "Tiene comprensión conceptual y aplica estrategías de desarrollo BDD o TDD",
                        "valor": 4
                    },
                    {
                        "id": 150,
                        "nombre": "Documentacion",
                        "descripcion": "Sabe documentar las APIs usando al menos uno de los lenguajes de descripcion (OpenAPI, RAML, AsyncAPI, API Blueprint)",
                        "valor": 2
                    },
                    {
                        "id": 340,
                        "nombre": "SDLC",
                        "descripcion": "Conoce las caracteristicas basicas del Dependency Manager y Build Automation de su lenguaje de programación primario y las integra con el proceso DevOps dentro del proyecto.",
                        "valor": 3
                    }
                ],
                "pragma_level": {
                    "id_seniority": 30,
                    "seniority": "Advanced",
                    "nivel": "L3",
                    "score_total": 3.5
                }
            
            }
                
    }

@app.get("/")
def read_root():
    return {"Copa Pragma": "Mapa de Crecimiento"}
    
@app.post("/chapter", response_description="Add new chapter", response_model=chapterModel)
async def create_chapter(chapter: chapterModel = Body(...)):
    
    chapter = jsonable_encoder(chapter)
    new_chapter = await db["chapter"].insert_one(chapter)
    created_chapter = await db["chapter"].find_one({"_id": new_chapter.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_chapter)


@app.post("/recomendacion", response_description="Add new recommendation", response_model=recommendationModel)
async def create_recommendation(recommendation: recommendationModel = Body(...)):
    
    recommendation = jsonable_encoder(recommendation)
    new_recommendation = await db["recomendaciones"].insert_one(recommendation)
    created_recommendation = await db["recomendaciones"].find_one({"_id": new_recommendation.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_recommendation)
    
@app.post("/valoracion", response_description="Add new valoration", response_model=valorationModel)
async def create_valoration(valoration: valorationModel = Body(...)):
    
    sqs_client =  boto3.resource(
        'sqs',
        region_name='us-east-1'
    )
    
    #almaacena valoracion en documentdb
    valoration = jsonable_encoder(valoration)
    new_valoration = await db["valoraciones"].insert_one(valoration)
    created_recommendation = await db["valoraciones"].find_one({"_id": new_valoration.inserted_id})

    #message = {"Copa Pragma": "Ganador Equipo 10"}
    Qname = sqs_client.get_queue_by_name(QueueName="valorationQueue")
    valoracion = {
        "id_valoracion": "V000014581",
        "fecha": "10/01/2023 09:12:45",
        "id_pragmatico": "xxxx@pragma.com.co",
        "id_rol": 1000,
        "rol": "Backend",
        "pragma_powers": [
            {
                "id": 330,
                "nombre": "Protocolos",
                "descripcion": "Es capaz de consumir un servicio utilizando REST y un protocolo de aplicacion adicional (STOMP, RSocket, gRPC o SOAP), entendiendo las caracteristicas del protocolo, estructura de los mensajes y modelo de procesado.",
                "valor": 3
            },
            {
                "id": 210,
                "nombre": "Frameworks",
                "descripcion": "Conoce en profundidad 1 Framework sobre su lenguaje de programacion primario, lo que le permite escribir codigo mas claro y menor boilerplate. (Seguridad, ORM y Programacion Orientada a Aspectos)",
                "valor": 3
            },
            {
                "id": 40,
                "nombre": "Bases de Datos",
                "descripcion": "Puede realizar cualquier operacion de SQL usando DML, TCL, DQL, DDL en bases de datos relacionales",
                "valor": 5
            },
            {
                "id": 260,
                "nombre": "No SQL",
                "descripcion": "Conoce las principales caracteristicas de las bases de datos NoSQL y sabe cuando usar SQL o No SQL.",
                "valor": 3
            },
            {
                "id": 250,
                "nombre": "Metodologias Desarrollo",
                "descripcion": "Tiene comprensión conceptual y aplica estrategías de desarrollo BDD o TDD",
                "valor": 4
            },
            {
                "id": 150,
                "nombre": "Documentacion",
                "descripcion": "Sabe documentar las APIs usando al menos uno de los lenguajes de descripcion (OpenAPI, RAML, AsyncAPI, API Blueprint)",
                "valor": 2
            },
            {
                "id": 340,
                "nombre": "SDLC",
                "descripcion": "Conoce las caracteristicas basicas del Dependency Manager y Build Automation de su lenguaje de programación primario y las integra con el proceso DevOps dentro del proyecto.",
                "valor": 3
            },
        ],
        "pragma_level": {
            "id_seniority": 30,
            "seniority": "Advanced",
            "nivel": "L3",
            "score_total": 3.5
        }
    }

    response = Qname.send_message(MessageBody=json.dumps(valoration))
    print(response)
    
    #return response
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_recommendation)