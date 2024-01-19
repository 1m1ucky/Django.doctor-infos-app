
## setup virtualenv
python -m venv .venv.python
source ./.venv.python/bin/activate

## python deps  
pip install -r requirements.txt

## enter proj
cd doctor_infos_proj

## db migration
./manage.py migrate 

## test
# ./manage.py test

## local srv
./manage.py runserver