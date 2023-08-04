def Monitoring():

    def get_system_info():
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        memory_total = memory_info.total / (1024.0 ** 3)  # convert bytes to GB
        memory_used = memory_info.used / (1024.0 ** 3)
        memory_percent = memory_info.percent

        total, used, free = shutil.disk_usage("F:")
        total=total // (2**30)
        used=used // (2**30)
        free=free // (2**30)
        return cpu_percent, memory_total, memory_used, memory_percent, total, used, free

    #header
    st.markdown("""
    <style>
    .big-font {
    font-size:50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">😃 Scanner Monitoring Dashboard 😃</p>', unsafe_allow_html=True)

    cpu_placeholder = st.empty()

    # Use columns for memory and storage placeholders
    mem_storage_col1, mem_storage_col2 = st.columns(2)
    memory_placeholder = mem_storage_col1.empty()
    storage_placeholder = mem_storage_col2.empty()

    #refresh page
    while True:
        cpu_percent, memory_total, memory_used, memory_percent, total, used, free = get_system_info()
        cpu_placeholder.metric(label="🖥️ CPU Usage 🖥️", value=f"{cpu_percent}%", delta=None)
        memory_placeholder.metric(label="🧠 RAM Usage 🧠", value=f"{memory_used:.2f} GB / {memory_total:.2f} GB", delta=f"{memory_percent}%")
        storage_placeholder.metric(label="💽 ROM Usage 💽", value=f"{used:.2f} GB / {total:.2f} GB", delta=f"{free} GB")

        # Set a delay between loops
        time.sleep(2)


def mapping_demo():
    

    st.markdown(f"# {list(page_names_to_funcs.keys())[3]}")
    st.write(
        """
        This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
to display geospatial data.
"""
    )

    @st.cache_data
    def from_data_file(filename):
        url = (
            "http://raw.githubusercontent.com/streamlit/"
            "example-data/master/hello/v1/%s" % filename
        )
        return pd.read_json(url)

    try:
        ALL_LAYERS = {
            "Bike Rentals": pdk.Layer(
                "HexagonLayer",
                data=from_data_file("bike_rental_stats.json"),
                get_position=["lon", "lat"],
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                extruded=True,
            ),
            "Bart Stop Exits": pdk.Layer(
                "ScatterplotLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius="[exits]",
                radius_scale=0.05,
            ),
            "Bart Stop Names": pdk.Layer(
                "TextLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_text="name",
                get_color=[0, 0, 0, 200],
                get_size=15,
                get_alignment_baseline="'bottom'",
            ),
            "Outbound Flow": pdk.Layer(
                "ArcLayer",
                data=from_data_file("bart_path_stats.json"),
                get_source_position=["lon", "lat"],
                get_target_position=["lon2", "lat2"],
                get_source_color=[200, 30, 0, 160],
                get_target_color=[200, 30, 0, 160],
                auto_highlight=True,
                width_scale=0.0001,
                get_width="outbound",
                width_min_pixels=3,
                width_max_pixels=30,
            ),
        }
        st.sidebar.markdown("### Map Layers")
        selected_layers = [
            layer
            for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)
        ]
        if selected_layers:
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v9",
                    initial_view_state={
                        "latitude": 37.76,
                        "longitude": -122.4,
                        "zoom": 11,
                        "pitch": 50,
                    },
                    layers=selected_layers,
                )
            )
        else:
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

def Plot():

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This page illustrates a combination of plotting and animation. We're generating a bunch of number of documents per date in a loop. Enjoy!
"""
    )

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    
    st.line_chart(df_time)

    progress_bar.empty()
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write('Today was scanned: ', today_date)
    with col2:
        st.write('Yesterday and today was scanned: ', yesterday_date)

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


def DateFrame():
    global df
    if "default" not in st.session_state:
        st.session_state["default"] = ["",[year_start,year_end] ]
    

    zero_time = datetime.min.time()
    one_time = datetime.max.time()
    st.markdown(f"# {list(page_names_to_funcs.keys())[0]}")
    st.write(
        """
        This page shows info about scanned files in time by territories
        """
    )

    


    
    all = st.checkbox("Select all regions")
    territories = st.multiselect(
        "Choose territories", list(df.territory.unique()), ["Lviv"]
    )
    if all:
        territories=list(df.territory.unique())

    filters['territory']=territories

    for col, value in filters.items():
        if value == 'All':  # Skip if value is 'All'
            continue
        elif isinstance(value, list):  # If the value is a list, use isin
            df = df[df[col].isin(value)]
        else:  # Otherwise, use equality
            df = df[df[col] == value]


    time_input=st.date_input('Choose date limits:', st.session_state["default"][1])
    
    button=st.button('Clear dates')
    
    
    
    if button:
        st.session_state["default"][1]=[year_start,year_end]
        filters['dateandtime']='All'
        st.session_state["default"][0]="**:blue[Done]**"
        st.experimental_rerun()
        #st.date_input('Choose date limits:', [])=[]

    if len(time_input)!=2: 
        pass
    else:
        start_date, end_date = time_input
        if start_date <= end_date:
            pass
        else:
            st.error('Error: DateStart is greater then DateEnd.')
        mask = (df['dateandtime'] > datetime.combine(start_date, zero_time)) & (df['dateandtime'] <= datetime.combine(end_date, one_time))
        df=df.loc[mask]

    st.write("### Table of scanned documents", df)

    for col, value in filters.items():
        if value == 'All':  # Skip if value is 'All'
            continue
        elif isinstance(value, list):  # If the value is a list, use isin
            df = df[df[col].isin(value)]
        else:  # Otherwise, use equality
            df = df[df[col] == value]

    if df.empty==True:
        pass
    else:
        sizes=list(df.territory[df['territory']==territories[i]].count() for i in range(len(territories)))

        
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes,  labels=territories, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)
        
   
   
        #st.dataframe(df)

        # data = data.T.reset_index()
        # data = pd.melt(data, id_vars=["index"]).rename(
        #     columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        # )
        # chart = (
        #     alt.Chart(data)
        #     .mark_area(opacity=0.3)
        #     .encode(
        #         x="year:T",
        #         y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
        #         color="Region:N",
        #     )
        # )
        # st.altair_chart(chart, use_container_width=True)


import warnings
warnings.filterwarnings("ignore")
from datetime import date
from datetime import datetime
import matplotlib.pyplot as plt
import pydeck as pdk
from urllib.error import URLError
import streamlit as st
import psutil
import time
import shutil
import pandas as pd
import numpy as np
from PsqlConnect import connect
global con, cursor, df, df_time, filters , year_start , year_end, today_date, yesterday_date
_ , con= connect()
cursor = con.cursor()
epoch_year = date.today().year
year_start = date(epoch_year, 1, 1)
year_end = date(epoch_year, 12, 31)




@st.cache_data
def get_data():
    df=pd.read_sql_query("""SELECT * FROM scantable order by dateandtime desc --limit 10000""", con)
    df['territory'].replace([0,1,2], ['Lviv', 'Mukachevo','Sambir'], inplace=True)


    df_time=pd.read_sql_query("""select dateandtime::date as ds, count(id) as y from scantable group by dateandtime::date order by ds asc;""", con)
    df_time['ds']=df_time['ds'].apply(pd.to_datetime)
    df_time.set_index(df_time['ds'], inplace=True)

    start=df_time['ds'][0]
    end=df_time['ds'][len(df_time)-1]
    date_range=pd.date_range(start=start, end=end, freq='D')
    df_date_range=pd.DataFrame(date_range, columns=['ds'])
    df_date_range.set_index('ds', inplace=True)
    df_full=df_date_range.join(df_time,how='left', on='ds')
    df_full.drop(columns=['ds'], inplace=True)
    df_full['y'].fillna(value=0, inplace=True)
    df_time=df_full


    cursor.execute('select count(*) from scantable where dateandtime::date >now();')
    today_date = cursor.fetchone()[0]
    cursor.execute("select count(*) from scantable where dateandtime::date >now()- interval '1 day';")
    yesterday_date = cursor.fetchone()[0]



    return df, df_time, today_date, yesterday_date

df, df_time, today_date, yesterday_date=get_data()

filters = {
   'dateandtime': 'All',
   'territory': 'All'
}

page_names_to_funcs = {
    "DataFrame": DateFrame,
    "Plotting": Plot,
    "Monitoring": Monitoring
    
    
}
#"Mapping Demo": mapping_demo
pages = st.sidebar.selectbox("Choose a page", page_names_to_funcs.keys())
page_names_to_funcs[pages]()

