# ## payload schema 

# delete all doctor
curl -XDELETE http://localhost:8000/doctor

sleep 1

# creating doctor
curl -XPOST http://localhost:8000/doctor -d "@./scripts/doctor.json" --header "Content-Type: application/json"

sleep 1

# # bulk create doctors
curl -XPOST http://localhost:8000/doctor -d "@./scripts/doctors.json" --header "Content-Type: application/json"

sleep 1

# # get all doctors
curl -XGET http://localhost:8000/doctor

sleep 1

# # get one doctor
curl -XGET http://localhost:8000/doctor/1

sleep 1

# # filtering doctors
curl -XGET http://localhost:8000/doctor?\
district="KWUN_TONG"\&\
category="GENERAL_PRACITIONER"\&\
price_range_from=0\&\
price_range_to=1000