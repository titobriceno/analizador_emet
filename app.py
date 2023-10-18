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
# this variable contain all data of nordem
df_production = production(company_data, 414)
df_production = df_production.round(2)
# este data frame tiene el acuamulado el añó de producción y ventas
df_resume_production = resume_production(df_production)
# en esta variable se desagrega el calculo de horas
df_resume_hours = resume_hours(df_production)
# Se calcula las tablas de personal
df_prod_personal, df_admin_personal = all_personal(company_data, 414)
#  en las siguientes variables se tiene variaciones mesuales y anuales
df_var_prod_mount, df_var_prod_year = production_var(df_production)
df_var_adm_mon, df_var_adm_yea = var_personal_admin(df_admin_personal)
df_var_prd_mon, df_var_prd_yea = var_personal_prod(df_prod_personal)


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


# This the funtions to generate graf of personal
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


# in this section generate the personal salaries graf
def salary_admin(personal_data):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["admin_per_dir"],
            mode="lines",
            name="admin_per_dir",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["admin_tem_dir"],
            mode="lines",
            name="admin_tem_dir",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["admin_tem_dir"],
            mode="lines",
            name="admin_por_empresa",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["admin_per_apr"],
            mode="lines",
            name="admin_per_apr",
        )
    )
    return fig


def salary_prod(personal_data):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["pro_per_dir"],
            mode="lines",
            name="per-dir",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["pro_tem_dir"],
            mode="lines",
            name="tem_dir",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["pro_per_emp"],
            mode="lines",
            name="prod_por_empresa",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=personal_data["Periodo"],
            y=personal_data["pro_per_apr"],
            mode="lines",
            name="pro_apr",
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
        html.Div(
            id="table",
            children=dash_table.DataTable(data=df_production.to_dict("records")),
        ),
        dcc.Graph(id="my-graph"),
        html.Div(children="Resumen Produccion y personal"),
        html.Div(children="Produccion - Ventas"),
        html.Div(children="Variación Mensual"),
        html.Div(
            id="vars_prod_mount",
            children=dash_table.DataTable(data=df_var_prod_mount.to_dict("records")),
        ),
        html.Div(children="Variación Anual"),
        html.Div(
            id="vars_prod_year",
            children=dash_table.DataTable(data=df_var_prod_year.to_dict("records")),
        ),
        html.Div(children="Año Acumulado"),
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
        html.Div(children="Variacion Mensual"),
        html.Div(
            id="adm_per_mount",
            children=dash_table.DataTable(data=df_var_adm_mon.to_dict("records")),
        ),
        html.Div(children="Variacion Anual"),
        html.Div(
            id="adm_per_year",
            children=dash_table.DataTable(data=df_var_adm_yea.to_dict("records")),
        ),
        html.Div(
            children="Grafica Numero empleados y Salarios Promedio Administrativos"
        ),
        dcc.Graph(id="admin_graf"),
        dcc.Graph(id="averange_salary"),
        html.Div(children="Personal de produccion"),
        html.Div(
            id="prod_personal",
            children=dash_table.DataTable(data=df_prod_personal.to_dict("records")),
        ),
        html.Div(children="Variacion Mensual"),
        html.Div(
            id="var_prod_mont",
            children=dash_table.DataTable(data=df_var_prd_mon.to_dict("records")),
        ),
        html.Div(children="Varación Anual"),
        html.Div(
            id="var_prod_year",
            children=dash_table.DataTable(data=df_var_prd_yea.to_dict("records")),
        ),
        html.Div(children="Grafica Numero empleados y Salarios Promedio Producción"),
        dcc.Graph(id="prod_graf"),
        dcc.Graph(id="averange_prod"),
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
        Output("averange_salary", "figure"),
        Output("averange_prod", "figure"),
        Output("vars_prod_mount", "children"),
        Output("vars_prod_year", "children"),
        Output("adm_per_mount", "children"),
        Output("adm_per_year", "children"),
        Output("var_prod_mont", "children"),
        Output("var_prod_year", "children"),
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
    averange_admin = salary_admin(df_admin)
    average_prod = salary_prod(df_prod)
    # variation per mount and year
    var_prod_mount, var_prod_year = production_var(df_actualizate_production)
    var_pr_mount = dash_table.DataTable(data=var_prod_mount.to_dict("records"))
    var_pr_year = dash_table.DataTable(data=var_prod_year.to_dict("records"))
    var_per_adm_mon, var_per_adm_yea = var_personal_admin(df_admin)
    var_per_adm_mon = dash_table.DataTable(data=var_per_adm_mon.to_dict("records"))
    var_per_adm_yea = dash_table.DataTable(data=var_per_adm_yea.to_dict("records"))
    var_per_prd_mon, var_per_prd_yea = var_personal_prod(df_prod)
    var_per_prd_mon = dash_table.DataTable(data=var_per_prd_mon.to_dict("records"))
    var_per_prd_yea = dash_table.DataTable(data=var_per_prd_yea.to_dict("records"))

    return (
        fig_actulizate,
        table,
        resume_table_prod,
        resume_table_hours,
        admin,
        prod,
        fig_per_admin,
        fig_per_prod,
        averange_admin,
        average_prod,
        var_pr_mount,
        var_pr_year,
        var_per_adm_mon,
        var_per_adm_yea,
        var_per_prd_mon,
        var_per_prd_yea,
    )


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
