import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
##################################################################
#EDA
data = pd.read_csv('Cars Data1.csv')
df = pd.DataFrame(data)
df = df.drop_duplicates()
df.drop_duplicates(inplace=True)
df.duplicated().sum()
df.dropna(how='all', inplace=True)
df.fillna(0, inplace=True)
df['MSRP'] = df['MSRP'].replace({'\$': '', ',': ''}, regex=True).str.strip()
df['MSRP'] = pd.to_numeric(df['MSRP'], errors='coerce')
df['MSRP'] = df['MSRP'].astype(int)
df['Invoice'] = df['Invoice'].replace({'\$': '', ',': ''}, regex=True).str.strip()
df['Invoice'] = pd.to_numeric(df['Invoice'], errors='coerce')
df['Invoice'] = df['Invoice'].astype(int)
df['Power_to_Weight'] = df['Horsepower'] / df['Weight']
df['Horsepower_per_Liter'] = df['Horsepower'] / df['EngineSize']
df['make_model'] = df['Make'] +' - ' + df['Model']
st.set_page_config(layout='wide')
##################################################################
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(['None', 'q1', 'q2', 'q3', 'q4', 'q5'])
tab00, tab6, tab7, tab8, tab9, tab10 = st.tabs(['None', 'q6', 'q7', 'q8', 'q9', 'q10'])
tab000, tab11, tab12, tab13, tab14 ,tab15= st.tabs(['None', 'q11', 'q12', 'q13', 'q14','q15'])
##################################################################
with tab1:
    st.title("1- What is the average MSRP (Manufacturer's Suggested Retail Price) of the vehicles in the dataset?")
    q1=px.box(df , x='MSRP' , title=" What is the average MSRP (Manufacturer's Suggested Retail Price) of the vehicles in the dataset?")
    st.plotly_chart(q1)
    
with tab2:
    st.title("2-Engine Size and Cylinders: Larger engines and more cylinders often mean more power, but also more fuel consumption.")
    df['Eng+Cyln']=df['EngineSize'] + df['Cylinders']
    engine_sieze=df.groupby(['Eng+Cyln' , 'Make' , 'Model'])['Invoice'].sum().reset_index()
    engine_sieze = engine_sieze.sort_values(by='Eng+Cyln' , ascending=0)
    engine_sieze['Eng_Cyln_Model'] = engine_sieze['Eng+Cyln'].astype(str) + ' - ' + engine_sieze['Model'] +' - '+engine_sieze['Make'].astype(str)
    q2 =px.histogram(engine_sieze, y='Eng+Cyln', x='Make',color='Eng_Cyln_Model',
                 barmode='group',
            category_orders={'Make': engine_sieze['Make'].value_counts().index} ,
            title='Engine Size and Cylinders: Larger engines and more cylinders often mean more power, but also more fuel consumption.').update_xaxes(categoryorder='total ascending')
    st.plotly_chart(q2)

with tab3:
    st.title("3-Horsepower: More horsepower usually equates to better acceleration and overall performance.")
    hpow = df.groupby(['Make' , 'make_model' , 'Horsepower'])['Invoice'].sum().reset_index()
    hpow = hpow.sort_values(by=['Horsepower' ,'Make' ], ascending=[0, 0])
    q3 = px.histogram(hpow , x='Make' , y='Horsepower' ,barmode='group',color='make_model',
                      category_orders={'Make': hpow['Make'].value_counts().index},
                      title='Horsepower: More horsepower usually equates to better acceleration and overall performance.')
    st.plotly_chart(q3)
    
with tab4:
    st.title("4-MPG (City and Highway): These figures tell you how fuel-efficient the car is. Higher MPG means better fuel economy.")
    q4 =px.bar(df , x='MPG_City' , y='MPG_Highway' ,color='make_model',barmode='group'
       , title='MPG (City and Highway): These figures tell you how fuel-efficient the car is. Higher MPG means better fuel economy.')
    q4_c=px.box(df , x='MPG_City',title= 'MPG_City')
    q4_h=px.box(df , x='MPG_Highway',title= 'MPG_Highway')
    st.plotly_chart(q4)
    st.title("(City and Highway)")
    st.plotly_chart(q4_c)
    st.plotly_chart(q4_h)
    
with tab5:
    st.title("5-Weight: Heavier cars may offer more stability but usually result in lower fuel efficiency top(10).")
    wei = df.groupby(['Weight' , 'make_model'])['Invoice'].sum().reset_index()
    wei = wei.sort_values(by='Weight', ascending=0).head(10)
    q5 =px.histogram(wei , x='Invoice' , y='Weight' , color='make_model' , barmode='group' , title='Weight: Heavier cars may offer more stability but usually result in lower fuel efficiency top(10).')
    st.plotly_chart(q5)

with tab6:
    st.title('6-Origin with car brand')
    origin_counts = df.groupby('Origin')['Make'].count().reset_index()
    q6 =px.pie(origin_counts , names='Origin' , values='Make' , title='Origin with car brand')
    st.plotly_chart(q6)

with tab7:
    st.title("7-MSRP Trend by Origin")
    msor = df.groupby('Origin')['MSRP'].sum().reset_index()
    msor = msor.sort_values(by='MSRP' , ascending=0)
    q7 = px.line(msor , x='Origin' , y='MSRP').update_xaxes(categoryorder = 'total ascending')
    st.plotly_chart(q7)
    
with tab8:
    st.title('8- EUR car with type')
    EUR = df[df['Origin'] == 'Europe']
    q8 = px.histogram(EUR, x='Make',color='Type',barmode='group'
                      , category_orders={'Make': EUR['Make'],'Type': EUR['Type'].value_counts().index})
    st.plotly_chart(q8)

with tab9:
    st.title("9-USA car with type")
    EUR = df[df['Origin'] == 'USA']
    q9 = px.histogram(EUR, x='Make',color='Type',barmode='group'
                  , category_orders={'Make': EUR['Make'],'Type': EUR['Type'].value_counts().index})
    st.plotly_chart(q9)

with tab10:
    st.title("10-Asia car with type")
    EUR = df[df['Origin'] == 'Asia']
    q10 = px.histogram(EUR, x='Make',color='Type',barmode='group'
                      , category_orders={'Make': EUR['Make'],'Type': EUR['Type'].value_counts().index})
    st.plotly_chart(q10)

with tab11:
    st.title("11-higest Horsepower_per_Liter")
    Horsepower_per_Liter = df.sort_values(by='Horsepower_per_Liter', ascending=0).head(5)
    q11 =px.histogram(Horsepower_per_Liter, x='Horsepower_per_Liter',barmode='group',
                      color='make_model', category_orders={'make_model': Horsepower_per_Liter['make_model'].value_counts().index})
    st.plotly_chart(q11)
    
with tab12:
    st.title("12-highest Power_to_Weight")
    Power_to_Weight = df.sort_values(by='Power_to_Weight' , ascending=0).head(5)
    q12 =px.histogram(Power_to_Weight , x='Power_to_Weight' ,y='make_model')
    st.plotly_chart(q12)
    
with tab13:
    st.title("13-DriveTrain with price and country")
    DriveTrain = df.sort_values(by='Invoice' ,ascending=0)
    q13 = px.histogram(DriveTrain , y='DriveTrain' , x='Invoice' , color='Origin' , barmode='group')
    st.plotly_chart(q13)

with tab14:
    st.title("14- highest Wheelbase")
    Wheelbase = df.sort_values(by='Wheelbase' , ascending=0).head(5)
    q14 = px.histogram(Wheelbase , x='Wheelbase' , y='make_model')
    st.plotly_chart(q14)

with tab15:
    st.title("15 -higest brand made")
    hig = df.groupby(['Make','Origin'])['Invoice'].sum().reset_index()
    hig = hig.sort_values(by='Invoice',ascending=0)
    q15=px.histogram(hig , x='Invoice' ,y='Make' , color='Origin')
    st.plotly_chart(q15)
