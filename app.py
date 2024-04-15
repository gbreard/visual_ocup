import dash
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Cargar datos
df = pd.read_excel("Datos-Coupa.xlsx")  # Ajusta la ruta a tu archivo


# In[7]:


# Inicializar la aplicación Dash
app = Dash(__name__)
server = app.server 

# Asegurarse de que las columnas de años son strings para facilitar la manipulación
df.columns = df.columns.map(str)

# Lista de años como strings para los sliders
years = [str(year) for year in range(2008, 2024)]

# Definir la disposición de la aplicación
app.layout = html.Div([
    html.H1("Dashboard de Ocupaciones"),
    dcc.Dropdown(
        id='occupation-dropdown',
        options=[{'label': i, 'value': i} for i in df['Ocupación'].unique()],
        value=df['Ocupación'].unique()[0]
    ),
    dcc.RangeSlider(
        id='year-range-slider',
        min=2008,
        max=2023,
        step=1,
        value=[2008, 2023],
        marks={year: year for year in years}
    ),
    dcc.Graph(id='employment-graph'),
    dcc.Graph(id='growth-graph'),
])

# Definir la interactividad
@app.callback(
    [Output('employment-graph', 'figure'), Output('growth-graph', 'figure')],
    [Input('occupation-dropdown', 'value'), Input('year-range-slider', 'value')]
)
def update_graphs(selected_occupation, year_range):
    # Filtrar por ocupación
    filtered_df = df[df['Ocupación'] == selected_occupation]
    
    # Transformar datos a formato long
    melted_df = filtered_df.melt(id_vars=['Ocupación', 'clasificacion_refinada', 'Descripción del Grupo'], 
                                 value_vars=[year for year in years if int(year) >= year_range[0] and int(year) <= year_range[1]],
                                 var_name='Año', value_name='Empleo')

    # Crear gráficos
    fig_employment = px.line(melted_df, x='Año', y='Empleo', title='Empleo a lo largo del tiempo')
    fig_growth = px.bar(melted_df, x='Año', y='Empleo', title='Crecimiento por Año')

    return fig_employment, fig_growth

# Correr la aplicación en modo adecuado para notebooks
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=os.environ.get('PORT', 8050))


