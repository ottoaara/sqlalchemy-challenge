# Import the dependencies.
import sqlalchemy
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#Home page route
@app.route("/")
def home():
    return "Welcome to the Home Page"

#rain page route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Perform a query to retrieve the last 12 months of precipitation data
    last_12_months = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date).all()

    # Convert the query results to a dictionary
    precipitation_data = []
    for date, prcp in last_12_months:
        precipitation_data.append({date: prcp})

    return jsonify(precipitation_data)

#stations page route
@app.route("/api/v1.0/stations")
def stations():
    # Perform a query to retrieve the stations
    station_data = session.query(Station.station, Station.name).all()

    # Convert the query results to a dictionary
    stations_dict = {}
    for station, name in station_data:
        stations_dict[station] = name

    return jsonify(stations_dict)

# temps page route
@app.route("/api/v1.0/tobs")
def tobs():
    # Perform a query to retrieve the temperature observations for the most active station
    last_12_months_tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date).all()

    # Convert the query results to a dictionary
    tobs_data = []
    for date, tobs in last_12_months_tobs:
        tobs_data.append({date: tobs})

    return jsonify(tobs_data)

#start route -dynamic
@app.route("/api/v1.0/<start>")
def start(start):
    # Perform a query to retrieve the minimum, average, and maximum temperature for a given start date
    temperature_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Convert the query results to a dictionary
    temperature_stats = {
        "min_temperature": temperature_data[0][0],
        "avg_temperature": temperature_data[0][1],
        "max_temperature": temperature_data[0][2]
    }

    return jsonify(temperature_stats)

#start end - dynamic route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Perform a query to retrieve the minimum, average, and maximum temperature for a given start-end range
    temperature_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # Convert the query results to a dictionary
    temperature_stats = {
        "min_temperature": temperature_data[0][0],
        "avg_temperature": temperature_data[0][1],
        "max_temperature": temperature_data[0][2]
    }

    return jsonify(temperature_stats)

#of port 5000 in use this will default to 5001 on error
if __name__ == "__main__":
    app.run(debug=True, port =5001)
