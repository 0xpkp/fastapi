# importing mongodb.py script
import mongodb

from fastapi import FastAPI, Path, Query, HTTPException, Security
from typing import Optional
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

# modulees for API authentication
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

# to convert pymongo output to pydantic JSON
from uuid import UUID, uuid4

# initializing api module
app = FastAPI()

# base model to convert dictionary to pydantic model


class Model_for_readdata(BaseModel):

    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    ip_address: Optional[str] = None

# base model to validate user data


class Model_for_writedata(BaseModel):

    first_name: str
    last_name: str
    email: str
    gender: str
    ip_address: str


# api endpoint to read data
@app.get('/get-item/{item_id}')
def get_Data(apikey: str, item_id: int):

    if mongodb.authenticate_apikeys(apikey) == "invalid":
        raise HTTPException(status_code=403, detail="invalid API key")

    item = mongodb.read_dataset(item_id)
    item = Model_for_readdata.parse_obj(item)
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="resource not found")

# api endpoint to write data


@app.post('/post-item/')
def create_data(apikey: str, item: Model_for_writedata):
    
    if mongodb.authenticate_apikeys(apikey) == "invalid":
        raise HTTPException(status_code=403, detail="invalid API key")

    
    response = mongodb.write_dataset(first_name=item.first_name, last_name=item.last_name,
                                     email=item.email, gender=item.gender, ip_address=item.ip_address)
    return {'Success': 'data updated to the server'}
