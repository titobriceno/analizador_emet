# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, State
from data import *

# Incorporate data
company_data = pd.read_excel("./data_source/filter_data.xlsx")
df_production = production(company_data, 414)
df_production = df_production.round(2)
df_resume_production = resume_production(df_production)
df_resume_hours = resume_hours(df_production)
df_prod_personal, df_admin_personal = all_personal(company_data, 414)


# !hacer una funcion para no repetir este codigo despues en callback
# esta funcion hace la primera vista de la grafica
def generate_graf(data_production):
    # Crea una figura de Plotly con la primera línea (Producción)
    fig = go.Figure()
    # Agrega una segunda línea (Ventas) a la figura existente
    fig.add_trace(
        go.Scatter(
            x=data_production["Periodo"],
            y=data_production["total_ventas"],
            mode="lines",
            name="Ventas",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data_production["Periodo"],
            y=data_production["Existen"],
            mode="lines",
            name="Existencias",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data_production["Periodo"],
            y=data_production["Produccion"],
            mode="lines",
            name="Produccion",
        )
    )
    return fig


# This the funtion to generate graf of personal
def personal_graf_prod(personal_data):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["#_prod_dir"],
            mode="lines",
            name="Prod_dir",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["#_prod_tem_dir"],
            mode="lines",
            name="Tem_dir",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["#_prod_tem_emp"],
            mode="lines",
            name="temp_empleo",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["#_prod_apr"],
            mode="lines",
            name="Apren",
        )
    )

    return fig


def personal_graf_admin(personal_data):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["#_admin_per_dir"],
            mode="lines",
            name="Prod_dir",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["#_admin_tem_dir"],
            mode="lines",
            name="Tem_dir",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["#_admin_tem_emp"],
            mode="lines",
            name="temp_emp",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["#_admin_ape"],
            mode="lines",
            name="Apren",
        )
    )

    return fig


# this create the initial graf
initial_fig = generate_graf(df_production)

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div(
    [
        html.Div(children="Esta es la tabla de producción"),
        html.Div(children="Seleccione la fuente"),
        html.Button("Buscar", id="submit-button", n_clicks=0),
        dcc.Input(id="input-value", type="number", value=414),
        # !la tabla no esta actualizando
        html.Div(
            id="table",
            children=dash_table.DataTable(data=df_production.to_dict("records")),
        ),
        dcc.Graph(id="my-graph"),
        html.Div(children="Resumen Produccion y personal"),
        html.Div(children="Produccion - Ventas"),
        html.Div(
            id="table_resume",
            children=dash_table.DataTable(data=df_resume_production.to_dict("records")),
        ),
        html.Div(children="Horas"),
        html.Div(
            id="hours",
            children=dash_table.DataTable(data=df_resume_hours.to_dict("records")),
        ),
        html.Div(children="Revision de Empleo"),
        html.Div(children="Personal Administrativo"),
        html.Div(
            id="admin_personal",
            children=dash_table.DataTable(data=df_admin_personal.to_dict("records")),
        ),
        dcc.Graph(id="admin_graf"),
        html.Div(children="Personal de produccion"),
        html.Div(
            id="prod_personal",
            children=dash_table.DataTable(data=df_prod_personal.to_dict("records")),
        ),
        dcc.Graph(id="prod_graf"),
    ]
)


# Add controls to build the interaction
@app.callback(
    [
        Output("my-graph", "figure"),
        Output("table", "children"),
        Output("table_resume", "children"),
        Output("hours", "children"),
        Output("admin_personal", "children"),
        Output("prod_personal", "children"),
        Output("admin_graf", "figure"),
        Output("prod_graf", "figure"),
    ],
    [Input("submit-button", "n_clicks")],
    [State("input-value", "value")],
)
def upgrate_production(n_clicks, input_value):
    if n_clicks is None:
        # La página se acaba de cargar y aún no se ha hecho clic en el botón
        raise PreventUpdate

    # in this line the data frame is update
    df_actualizate_production = production(company_data, input_value)
    df_prod, df_admin = all_personal(company_data, input_value)
    # update the production graf
    fig_actulizate = generate_graf(df_actualizate_production)
    print(df_actualizate_production)
    print("nodem =" + str(input_value))

    table = dash_table.DataTable(data=df_actualizate_production.to_dict("records"))
    # actualitation resume production
    acumulate_prod = resume_production(df_actualizate_production)
    resume_table_prod = dash_table.DataTable(data=acumulate_prod.to_dict("records"))
    # update hoours tables
    hours = resume_hours(df_actualizate_production)
    resume_table_hours = dash_table.DataTable(data=hours.to_dict("records"))
    # update peronal tables
    admin = dash_table.DataTable(data=df_admin.to_dict("records"))
    prod = dash_table.DataTable(data=df_prod.to_dict("records"))
    # admin and production tables.
    fig_per_admin = personal_graf_admin(df_admin)
    fig_per_prod = personal_graf_prod(df_prod)

    return (
        fig_actulizate,
        table,
        resume_table_prod,
        resume_table_hours,
        admin,
        prod,
        fig_per_admin,
        fig_per_prod
    )


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
