from __future__ import print_function

from typing import List

from fastapi import FastAPI, HTTPException, APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

import random
import string
import datetime

from models import Task_Pydantic, TaskIn_Pydantic, Tasks

router = APIRouter()


class Status(BaseModel):
    message: str


import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


async def google_get_tasks():

    SAMPLE_SPREADSHEET_ID = '1gAUVFyP8Dhx8Dh4gj-cvI5NIxCsdWjTDeHErR8nS2mY'
    SAMPLE_RANGE_NAME = 'Tasks!A2:F'

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds, cache_discovery=False)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    return values


@router.get("/", response_model=List[Task_Pydantic])
async def get_tasks():
    return await Task_Pydantic.from_queryset(Tasks.all())

@router.get("/{task_id}", response_model=Task_Pydantic)
async def get_task(task_id: int):
    return await Tasks.get(id=task_id)


@router.get("/google_init_tasks")
async def google_init_tasks():
    table_values = await google_get_tasks()
    for row in table_values:
        if row[5] == 'Активно':
            task = await Tasks.filter(question=row[2]).all()
            if not task:
                tk = {
                    'theme': row[0],
                    'link_theme': row[1],
                    'question': row[2],
                    'right_ans': row[3],
                    'feedback': row[4]
                }
                tk_obj = await Tasks.create(**tk)
        if row[5] == 'Неактивно':
            task = await Tasks.get(question=row[2])
            if task:
                deleted_count = await Tasks.filter(question=row[2]).delete()
    return {'status': 'completed'}