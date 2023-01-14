#run this code on command prompt (activate conda base and run from the correct path)

import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt

#function to calculate the average monthly family expenses and count different types of occupation
def calc_exp_occ(df_map, currlat, currlon):

    index_list = []
    expenses_list = []
    occ_list = []
    for index, row in df_map.iterrows():
        lon1 = row['lon']
        lat1 = row['lat']
        
        loc1 =(currlat , currlon)
        loc2 =(lat1 , lon1)
        distance = 2         
        
        if distance < 2:
            index_list.append(index+1)
            expenses_list.append(row['FamilyExpenses_monthly'])
            occ_list.append(row['Occupation'])

    chart_data = pd.DataFrame({'Location': [str(x) for x in index_list],
                                'Expenses': expenses_list,
                                'Occupation': occ_list})
    
    #display bar chart of monthly expenses for address within 2km of that location
    c = alt.Chart(chart_data).mark_bar(size=10).encode( 
    x='Location',
    y='Expenses')

    #display line of the average value of montnly expenses for address within 2km of that location
    r = alt.Chart(chart_data).mark_rule(color='red').encode(
            y= 'mean(Expenses)')
    
    c2.text('2. Average Monthly Family Expenses for Address Within 2KM')
    c2.altair_chart((c+r).interactive(), use_container_width=True)    
    c2.text('Average Value: ' + str(round(chart_data['Expenses'].mean(),2)))

    df_occ_count = chart_data['Occupation'].value_counts().rename_axis('Occupation').reset_index(name='Count')
    
    #display bar chart of the count of different types of occupation in that location
    occ = alt.Chart(df_occ_count).mark_bar(color='purple').encode(
    x='Occupation', y='Count')
    c2.text('3. Count for Different Types of Occupation')
    c2.altair_chart(occ, use_container_width=True)    

#extract data
df1 = pd.read_csv('q2.csv')
df_map = df1.reset_index()

st.set_page_config(layout="wide")   
c1, padding, c2 = st.columns((10,2,10))

c1.title("Question 2")

#drop down box to select all or specific location
df_map['loc_index'] = df_map['index'].copy()
df_map['loc_index'] += 1 
df_map['loc_index'] = df_map['loc_index'].astype("string")
loc_list = df_map[['loc_index']]
new_loc_list = pd.concat([pd.Series(['All']), loc_list['loc_index']]).reset_index(drop = True)
loc_num = c1.selectbox('Please choose a location:', new_loc_list)

#if location selection is all, user will be able to view all locations on the map
if loc_num == 'All': 

    c1.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=3.15,
            longitude=101.7,
            zoom=11,
            pitch=50,
        ),
        tooltip={"html": "<b>Location:</b> {index}" "<br/> <b>Latitude:</b> {lat}" "<br/> <b>Longitude:</b> {lon}", "style": {"color": "white"}},
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_map,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=100,
                pickable=True,
                extruded=True,         
            ),
        ],
    ))
    
#if location selection is specific location, user will be able to view specified location and the three charts 
else:
    lat = df_map['lat'][int(loc_num)]
    lon = df_map['lon'][int(loc_num)]

    c1.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=lat,
            longitude=lon,
            zoom=16,
            pitch=50,
        ),
        tooltip={"html": "<b>Location:</b> {index}" "<br/> <b>Latitude:</b> {lat}" "<br/> <b>Longitude:</b> {lon}", "style": {"color": "white"}},
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_map,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=50,
                pickable=True,
                extruded=True,         
            ),
        ],
    ))
    
    place_name = df_map.columns.tolist()[-6:-1]
    place_count = df_map.loc[(df_map['lat'] == lat)][df_map.columns[-6:-1]].values
    place_count = place_count.flatten().tolist()

    place_data = pd.DataFrame(place_name, columns=['Place Name'])
    place_data['Count'] = place_count
    
    #display bar chart for count of top-5 business/retail in that specified location
    place_frequency = alt.Chart(place_data).mark_bar(color='green').encode(
    x='Place Name', y='Count')

    c2.title('Charts')
    c2.text('1. Count of Top-5 Retail/Business')
    c2.altair_chart(place_frequency, use_container_width=True) 

    #function called to calculate and display chart of average family monthly expenses and count for different types of occupation
    calc_exp_occ(df_map, lat, lon)

st.write(st.__version__)
st.write(pd.__version__)
st.write(pdk.__version__)
st.write(alt.__version__)
