from __future__ import print_function

from typing import List

from fastapi import FastAPI, HTTPException, APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

import random
import string
import datetime

from models import Task_Pydantic, TaskIn_Pydantic, Tasks, Question_Pydantic, QuestionIn_Pydantic, Questions, User_Pydantic, UserIn_Pydantic, Users

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


async def google_get_settings():

    SAMPLE_SPREADSHEET_ID = '1gAUVFyP8Dhx8Dh4gj-cvI5NIxCsdWjTDeHErR8nS2mY'
    SAMPLE_RANGE_NAME = 'Settings!A2:C'

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


@router.get("/question/{telegram_id}")
async def get_question(telegram_id: int):
    questions = await Questions.filter(telegram_id=telegram_id).all()
    flag = True
    while flag:
        al = len(questions)
        ri = random.randint(0, al)
        if questions[ri].repeats != 0:
            flag = False
            return questions[ri]



@router.post("/complete")
async def complete_question(question_id: int, answer: str):
    question = await Questions.get(id=question_id)
    task = await Tasks.get(id=question.task_id)
    if task.right_ans == answer:
        qs = {
            'telegram_id': question.telegram_id,
            'task_id': question.task_id,
            'repeats': question.repeats - 1
        }
        await Questions.filter(id=question_id).update(**qs)
        return await Question_Pydantic.from_queryset(Questions.get(id=question_id))
    else:
        return {'correct': 'false'}


@router.get("/get_current_settings")
async def google_init_tasks():
    table_values = await google_get_settings()
    return {'period': table_values[0], 'response': table_values[1], 'repeats': table_values[2]}


@router.get("/google_init_questions")
async def google_init_questions():
    user_values = await User_Pydantic.from_queryset(Users.all())
    settings = await google_get_settings()
    table_values = await Tasks.all()
    for user in user_values:
        for row in table_values:
            question = await Questions.filter(task_id=row.id, telegram_id=user.telegram_id).all()
            if not question:
                qs = {
                    'telegram_id': user.telegram_id,
                    'task_id': table_values.id,
                    'repeats': settings[0][2]
                }
                qs_obj = await Questions.create(**qs)
    return {'status': 'completed'}
