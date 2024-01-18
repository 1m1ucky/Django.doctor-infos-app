from django.shortcuts import render

from django.http import Http404
from doctor_infos_app.models import DoctorInfo
# from doctor_infos_app.schemas import DoctorInfoSchema
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.exceptions import APIException

from doctor_infos_app.models import DoctorInfo, LANG
import logging
from typing import List

import sys

from ninja import Query, Router, Schema

router = Router(tags=["doctors"])

class APISchemaException(APIException):
    status_code = 400
    default_detail = 'Wrong API schema'
    default_code = 'WRONG_API_SCHEMA'

class DoctorViewSet(viewsets.ModelViewSet):

    queryset = DoctorInfo.objects.all()

    serializer_class = DoctorInfo.Serializer

    @staticmethod
    def validate_schema_of_doctor(obj):
        try:
            assert 'doctor_name' in obj
            assert 'doctor_category' in obj
            assert 'address' in obj
            assert 'clinic_fee' in obj
            assert 'clinic_fee_remark' in obj
            assert 'member_discount_remark' in obj
            assert 'phone_nums' in obj
            assert 'opening_hours' in obj
            assert 'language' in obj
        except Exception:
            raise APISchemaException()
        pass

    @router.post("/", response=None)
    def create(
            self,
            request,
            # doctor #: DoctorInfoSchema
        ):

        logging.info('##################### create #####################')

        doctor = request.data
        
        # validation
        # self.validate_schema_of_doctor(doctor)

        if isinstance(doctor, list):

            return self.bulk_create(request)

        else:

            doctor = DoctorInfo.CRUD().create(
                **doctor
            )

            return Response(data = doctor)
    
    @router.post("/", response=None)
    def bulk_create(
            self,
            request,
            # doctors #: List[DoctorInfoSchema]
        ):

        logging.info('##################### bulk create #####################')

        doctors = request.data

        # validation
        # [self.validate_schema_of_doctor(d) for d in doctors]

        doctors = DoctorInfo.CRUD().bulk_create(
            doctors
        )

        return Response(data = doctors)

    @router.get("/", response=None)
    def list(self,
             request,
             district:str = None,
             category:str = None,
             price_range_from:int = 0,
             price_range_to:int = 0,
             language:str = None,
        ):

        logging.info('##################### list #####################')

        # TODO: old way to get query params
        #
        query = request.query_params
        
        doctors = DoctorInfo.CRUD().find(
            district = query.get('district', None),
            doctor_category = query.get('category', None),
            price_range_from = int(query.get('price_range_from', 0)),
            price_range_to = int(query.get('price_range_to', sys.maxsize)),
            language = query.get('language', None)
        )

        # doctors = DoctorInfo.CRUD().find(
        #     district = district,
        #     doctor_category = category,
        #     price_range_from = price_range_from,
        #     price_range_to = price_range_to,
        #     language = language,
        # )

        return Response(data = doctors)

    @router.get("/{int:id}", response=None)
    def retrieve(
            self,
            request,
            id #:int = None
        ):

        logging.info('##################### retrieve #####################')

        doctor = DoctorInfo.CRUD().get_one_by_id(id = id)

        if doctor == None:
            raise Http404
        else:
            return Response(data = doctor)
