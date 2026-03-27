from pydantic import BaseModel,Field,field_validator

import datetime

import uuid

from typing import Any, Dict, List,Optional,Tuple,Union

import re

class MaysonPlatformAuth(BaseModel):
    email: str
    password: str
    is_verified: Optional[str]=None
    created_at: datetime.time


class ReadMaysonPlatformAuth(BaseModel):
    email: str
    password: str
    is_verified: Optional[str]=None
    created_at: datetime.time
    class Config:
        from_attributes = True




# Query Parameter Validation Schemas

class GetAgentQueryParams(BaseModel):
    """Query parameter validation for get_agent"""
    prompt: Optional[str] = Field(None)

    class Config:
        populate_by_name = True
