from django.db import models

# from djmoney.models.fields import MoneyField

from datetime import datetime

from typing import List, Optional, Dict

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

import sys

import json

import logging

from django.db import connection

from django.db.models import Q

class Address(
    models.Model
):

    class DISTRICT(models.TextChoices):
        CENTRAL = "CENTRAL"
        NEW_TERRITORIES = "NEW_TERRITORIES"
        KWUN_TONG = "KWUN_TONG"

    id = models.BigAutoField(
        auto_created=True, primary_key=True
    )

    room = models.CharField(
        "room",
        max_length=1024,
    )

    building = models.CharField(
        "building",
        max_length=1024,
    )

    street = models.CharField(
        "street",
        max_length=1024,
    )

    district = models.CharField(
        max_length=30,
        choices=DISTRICT.choices,
        default=DISTRICT.CENTRAL
    )

    class Meta:
        db_table = "T_address"
    
    @classmethod
    def to_string(address):
        return address.building + "," + address.district + "," + address.street + "," + address.room

    class CRUD:

        def __init__():

            class Serializer(serializers.ModelSerializer):
                class Meta:
                    model = Address
                    fields = '__all__'

                def validate(self, data):
                    # TODO: validating district
                    pass
        
        def create(
                self,
                room,
                building,
                street,
                district
            ):

            # TODO: serializer validating address

            obj_address = Address(
                room,
                building,
                street,
                district
            )

            obj_address.save()

            return obj_address

class DoctorCategory(models.TextChoices):
    GENERAL_PRACITIONER = "GENERAL_PRACITIONER"
    SPECIAL = "SPECIAL"

class LANG(models.TextChoices):
    ENG = "ENG"
    CHI = "CHI"

class DoctorInfo(
    models.Model
):
    id = models.BigAutoField(
        auto_created=True, primary_key=True
    )

    doctor_name = models.CharField(max_length = 32)

    doctor_category = models.CharField(
        max_length=20,
        choices=DoctorCategory.choices,
        default=DoctorCategory.GENERAL_PRACITIONER,
    )

    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    clinic_fee = models.IntegerField()

    clinic_fee_remark = models.TextField()

    member_discount_remark = models.TextField()

    language = models.CharField(
        max_length=5,
        choices=LANG.choices,
        default=LANG.ENG
    )

    class Meta:
        db_table = "T_doctor_info"

    class CRUD:
        def __init__(self):

            class AddressSerializer(serializers.ModelSerializer):
                class Meta:
                    model = Address
                    fields = '__all__'
            
            class PhoneNumSerializer(serializers.ModelSerializer):
                class Meta:
                    model = PhoneNum 
                    fields = '__all__'

            class OpeningHoursSerializer(serializers.ModelSerializer):
                class Meta: 
                    model = OpeningHour
                    fields = '__all__'

            class DoctorInfoSerializer(serializers.ModelSerializer):
                address = AddressSerializer()
                phone_nums = PhoneNumSerializer(many=True)
                opening_hours = OpeningHoursSerializer(many=True)

                class Meta:
                    model = DoctorInfo
                    fields = '__all__'
                
                def to_representation(self, instance):

                    data = super().to_representation(instance)

                    data['address'] = json.loads(json.dumps(data['address']))

                    data['phone_nums'] = list(map((lambda o: json.loads(json.dumps(o))['digits']), (data['phone_nums'])))

                    data['opening_hours'] = list(map((lambda o: json.loads(json.dumps(o))), (data['opening_hours'])))

                    return data

                def validate(self, data):
                    # TODO: validating phone num, clinic_fee, etc (not in requirements.txt)
                    return super.validate()
            
            Address.Serializer = AddressSerializer

            DoctorInfo.Serializer = DoctorInfoSerializer

        def create(
                self,
                doctor_name = "doctor_name",
                doctor_category = DoctorCategory.GENERAL_PRACITIONER,
                address = {
                    "room": "room",
                    "building": "building",
                    "street": "street",
                    "district": "district"
                },
                clinic_fee = 0,
                clinic_fee_remark = "",
                member_discount_remark = "",
                phone_nums = ["12345678","87654321"],
                opening_hours = [
                    {
                        "weekday": 1,
                        "from_hour": "9:00",
                        "to_hour": "13:00",
                        "is_closed": False
                    },
                ],
                language = LANG.ENG
            ):

            obj_address = Address(
                room = address['room'],
                building = address['building'],
                street = address['street'],
                district = address['district']
            )

            # TODO: validating by serializer

            obj_address.save()

            obj_doctor = DoctorInfo(
                doctor_name = doctor_name,
                doctor_category = doctor_category,
                address = obj_address,
                clinic_fee = clinic_fee,
                clinic_fee_remark = clinic_fee_remark,
                member_discount_remark = member_discount_remark,
                language = language
            )

            # TODO: validating by serializer

            obj_doctor.save()

            o = DoctorInfo.objects.all()

            for opening in opening_hours:

                obj_opening_hours = OpeningHour(
                    doctor = obj_doctor,
                    weekday = opening['weekday'],
                    from_hour = opening['from_hour'],
                    to_hour = opening['to_hour'],
                    is_closed = opening['is_closed']
                )

                # TODO: validating by serializer

                obj_opening_hours.save()
            
            for digits in phone_nums:

                obj_phone_num = PhoneNum(
                    doctor = obj_doctor,
                    digits = digits
                )

                # TODO: validating by serializer

                obj_phone_num.save()
            
            serialized_data = DoctorInfo.Serializer(obj_doctor).data

            return serialized_data
        
        def bulk_create(
            self,
            doctors = [
                {
                "doctor_name": "",
                "doctor_category": "",
                "address": {
                    "room": "room",
                    "building": "building",
                    "street": "street",
                    "district": "district"
                },
                "clinic_fee": 0,
                "clinic_fee_remark": "",
                "member_discount_remark": "",
                "phone_nums": ["12345678","87654321"],
                "opening_hours": [
                        {
                            "weekday": 1,
                            "from_hour": "9:00",
                            "to_hour": "13:00",
                            "is_closed": False
                        },
                ],
                "language": "ENG"
                },
            ]
            ):

            list_obj_doctors = []

            list_obj_doctors_address = []

            for doctor in doctors:

                address = doctor['address']

                obj_address = Address(
                    room = address['room'],
                    building = address['building'],
                    street = address['street'],
                    district = address['district']
                )

                list_obj_doctors_address.append(obj_address)

                # TODO: validating by serializer

            # 1 way bulk create SQL :)
            list_bulk_created_addresses = Address.objects.bulk_create(
                list_obj_doctors_address
            )

            for i in range(0, len(doctors)):

                obj_doctor = DoctorInfo(
                    doctor_name = doctors[i]['doctor_name'],
                    doctor_category = doctors[i]['doctor_category'],
                    address = list_bulk_created_addresses[i],
                    clinic_fee = doctors[i]['clinic_fee'],
                    clinic_fee_remark = doctors[i]['clinic_fee_remark'],
                    member_discount_remark = doctors[i]['member_discount_remark'],
                    language = doctors[i]['language'],
                    # opening_hours = list_bulk_created_opening_hours
                )

                # TODO: validating by serializer

                list_obj_doctors.append(obj_doctor)

            # 1 way bulk create SQL :)
            list_bulk_created_doctors = DoctorInfo.objects.bulk_create(
                list_obj_doctors
            )

            list_pending_bulk_created_opening_hours = []

            for i in range(0, len(list_bulk_created_doctors)):

                for j in range(0, len(doctors[i]['opening_hours'])):

                    doctors[i]['opening_hours'][j].update({
                        "doctor_id": list_bulk_created_doctors[i].id
                    })

                    list_pending_bulk_created_opening_hours.append(
                        OpeningHour(
                            **(doctors[i]['opening_hours'][j])
                        )
                    )
            
            # 1 way bulk create SQL :)
            OpeningHour.objects.bulk_create(
                list_pending_bulk_created_opening_hours
            )

            serializer = DoctorInfo.Serializer(list_bulk_created_doctors, many=True)

            data = [json.loads(json.dumps(data)) for data in serializer.data]

            return data
        
        def find(
                self,
                district = None,
                doctor_category = None,
                price_range_from = 0,
                price_range_to = sys.maxsize,
                language = None
            ):

            objs = DoctorInfo.objects.filter(
                (Q(address__district = district) if district != None else Q()) &
                (Q(doctor_category = doctor_category) if doctor_category != None else Q()) &
                Q(clinic_fee__lte = price_range_to) &
                Q(clinic_fee__gte = price_range_from) &
                Q(language = language if language != None else Q())
            )

            serializer = DoctorInfo.Serializer(objs, many=True)

            data = [json.loads(json.dumps(data)) for data in serializer.data]

            return data

        def list_all(self):

            objs = DoctorInfo.objects.all()

            serializer = DoctorInfo.Serializer(objs, many=True)

            data = [json.loads(json.dumps(data)) for data in serializer.data]

            return data
        
        def get_one_by_id(self, id = None):

            if (id == None):
                return None 

            obj = None

            try:

                obj = DoctorInfo.objects.get(id = id)
            
            except ObjectDoesNotExist:

                return None

            serializer = DoctorInfo.Serializer(obj)

            return serializer.data
        
        def delete_all(self):
            DoctorInfo.objects.all().delete()
        
        def serialize(self, orm_obj_doctor):
            pass


class PhoneNum(
    models.Model
):
    doctor = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE, related_name="phone_nums")
    # phone num format
    digits = models.CharField(max_length=8)

    class Meta:
        db_table = "T_phone_num"

WEEKDAYS = [
  (1, 1),
  (2, 2),
  (3, 3),
  (4, 4),
  (5, 5),
  (6, 6),
  (7, 7),
  (8, 8)
]

class OpeningHour(
    models.Model
):
    doctor = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE, related_name="opening_hours")
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    is_closed = models.BooleanField()

    class Meta:
        db_table = "T_opening_hour"

# init
DoctorInfo.CRUD()