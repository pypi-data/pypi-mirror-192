from pydantic import BaseModel

class Base(BaseModel):
    def dict(self, *args, **kwargs):

        if kwargs and kwargs.get("exclude_none") in [None, True]:
            kwargs["exclude_none"] = True

        return BaseModel.dict(self, *args, **kwargs)