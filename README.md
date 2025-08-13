# Final-Project - Documentation

Urban Heat Island (UHI) – Analysis and
Visualization for Austria with WebGIS/Python
1. State of the Art
The Urban Heat Island (UHI) effect is a well-documented phenomenon in which
urban areas experience elevated temperatures compared to their surrounding rural
areas. This difference arises due to factors such as high building density,
impervious surfaces, reduced vegetation cover, and anthropogenic heat sources.
UHI research has been ongoing for several decades, with a wealth of
peer-reviewed studies and reports highlighting its implications for urban planning,
public health, and climate adaptation strategies. Satellite-based remote sensing
has played a central role in UHI studies. Instruments like Landsat Thermal Infrared
Sensor (TIRS) and MODIS (Moderate Resolution Imaging Spectroradiometer)
provide valuable surface temperature measurements, allowing for regional and
temporal comparisons. However, satellite overpass frequency limits real-time
analysis, which is often crucial for heatwave monitoring. In parallel, meteorological
station networks, both governmental and private, deliver high-frequency weather
data but with limited spatial coverage. Integrating these two data sources—broad
spatial coverage from satellites and high temporal resolution from
stations—remains a challenge. In recent years, machine learning models have
been used to fuse different datasets, providing improved spatiotemporal resolution.
Web-based GIS (WebGIS) systems have emerged as a powerful way to
communicate UHI findings to stakeholders. Unlike desktop GIS applications such
as ArcGIS or QGIS, WebGIS platforms run in browsers and require no installation,
making them more accessible. Tools such as Leaflet.js, Mapbox GL JS, and
OpenLayers are commonly used to build such interactive systems. In Austria,
studies on UHI have been conducted in cities like Vienna, Graz, and Linz, often
linked to EU-funded projects or national climate adaptation programs. However,
these efforts are usually city-specific and lack a unified, interactive, nationwide
platform. This gap presents an opportunity for developing an easy-to-use,
Austria-wide WebGIS that can present both current weather and temperature
forecasts alongside UHI indicators.
2. Problem Statement
A persistent difficulty in UHI analysis lies in acquiring datasets that are both
spatially detailed and temporally current. For example, while Landsat can capture
thermal imagery at 30–100 m resolution, it only revisits a given location every 16
days, and cloud cover can further limit usable data. This means that during critical
events like heatwaves, relevant satellite data may not be available. On the other
hand, meteorological stations provide continuous, near-real-time readings but are
often spaced too far apart to capture microclimatic variations within urban areas.
This creates a mismatch between spatial and temporal coverage, which limits the
ability to provide actionable insights for city planners, emergency services, and the
general public. A second challenge lies in data accessibility. While professional
analysts can process raw satellite data and interpret complex GIS layers,
non-expert users—including local government officials or citizens—often require
simplified, visually intuitive platforms. Many existing portals focus on static maps or
raw data downloads, missing the opportunity to provide interactive exploration and
instant feedback. Finally, forecasting capability is often missing in public UHI tools.
Knowing the current temperature pattern is helpful, but anticipating changes over
the next several days can greatly enhance preparedness. This is particularly
relevant for public health, as vulnerable populations can be warned in advance of
dangerous heat conditions.
3. Objective / Question
The objective of this project was to design and implement a WebGIS application
that bridges the gap between scientific analysis and public accessibility for
UHI-related data. The goals included: 1. Mapping Austria at the NUTS-3
administrative level, providing a nationwide view of regional differences. 2.
Assigning a Land Surface Temperature (LST) value to each region, using synthetic
data as a placeholder for real satellite measurements. 3. Integrating live weather
data from an open-source API to display temperature, apparent temperature,
humidity, and wind speed. 4. Incorporating a 5-day weather forecast to provide
forward-looking insights, with minimum and maximum daily temperatures and
precipitation totals. 5. Ensuring the application runs entirely in a web browser
without requiring users to install additional software or possess GIS expertise. The
guiding research question was: How can a lightweight, browser-based mapping
application be developed to effectively combine current and forecasted weather
data with UHI indicators for the whole of Austria, in a way that remains
understandable and accessible to a non-specialist audience?
4. Method
4.1. Data Sources - Administrative boundaries (NUTS-3): Downloaded via the
GISCO service from the European Commission. These boundaries were provided
in GeoJSON format and referenced in EPSG:4326 (WGS84) for compatibility with
web mapping tools. - Weather data and forecasts: Retrieved from the Open-Meteo
API, a free service that requires no authentication key. It provides both current and
forecasted weather parameters in JSON format. - LST data: Generated
synthetically using Python’s NumPy library to simulate regional variation. The
method involved creating a temperature gradient across Austria and adding
random noise to mimic spatial heterogeneity. 4.2. Software & Libraries - Backend:
Python with Flask for the web server, GeoPandas for spatial operations, Rasterio
for raster handling, Requests for API calls, and NumPy for numerical processing. -
Frontend: Leaflet.js for interactive maps, HTML5 and CSS3 for layout and styling,
and vanilla JavaScript for asynchronous data fetching. - Development
environment: Python virtual environment for dependency isolation, and Git for
version control. 4.3. Implementation Steps 1. Set up project structure with clear
separation of backend services, static frontend files, and data storage. 2.
Implement backend API routes: - `/api/neighborhoods`: Returns the NUTS-3
boundaries enriched with synthetic LST statistics. - `/api/weather`: Fetches and
returns current weather data for given coordinates. - `/api/forecast`: Fetches and
returns a 5-day forecast for given coordinates. 3. Generate synthetic raster and
calculate mean LST per region by intersecting boundaries with the raster. 4.
Develop the Leaflet-based frontend map, styling regions by their LST values with a
color scale and adding click events to trigger data requests. 5. Implement a sidebar
to display the selected region’s LST data, current weather conditions, and forecast
in a tabular format. 6. Test across multiple browsers and screen sizes to ensure
compatibility and responsiveness.
5. Results
The final application meets all stated objectives and offers the following
functionality: - Interactive map of Austria, segmented by NUTS-3 boundaries. -
Each region is colored according to its average synthetic LST, allowing for
immediate visual comparison. - Clicking a region triggers API calls to display both
current weather and a 5-day forecast in the sidebar. - The system retrieves live
data from Open-Meteo at the time of user interaction, ensuring freshness. The
application is designed to be easily extendable. The synthetic LST raster can be
replaced with actual satellite-derived datasets without altering the frontend or most
backend code. Additional indicators, such as hourly forecasts, air quality metrics,
or climate model projections, could be integrated with minimal restructuring. In
conclusion, the project successfully demonstrates a browser-based, accessible,
and informative approach to visualizing UHI indicators alongside weather
information for an entire country. While the current version uses simulated LST
data, it lays a solid foundation for operational deployment with real datasets. This
could be valuable for government agencies, urban planners, researchers, and
even the general public in preparing for and mitigating the impacts of extreme heat
events.
