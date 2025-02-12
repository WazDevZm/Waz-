import json
import datetime as dt
from typing import Union

from pydantic import BaseModel

from fastapi import FastAPI, HTTPException, Depends
from fastapi.requests import Request

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = ""



engine =create_engine(DATABASE)
