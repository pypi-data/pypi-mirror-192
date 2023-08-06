# from pydantic import BaseModel
from .base import Base
from typing import List
from .status import Status
from .message import Message


class InfoSuccess(Base):
    status: str = Status.success


class InfoWarning(Base):
    status: str = Status.warning
    warnings: List[Message] = []


class InfoError(Base):
    status: str = Status.error
    warnings: List[Message] = []
    errors: List[Message] = []
