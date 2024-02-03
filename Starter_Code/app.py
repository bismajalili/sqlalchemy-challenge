# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
# reflect an existing database into a new model 
Base=automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)
# reflect the tables


# Save references to each table
# Save references to each table
measurement=Base.classes.measurement
station=Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)
year=dt.date(2017,8,23)-dt.timedelta(days=365)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """This function describes the available routes."""
    return (f"""
<center> <h1> welcome to my climate api</h1></center><br>                   
<center>/api/v1.0/precipitation</center><br>
            <center>/api/v1.0/stations</center><br>
            <center>/api/v1.0/tobs</center><br>
            <center>/api/v1.0/start</center><br>
            <center>/api/v1.0/start/end</center><br>
            """)

@app.route("/api/v1.0/precipitation")
def precip():
    
    prcplist=session.query(measurement.date,measurement.prcp).filter(measurement.date>=year).all()
    session.close()
    prcp=[]
    for date,precipitation in prcplist:
        prcpdict={}
        prcpdict["Date"]=date
        prcpdict["Precipitation"]=precipitation
        prcp.append(prcpdict)

    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    results=session.query(station.station).all()
    session.close()

    return jsonify(list(np.ravel(results)))

@app.route("/api/v1.0/tobs")
def tob ():
    year_temp=session.query(measurement.tobs).filter(measurement.station=="USC00519281").filter(measurement.date>=year).all()
    session.close()
    return jsonify(list(np.ravel(year_temp)))

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats (start=None,end=None):
    stats=[func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)]
    
    if not end:
        results=session.query(*stats).filter(measurement.date>= start).all()
        
        session.close()
        return jsonify(list(np.ravel(results)))
    results=session.query(*stats).filter(measurement.date>= start).filter(measurement.date<= end).all()

    session.close()
    return jsonify(list(np.ravel(results)))
if __name__=="__main__":
    app.run()