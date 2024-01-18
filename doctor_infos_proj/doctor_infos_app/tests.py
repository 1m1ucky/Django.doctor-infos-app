from django.test import TestCase
from rest_framework.test import APIRequestFactory
from doctor_infos_app.models import DoctorCategory, DoctorInfo, Address, PhoneNum, OpeningHours
from django.db import connection
from django.urls import reverse

import logging, colorlog
TRACE = 5
logging.addLevelName(TRACE, 'TRACE')
formatter = colorlog.ColoredFormatter(log_colors={'TRACE': 'yellow'})
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger('TEST')
logger.addHandler(handler)
logger.setLevel('TRACE')
logger.log(TRACE, 'TESTING...')

# TODO: functional tests
class FunctionalUnitTestCase(TestCase):

    def setUp(self):
        from django.conf import settings
        settings.DstEBUG = True

    def tearDown(self):
        from django.db import connection
        for query in connection.queries:
            print(f"✅ {query['sql']}\n")
    
    def test_viewset_validate_schema_of_doctor(self):
        try:
            DoctorViewSet.validate_schema_of_doctor({
            })
        except Exception:
            print("assertion error")

    def test_orm_bulk_create(self):

        arr_addresses = []
        list_doctors = []

        for i in range(0,10):
            obj_address = Address(
                room = 'room-' + str(i),
                building = 'building',
                street = 'street',
                district = 'district'
            )
        
            arr_addresses.append(obj_address)

        list_addresses_bulk_created = Address.objects.bulk_create(
            arr_addresses
        )
        
        for i in range(0, len(arr_addresses)):
            obj_doctor = DoctorInfo(
                doctor_name = 'doctor_name',
                doctor_category = 'doctor_category',
                address = list_addresses_bulk_created[i],
                clinic_fee = 100,
                clinic_fee_remark = 'clinic_fee_remark',
                member_discount_remark = 'member_discount_remark'
            )
            list_doctors.append(obj_doctor)

        DoctorInfo.objects.bulk_create(
            list_doctors
        )

        objs_addr = Address.objects.all()
        objs_doctor = DoctorInfo.objects.all()

        self.assertEqual(len(objs_addr), len(objs_doctor))

# TODO: component tests
class ComponentTestCase(TestCase):

    def test_obj_AddressSerializer(self):

        DoctorInfo.CRUD()

        serializer = Address.Serializer

        address = serializer({
            "room": "room",
            "building": "building",
            "street": "street",
            "district": "district"
        }).data

        self.assertEqual(address, {
            "room": "room",
            "building": "building",
            "street": "street",
            "district": "district"
        })

# TODO: model tests
class ModelTestCase(TestCase):

    class Helper():

        @staticmethod
        def assert_valid_shape_of_doctorinfos(assertor, obj):
            assertor.assertIn('doctor_name', obj)
            assertor.assertIn('doctor_category', obj)
            assertor.assertIn('address', obj)
            assertor.assertIn('clinic_fee', obj)
            assertor.assertIn('clinic_fee_remark', obj)
            assertor.assertIn('member_discount_remark', obj)
            assertor.assertIn('phone_nums', obj)
            assertor.assertIn('opening_hours', obj)
            assertor.assertIn('language', obj)

    def setUp(self):

        DoctorInfo.CRUD().delete_all()

        doctor = DoctorInfo.CRUD().create(
            doctor_name = 'sample_doctor',
            doctor_category = 'doctor_category',
            address = {
                "room": "room",
                "building": "building",
                "street": "street",
                "district": "district"
            },
            clinic_fee = 100,
            clinic_fee_remark = "clinic_fee_remark",
            member_discount_remark = "member_discount_remark",
            phone_nums = ["12345678","87654321"],
            opening_hours = [{
                "weekday": 1,
                "from_hour": "9:00",
                "to_hour": "13:00",
                "is_closed": False
            }],
            language = "ENG"
        )

        self.crud_created_doctor = doctor

    def test_model_doctor_create(self):

        ModelTestCase.Helper.assert_valid_shape_of_doctorinfos(self, self.crud_created_doctor)

        # assert doctor's related infos are correctly commited
        objs_doctor = DoctorInfo.objects.all()
        objs_address = Address.objects.all()
        objs_phonenum = PhoneNum.objects.all()
        objs_opening_hours = OpeningHours.objects.all()

        self.assertEqual(list(objs_address)[0].id, self.crud_created_doctor['address']['id'])
        self.assertEqual(list(objs_phonenum)[0].digits, '12345678')
        self.assertEqual(list(objs_opening_hours)[0].weekday, self.crud_created_doctor['opening_hours'][0]['weekday'])

    def test_model_doctor_bulk_create(self):

        list_serialized_doctor = DoctorInfo.CRUD().bulk_create(
            [
                {
                    "doctor_name": "D1",
                    "doctor_category": "GENERAL_PRACITIONER",
                    "address": {
                        "room": "room",
                        "building": "building",
                        "street": "street",
                        "district": "NEW_TERRITORIES"
                    },
                    "clinic_fee": 50,
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
                {
                    "doctor_name": "D2",
                    "doctor_category": "SPECIAL",
                    "address": {
                        "room": "room",
                        "building": "building",
                        "street": "street",
                        "district": "CENTRAL"
                    },
                    "clinic_fee": 700,
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
                {
                    "doctor_name": "D3",
                    "doctor_category": "GENERAL_PRACITIONER",
                    "address": {
                        "room": "room",
                        "building": "building",
                        "street": "street",
                        "district": "KWUN_TONG"
                    },
                    "clinic_fee": 20000,
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
        )

        objs_doctor = DoctorInfo.objects.all()

        self.assertEqual(
           len(list_serialized_doctor),
           3
        )
        
        self.assertEqual(
           len(objs_doctor),
           4
        )

        ModelTestCase.Helper.assert_valid_shape_of_doctorinfos(
            self,
            list_serialized_doctor[0]
        )

        self.assertEqual(
            list_serialized_doctor[0]['doctor_name'],
            "D1"
        )
    
    def test_model_doctor_list_all(self):

        list_serialized_doctor = DoctorInfo.CRUD().list_all()

        self.assertEqual(
            len(list_serialized_doctor),
            1
        )

        [
            ModelTestCase.Helper.assert_valid_shape_of_doctorinfos(self, d)
            for d in list_serialized_doctor
        ]

    def test_model_doctor_get_one(self):

        serialized_doctor = DoctorInfo.CRUD().get_one_by_id(
            self.crud_created_doctor['id']
        )

        ModelTestCase.Helper.assert_valid_shape_of_doctorinfos(self, serialized_doctor)

        self.assertEqual(
            serialized_doctor['id'],
            self.crud_created_doctor['id']
        )

    def test_model_doctor_filters(self):

        DoctorInfo.CRUD().bulk_create(
            [
                {
                    "doctor_name": "D1",
                    "doctor_category": "GENERAL_PRACITIONER",
                    "address": {
                        "room": "room",
                        "building": "building",
                        "street": "street",
                        "district": "NEW_TERRITORIES"
                    },
                    "clinic_fee": 50,
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
                {
                    "doctor_name": "D2",
                    "doctor_category": "SPECIAL",
                    "address": {
                        "room": "room",
                        "building": "building",
                        "street": "street",
                        "district": "CENTRAL"
                    },
                    "clinic_fee": 700,
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
                                {
                    "doctor_name": "D3",
                    "doctor_category": "GENERAL_PRACITIONER",
                    "address": {
                        "room": "room",
                        "building": "building",
                        "street": "street",
                        "district": "NEW_TERRITORIES"
                    },
                    "clinic_fee": 2000,
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
        )

        # case 1
        serialized_doctors = DoctorInfo.CRUD().find(
            district = Address.DISTRICT.CENTRAL,
            doctor_category = DoctorCategory.SPECIAL,
            price_range_from = 500,
            price_range_to = 1000,
        )

        self.assertEqual(len(serialized_doctors), 1)

        self.assertEqual(
            serialized_doctors[0]['doctor_name'],
            "D2"
        )

        # case 2
        serialized_doctors = DoctorInfo.CRUD().find(
            district = Address.DISTRICT.NEW_TERRITORIES,
            doctor_category = DoctorCategory.GENERAL_PRACITIONER,
            price_range_from = 1000,
            price_range_to = 3000,
        )

        self.assertEqual(len(serialized_doctors), 1)

        self.assertEqual(
            serialized_doctors[0]['doctor_name'],
            "D3"
        )

# TODO: API tests
from doctor_infos_app.views import DoctorViewSet

from django.test import Client

class DoctorAPIViewTestCase(TestCase):

    class Helper():

        @staticmethod
        def assert_valid_shape_of_response_data(assertor, obj):
            assertor.assertIn('doctor_name', obj)
            assertor.assertIn('doctor_category', obj)
            assertor.assertIn('address', obj)
            assertor.assertIn('clinic_fee', obj)
            assertor.assertIn('clinic_fee_remark', obj)
            assertor.assertIn('member_discount_remark', obj)
            assertor.assertIn('phone_nums', obj)
            assertor.assertIn('opening_hours', obj)

    def setUp(self):
        logging.info('##################### setup #####################')

        self.httpclient = Client()

        self.fixture = {
            "doctor_name": 'sample_doctor',
            "doctor_category": 'SPECIAL',
            "address": {
                "room": "room",
                "building": "building",
                "street": "street",
                "district": "CENTRAL"
            },
            "clinic_fee": 100,
            "clinic_fee_remark": "clinic_fee_remark",
            "member_discount_remark": "member_discount_remark",
            "phone_nums": ["12345678","87654321"],
            "opening_hours": [{
                "weekday": 1,
                "from_hour": "9:00",
                "to_hour": "13:00",
                "is_closed": False
            }],
            "language": "ENG"
        }

    def test_api_create_doctor(self):

        httpclient = self.httpclient

        logging.info('##################### test_api_create_doctor #####################')

        response = httpclient.post('/doctor', 
            self.fixture,
            content_type="application/json"
        )

        self.assertIn('id', response.data)

        response = httpclient.get('/doctor')

        self.assertTrue(len(response.data) == 1)

        DoctorAPIViewTestCase.Helper.assert_valid_shape_of_response_data(self, response.data[0])

    def test_api_bulk_create_doctor(self):

        logging.info('##################### test_api_bulk_create_doctor #####################')

        httpclient = self.httpclient

        response = httpclient.post('/doctor', [
            self.fixture,
            self.fixture,
            self.fixture,
            self.fixture,
        ],
            content_type="application/json"
        )

        print(response)

        self.assertEqual(len(response.data), 4)

        response = httpclient.get('/doctor')

        self.assertEqual(len(response.data), 4)

        DoctorAPIViewTestCase.Helper.assert_valid_shape_of_response_data(self, response.data[0])
    
    def test_api_list_doctors(self):

        logging.info('##################### test_api_list_doctor #####################')

        httpclient = self.httpclient
                 
        response = httpclient.get('/doctor')

        self.assertTrue(len(response.data) == 0)

        response = httpclient.post('/doctor',
            self.fixture,
            content_type="application/json"
        )

        response = httpclient.get('/doctor')

        self.assertTrue(len(response.data) == 1)

        # list filter 1
        # https://docs.djangoproject.com/en/5.0/topics/testing/tools/#django.test.Client.get

        response = httpclient.get("/doctor", {
            'category': "SPECIAL",
            'district': "CENTRAL",
            'price_range_from': 0,
            'price_range_to': 200
        })

        self.assertTrue(len(response.data) == 1)

        DoctorAPIViewTestCase.Helper.assert_valid_shape_of_response_data(self, response.data[0])

        # list filter 2
        response = httpclient.get("/doctor", {
            'category': "SPECIAL",
            'district': "CENTRAL",
            'price_range_from': 400,
            'price_range_to': 800
        })

        self.assertTrue(len(response.data) == 0)

        # list filter 3
        response = httpclient.get("/doctor", {
            'category': "SPECIAL",
            'district': "CENTRAL",
        })

        self.assertTrue(len(response.data) == 1)

        # list filter 4
        response = httpclient.get("/doctor", {
            'district': "CENTRAL",
        })

        self.assertTrue(len(response.data) == 1)

        # list filter 5
        response = httpclient.get("/doctor", {
            'category': "OTHER",
            'district': "CENTRAL",
        })

        self.assertTrue(len(response.data) == 0)

        # list filter 6
        response = httpclient.get("/doctor", {
            'category': "SPECIAL",
            'district': "OTHER",
        })

        self.assertTrue(len(response.data) == 0)

    def test_api_get_one_doctor(self):

        logging.info('##################### test_api_get_one_doctor #####################')

        httpclient = self.httpclient

        response = httpclient.post('/doctor',
            self.fixture,
            content_type="application/json"
        )
        
        id = response.data['id']

        # list filter 1
        response = httpclient.get('/doctor/' + str(id))

        DoctorAPIViewTestCase.Helper.assert_valid_shape_of_response_data(self, response.data)

# TODO: story tests
class StoryTestCase(TestCase):

    class Helper():

        @staticmethod
        def assert_valid_shape_of_response_data(assertor, obj):
            assertor.assertIn('doctor_name', obj)
            assertor.assertIn('doctor_category', obj)
            assertor.assertIn('address', obj)
            assertor.assertIn('clinic_fee', obj)
            assertor.assertIn('clinic_fee_remark', obj)
            assertor.assertIn('member_discount_remark', obj)
            assertor.assertIn('phone_nums', obj)
            assertor.assertIn('opening_hours', obj)
            assertor.assertIn('language', obj)

    def setUp(self):

        logging.info('##################### setup #####################')

        self.httpclient = Client()

        doctor_1 = {
            "doctor_name": 'D1',
            "doctor_category": 'SPECIAL',
            "address": {
                "room": "room",
                "building": "building",
                "street": "street",
                "district": "CENTRAL"
            },
            "clinic_fee": 100,
            "clinic_fee_remark": "clinic_fee_remark",
            "member_discount_remark": "member_discount_remark",
            "phone_nums": ["12345678","87654321"],
            "opening_hours": [{
                "weekday": 1,
                "from_hour": "9:00",
                "to_hour": "13:00",
                "is_closed": False
            }],
            "language": "ENG"
        }

        import copy
        doctor_2 = copy.deepcopy(doctor_1)
        doctor_2['doctor_name'] = 'D2'
        doctor_2['doctor_category'] = 'SPECIAL'
        doctor_2['address']['district'] = 'CENTRAL'
        doctor_2['clinic_fee'] = 2000
        doctor_2['language'] = 'ENG'

        doctor_3 = copy.deepcopy(doctor_1)
        doctor_3['doctor_name'] = 'D3'
        doctor_3['doctor_category'] = 'SPECIAL'
        doctor_3['address']['district'] = 'KWUN_TONG'
        doctor_3['clinic_fee'] = 3000
        doctor_3['language'] = 'CHI'

        doctor_4 = copy.deepcopy(doctor_1)
        doctor_4['doctor_name'] = 'D4'
        doctor_4['doctor_category'] = 'SPECIAL'
        doctor_4['address']['district'] = 'NEW_TERRITORIES'
        doctor_4['clinic_fee'] = 4000
        doctor_4['language'] = 'ENG'

        doctor_5 = copy.deepcopy(doctor_1)
        doctor_5['doctor_name'] = 'D5'
        doctor_5['doctor_category'] = 'GENERAL_PRACITIONER'
        doctor_5['address']['district'] = 'NEW_TERRITORIES'
        doctor_5['clinic_fee'] = 5000
        doctor_5['language'] = 'CHI'

        doctor_6 = copy.deepcopy(doctor_1)
        doctor_6['doctor_name'] = 'D6'
        doctor_6['doctor_category'] = 'GENERAL_PRACITIONER'
        doctor_6['address']['district'] = 'CENTRAL'
        doctor_6['clinic_fee'] = 6000
        doctor_6['language'] = 'ENG'

        doctor_7 = copy.deepcopy(doctor_1)
        doctor_7['doctor_name'] = 'D7'
        doctor_7['doctor_category'] = 'GENERAL_PRACITIONER'
        doctor_7['address']['district'] = 'KWUN_TONG'
        doctor_7['clinic_fee'] = 7000
        doctor_7['language'] = 'CHI'

        self.doctors = [
            doctor_1,
            doctor_2,
            doctor_3,
            doctor_4,
            doctor_5,
            doctor_6,
            doctor_7,
        ]

    def test_story(self):
        # create one doctor

        httpclient = self.httpclient

        # create one doctors
        response = httpclient.post('/doctor',
            self.doctors[0],
            content_type="application/json"
        )
        
        # create some doctors
        response = httpclient.post('/doctor',
            self.doctors[1:7],
            content_type="application/json"
        )

        self.assertEqual(len(response.data), 6)

        # get all doctors
        response = httpclient.get("/doctor")

        self.assertEqual(len(response.data), 7)

        # get one doctors
        id = (max(list(map(lambda d: d['id'], response.data))))

        response = httpclient.get("/doctor/" + str(id))

        self.assertEqual(response.data['id'], id)

        # filter doctors
        response = httpclient.get("/doctor", {
            'category': "SPECIAL",
            'district': "OTHER",
            'price_range_from': 0,
            'price_range_to': 1000,
            "language": "ENG"
        })

        self.assertEqual(len(response.data), 0)

        response = httpclient.get("/doctor", {
            'category': "SPECIAL",
            'district': "CENTRAL",
            'price_range_from': 0,
            'price_range_to': 2000,
            "language": "ENG"
        })

        self.assertEqual(len(response.data), 2)

        response = httpclient.get("/doctor", {
            'category': "GENERAL_PRACITIONER",
            'district': "KWUN_TONG",
            'price_range_from': 0,
            'price_range_to': 3000,
            "language": "ENG",
        })

        self.assertEqual(len(response.data), 0)

        response = httpclient.get("/doctor", {
            'category': "SPECIAL",
            'district': "NEW_TERRITORIES",
            'price_range_from': 0,
            'price_range_to': 4000,
            "language": "ENG",
        })

        self.assertEqual(len(response.data), 1)

        response = httpclient.get("/doctor", {
            "language": "CHI",
        })

        self.assertEqual(len(response.data), 3)