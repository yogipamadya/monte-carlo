import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np

tabel = {'input':['min','max','mean','stdev'],
        'luas meter2':[1000,2000,1500,40],
         'ketebalan meter':[1,2,3,4],
         'ntg persen':[50,70,12,1],
         'por persen':[10,20,15,2],
         'sw persen':[30,50,20,5],
         'bo':[1,1,1,1]}

iteration = {'iteration':[10000]}

df = pd.DataFrame(tabel)
df2 = pd.DataFrame(iteration)

app = dash.Dash(__name__)



app.layout = html.Div(
[
    html.H1('Simulasi Monte Carlo ver. 1 Beta'),
    html.H2('Metode Distribusi Data: Truncated Normal Distribution'),
    dcc.Markdown('''
                 _Silahkan isi tabel dengan angka yang diinginkan_
                 '''),
    
    html.Div([dash_table.DataTable(
    id='table-input',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    editable=True,
    )]),
   
    html.Br(),
   
    html.Div([dash_table.DataTable(
    id='table-input2',
    columns=[{"name": 'iteration', "id": 'iteration'}],
    data=df2.to_dict('records'),
    editable=True,
    )]),
   
    html.Br(),
   
    dcc.Graph(id='grafik'),
    
    html.Br(),
   
    html.Div(id='deskripsi'),
    
    html.Br(),
    
    dcc.Markdown('''
                  _yogipamadya_
                  
                  ''')
       
])
 
@app.callback(
    [Output('deskripsi','children'),Output('grafik','figure')],
    [Input('table-input','data'),Input('table-input','columns'),Input('table-input2','data'),Input('table-input2','columns')]
)
def calculator(a,b,c,d):
    df3 = pd.DataFrame(a,columns=[i['name'] for i in b])
    df4 = pd.DataFrame(c,columns=[i['name'] for i in d])
    
    luas = np.random.normal(int(df3.iloc[2,1]),int(df3.iloc[3,1]),int(df4.iloc[0,0]))
    luas2 = luas.clip(int(df3.iloc[0,1]),int(df3.iloc[1,1]))

    ketebalan = np.random.normal(int(df3.iloc[2,2]),int(df3.iloc[3,2]),int(df4.iloc[0,0]))
    ketebalan2 = ketebalan.clip(int(df3.iloc[0,2]),int(df3.iloc[1,2]))

    ntg = np.random.normal(int(df3.iloc[2,3]),int(df3.iloc[3,3]),int(df4.iloc[0,0]))
    ntg2 = ntg.clip(int(df3.iloc[0,3]),int(df3.iloc[1,3]))

    por = np.random.normal(int(df3.iloc[2,4]),int(df3.iloc[3,4]),int(df4.iloc[0,0]))
    por2 = por.clip(int(df3.iloc[0,4]),int(df3.iloc[1,4]))

    sw = np.random.normal(int(df3.iloc[2,5]),int(df3.iloc[3,5]),int(df4.iloc[0,0]))
    sw2 = sw.clip(int(df3.iloc[0,5]),int(df3.iloc[1,5]))

    bo = np.random.uniform(int(df3.iloc[0,6]),int(df3.iloc[1,6]),int(df4.iloc[0,0]))

    cadangan = 7758*(luas2*0.000247105)*(ketebalan2*3.28084)*(ntg2/100)*((100-sw2)/100)*(por2/100)/bo

    total = pd.DataFrame(cadangan,columns=['OOIP']).describe(percentiles=[.1,.2,.25,.5,.6,.75,.9]).round().T
    
    fig = go.Figure()

    fig.add_trace(go.Histogram(x=cadangan,cumulative_enabled=True))
    fig.update_layout(
    title_text='OOIP Iteration '+ str(df4.iloc[0,0]) , # title of plot
    xaxis_title_text='Barrel Oil', # xaxis label
    yaxis_title_text='Count', # yaxis label
    )
    des = [dash_table.DataTable(
    id='tes',
    columns=[{"name": i, "id": i} for i in total.columns],
    data=total.to_dict('records'),
    )]
    
    return (des,fig)
    
    

if __name__ == '__main__':
    app.run_server(debug=True)
