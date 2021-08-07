# HKtraffic
This repository if for scraping the data posted to https://www.immd.gov.hk daily regarding travelers entering and leaving Hong Kong. Though many believe this data to be inaccurate, the collection process was easy enough to automate that I felt it worth gathering.

This project uses a Postgresql database and the Django framework. There is a config.ini file to connect to the database, as well as to utilize proxies if desired.

Functions are contained in hktraffic/hktraffic/scraper.py

Django models are at hktraffic/hktraffic/models.py



## Instructions

For help setting up Django with PostgreSQL, this guide can be followed even if you have little knowledge:

https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04


hktraffic/config.ini contains all manual settings for connecting to the database.

hktraffic/hktraffic/proxies.py was written to work with Blazing SEO Proxy. It will shuffle your list of proxies and then cycle through them, exhausting the whole list before reshuffling. https://blazingseollc.com

After you have set up the config and applied the migrations, the program can be set up to run as a cronjob or similar by calling scraper.update(). This works backwards from yesterday until it finds pre-existing db entries. If it is your first time running, 

The English webpage for 1 date in July 2020 is broken. The data can be collected manually by using the Chinese page instead.
