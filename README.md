# HKtraffic
This repository if for scraping the data posted to https://www.immd.gov.hk daily regarding travelers entering and leaving Hong Kong. Though many believe this data to be inaccurate, the collection process was easy enough to automate that I felt it worth gathering.

This project uses a Postgresql database and the Django framework. There is a config.ini file to connect to the database, as well as a few other settings.

Functions are contained in hktraffic/hktraffic/scraper.py

Django models are at hktraffic/hktraffic/models.py


