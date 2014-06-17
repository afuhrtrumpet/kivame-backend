hacksummit
==========

Created at Hack Summit 2014, this project provides the backend for a Kiva loan recommendation system.

How to run
==========
* Clone the repository.
* Go to the directory and run:
```
sudo pip install -r requirements.txt
```
* Edit kiva_recommendations/kiva_recommendations/settings.py
Replace `KIVA_CLIENT_ID` with your Kiva client iD
Replace `KIVA_CLIENT_SECRET` with your Kiva client secret.
* Run:
```
python kiva_recommendations/manage.py runserver
```
