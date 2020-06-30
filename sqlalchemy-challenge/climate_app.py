import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect Database
Base = automap_base()
Base.prepare(engine, reflect = True)

# Save table references
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

# Setup Flask
app = Flask(__name__)


#Set Flask Routes

@app.route("/")
def main():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<start><br/>"
        f"/api/v1.0/between<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    precipitation_data = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_precipitations = []
    for date, prcp in precipitation_data:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitations.append(precipitation_dict)


    return jsonify(all_precipitations)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(Station.name).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    most_active_station = 'USC00519397'

    temp_observation = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).\
    filter(func.strftime("%Y-%m-%d", Measurement.date) > dt.date(2016, 12, 31)).all()

    session.close()

    all_temps = []
    for date, tobs in temp_observation:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        all_temps.append(temp_dict)


    return jsonify(all_temps)   


@app.route("/api/v1.0/start")
def start():
    
    session = Session(engine)

    start_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.date(2016, 12, 31)).all()

    session.close()
    
    all_start = list(np.ravel(start_data))


    return jsonify(all_start)   


@app.route("/api/v1.0/between")
def between():
    
    session = Session(engine)

    between_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= dt.date(2016, 1, 1)).filter(Measurement.date <= dt.date(2016, 12, 31)).all()

    session.close()
    
    all_between = list(np.ravel(between_data))


    return jsonify(all_between)   


if __name__ == '__main__':
    app.run(debug=True)
