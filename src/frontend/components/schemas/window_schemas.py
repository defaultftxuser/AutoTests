from pydantic import BaseModel


class WindowSizeSchema(BaseModel):
    width: int
    height: int
