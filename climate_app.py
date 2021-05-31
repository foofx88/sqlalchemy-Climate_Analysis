#import all dependencies
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify, render_template

#declare variables and prepare hawaii sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
a_year_ago = dt.date(2017, 8, 23)
year_range = a_year_ago - dt.timedelta(days=365)

#Flask setup
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)
app = Flask(__name__)

#Flask routes
#main index to return all different routes
@app.route("/")
def index():
    return (
        f"Routes:<br />"
        f"<br />"
        f"/api/v1.0/precipitation<br />"
        f"/api/v1.0/stations<br />"
        f"/api/v1.0/tobs<br />"
        f"/api/v1.0/temp/start/end<br />"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_range).all()
    precip = {}
    for result in prcp_query:
        prcp_list = {result.date: result.prcp, "prcp": result.prcp}
        precip.update(prcp_list)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def station():
    stations_list = session.query(Station.station).all()
    stationz = list(np.ravel(stations_list))
    return jsonify(stationz)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_range).all()
    tobs_list = list(np.ravel(tobs_query))
    return jsonify(tobs_list)

@app.route("/api/v1.0/temp/<start>")
def starts():
    # Only calculating TMIN, TAVG, and TMAX for all dates >= start date.
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    session.close()

    temps = []
    for result in results:
        row = {}
        row["TMIN"] = result[0]
        row["TMAX"] = result[1]
        row["TAVG"] = result[2]

        temps.append(row)

    return jsonify(temps)
    
@app.route("/api/v1.0/temp/<start>/<end>")
#using function from ipynb to get data for start and end
def calc_temps(start, end):
    """TMIN, TAVG, and TMAX for a list of dates.
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """

    if end != "":
        temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
            func.max(Measurement.tobs)).filter(Measurement.date.between(year_range, a_year_ago)).all()
        t_stats = list(np.ravel(temp_stats))
        return jsonify(temp_stats)

    else:
        temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
            func.max(Measurement.tobs)).filter(Measurement.date > a_year_ago).all()
        t_stats = list(np.ravel(temp_stats))
        return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True)