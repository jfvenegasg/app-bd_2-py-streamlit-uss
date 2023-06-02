from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import os
from google.cloud import bigquery
import plotly.express as px

#pip install protobuf==3.20.*

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'shiny-apps-385622-08e5b9820326.json'

client = bigquery.Client()

query = """ SELECT * from `bigquery-public-data.austin_bikeshare.bikeshare_trips` LIMIT 100"""

query_job = client.query(query)
df = query_job.to_dataframe()
grouped_data = df.groupby('subscriber_type')['duration_minutes'].sum().reset_index()

#Aca se genera el grafico,de acuerdo a los datos extraidos en la consulta SQL.
#El grafico muestra en el eje x el tipo de suscriptor y en el eje y la duracion en minutos de los viajes
fig = px.bar(grouped_data, x='subscriber_type', y='duration_minutes')
"""
# Esta una app de demostración realizada con la libreria StreamLit. Esta app se puede desplegar en contenedores de forma local asi como en la nube.
"""
c=st.empty()
        
        
c.image("uss.png")

st.dataframe(df.head(10))
st.plotly_chart(fig)

with st.echo(code_location='below'):
    total_points = st.slider("Numero de puntos en el espiral", 1, 5000, 2000)
    num_turns = st.slider("Numero de giros en el espiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))

