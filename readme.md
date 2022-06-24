# IM4017 Database Administration 2 - Final Exam Project
## Introduction
This project stores the traffic accident in current year using MongoDB. User can use the web interface to query the location of traffic accident by using the web interface. Also, user can update the data by web interface.
## Technology
- Python 
  - Flask 
  - pandas 
  - pymongo 
- MongoDB 
- Leaflet & OpenStreetMap 
## Server Install
```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
export DB_URL="mongodb+srv://traffic-app:<password>@w10923201cluster.bahwr.mongodb.net/?retryWrites=true&w=majority"
python3 setup.py
```
###  debug mode
```sh
export FLASK_ENV=development
```
###  run server
```sh
source .venv/bin/activate 
export DB_URL="mongodb+srv://traffic-app:<password>@w10923201cluster.bahwr.mongodb.net/?retryWrites=true&w=majority"
python3 run.py
```
> Note: If you face any OSError: [Errno 98] Address already in use (port 5000 occupied issues) :
#check which port is running
`netstat -tulpn`
#kill a certain port process that is running
`sudo kill $(sudo lsof -t -i:5000)`
