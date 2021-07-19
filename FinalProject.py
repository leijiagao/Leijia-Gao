import csv
from PIL import Image
import streamlit as st
import pydeck as pdk
import pandas as pd
import statistics
import altair as alt
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

def welcome(name,msg="Let's analyse the California Wild Fire Incident from 2013-2019"):
    print("Hello", name,",",msg)

def pie():
    global YearList,YearFire,YearName
    with open(filename, mode='r') as csv_file:
        data = csv.DictReader(csv_file)
        YearList = {}
        Year = []
        Y = []
        for row in data:
            Firename = row['Name']
            Year = row ['ArchiveYear']
            Y.append((Year,Firename))
            if Year in YearList.keys():
                # check if item_name is in the values for this category at [0]
                YearList[Year].append([Firename,Year])
            else:
                YearList[Year]= [[Firename,Year]]
        a = pd.Series(YearList).value_counts()
        #print(a)
        #print(YearList)
        YearFire = []
        YearName = []
        for i in YearList:
            YearName.append(i)
            count = 0
            for element in YearList[i]:
                count += 1
            YearFire.append(count)
        #print(YearFire)
        # explode the first wedge
        fig, ax = plt.subplots()
        labels=[2013,2014,2015,2016,2017,2018,2019]
        colors = ['#ffd2c5','#8ebd9d','#9be5dc','#cadbd6','#de9c38','#ffaaaa','#b8bd6c']

        ax.pie(YearFire, explode=[0.05,0.05, 0.05,0.05,0.05,0.05,0.05],labels=YearName, autopct='%1.1f%%',startangle=90,pctdistance=0.85,colors=colors )
        ax.axis('equal')
        plt.title("Fires each Year",color='black',fontsize=16)
        plt.xticks(rotation=45)
        plt.grid(visible=False)
        plt.rcParams["font.family"] = "sans-serif"
        ax.legend(loc="center", bbox_to_anchor=(1, 0.5),labels =YearName)
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        fig.set_size_inches(20, 10, forward=True)
        plt.tight_layout()
        st.pyplot(fig)




def CFire(selection,County_name):
    FireinCounty = []
    for i in County_name:
        if selection == i:
            for a in County_name[i]:
                a=tuple(a)
                FireinCounty.append((a))
    return FireinCounty


#Dataset Preview
df = pd.DataFrame(DatasetPreview, columns=["Fire Name","County","Location","Burned Area","Year","Started Time","Extinguished Time","Latitude", "Longitude"])
df[["Latitude", "Longitude","Burned Area"]] = df[["Latitude", "Longitude","Burned Area"]].apply(pd.to_numeric)
#print(df)


#Header/County Selection
img = Image.open("Wildfire.jpg")


#col2.title('California WildFire')

st.markdown("<h1 style='text-align: center; color: Black;'>California WildFire</h1>", unsafe_allow_html=True)
st.image(img,use_column_width=True,caption='Random image for sizing')
#col1, col2, col3 = st.beta_columns([1,1,1])
#col1,col2,col3 = st.beta_columns([1,1,2.5])
#col2.image(img,width = 800)
your_name = st.text_input("Name: ", "Leijia")
welcomeMessage = welcome(your_name)
st.write(welcomeMessage)
page = st.selectbox("Choose your page", ["Main", "Search By County","Year"])
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
    Loc = County
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
    col1.subheader("Historical Number of Fire by County")
    col1.area_chart(graphData)
    col2.write(graphData)

    col3,col4 = st.beta_columns([1, 4])
    with col4:
        col4.subheader("Historical Number of Fire by Year")
        pie()
    with col3:
        d = list(zip(YearName, YearFire))
        df = pd.DataFrame(data=d, columns=['Year', 'Number'])
        # make Year the index
        df.set_index('Year', inplace=True)
        st.table(df)

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
    #selection2 = st.sidebar.selectbox('Please select a YEAR to analyze',(2013,2014,2015,2016,2017,2018,2019))
    #selection2 = st.checkbox('Select a YEAR to analyze',['2013','2014','2015','2016'], False)


    MAPKEY = "pk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DApk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DA"

    locations = CFire(selection,County_name)
    #DataFrame
    df = pd.DataFrame(locations, columns=["Fire Name","County","Location","Burned Area","Year","Started Time","Extinguished Time","Latitude", "Longitude"])
    df[["Latitude", "Longitude", "Burned Area"]] = df[["Latitude", "Longitude","Burned Area"]].apply(pd.to_numeric)
    #df['Year'] = pd.to_datetime(df['Year'])
    #df = df[df['Year'].dt.year == selection2]
    #df = df.sort_values(by=['Burned Area'])
    st.header(f"Wild Fire In {selection}")
    df.set_index('Fire Name', inplace=True)
    st.table(df)
    st.sidebar.write("There were total of",len(df), f"fires occured in {selection}")


   

    df = pd.DataFrame(locations, columns=["Fire Name","County","Location","Burned Area","Year","Started Time","Extinguished Time","Latitude", "Longitude"])
    df[["Latitude", "Longitude"]] = df[["Latitude", "Longitude"]].apply(pd.to_numeric)
    df= df[(df["Latitude"] != 0) & (df["Longitude"] != 0)]
    print(df)

    #st.write("Simple Map: st.map(df)")
    #st.map(df)
    Zoom = st.sidebar.slider("Map:Zoom Factor",1,4)
    st.subheader("Fire Map with tool tips")
    view_state = pdk.ViewState(
        latitude=df["Latitude"].mean(),
        longitude=df["Longitude"].mean(),
        zoom=(7+Zoom),
        pitch=1)



    layer1 = pdk.Layer('ScatterplotLayer',
                      data=df,
                      get_position='[Longitude, Latitude]',
                      get_radius=500,
                      get_color=[200, 30, 0, 160],
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
        map_style='mapbox://styles/mapbox/outdoors-v11',
        initial_view_state=view_state,
      #  mapbox_key=MAPKEY,
        layers=[layer1],
        tooltip= tool_tip
    )

    st.pydeck_chart(map)

elif page == 'Year':
    selection3 = st.text_input('Please enter the year you want to check(2013-2019):','2013')
    selection3 = int(selection3)
    df = pd.DataFrame(DatasetPreview, columns=["Fire Name","County","Location","Burned Area","Year","Started Time","Extinguished Time","Latitude", "Longitude"])
    df[["Latitude", "Longitude", "Burned Area"]] = df[["Latitude", "Longitude","Burned Area"]].apply(pd.to_numeric)
    df['Year'] = pd.to_datetime(df['Year'])
    df = df[df['Year'].dt.year == selection3]
    df = df.sort_values(by=['County'])
    st.header(f"Wild Fire In {selection3}")
    st.write('There were total of',len(df),f'fires in {selection3}.' )
    st.dataframe(df)
    newdf = df.groupby(['County']).size().to_frame('Number').reset_index()
    #data = pd.DataFrame({x:[df]})
    graph = alt.Chart(newdf).mark_bar().encode(x = 'County', y = 'Number')
    col1, col2 = st.beta_columns([4, 1])
    col1.subheader(f"Number of fire by County in {selection3}")
    col1.write(graph)
    col2.dataframe(newdf)
