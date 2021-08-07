# HKtraffic
This repository if for scraping the data posted to https://www.immd.gov.hk daily regarding travelers entering and leaving Hong Kong. 

This project uses a Postgresql database and Django. There is a config.ini file to connect to the database, as well as to utilize proxies if desired.

Functions are contained in hktraffic/hktraffic/scraper.py

 
## Django & PostgreSQL Database
For help setting up Django with PostgreSQL, this guide can be followed even if you have little knowledge:
- https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04

Django models are at hktraffic/hktraffic/models.py


## Configuration
hktraffic/config.ini contains all manual settings for connecting to the database.


## Proxy Connections
hktraffic/hktraffic/proxies.py was written to work with Blazing SEO Proxy. It will shuffle your list of proxies and then cycle through them, exhausting the whole list before reshuffling. 
- https://blazingseollc.com


## Operation
After you have set up the config and applied the migrations, the program can be set up to run as a cronjob or similar by calling scraper.update(). This works backwards from yesterday until it finds pre-existing db entries. The first publication date is January 24th, 2020.

You can also print out the database as a CSV at any time by calling scraper.convert_csv(). This will created a file named 'HKtraffic.csv' with all info.

### Note:
The English webpage for July 6th, 2020 is broken. The data can be collected manually by using the Chinese page instead.

- Broken English Page: https://www.immd.gov.hk/eng/stat_20200706.html
- Chinese Page: https://www.immd.gov.hk/hks/stat_20200706.html
