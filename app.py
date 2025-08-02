import streamlit as st
import pandas as pd

from crud import curobj
from dblogic import DB
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
# creating sidebar
st.sidebar.title("Flights Analytics")
# creating drop down menu in sidebar and when user selects any option
# then we store that option into some variable.
user_option = st.sidebar.selectbox('Menu',['Select One','Check Flights','Analytics'])

# creating an object of class
db_obj = DB()
# now this object can access all the methods of class DB.

# now based on user_option we will create navigation stuff like if usre selects Check Flights
# option then we navigate to that page.
if user_option == 'Select One':
    st.title("Discover Flight Insights")

    # --- Place your image loading and display code here ---
    try:
        # REPLACE 'your_image_name.png' with the actual file name of your image
        # and adjust the path if it's in a subfolder (e.g., 'images/your_image_name.png')
        image = Image.open(r'C:\Users\Adnan khalid\PycharmProjects\PYTHON_MYSQL_FLIGHTS\Image_folder\flights_image.png')  # <--- Put your image path/filename here
        st.image(image, use_container_width=True)
    except FileNotFoundError:
        st.warning("Image file not found. Please ensure the image is in the correct path.")
    # --- End of image code ---

    st.write("This application is designed to provide insightful analytics and tools for exploring flight data.")
    st.markdown("---")

    st.header("What can you do here?")
    st.write("""
        This project offers two main functionalities:

        * **Check Flights:** Easily search for available flights between your desired source and destination cities. Get up-to-date information on flight routes.
        * **Analytics:** Dive deep into the flight dataset with interactive visualizations. Understand trends in airline frequency, identify the busiest airports, and observe daily flight patterns.
        """)

    st.header("Why this project?")
    st.write("""
        The aviation industry generates vast amounts of data, and analyzing this data can reveal valuable insights for various stakeholders, including:

        * **Travelers:** To understand flight availability and common routes.
        * **Airlines:** To optimize operations, identify popular routes, and manage resources effectively.
        * **Airport Authorities:** To assess airport traffic and plan for expansion or improvements.

        This project aims to demonstrate how data analytics can transform raw flight data into actionable intelligence.
        """)

    st.header("Technologies Used")
    st.write("""
        This application is built using:

        * **Python:** The core programming language for backend logic and data processing.
        * **MySQL:** As the database to store and manage flight data.
        * **Streamlit:** For creating the interactive web application.
        * **Plotly:** For generating compelling and interactive data visualizations.
        """)

    st.markdown("---")
    st.info("Select an option from the sidebar to start exploring flight data.")

elif user_option == 'Check Flights':
    st.title("Check Flights")
    col1, col2 = st.columns(2)
    cities = db_obj.fetch_city_names()
    with col1:
        src_city = st.selectbox('Source',cities)
    with col2:
        des_city = st.selectbox('Destination',cities)
    if st.button("Search"):
        if src_city == des_city:
            st.warning(f"SOURCE AND DESTINATION CAN NOT BE SAME!!!")
        else:
            col_list,result_set,row_count = db_obj.get_all_flights(src_city,des_city)

            if row_count >= 1:
                # st.dataframe(result_set) this thing only gives table rows not columns
                # so better to use pandas lib and follow below code.
                df = pd.DataFrame(result_set, columns = col_list)
                st.dataframe(df)
            else:
                st.info(f"No Flights Available From {src_city} To {des_city}")
else:
    st.title('Flight Data Analytics Dashboard')
    st.markdown('---')

    # making pie char to show the airlines and its frequency
    airlines, frequency = db_obj.fetch_airline_frequency()
    fig = go.Figure(
        go.Pie(
            labels = airlines,
            values = frequency,
            hoverinfo = 'label+percent',
            textinfo = "value"
        ) )

    st.subheader("Airline Distribution")  # heading for Pie Chart
    st.write("This chart shows the proportion of flights operated by different airlines.")
    st.markdown('---')
    st.plotly_chart(fig)

    # making barchart to show Top busiest airport cities.
    cities, tot_io_flights = db_obj.get_busiest_airports()

    fig = px.bar(
        x = cities,
        y = tot_io_flights,
        labels={'x': 'City', 'y': 'Total In/Out Flights'},
        title="Top Busiest Airport Cities"  # Title within the Plotly chart
    )
    st.subheader("Busiest Airport Cities")  # heading for Bar Chart
    st.write("This chart highlights the cities with the highest volume of incoming and outgoing flights.")
    st.markdown('---')
    st.plotly_chart(fig, theme=None, use_container_width=True)

    # making linechart to show daily frequency of flights.
    dates, frequency1 = db_obj.get_daily_frequency()

    fig = px.line(
        x = dates,
        y = frequency1,
        labels={'x': 'Date', 'y': 'Number of Flights'},
        title="Daily Flight Frequency"  # Title within the Plotly chart
    )
    st.subheader("Daily Flight Trends")  # heading for Line Chart
    st.write("This chart illustrates the number of flights on a daily basis.")
    st.markdown('---')
    st.plotly_chart(fig, theme=None, use_container_width=True)




