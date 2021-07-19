import csv
from PIL import Image
import numpy as np
import streamlit as st
import pydeck as pdk
import pandas as pd
import mapbox as mb
import statistics
import datetime as dt
import matplotlib.pyplot as plt



#Get File
st.set_page_config(layout="wide")

filename = "California_Fire_Incidents.csv"
with open(filename, mode='r') as csv_file:
    data = csv.DictReader(csv_file)
    County_name = {}
    Fire_name =[]
    DatasetPreview = []
    for row in data:
        County = row['Counties']
        Firename = row['Name']
        Location = row['Location']
        ETime = row ['Extinguished']
        Latitude = row['Latitude']
        Longitude = row ['Longitude']
        BurnedArea = row ['AcresBurned']
        Stime = row ['Started']
        Year = row ['ArchiveYear']
        DatasetPreview.append((Firename,County,Location,BurnedArea,Year,Stime, ETime,Latitude, Longitude))
        if County in County_name.keys():
            # check if item_name is in the values for this category at [0]
            County_name[County].append([Firename,County,Location,BurnedArea,Year,Stime, ETime,Latitude, Longitude])
            Fire_name.append(Firename)
        else:
            County_name[County]= [[Firename,County,Location,BurnedArea,Year,Stime, ETime,Latitude, Longitude]]
            Fire_name.append(Firename)
list1 = []
for fire in County_name:
    list1.append(fire)
FireCounty = list1
list1.sort()

#Graphing Data
# zip the lists and create dataframe
def GraphingData():
    CountyName = []
    FireNumber = [] #unsorted
    for i in County_name:
        CountyName.append(i)
        print(i)
        count = 0
        for element in County_name[i]:
            count += 1
        print(count)
        FireNumber.append(count)
    print(CountyName)
    print(FireNumber)
    d = list(zip(CountyName, FireNumber))
    print(d)
    df = pd.DataFrame(data=d, columns=['County', 'Number'])
    # make date the index
    df.set_index('County', inplace=True)
    return df
def a(x=0):
    pass

n=a(1)
#Dataset Preview
df = pd.DataFrame(DatasetPreview, columns=["Fire Name","County","Location","Burned Area","Year","Started Time","Extinguished Time","Latitude", "Longitude"])
df[["Latitude", "Longitude","Burned Area"]] = df[["Latitude", "Longitude","Burned Area"]].apply(pd.to_numeric)
#print(df)


#Header/County Selection
img = Image.open("Wildfire.jpg")
st.markdown("<h1 style='text-align: center; color: Black;'>California WildFire</h1>", unsafe_allow_html=True)
st.image(img,use_column_width=True,caption='Random image for sizing')
#col1, col2, col3 = st.beta_columns([1,1,1])
#col2.image(img,width = 800)
page = st.selectbox("Choose your page", ["Main", "Search By County"])
if page == "Main":
    st.header("Dataset Preview")
    st.dataframe(df)

    # calculate the fields
    TotalFire = len(Fire_name)
    NumberFire= []
    for i in County_name:
        count = 0
        for element in County_name[i]:
            count += 1
        NumberFire.append(count)
    #print(NumberFire)
    dataSet = NumberFire
    dataSet.sort()
    mean = statistics.mean(NumberFire)
    #print(mean)
    minimum = dataSet[0]
    #print(minimum)
    sDev = statistics.stdev(dataSet)
    #print(sDev)
    maximum = dataSet[::-1][0]
    maximumarea= df['Burned Area'].max()
    minimumarea= df['Burned Area'].min()

    #print(maximum)
    outTable = [
        ["Count:", f"{TotalFire:<5}"],
        ["Minimum Burned Area", f"{minimumarea:<5}"],
        ["Maximum Burned Area", f"{maximumarea:<5}"]
    ]
    outTable2 = [
        ["Mean by County:", f"{mean:<5.6f}"],
        ["Standard Deviation:", f"{sDev:5.6f}"],
        ["Maximum Fire Number by County:", f"{maximum:<5}"],
        ["Minimum Fire Number by County:", f"{minimum:<5}"]
    ]
    # statistics output
    st.header("Descriptive Statistics")
    col3,col4 = st.beta_columns([1,1])
    with col3:
        st.write(f'Basic statistics regarding California Fire\n')
        col_width = max(len(str(word)) for row in outTable for word in row) + 5  # padding
        for a in outTable:
            st.text("".join(str(word).ljust(col_width) for word in a))
    with col4:
        col_width = max(len(str(word)) for row in outTable2 for word in row) + 5  # padding
        for a in outTable2:
            st.text("".join(str(word).ljust(col_width) for word in a))

    # graphical output
    col1, col2 = st.beta_columns([3, 1])
    graphData = GraphingData()
    col1.subheader("Historical number of fire by Count")
    col1.area_chart(graphData)
    col2.subheader("Number of fire by Count")
    col2.write(graphData)

    #st.header('Chart')
    #st.write(f'Below is the chart about historical number of fire by Count.')
    #graphData = GraphingData()
    #st.area_chart(graphData)

elif page == "Search By County":
    st.sidebar.header ('Inputs')
    # Add a selectbox :
    selection = st.sidebar.selectbox(
        'Please select a COUNTY to analyze:',
        (list1)
    )
    selection2 = st.sidebar.selectbox('Please select a YEAR to analyze',(2013,2014,2015,2016,2017,2018,2019))
    #selection2 = st.checkbox('Select a YEAR to analyze',['2013','2014','2015','2016'], False)

    FireinCounty = []
    for i in County_name:
        if selection == i:
            for a in County_name[i]:
                a=tuple(a)
                FireinCounty.append((a))

    MAPKEY = "pk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DApk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DA"

    locations = FireinCounty
    #DataFrame
    df = pd.DataFrame(locations, columns=["Fire Name","County","Location","Burned Area","Year","Started Time","Extinguished Time","Latitude", "Longitude"])
    df[["Latitude", "Longitude", "Burned Area"]] = df[["Latitude", "Longitude","Burned Area"]].apply(pd.to_numeric)
    df['Year'] = pd.to_datetime(df['Year'])
    df = df[df['Year'].dt.year == selection2]
    df = df.sort_values(by=['Burned Area'])
    st.header(f"Wild Fire In {selection}")
    st.table(df)
    '''
    Map
    '''

    df= df[df["Latitude"] != 0]
    print(df)

    #st.write("Simple Map: st.map(df)")
    #st.map(df)
    Zoom = st.sidebar.slider("Map:Zoom Factor",1,4)
    st.write("Customized Fire Map with Tool Tips")
    view_state = pdk.ViewState(
        latitude=df["Latitude"].mean(),
        longitude=df["Longitude"].mean(),
        zoom=(7+Zoom),
        pitch=0)

    layer1 = pdk.Layer('ScatterplotLayer',
                      data=df,
                      get_position='[Longitude, Latitude]',
                      get_radius=500,
                      get_color=[0,0,255],
                      pickable=True
                      )

    # simple tool tip
    #tool_tip = {"html" : "This is {University}"}
    # stylish tool tip
    tool_tip = {"html": "Fire Name:<br/> <b>{Fire Name}</b><br/>{Location}<br/>{Started Time}",
                "style": { "backgroundColor": "steelblue",
                            "color": "white"}
              }

    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v11',
        initial_view_state=view_state,
      #  mapbox_key=MAPKEY,
        layers=[layer1],
        tooltip= tool_tip
    )

    st.pydeck_chart(map)




#CountyName = []
#FireNumber = [] #unsorted
#for i in County_name:
    #CountyName.append(i)
    #count = 0
    #for element in County_name[i]:
        #count += 1
    #FireNumber.append(count)
#print(CountyName)
#print(FireNumber)
#d = list(zip(CountyName, FireNumber))
#d.sort(key=lambda x: int(x[1]))
#print(d)
#dataSet = d
#mean = statistics.mean(NumberFire)
#print(mean)
#minimum = dataSet[1][0]
#print(minimum)
#sDev = statistics.stdev(dataSet[1])
#print(sDev)
#maximum = dataSet[::-1][0]


