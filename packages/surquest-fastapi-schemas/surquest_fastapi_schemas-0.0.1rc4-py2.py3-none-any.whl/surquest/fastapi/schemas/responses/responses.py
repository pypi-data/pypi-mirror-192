# from pydantic import BaseModel
from .base import Base
from .info import InfoSuccess, InfoWarning, InfoError
from .metadata import Metadata
from typing import Union, List, Dict, Optional


class ResponseSuccess(Base):
    info: InfoSuccess = InfoSuccess()
    meta: Optional[Metadata] = None
    data: Union[List, Dict]


class ResponseWarning(Base):

    info: InfoWarning = InfoWarning()
    meta: Optional[Metadata] = None
    data: Optional[Union[List, Dict]] = None

    @classmethod
    def set(cls, warnings, data):

        return cls(
            info=InfoWarning(warnings=warnings),
            data=data
        )


class ResponseError(Base):
    info: InfoError = InfoError()

    @classmethod
    def set(cls, errors, warnings=[]):
        return cls(
            info=InfoError(
                warnings=warnings,
                errors=errors
            )
        )
