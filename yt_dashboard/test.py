import streamlit as st
import pandas as pd

import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

st.header('YouTube')

df = pd.read_csv('file.csv')
st.dataframe(df)
st.sidebar.success('Complete')

# ---- MAINPAGE ----
st.title(":bar_chart: Youtube Dashboard")
st.markdown("##")

# TOP KPI's
total_views = int(df["view_count"].sum())
average_likes = round(df["like_count"].mean(), 1)
average_views_per_video = round(df["view_count"].mean(), 2)
video_count = int(df['video_id'].count())

fourth_column, left_column, middle_column, right_column, = st.columns(4)
with fourth_column:
    st.metric(label='Video Count:', value=video_count)
with left_column:
    st.metric(label='Total Views:', value=total_views)
with middle_column:
    st.metric(label='Average Views:', value=average_views_per_video)
with right_column:
    st.metric(label='Average Like Count:', value=average_likes)

st.markdown("""---""")

left_column, right_column = st.columns(2)

with left_column:
    
    df_highest_views = df.nlargest(n=5, columns=['view_count'])
    
    #st.dataframe(df_highest_views)
    
    fig_product_sales = px.bar(
        df_highest_views,
        x=df_highest_views['view_count'],
        y=df_highest_views['video_title'],
        orientation="h",
        title="<b>Most viewed videos</b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white",
    )

    fig_product_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis={'categoryorder':'total ascending'}
    )
    st.plotly_chart(fig_product_sales, use_container_width=True)

with right_column:
    max_views_index = df['view_count'].idxmax()
    ytid = df.loc[max_views_index, 'video_id']
    
    yt_img = f'http://img.youtube.com/vi/{ytid}/hqdefault.jpg'
    st.image(yt_img,use_column_width='Auto')
    st.metric(label = df.loc[max_views_index, 'video_title'], value= df.loc[max_views_index, 'view_count'])

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
            
st.markdown(hide_st_style, unsafe_allow_html=True)
