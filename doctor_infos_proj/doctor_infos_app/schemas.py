from ninja import Query, Router, Schema, Field
from typing import List
import datetime

# TODO: API JSON Schema and validation for the app
# https://django-ninja.dev/guides/response/django-pydantic/
# https://docs.pydantic.dev/latest/concepts/validators/ 

class AddressAPISchema(Schema):
  id: int
  room: str
  building: str
  street: str
  district: str
  # default=DISTRICT.CENTRAL

class OpeningHourAPISchema(Schema):
  weekday: int 
  from_hour: datetime.time
  to_hour: datetime.time
  is_closed: bool

class DoctorInfoAPISchema(Schema):
  doctor_name: str
  doctor_category: str
  address: str
  clinic_fee: int
  clinic_fee_remark: str
  member_discount_remark: str
  phone_nums: List[str]
  opening_hours: List[OpeningHourAPISchema]
  language: str
