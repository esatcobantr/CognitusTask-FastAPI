from fastapi import FastAPI
from algorithm import train_service, prediction_service
from pydantic import BaseModel


cognitus = FastAPI()


class RequestAlgorithmModel(BaseModel):
    text: str


@cognitus.post("/train")
def train():
    train_service.delay()
    return {'status': 'True'}


@cognitus.post('/prediction')
def prediction(items: RequestAlgorithmModel):
    result = prediction_service(items.text)
    return {'result': result}