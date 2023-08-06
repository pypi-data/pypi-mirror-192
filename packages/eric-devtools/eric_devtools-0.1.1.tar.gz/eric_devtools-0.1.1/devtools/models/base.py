from pydantic import BaseModel


class Model(BaseModel):
    def serialize(self):
        return self.dict(by_alias=True)

    class Config:
        frozen = True
        orm_mode = True
