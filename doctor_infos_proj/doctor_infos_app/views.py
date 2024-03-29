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

    def create(
            self,
            request,
        ):

        logging.info('##################### create #####################')

        doctor = request.data

        if isinstance(doctor, list):

            return self.bulk_create(request)

        else:
            
            self.validate_schema_of_doctor(doctor)

            doctor = DoctorInfo.CRUD().create(
                **doctor
            )

            return Response(data = doctor)
    
    def bulk_create(
            self,
            request,
        ):

        logging.info('##################### bulk create #####################')

        doctors = request.data

        [self.validate_schema_of_doctor(d) for d in doctors]

        doctors = DoctorInfo.CRUD().bulk_create(
            doctors
        )

        return Response(data = doctors)

    def list(self,
             request,
             district = None,
             category = None,
             price_range_from = 0,
             price_range_to = 0,
             language = None,
        ):

        logging.info('##################### list #####################')

        # TODO: old way to get query params

        query = request.query_params
        
        doctors = DoctorInfo.CRUD().find(
            district = query.get('district', None),
            doctor_category = query.get('category', None),
            price_range_from = int(query.get('price_range_from', 0)),
            price_range_to = int(query.get('price_range_to', sys.maxsize)),
            language = query.get('language', None)
        )

        return Response(data = doctors)

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

    def delete(
            self,
            request
        ):

        logging.info('##################### delete #####################')

        DoctorInfo.CRUD().delete_all()

        return Response(status=status.HTTP_200_OK)