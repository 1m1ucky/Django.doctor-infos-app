## payload schema 

# # creating doctor
# curl -v2 POST http://localhost:8000/doctor -d @doctor.json --header "Content-Type: application/json"

# # # # bulk create doctors
# curl -v2 POST http://localhost:8000/doctor -d @doctors.json --header "Content-Type: application/json"

# # # get all doctors
# curl -v2 GET http://localhost:8000/doctor

# # # get one doctor
# curl -v2 GET http://localhost:8000/doctor/1

# # filtering doctors
curl -v2 GET localhost:8000/doctor?\
category="SPECIAL"&\
district="CENTRAL"&\
price_range_from=0&\
price_range_to=0\
--header "Content-Type: application/json"