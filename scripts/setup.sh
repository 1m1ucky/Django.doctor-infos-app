
## setup virtualenv
python -m venv .venv 
source ../.venv/bin/activate

## python deps  
pip install requirements.txt

## enter proj
cd doctor_infos_proj

## db migration
./manage.py migrate 

## test
./manage.py test

## local srv
./manage.py runserver