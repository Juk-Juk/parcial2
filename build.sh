set -o errexit

# install dependecies
pip install -r requirements.txt

# migrations
python manage.py migrate --noinput

# collectstatic
python manage.py collectstatic --noinput