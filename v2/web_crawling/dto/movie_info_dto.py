from pydantic import BaseModel, Field
from common.theater_enum import Theater

class MovieInfoDto(BaseModel):
    movie_title: str = Field(frozen=True)
    movie_date: str = Field(frozen=True)
    theater: Theater = Field(frozen=True)

    class Config:
        use_enum_values = True