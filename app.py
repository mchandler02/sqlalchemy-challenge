import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from flask import Flask

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()
# Save reference to the table
Stations = Base.classes.station
Measurements = Base.classes.measurement
#create a database session object
session = Session(engine)

app = Flask(__name__)

#Home Page
@app.route("/")
def home():
    return(
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'> Precipitation </a><br/>" 
        f"<a href='/api/v1.0/stations'> Stations </a><br/>"
        f"<a href='/api/v1.0/tobs'> Total Observations </a><br/>"
        f"<a href='/api/v1.0/<start>'> Start Date Given </a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'> Start and End Date Given </a><br/>"
    )

#Preciptiation Page
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    precip = session.query(Measurements.date, Measurements.prcp).all()
    session.close()
    precip_measurements = {}
    for date, prcp in precip:
        precip_measurements[date]=prcp
    return jsonify(precip_measurements)


#Stations Page
@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    stations = session.query(Stations.station, Stations.name, Stations.latitude, Stations.longitude, Stations.elevation).all()
    session.close()
    station_info = []
    for station, name, lat, lng, elevation in stations:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = lat
        station_dict['longitude'] = lng
        station_dict['elevation'] = elevation
        station_info.append(station_dict)
    return jsonify(station_info)

#TempObs Page
@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    tobs = session.query(Measurements.tobs, Measurements.date).filter(Measurements.station == 'USC00519523').all()
    session.close()
    tobs_info = []
    for temp, date in tobs:
        temp_dict = {}
        temp_dict['temperature'] = temp
        temp_dict['date'] = date
        tobs_info.append(temp_dict)
    return jsonify(tobs_info)


# #Start Page
# @app.route('/api/v1.0/<start>')

# #Start/End Page
# @app.route('/api/v1.0/<start>/<end>')

if __name__ == "__main__":
    app.run(debug=True)