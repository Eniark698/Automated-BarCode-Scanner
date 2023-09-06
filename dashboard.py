def DateFrame():
    df = get_data_dataframe()

    if "default" not in st.session_state:
        st.session_state["default"] = ["Lviv"] 
    if 'date_input' not in st.session_state:
        st.session_state['date_input'] = [monday, sunday]
    if 'disable_opt' not in st.session_state:
        st.session_state.disable_opt = False

    
    st.markdown(f"# {list(page_names_to_funcs.keys())[0]}")
    st.write(
        """
        Ця сторінка показує інформацію щодо просканованих файлів в часі по територіях.
        """
    )


    all = st.checkbox("Вибрати усі регіони")
    
    if all:
        st.session_state.disable_opt = True

        territories=list(df.territory.unique())
        st.session_state["default"]= territories
    else:
        st.session_state["default"] = ['Lviv']
        territories=['Lviv']
        st.session_state.disable_opt = False


    territories = st.multiselect(
        "Вибрати регіони", list(df.territory.unique()), st.session_state["default"], disabled = st.session_state.disable_opt
    )
    

    filters['territory']=territories

    for col, value in filters.items():
        if value == 'All':  # Skip if value is 'All'
            continue
        elif isinstance(value, list):  # If the value is a list, use isin
            df = df[df[col].isin(value)]
        else:  # Otherwise, use equality
            df = df[df[col] == value]


    time_input=st.date_input('Вибрати часові межі:', st.session_state["date_input"], format='DD/MM/YYYY')

    st.session_state['date_input'] = time_input

    button=st.button('Очистити часовий фільтр')
    
 
    if button:
        st.session_state['date_input'] = ()
        # st.session_state["default"][0]=[]
        filters['dateandtime']='All'
        st.experimental_rerun()
        #st.date_input('Choose date limits:', [])=[]

    
    
    if len(time_input)!=2: 
        
        try:
            mask = (df['dateandtime'] > datetime.combine(time_input[0], zero_time))
            df=df.loc[mask]
        except:
            try:
                mask =  (df['dateandtime'] <= datetime.combine(time_input[1], one_time))
                df=df.loc[mask]
            except:
                pass
        
    else:
        start_date, end_date = time_input
        if start_date <= end_date:
            pass
        else:
            st.error('Error: DateStart is greater then DateEnd.')
        mask = (df['dateandtime'] > datetime.combine(start_date, zero_time)) & (df['dateandtime'] <= datetime.combine(end_date, one_time))
        df=df.loc[mask]

   
    for col, value in filters.items():
        if value == 'All':  # Skip if value is 'All'
            continue
        elif isinstance(value, list):  # If the value is a list, use isin
            df = df[df[col].isin(value)]
        else:  # Otherwise, use equality
            df = df[df[col] == value]


    st.write("### Таблиця просканованих документів", df)

    cols_numbers=st.columns([1,1])
    with cols_numbers[0]:
        try:
            st.write('Сторінок : ', df['id'].nunique())
        except:
            st.write('Сторінок : ', df['id'].loc[mask].nunique())
    with cols_numbers[1]:
        try:
            st.write('Документів: ', df['barcode'].nunique())
        except:
            st.write('Документів: ', df['barcode'].loc[mask].nunique())

            

    cols = st.columns([1, 1])

    

    if df.empty==True:
            pass
    else:
        with cols[0]:
                df_drop = df.drop_duplicates(subset='barcode', keep='first')
                sizes=list(df_drop.territory[df_drop['territory']==territories[i]].count() for i in range(len(territories)))

                # fig1, ax1 = plt.subplots()
                # ax1.pie(sizes,  labels=territories, autopct='%1.1f%%',
                #         shadow=True, startangle=90)
                # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                # st.pyplot(fig1)
                # Create a new DataFrame for plotting
                df_pie = pd.DataFrame({
                    'Територія': territories,
                    'Кількість': sizes
                })

                # Create pie chart using Plotly Express
                fig1 = px.pie(df_pie, names='Територія', values='Кількість', 
                            title='Поширення листків по територіях',
                            hover_name='Територія', hover_data=['Кількість'])
                # fig1.update_layout(
                #     margin=dict(t=50, b=50, l=50, r=50),
                #     legend=dict(x=1.05, y=0.5, orientation='v')
                # )
                fig1.update_layout(showlegend=False)


                # Display the pie chart in Streamlit
                st.plotly_chart(fig1, config={'displayModeBar': True, 'modeBarButtonsToRemove': ['pan2d','select2d','lasso2d'], 'displaylogo': False, 'modeBarButtonsToAdd': ['resetScale2d'], 'modeBarButtonsPosition': 'left'})

           

            
        with cols[1]:
            sizes=list(df.territory[df['territory']==territories[i]].count() for i in range(len(territories)))

            # fig1, ax1 = plt.subplots()
            # ax1.pie(sizes,  labels=territories, autopct='%1.1f%%',
            #         shadow=True, startangle=90)
            # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # st.pyplot(fig1)
            # Create a new DataFrame for plotting
            df_pie = pd.DataFrame({
                'Територія': territories,
                'Кількість': sizes
            })

            # Create pie chart using Plotly Express
            fig2 = px.pie(df_pie, names='Територія', values='Кількість', 
                        title='Поширення документів по територіях',
                        hover_name='Територія', hover_data=['Кількість'])
            # fig2.update_layout(
            #     margin=dict(t=50, b=50, l=50, r=50),
            #     legend=dict(x=1.05, y=0.5, orientation='v')
            # )
            # Display the pie chart in Streamlit

            fig2.update_layout(
                legend=dict(
                    x=0,
                    y=1,
                    xanchor="left",
                    yanchor="top"
                )
            )
            st.plotly_chart(fig2, config={'displayModeBar': True, 'modeBarButtonsToRemove': ['pan2d','select2d','lasso2d'], 'displaylogo': False, 'modeBarButtonsToAdd': ['resetScale2d'], 'modeBarButtonsPosition': 'left'})


        #fig = px.pie(sizes, values='id', names='territory', title='Population of European continent')


    
   
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



def GeospatialAnalysis():
    df=get_data_dataframe()
    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write("Ця сторінка показує візуалізації карти розподілення документів по територіях (за весь час)")
    
    
    
    
    # locations should be generated from your actual data source
    locations = pd.DataFrame({
        'territory': ['Lviv', 'Mukachevo', 'Sambir', 'Ternopil', 'Vinnytsia', 'Zhytomyr', 'Rivne', 'Lutsk', 'Khmelnytskyi', 'Frankivsk', 'Chernivtsi'],
        'lat': [49.8382600, 48.4391900, 49.5183000, 49.5558900, 49.2327800, 50.2648700, 50.6230800, 50.7593200 , 49.4216100, 48.9215000, 48.2914900],
        'lon': [24.0232400, 22.7177900, 23.1975200, 25.6055600, 28.4809700, 28.6766900, 26.2274300, 25.3424400 , 26.9965300, 24.7097200, 25.9403400]
    })
    
    # Merge the df and locations dataframes on the 'territory' column
    df_drop = df.drop_duplicates(subset='barcode', keep='first')

    counts = df_drop.groupby('territory')['barcode'].count().reset_index()
    
    counts.columns = ['territory', 'count']

    data = pd.merge(counts, locations, on='territory')
    data['scaled_count'] = data['count'].apply(lambda x: np.log(x + 1))

    #data.rename({'count':'Amount of documents'}, inplace=True)
    col1,col2=st.columns([1,1])
    sum=data['count'].sum()
    data['percentage']=round(data['count']/sum,2)*100
    data['formatted_count'] = data['count'].apply(lambda x: "{:,.2f}".format(x).replace(',', ' ').replace('.', ',')[:-3])

    data.rename(columns={'territory':'Територія','count': 'Кількість', 'scaled_count':'Маштабована кількість', 'lat': 'Широта', 'lon': 'Довгота', 'percentage':'Відсоток кількості'}, inplace=True)
    with col1:
        st.dataframe(data[['Територія','Кількість','Відсоток кількості']])
    st.markdown("""
    <style>
    .big-card {
        background-color: #f9f9f9;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0px;
        box-shadow: 2px 2px 12px grey;
        font-size: 14px;
        color: #4a4a4a;
        font-family: Arial, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='big-card'><b>Документів було проскановано:</b> {df['barcode'].nunique():,}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='big-card'><b>Сторінок було проскановано:</b> {df['id'].nunique():,}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='big-card'><b>Середня кількість сторінок на документ:</b> {df['id'].nunique()/df['id'].nunique():,}</div>", unsafe_allow_html=True)

    data.rename(columns={'Територія':'territory','Кількість': 'count', 'Маштабована кількість':'scaled_count', 'Широта': 'lat', 'Довгота': 'lon','Відсоток кількості':'percentage'}, inplace=True)

    
    
    # m = folium.Map(location=[49.5, 24.0], zoom_start=7, tiles='cartodb positron')
    # # Define a color palette
    # colors = ['blue', 'green', 'red', 'purple', 'orange', 'darkred']
    
    # for i, (lat, lon, scaled_count, count, territory) in enumerate(zip(data['lat'], data['lon'], data['scaled_count'], data['count'], data['territory'])):
    #     folium.CircleMarker(
    #         location=[lat, lon],
    #         radius=scaled_count * 3,  # scale up the size for better visibility
    #         popup=f'<i>{territory}</i><br>Кількість: <b>{count}</b> <br> Відсоток кількості: <b>{round(count/sum,2)}</b>',
    #         color=colors[i % len(colors)],  # cycle through colors
    #         fill=True,
    #         fill_color=colors[i % len(colors)],
    #         fill_opacity=0.6,  # set fill opacity
    #         line_opacity=0.9,
    #     ).add_to(m)
    
    # # Display the map in Streamlit
    # folium_static(m, width=1000)  # set the width to 1000 pixels

    def assign_color(index):
        colors = {
        'blue': [0, 0, 255, 200],
        'green': [0, 128, 0, 200],
        'red': [255, 0, 0, 200],
        'purple': [128, 0, 128, 200],
        'orange': [255, 165, 0, 200],
        'darkred': [139, 0, 0, 200]
        }
        color_names = list(colors.keys())
        return colors[color_names[index % len(color_names)]]
        
    data['color']=data.index.map(assign_color)
    # ... [Your previous code here]

    # Use Pydeck for more customization
    view_state = pdk.ViewState(
        latitude=50,
    longitude=28.00,
    zoom=5.9,
    pitch=0,
    )
    layer = pdk.Layer(
    'ScatterplotLayer',
    data=data,
    get_position='[lon, lat]',
    get_fill_color='color',
    get_radius='scaled_count * 2100',  # Adjust size of circle based on count of documents
    pickable=True,
    extruded=True,
    )

    tooltip = {
    "html": "<b>{territory}</b><br>Кількість: {formatted_count}<br>Відсоток кількості: {percentage}",
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
    }

    st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[layer],
    tooltip=tooltip
    ))

    st.button("Перезавантажити")


def Plot():
    df_time,df_time_all,final_data=get_data_chart()
    df = get_data_dataframe()
    df_time=final_data#.set_index('ds')
    df_time_all=df_time_all#.set_index('ds')

    cursor.execute('select count(*) from scantable where dateandtime::date >=now()::date;')
    today_date = cursor.fetchone()[0]
    cursor.execute("select count(*) from scantable where dateandtime::date >=(now()- interval '1 day')::date;")
    yesterday_date = cursor.fetchone()[0]

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        Ця сторінка ілюструє комбінацію лінійного графіку та гістограми. 
        """
    )
    
    if "default_plot" not in st.session_state:
        st.session_state["default_plot"] = "Lviv"
    if 'disable_opt_plot' not in st.session_state:
        st.session_state.disable_opt = False
    def initialize_state():
        if 'date_range' not in st.session_state:
            st.session_state.date_range = ()
    initialize_state()




    #progress_bar = st.sidebar.progress(0)
    #status_text = st.sidebar.empty()
    
    all = st.checkbox("Вибрати усі регіони")
    
    if all:
        st.session_state.disable_opt = True

        
    else:
        st.session_state["default_plot"] = 'Lviv'
        territories='Lviv'
        st.session_state.disable_opt = False

    
    
    territories = st.selectbox(
        "Вибрати територію", df_time.territory.unique(), index=list(df_time.territory.unique()).index(st.session_state["default_plot"]), disabled = st.session_state.disable_opt
    )
    st.session_state["default_plot"] = territories
    

    filters_plot['territory']=[territories]

    time_input = st.date_input('Вибрати часові межі', st.session_state.date_range, key='date_range_picker',format='DD/MM/YYYY')

    # Saving the chosen date range to session state
    st.session_state.date_range = time_input


    # Display a button to clear the date filter
    if st.button("Очистити часовий фільтр"):
        st.session_state.date_range = ()
        filters_plot['ds']='All'
        #st.experimental_rerun()




    # time_input=st.date_input('Вибрати часові межі:', st.session_state["date_input_plot"], format='DD/MM/YYYY')

    # st.session_state['date_input_plot'] = time_input


   


    # button=st.button('Очистити часовий фільтр')
 
    # if button:
    #     st.session_state['date_input_plot'] = []

    #     # st.session_state["default"][0]=[]
    #     filters_plot['ds']='All'
    #     st.experimental_rerun()
    #     #st.date_input('Choose date limits:', [])=[]


  

    
    
    if len(time_input)!=2: 
        
        try:
            mask = (df_time['ds'] > datetime.combine(time_input[0], zero_time))
            df_time=df_time.loc[mask]
            mask_all = (df_time_all['ds'] > datetime.combine(time_input[0], zero_time))
            df_time_all=df_time_all.loc[mask_all]
        except:
            try:
                mask =  (df_time['ds'] <= datetime.combine(time_input[1], one_time))
                df_time=df_time.loc[mask]
                mask_all =  (df_time_all['ds'] <= datetime.combine(time_input[1], one_time))
                df_time_all=df_time_all.loc[mask_all]
            except:
                pass
        
    else:
        start_date, end_date = time_input
        if start_date <= end_date:
            pass
        else:
            st.error('Error: DateStart is greater then DateEnd.')
        mask = (df_time['ds'] > datetime.combine(start_date, zero_time)) & (df_time['ds'] <= datetime.combine(end_date, one_time))
        df_time=df_time.loc[mask]
        mask_all = (df_time_all['ds'] > datetime.combine(start_date, zero_time)) & (df_time_all['ds'] <= datetime.combine(end_date, one_time))
        df_time_all=df_time_all.loc[mask_all]






    for col, value in filters_plot.items():
        if value == 'All':  # Skip if value is 'All'
            continue
        elif isinstance(value, list):  # If the value is a list, use isin
            df_time = df_time[df_time[col].isin(value)]
        else:  # Otherwise, use equality
            df_time = df_time[df_time[col] == value]

    for col, value in filters_plot_all.items():
        if value == 'All':  # Skip if value is 'All'
            continue
        elif isinstance(value, list):  # If the value is a list, use isin
            df_time_all = df_time_all[df_time_all[col].isin(value)]
        else:  # Otherwise, use equality
            df_time_all = df_time_all[df_time_all[col] == value]

    
    df_time=df_time.set_index('ds')
    df_time_all=df_time_all.set_index('ds')

    try:
        # Removing leading zeros
        df_time = df_time.loc[(df_time['y'] != 0).idxmax():]

        # Removing trailing zeros
        df_time = df_time.loc[:df_time.loc[df_time['y'] != 0].index[-1]]
    except:
        df_time=pd.DataFrame({})
    #progress_bar.empty()

    if df_time.empty == True or df_time_all.empty == True:
        st.error('У вибраних фільтрах немає даних', icon="🚨")
    else:
        if all:
            
            fig = px.line(df_time_all, x=df_time_all.index, y='y', title='Кількість документів по днях', markers=True)

            fig.update_traces(line=dict(width=6, color='#87bc45'), hoverlabel=dict(font_size=16))

            fig.update_xaxes(title_text='Дата', tickformat='%d-%m-%Y')
            fig.update_yaxes(title_text='Кількість документів')
            fig.update_traces(hovertemplate='Дата: %{x}<br>Документів: %{y}')

            st.plotly_chart(fig)

            df_time_all.drop(columns=['territory'], inplace=True)

            fig2 = px.histogram(y=df_time_all['y'], x=df_time_all.index, nbins=365,
                                title='Кількість документів по днях',
                                labels={'x': 'Date', 'sum of Number of Documents': 'Number of Documents'})
            fig2.update_yaxes(title_text='Кількість документів')
            fig2.update_xaxes(tickformat='%d-%m-%Y')

            fig2.update_traces(marker=dict(color='blue', line=dict(color='#87bc45', width=420/len(df_time_all['y']))),
                   hoverlabel=dict(font_size=16),
                  hovertemplate='Дата: %{x}<br>Документів: %{y}')



            st.plotly_chart(fig2)
        else:
            fig = px.line(df_time, x=df_time.index, y='y', title='Кількість документів по днях', markers=True)

            fig.update_traces(line=dict(width=6, color='#87bc45'), hoverlabel=dict(font_size=16))

            fig.update_xaxes(title_text='Дата', tickformat='%d-%m-%Y')
            fig.update_yaxes(title_text='Кількість документів')
            fig.update_traces(hovertemplate='Дата: %{x}<br>Документів: %{y}')

            st.plotly_chart(fig)




            fig1 = px.histogram(y=df_time['y'], x=df_time.index, nbins=365, title='Кількість документів по днях',
                                labels={'x': 'Дата', 'y': 'Кількість документів'})
            fig1.update_yaxes(title_text='Кількість документів')
            fig1.update_xaxes(tickformat='%d-%m-%Y')

            fig1.update_traces(marker=dict(color='blue', line=dict(color='#87bc45', width=420/len(df_time['y']))),
                   hoverlabel=dict(font_size=16),
                  hovertemplate='Дата: %{x}<br>Документів: %{y}')


            st.plotly_chart(fig1)
    
    
    
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write('Сьогодні було проскановано: ', today_date)
    with col2:
        st.write('Вчора та сьогодні було проскановано: ', yesterday_date)

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Перезавантажити")

   
    



import warnings
warnings.filterwarnings("ignore")
from datetime import date
from datetime import datetime, timedelta
import streamlit as st
#import time
import pandas as pd
import numpy as np
import plotly.express as px
#import folium
#from streamlit_folium import folium_static
import pydeck as pdk

# Set the layout to wide mode
st.set_page_config(layout='wide')


from PsqlConnect import connect
global con, cursor, monday, sunday, zero_time, one_time


@st.cache_resource(show_spinner="Утворення з'єднання до бази PSQL...", ttl=180)
def psqlconnection():
    _ , con= connect()
    return con


con=psqlconnection()
cursor = con.cursor()



epoch_year = date.today().year

year_start = date(epoch_year, 1, 1)#.strftime('%d/%m/%Y')
year_end = date(epoch_year, 12, 31)#.strftime('%d/%m/%Y')

now=datetime.now()
monday = now - timedelta(days = now.weekday())
sunday = monday + timedelta(days = 6)
zero_time = datetime.min.time()
one_time = datetime.max.time()
monday=datetime.combine(monday, zero_time)#.strftime('%d/%m/%Y, %H:%M:%S')
sunday=datetime.combine(sunday, one_time)#.strftime('%d/%m/%Y, %H:%M:%S')





@st.cache_data(show_spinner="Отримання даних з бази PSQL...", ttl=120)
def get_data_dataframe():
    df=pd.read_sql_query("""SELECT * FROM scantable order by dateandtime desc """, con)
    return df


@st.cache_data(show_spinner="Отримання даних з бази PSQL...",ttl=120)
def get_data_chart():
    df_time=pd.read_sql_query("""select territory,dateandtime::date as ds, count(id) as y from scantable group by dateandtime::date, territory order by ds asc;""", con)
    df_time['ds']=df_time['ds'].apply(pd.to_datetime)
    #df_time.set_index('ds', inplace=True)
    df_time_all=pd.read_sql_query("""select dateandtime::date as ds, count(id) as y from scantable group by dateandtime::date order by ds asc;""", con)
    df_time_all['ds']=df_time_all['ds'].apply(pd.to_datetime)

    # Generate a date range between the minimum and maximum dates
    date_range = pd.date_range(start=df_time['ds'].min(), end=df_time['ds'].max())

    # List to store dataframes
    dfs = []

    # For each unique territory in the data
    for territory in df_time['territory'].unique():
        # Filter data for the current territory
        territory_data = df_time[df_time['territory'] == territory]
        
        # Create a new dataframe with the complete range of dates
        complete_dates = pd.DataFrame({'ds': date_range})
        complete_dates['territory'] = territory
        
        # Merge this new dataframe with the territory data
        merged_data = pd.merge(complete_dates, territory_data, on=['ds', 'territory'], how='left')
        
        # Fill missing 'y' values with zeros
        merged_data['y'] = merged_data['y'].fillna(0)
        
        # Append the result to the list
        dfs.append(merged_data)

    # Concatenate all dataframes in the list to create a single dataframe
    final_data = pd.concat(dfs, ignore_index=True)

    # Now, use this `final_data` DataFrame to plot your chart
     # Merge this new dataframe with the territory data
    dfs_all=[]
    merged_data = pd.merge(complete_dates, df_time_all, on=['ds'], how='left')
    
    # Fill missing 'y' values with zeros
    merged_data['y'] = merged_data['y'].fillna(0)
    
    # Append the result to the list
    dfs_all.append(merged_data)
    df_time_all = pd.concat(dfs_all, ignore_index=True)
    
    df_time_reset = df_time.reset_index()
    merged_data = pd.merge(complete_dates, df_time_reset, on='ds', how='left')
    merged_data['y'] = merged_data['y'].fillna(0)





    return  df_time,df_time_all,final_data



filters = {
   'dateandtime': 'All',
   'territory': 'All'
}

filters_plot = {
   'ds': 'All',
   'territory': 'All'
}

filters_plot_all = {
   'ds': 'All'
}

page_names_to_funcs = {
    "Таблиця": DateFrame,
    "Карта": GeospatialAnalysis,
    "Графік": Plot


}
#"Mapping Demo": mapping_demo
pages = st.sidebar.selectbox("Виберіть сторінку", page_names_to_funcs.keys())
page_names_to_funcs[pages]()

