#!/usr/bin/env python3

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

def find_next_id():
    return max(country.country for country in countries) +1

class Country(BaseModel):
    country_id: int = Field(default_factory=find_next_id, alias="id")
    name: str
    capital: str
    area: int

countries = [
    Country(id=1, name="Tailandia", capital="Bangkok", area=513120),
    Country(id=2, name="Autralia", capital="Canberra", area=7169630),
    Country(id=3, name="Egipto", capital="Cairo", area=1010408)
]

for i in countries:
    print(i)


@app.get("/countries")
async def get_countries():
    return countries

@app.post("/countries", status_code=201)
async def add_country(country: Country):
    countries.append(country)
    return country
