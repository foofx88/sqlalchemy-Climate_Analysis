<h3>SQLAlchemy - Climate Analysis and Exploration</h3>
<hr>

<p>Upon exploring the <a href="/Resources/hawaii.sqlite">dataset</a> and choosing a start and end date for the a trip</p>
<p>The date range is approximately 3-15 days total</p>
<p>Used the <a href="/climate_starter.ipynb">Jupyter Notebook</a> to perform the following:</p>
<ul>
  <li>Used SQLAlchemy's `create_engine` to connect to the dataset </li>
  <li>Used SQLAlchemy's `automap_base()` to reflect tables into classes and saved a reference to those classes called `Station` and `Measurement`</li>
  <li>Designed a Query to retrieve the last 12 months of precipitation data</li>
  <li>Load Query results into Pandas DataFrame and set index to date column</li>
  <li>Sort DataFrame values by Date</li>
  <li>Print the summary statistics and plot  the precipitation data</li>
  <img width="80%" src="/Output/precipitation.png">
  <li>Queried to calculate the total number of stations and the most active station</li>
  <li>Plot the temperature frequency at the most active station</li>
  <img height="60%" src="/Output/temp_freq.png">
</ul>

After completed initial analysis, a <a href="/climate_app.py">Flask API</a> was designed based on the above queries.

