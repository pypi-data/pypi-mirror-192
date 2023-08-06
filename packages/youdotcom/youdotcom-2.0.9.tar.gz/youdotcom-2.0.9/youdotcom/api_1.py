from fastapi import FastAPI
import asyncio
import json
import os
import platform
import re
import subprocess
import time
import urllib.parse
import uvicorn
import cloudscraper
import markdownify
import undetected_chromedriver as uc
import urllib3
from pyvirtualdisplay import Display
from ratelimit import limits
from selenium.common import exceptions as SeleniumExceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from gtts import gTTS
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request
from fastapi.responses import FileResponse
from io import BytesIO
import string
from api_analytics.fastapi import Analytics
import traceback
import requests
import random
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from youdotcom import Webdriver
from starlette.responses import PlainTextResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from PIL import Image
from typing import Optional, Any
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_queue import DistributedTaskApplyManager
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import aioredis

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
redis = aioredis.Redis.from_url("redis://localhost")
origins = ["*"]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "expected": "http://localhost/chat?message=YOURMESSAGE",
                "info": "more info and code can be found on the main page: https://betterapi.net/",
            }
        ),
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def get_response(success_status: bool, result: Any) -> JSONResponse | dict:
    if success_status:
        return result
    if result == -1:
        return JSONResponse(status_code=503, content=f"Service Temporarily Unavailable")
    else:
        return JSONResponse(status_code=500, content=f"Internal Server Error")


@app.get("/chat")
@limiter.limit("15/minute")
async def YouChat(request: Request, message, contextid=""):
    success_status: bool = False
    try:
        async with DistributedTaskApplyManager(
            redis=redis,
            request_path=request.url.path,
        ) as dtmanager:
            if not dtmanager.success():
                return JSONResponse(
                    status_code=503,
                    content="Service Temporarily Unavailable, please note that the api is still in dev.",
                )
            ip = request.headers.get("cf-connecting-ip")
            url = str(request.url)
            success_status, result = await dtmanager.rclt(
                form_data={
                    "message": message,
                    "contextid": contextid,
                    "ip": ip,
                    "url": url,
                },
                task_level=0,
            )
        return get_response(success_status, result)
    except aioredis.exceptions.ResponseError:
        return {"error": "backend server not running. use: from youdotcom import backend | backend.run() (| repersenting a new line)"}

@app.get("/")
async def main():
    response = RedirectResponse(url='/redoc')
    return response

ip="0.0.0.0"
port=80


try:
    uvicorn.run(app, host=ip, port=port)
except:
    print(traceback.format_exc())
        
