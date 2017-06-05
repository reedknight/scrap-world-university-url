# WEB SCAPPER FOR https://univ.cc/world.php
For collecting a list of urls of worldwide University websites for analysis using Python Scrapy.

Collected 7000+ urls of Universities World Wide.

## For execution
```
virtualenv -p /usr/bin/python2.7 --no-site-packages vEnv
source vEnv/bin/activate
pip install -r requirements.txt
cd univ_cc
scrapy crawl univ -o ../world_universities.json
```
