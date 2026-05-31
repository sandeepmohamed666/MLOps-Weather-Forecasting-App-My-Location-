# #==================================================
# # From Grok-Gemini
# #==================================================
import streamlit as st
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import os
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="MLOps Weather Forecasting App", page_icon="🌤️", layout="wide")

st.title("🌤️ Real-Time Weather Forecasting Dashboard")
st.markdown("This application fetches live weather forecasts using the Open-Meteo API, displays the metrics, and stores data locally.")

# ====================== SETUP OPEN-METEO CLIENT ======================
@st.cache_resource
def get_api_client():
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    return openmeteo_requests.Client(session=retry_session)

openmeteo = get_api_client()

# ====================== DATA FETCHING LOGIC ======================
def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 8.5241,
        "longitude": 76.9366,
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", 
                   "rain", "wind_speed_10m", "wind_direction_10m"],
    }
    
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    
    # Process hourly data
    hourly = response.Hourly()
    
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
    }
    
    hourly_data["temperature_2m"] = hourly.Variables(0).ValuesAsNumpy()
    hourly_data["relative_humidity_2m"] = hourly.Variables(1).ValuesAsNumpy()
    hourly_data["dew_point_2m"] = hourly.Variables(2).ValuesAsNumpy()
    hourly_data["rain"] = hourly.Variables(3).ValuesAsNumpy()
    hourly_data["wind_speed_10m"] = hourly.Variables(4).ValuesAsNumpy()
    hourly_data["wind_direction_10m"] = hourly.Variables(5).ValuesAsNumpy()
    
    df = pd.DataFrame(data=hourly_data)
    
    # Format date for better readability in the UI
    df["date"] = pd.to_datetime(df["date"]).dt.tz_convert(None)
    
    metadata = {
        "lat": response.Latitude(),
        "lon": response.Longitude(),
        "elevation": response.Elevation()
    }
    
    return df, metadata

# ====================== RENDER DASHBOARD ======================

# Fetch data
try:
    with st.spinner("Fetching data from Open-Meteo API..."):
        hourly_dataframe, meta = fetch_weather_data()
    
    # 1. Sidebar Metadata & Actions
    st.sidebar.header("📍 Location Metadata")
    st.sidebar.write(f"**Coordinates:** {meta['lat']:.4f}°N, {meta['lon']:.4f}°E")
    st.sidebar.write(f"**Elevation:** {meta['elevation']} m asl")
    
    # Map visualizer in the sidebar
    map_data = pd.DataFrame({'lat': [meta['lat']], 'lon': [meta['lon']]})
    st.sidebar.map(map_data, zoom=10)
    
    # Save to local folder functionality
    if st.sidebar.button("💾 Trigger Local Ingestion Save"):
        data_folder = "data"
        os.makedirs(data_folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"weather_thiruvananthapuram_{timestamp}.csv"
        csv_path = os.path.join(data_folder, csv_filename)
        
        hourly_dataframe.to_csv(csv_path, index=False)
        st.sidebar.success(f"Saved locally to: `{csv_path}`")

    # 2. Key Metrics Row (Using average or current data point)
    st.subheader("📊 Current Forecast Highlights (Averages)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Temp (°C)", f"{hourly_dataframe['temperature_2m'].mean().round(1)}°C")
    col2.metric("Avg Humidity (%)", f"{hourly_dataframe['relative_humidity_2m'].mean().round(1)}%")
    col3.metric("Total Expected Rain (mm)", f"{hourly_dataframe['rain'].sum().round(1)} mm")
    col4.metric("Avg Wind Speed (km/h)", f"{hourly_dataframe['wind_speed_10m'].mean().round(1)} km/h")

    # 3. Interactive Chart
    st.subheader("📈 Temperature Trend Over Time")
    st.line_chart(data=hourly_dataframe, x="date", y="temperature_2m", use_container_width=True)

    # 4. Data Preview & Download
    st.subheader("📋 Forecast Data Preview")
    st.dataframe(hourly_dataframe, use_container_width=True)
    
    # Browser CSV download option
    csv_bytes = hourly_dataframe.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Dataset as CSV",
        data=csv_bytes,
        file_name=f"weather_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"Failed to fetch data or render the app. Error: {e}")


# # # #==================================================
# # # # From Grok-deepseek
# # # #==================================================

# # app.py - Streamlit Weather Dashboard for Thiruvananthapuram

# import openmeteo_requests
# import pandas as pd
# import requests_cache
# from retry_requests import retry
# import os
# from datetime import datetime
# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go

# # ====================== PAGE CONFIGURATION ======================
# st.set_page_config(
#     page_title="Weather Dashboard - Thiruvananthapuram",
#     page_icon="🌤️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ====================== CACHE DATA LOADING ======================
# @st.cache_data(ttl=3600)  # Cache data for 1 hour
# def fetch_weather_data():
#     """Fetch weather data from Open-Meteo API"""
    
#     # Create 'data' folder if it doesn't exist
#     data_folder = "data"
#     os.makedirs(data_folder, exist_ok=True)
    
#     # Setup Open-Meteo client
#     cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#     retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#     openmeteo = openmeteo_requests.Client(session=retry_session)
    
#     # API request parameters for Thiruvananthapuram
#     url = "https://api.open-meteo.com/v1/forecast"
#     params = {
#         "latitude": 8.5241,
#         "longitude": 76.9366,
#         "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", 
#                    "rain", "wind_speed_10m", "wind_direction_10m"],
#     }
    
#     try:
#         responses = openmeteo.weather_api(url, params=params)
#         response = responses[0]
        
#         # Process hourly data
#         hourly = response.Hourly()
        
#         hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
#         hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
#         hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
#         hourly_rain = hourly.Variables(3).ValuesAsNumpy()
#         hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
#         hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()
        
#         hourly_data = {
#             "date": pd.date_range(
#                 start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
#                 end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
#                 freq=pd.Timedelta(seconds=hourly.Interval()),
#                 inclusive="left"
#             )
#         }
        
#         hourly_data["temperature_2m"] = hourly_temperature_2m
#         hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
#         hourly_data["dew_point_2m"] = hourly_dew_point_2m
#         hourly_data["rain"] = hourly_rain
#         hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
#         hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
        
#         df = pd.DataFrame(data=hourly_data)
        
#         # Save to CSV with timestamp
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         csv_filename = f"weather_thiruvananthapuram_{timestamp}.csv"
#         csv_path = os.path.join(data_folder, csv_filename)
#         df.to_csv(csv_path, index=False)
        
#         return df, response.Latitude(), response.Longitude(), response.Elevation()
        
#     except Exception as e:
#         st.error(f"Error fetching weather data: {str(e)}")
#         return None, None, None, None

# # ====================== MAIN APP ======================
# def main():
#     # Header
#     st.title("🌤️ Weather Forecast Dashboard")
#     st.markdown("### Thiruvananthapuram, Kerala, India")
#     st.markdown("---")
    
#     # Fetch data
#     with st.spinner("Fetching latest weather data..."):
#         df, lat, lon, elevation = fetch_weather_data()
    
#     if df is None:
#         st.error("Failed to load weather data. Please try again later.")
#         return
    
#     # Display location info in sidebar
#     with st.sidebar:
#         st.header("📍 Location Info")
#         st.metric("Latitude", f"{lat:.4f}°N" if lat else "N/A")
#         st.metric("Longitude", f"{lon:.4f}°E" if lon else "N/A")
#         st.metric("Elevation", f"{elevation:.0f} m asl" if elevation else "N/A")
        
#         st.header("📊 Data Overview")
#         st.metric("Total Records", len(df))
#         st.metric("Date Range", f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
        
#         st.header("💾 Data Export")
#         csv_export = df.to_csv(index=False)
#         st.download_button(
#             label="📥 Download CSV",
#             data=csv_export,
#             file_name=f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
#             mime="text/csv"
#         )
    
#     # Main content area with tabs
#     tab1, tab2, tab3, tab4, tab5 = st.tabs([
#         "📈 Temperature", "💧 Humidity", "🌧️ Rainfall", 
#         "💨 Wind", "📋 Raw Data"
#     ])
    
#     with tab1:
#         st.subheader("Temperature Analysis")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Temperature line chart
#             fig_temp = px.line(
#                 df, x="date", y="temperature_2m",
#                 title="Temperature Trend",
#                 labels={"date": "Time", "temperature_2m": "Temperature (°C)"},
#                 color_discrete_sequence=["#ff6b6b"]
#             )
#             fig_temp.update_layout(hovermode='x unified')
#             st.plotly_chart(fig_temp, use_container_width=True)
        
#         with col2:
#             # Temperature metrics
#             current_temp = df['temperature_2m'].iloc[-1]
#             max_temp = df['temperature_2m'].max()
#             min_temp = df['temperature_2m'].min()
#             avg_temp = df['temperature_2m'].mean()
            
#             st.metric("Current Temperature", f"{current_temp:.1f}°C")
#             st.metric("Maximum Temperature", f"{max_temp:.1f}°C")
#             st.metric("Minimum Temperature", f"{min_temp:.1f}°C")
#             st.metric("Average Temperature", f"{avg_temp:.1f}°C")
        
#         # Temperature histogram
#         fig_hist = px.histogram(
#             df, x="temperature_2m", 
#             title="Temperature Distribution",
#             labels={"temperature_2m": "Temperature (°C)", "count": "Frequency"},
#             color_discrete_sequence=["#ff6b6b"]
#         )
#         st.plotly_chart(fig_hist, use_container_width=True)
    
#     with tab2:
#         st.subheader("Humidity Analysis")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Humidity line chart
#             fig_humidity = px.line(
#                 df, x="date", y="relative_humidity_2m",
#                 title="Humidity Trend",
#                 labels={"date": "Time", "relative_humidity_2m": "Relative Humidity (%)"},
#                 color_discrete_sequence=["#4ecdc4"]
#             )
#             fig_humidity.update_layout(hovermode='x unified')
#             st.plotly_chart(fig_humidity, use_container_width=True)
        
#         with col2:
#             # Humidity metrics
#             current_humidity = df['relative_humidity_2m'].iloc[-1]
#             max_humidity = df['relative_humidity_2m'].max()
#             min_humidity = df['relative_humidity_2m'].min()
#             avg_humidity = df['relative_humidity_2m'].mean()
            
#             st.metric("Current Humidity", f"{current_humidity:.1f}%")
#             st.metric("Maximum Humidity", f"{max_humidity:.1f}%")
#             st.metric("Minimum Humidity", f"{min_humidity:.1f}%")
#             st.metric("Average Humidity", f"{avg_humidity:.1f}%")
        
#         # Humidity vs Temperature scatter plot
#         fig_scatter = px.scatter(
#             df, x="temperature_2m", y="relative_humidity_2m",
#             title="Humidity vs Temperature",
#             labels={"temperature_2m": "Temperature (°C)", "relative_humidity_2m": "Relative Humidity (%)"},
#             color="temperature_2m",
#             color_continuous_scale="Viridis"
#         )
#         st.plotly_chart(fig_scatter, use_container_width=True)
    
#     with tab3:
#         st.subheader("Rainfall Analysis")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Rainfall bar chart
#             fig_rain = px.bar(
#                 df, x="date", y="rain",
#                 title="Rainfall Intensity",
#                 labels={"date": "Time", "rain": "Rainfall (mm)"},
#                 color_discrete_sequence=["#45b7d1"]
#             )
#             fig_rain.update_layout(hovermode='x unified')
#             st.plotly_chart(fig_rain, use_container_width=True)
        
#         with col2:
#             # Rainfall metrics
#             total_rain = df['rain'].sum()
#             max_rain = df['rain'].max()
#             rainy_hours = (df['rain'] > 0).sum()
            
#             st.metric("Total Rainfall", f"{total_rain:.1f} mm")
#             st.metric("Maximum Rainfall (per hour)", f"{max_rain:.1f} mm")
#             st.metric("Rainy Hours", rainy_hours)
#             st.metric("Rain Probability", f"{(rainy_hours/len(df))*100:.1f}%")
        
#         # Rainfall intensity distribution
#         df_rainy = df[df['rain'] > 0]
#         if len(df_rainy) > 0:
#             fig_rain_dist = px.histogram(
#                 df_rainy, x="rain", nbins=20,
#                 title="Rainfall Intensity Distribution",
#                 labels={"rain": "Rainfall (mm)", "count": "Frequency"},
#                 color_discrete_sequence=["#45b7d1"]
#             )
#             st.plotly_chart(fig_rain_dist, use_container_width=True)
    
#     with tab4:
#         st.subheader("Wind Analysis")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Wind speed line chart
#             fig_wind = px.line(
#                 df, x="date", y="wind_speed_10m",
#                 title="Wind Speed Trend",
#                 labels={"date": "Time", "wind_speed_10m": "Wind Speed (km/h)"},
#                 color_discrete_sequence=["#f9ca24"]
#             )
#             fig_wind.update_layout(hovermode='x unified')
#             st.plotly_chart(fig_wind, use_container_width=True)
        
#         with col2:
#             # Wind metrics
#             current_wind = df['wind_speed_10m'].iloc[-1]
#             max_wind = df['wind_speed_10m'].max()
#             avg_wind = df['wind_speed_10m'].mean()
            
#             st.metric("Current Wind Speed", f"{current_wind:.1f} km/h")
#             st.metric("Maximum Wind Speed", f"{max_wind:.1f} km/h")
#             st.metric("Average Wind Speed", f"{avg_wind:.1f} km/h")
        
#         # Wind rose (directional distribution)
#         fig_wind_rose = px.bar_polar(
#             df, r="wind_speed_10m", theta="wind_direction_10m",
#             title="Wind Direction Distribution",
#             color="wind_speed_10m",
#             color_continuous_scale="Viridis",
#             template="plotly_dark"
#         )
#         st.plotly_chart(fig_wind_rose, use_container_width=True)
        
#         # Combined wind speed and direction
#         fig_wind_scatter = px.scatter(
#             df, x="date", y="wind_speed_10m", 
#             color="wind_direction_10m",
#             title="Wind Speed Colored by Direction",
#             labels={"date": "Time", "wind_speed_10m": "Wind Speed (km/h)", 
#                    "wind_direction_10m": "Direction (°)"},
#             color_continuous_scale="Viridis"
#         )
#         st.plotly_chart(fig_wind_scatter, use_container_width=True)
    
#     with tab5:
#         st.subheader("Raw Weather Data")
        
#         # Date range selector
#         col1, col2 = st.columns(2)
#         with col1:
#             start_date = st.date_input("Start Date", df['date'].min())
#         with col2:
#             end_date = st.date_input("End Date", df['date'].max())
        
#         # Filter data
#         mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
#         filtered_df = df[mask]
        
#         # Display dataframe
#         st.dataframe(
#             filtered_df,
#             use_container_width=True,
#             hide_index=True,
#             column_config={
#                 "date": st.column_config.DatetimeColumn("Date/Time"),
#                 "temperature_2m": st.column_config.NumberColumn("Temperature (°C)", format="%.1f"),
#                 "relative_humidity_2m": st.column_config.NumberColumn("Humidity (%)", format="%.1f"),
#                 "dew_point_2m": st.column_config.NumberColumn("Dew Point (°C)", format="%.1f"),
#                 "rain": st.column_config.NumberColumn("Rain (mm)", format="%.2f"),
#                 "wind_speed_10m": st.column_config.NumberColumn("Wind Speed (km/h)", format="%.1f"),
#                 "wind_direction_10m": st.column_config.NumberColumn("Wind Direction (°)", format="%.0f")
#             }
#         )
        
#         # Statistics
#         st.subheader("Statistical Summary")
#         st.dataframe(filtered_df.describe(), use_container_width=True)
    
#     # Footer
#     st.markdown("---")
#     st.markdown(
#         f"<div style='text-align: center; color: gray;'>"
#         f"Data fetched from Open-Meteo API • Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
#         f"</div>",
#         unsafe_allow_html=True
#     )

# if __name__ == "__main__":
#     main()

# # #==================================================
# # # From Grok-Grok
# # #==================================================
# import streamlit as st
# import openmeteo_requests
# import pandas as pd
# import requests_cache
# from retry_requests import retry
# import os
# from datetime import datetime

# # ====================== PAGE CONFIG ======================
# st.set_page_config(
#     page_title="Weather Forecast - Thiruvananthapuram",
#     page_icon="🌤️",
#     layout="wide"
# )

# st.title("🌤️ Weather Forecast Dashboard")
# st.markdown("### Real-time Weather Data from Open-Meteo API")

# # ====================== SIDEBAR ======================
# st.sidebar.header("Location Settings")
# latitude = st.sidebar.number_input("Latitude", value=8.5241, format="%.4f")
# longitude = st.sidebar.number_input("Longitude", value=76.9366, format="%.4f")

# if st.sidebar.button("🔄 Fetch Latest Weather Data", type="primary"):
#     with st.spinner("Fetching weather data..."):
#         try:
#             # ====================== SETUP CLIENT ======================
#             cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#             retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#             openmeteo = openmeteo_requests.Client(session=retry_session)

#             # ====================== API REQUEST ======================
#             url = "https://api.open-meteo.com/v1/forecast"
#             params = {
#                 "latitude": latitude,
#                 "longitude": longitude,
#                 "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m",
#                           "rain", "wind_speed_10m", "wind_direction_10m"],
#             }

#             responses = openmeteo.weather_api(url, params=params)
#             response = responses[0]

#             # ====================== PROCESS DATA ======================
#             hourly = response.Hourly()

#             hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
#             hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
#             hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
#             hourly_rain = hourly.Variables(3).ValuesAsNumpy()
#             hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
#             hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()

#             hourly_data = {
#                 "date": pd.date_range(
#                     start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
#                     end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
#                     freq=pd.Timedelta(seconds=hourly.Interval()),
#                     inclusive="left"
#                 )
#             }

#             hourly_data["temperature_2m"] = hourly_temperature_2m
#             hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
#             hourly_data["dew_point_2m"] = hourly_dew_point_2m
#             hourly_data["rain"] = hourly_rain
#             hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
#             hourly_data["wind_direction_10m"] = hourly_wind_direction_10m

#             df = pd.DataFrame(data=hourly_data)

#             # ====================== SAVE CSV ======================
#             data_folder = "data"
#             os.makedirs(data_folder, exist_ok=True)
            
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             csv_filename = f"weather_{latitude}_{longitude}_{timestamp}.csv"
#             csv_path = os.path.join(data_folder, csv_filename)
#             df.to_csv(csv_path, index=False)

#             # ====================== DISPLAY RESULTS ======================
#             st.success("✅ Data fetched successfully!")

#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.metric("Latitude", f"{response.Latitude():.4f}°")
#             with col2:
#                 st.metric("Longitude", f"{response.Longitude():.4f}°")
#             with col3:
#                 st.metric("Elevation", f"{response.Elevation()} m")

#             st.subheader("Hourly Weather Data")
#             st.dataframe(df.head(24), use_container_width=True)  # Show next 24 hours

#             # Download button
#             csv_data = df.to_csv(index=False).encode('utf-8')
#             st.download_button(
#                 label="📥 Download Full Data as CSV",
#                 data=csv_data,
#                 file_name=csv_filename,
#                 mime="text/csv"
#             )

#             # Preview statistics
#             st.subheader("Quick Statistics")
#             st.write(f"**Total Records:** {len(df)}")
#             st.write(f"**Temperature Range:** {df['temperature_2m'].min():.1f}°C to {df['temperature_2m'].max():.1f}°C")

#         except Exception as e:
#             st.error(f"Error fetching data: {str(e)}")
# else:
#     st.info("👈 Use the sidebar to fetch weather data")

# # Footer
# st.caption("Built with Streamlit + Open-Meteo API | Location: Thiruvananthapuram, Kerala")


# ##==================================================
# ## From Grok-coilot
# ##==================================================
# # app.py
# # ==================================================
# # Streamlit Weather Dashboard using Open-Meteo API
# # ==================================================
# import streamlit as st
# import openmeteo_requests
# import pandas as pd
# import requests_cache
# from retry_requests import retry
# import os
# from datetime import datetime
# import plotly.express as px

# # ====================== PAGE CONFIG ======================
# st.set_page_config(page_title="Weather Dashboard", layout="wide")
# st.title("🌤️ Real-Time Weather Data - Thiruvananthapuram")

# # ====================== CREATE DATA FOLDER ======================
# data_folder = "data"
# os.makedirs(data_folder, exist_ok=True)

# # ====================== SETUP OPEN-METEO CLIENT ======================
# cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
# retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
# openmeteo = openmeteo_requests.Client(session=retry_session)

# # ====================== API REQUEST ======================
# url = "https://api.open-meteo.com/v1/forecast"
# params = {
#     "latitude": 8.5241,
#     "longitude": 76.9366,
#     "hourly": [
#         "temperature_2m", "relative_humidity_2m", "dew_point_2m",
#         "rain", "wind_speed_10m", "wind_direction_10m"
#     ],
# }

# responses = openmeteo.weather_api(url, params=params)
# response = responses[0]

# # ====================== PROCESS HOURLY DATA ======================
# hourly = response.Hourly()
# hourly_data = {
#     "date": pd.date_range(
#         start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
#         end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
#         freq=pd.Timedelta(seconds=hourly.Interval()),
#         inclusive="left"
#     ),
#     "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
#     "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
#     "dew_point_2m": hourly.Variables(2).ValuesAsNumpy(),
#     "rain": hourly.Variables(3).ValuesAsNumpy(),
#     "wind_speed_10m": hourly.Variables(4).ValuesAsNumpy(),
#     "wind_direction_10m": hourly.Variables(5).ValuesAsNumpy(),
# }

# df = pd.DataFrame(hourly_data)

# # ====================== SAVE TO CSV ======================
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# csv_filename = f"weather_thiruvananthapuram_{timestamp}.csv"
# csv_path = os.path.join(data_folder, csv_filename)
# df.to_csv(csv_path, index=False)

# # ====================== DISPLAY DATA ======================
# st.success(f"✅ Data successfully saved to: {csv_path}")
# st.write(f"**Total records:** {len(df)}")
# st.dataframe(df.head())

# # ====================== VISUALIZATION ======================
# st.subheader("📊 Temperature & Humidity Trends")
# fig_temp = px.line(df, x="date", y="temperature_2m", title="Hourly Temperature (°C)")
# fig_humidity = px.line(df, x="date", y="relative_humidity_2m", title="Hourly Relative Humidity (%)")
# st.plotly_chart(fig_temp, use_container_width=True)
# st.plotly_chart(fig_humidity, use_container_width=True)

# # ====================== DOWNLOAD OPTION ======================
# st.download_button(
#     label="📥 Download CSV Data",
#     data=open(csv_path, "rb").read(),
#     file_name=csv_filename,
#     mime="text/csv"
# )


# # # #==================================================
# # # # From Grok-chatgpt
# # # #==================================================

# import streamlit as st
# import openmeteo_requests
# import pandas as pd
# import requests_cache
# from retry_requests import retry
# import os
# from datetime import datetime

# st.set_page_config(
#     page_title="Weather Data Downloader",
#     page_icon="🌦️",
#     layout="wide"
# )

# st.title("🌦️ Thiruvananthapuram Weather Data")
# st.write("Fetch hourly weather forecast data from Open-Meteo API and download as CSV.")

# # Create data folder
# data_folder = "data"
# os.makedirs(data_folder, exist_ok=True)

# # Setup Open-Meteo client
# cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
# retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
# openmeteo = openmeteo_requests.Client(session=retry_session)

# if st.button("Fetch Weather Data"):

#     with st.spinner("Fetching weather data..."):

#         url = "https://api.open-meteo.com/v1/forecast"

#         params = {
#             "latitude": 8.5241,
#             "longitude": 76.9366,
#             "hourly": [
#                 "temperature_2m",
#                 "relative_humidity_2m",
#                 "dew_point_2m",
#                 "rain",
#                 "wind_speed_10m",
#                 "wind_direction_10m"
#             ],
#         }

#         responses = openmeteo.weather_api(url, params=params)
#         response = responses[0]

#         st.success("Data fetched successfully!")

#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.metric("Latitude", f"{response.Latitude():.4f}")

#         with col2:
#             st.metric("Longitude", f"{response.Longitude():.4f}")

#         with col3:
#             st.metric("Elevation", f"{response.Elevation():.1f} m")

#         # Process hourly data
#         hourly = response.Hourly()

#         hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
#         hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
#         hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
#         hourly_rain = hourly.Variables(3).ValuesAsNumpy()
#         hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
#         hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()

#         hourly_data = {
#             "date": pd.date_range(
#                 start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
#                 end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
#                 freq=pd.Timedelta(seconds=hourly.Interval()),
#                 inclusive="left"
#             )
#         }

#         hourly_data["temperature_2m"] = hourly_temperature_2m
#         hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
#         hourly_data["dew_point_2m"] = hourly_dew_point_2m
#         hourly_data["rain"] = hourly_rain
#         hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
#         hourly_data["wind_direction_10m"] = hourly_wind_direction_10m

#         hourly_dataframe = pd.DataFrame(hourly_data)

#         # Save CSV
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         csv_filename = f"weather_thiruvananthapuram_{timestamp}.csv"
#         csv_path = os.path.join(data_folder, csv_filename)

#         hourly_dataframe.to_csv(csv_path, index=False)

#         st.subheader("Weather Data Preview")
#         st.dataframe(hourly_dataframe.head(20), use_container_width=True)

#         st.subheader("Temperature Trend")
#         st.line_chart(
#             hourly_dataframe.set_index("date")["temperature_2m"]
#         )

#         st.info(f"CSV saved locally as: {csv_path}")
#         st.write(f"Total Records: {len(hourly_dataframe)}")

#         # Download button
#         csv_data = hourly_dataframe.to_csv(index=False).encode("utf-8")

#         st.download_button(
#             label="📥 Download CSV",
#             data=csv_data,
#             file_name=csv_filename,
#             mime="text/csv"
#         )
