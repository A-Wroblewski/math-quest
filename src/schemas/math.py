from pydantic import BaseModel


class EquationBase(BaseModel):
    equation: str
    result: int


class EquationResponse(EquationBase):
    pass
