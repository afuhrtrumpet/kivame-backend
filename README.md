HackSummit 2014 - Kiva Challenge
==========

The backend for a KivaMe, a personalized loan recommendation system created at Hack Summit 2014.

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
