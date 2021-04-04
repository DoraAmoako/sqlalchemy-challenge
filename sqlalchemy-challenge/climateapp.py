#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 19:15:18 2021

@author: doraamoako
"""
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

###############################################################
# Database Setup
###############################################################

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

##############################################################
#Flask Routes
##############################################################

@app.route("/")
def home():
     """List all available api routes."""   
     return (
        f"Availabe Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- List of dates and precipitation observed from the last year<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of stations from the dataset<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List of temperature observations from the previous year<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"- List minimum temperature, average temperature, and maximun temperature for a given start or start-end range<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- List minimum temperature, average temperature, and maximun temperature for a given start or start-end range, inclusive<br/>"
        
    )
 
  
@app.route("/api/v10/precipitation")
def precipitation():
    """List of dates and precipitation observed from the last year"""
    
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    rain = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date > last_year).\
        order_by(measurement.date).all()
    
    
    prcp_totals = []
    for result in rain:
        row = {}
        row["date"] = rain[0]
        row["prcp"] = rain[1]
        prcp_totals.append(row)
    
    
    return jsonify(prcp_totals)
    
@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(station.name, station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())


def tobs():
    """List of temperature observations from the previous year"""

    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date > last_year).\
        order_by(measurement.date).all()

    temp_totals = []
    for result in temperature:
        row = {}
        row["date"] = temperature[0]
        row["tobs"] = temperature[1]
        temp_totals.append(row)

    return jsonify(temp_totals)


@app.route("/api/v1.0/<start>")
def option1(start):

    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)


@app.route("/api/v1.0/<start>/<end>")
def option2(start,end):

    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

if __name__ == "__main__":
    app.run(debug=True)








    