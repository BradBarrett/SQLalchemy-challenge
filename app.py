import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect 
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Set db reflection

Base = automap_base()

Base.prepare(engine, reflect = True)

measurement = Base.classes.measurement
station = Base.classes.station

#flask

app = Flask(__name__)
@app.route("/")

def launch():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
#link session
def precipitation():
    session = Session(engine)

    data = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > '2016-08-22').order_by(measurement.date).all()

#set new dict and complile prcp data
    measure_data = []
    for i in data:
        prpc_dict = {}
        prpc_dict[i[0]] = i[1]
        measure_data.append(prpc_dict)

    return jsonify(measure_data)


#station data
@app.route("/api/v1.0/stations")

def stations():
    session = Session(engine)
    #return station data
    data = session.query(station.station, station.name).all()
    session.close()

    return jsonify(data)

@app.route("/api/v1.0/tobs")

def tobs():
    session = Session(engine)
    data = session.query(measurement.date, measurement.tobs, measurement.station).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date > '2016-08-22').all()
    session.close()

    tobs_data = []

    for temperature_observation, date, station in data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = temperature_observation
        tobs_dict["station"] = station
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):


    if not end:
        session = Session(engine)
        data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).all()

        result = list(np.ravel(data))

        return jsonify(result=result)

    session = Session(engine)
    data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

    result = list(np.ravel(data))

    return jsonify(result=result)


if __name__ == '__main__':
    app.run(debug=True)









