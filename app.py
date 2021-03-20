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
    precip_measurements = []
    for date, prcp in precip:
        precip_dict = {}
        precip_dict[date] = prcp
        #precip_dict['Precipitation'] = prcp
        precip_measurements.append(precip_dict)
    return jsonify(precip_measurements)


# #Stations Page
# @app.route('/api/v1.0/stations')


# #TempObs Page
# @app.route('/api/v1.0/tobs')


# #Start Page
# @app.route('/api/v1.0/<start>')

# #Start/End Page
# @app.route('/api/v1.0/<start>/<end>')

if __name__ == "__main__":
    app.run(debug=True)