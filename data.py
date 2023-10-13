# data.py
import pandas as pd
import numpy as np

# *import the data of company data for test
company_data = pd.read_excel("./data_source/filter_data.xlsx")


def production(company_data, company_nordem):
    production_data = company_data.copy()
    production_data = production_data[production_data["id_numord"] == company_nordem]

    # Sumatory of all salaries
    production_data["sum_salarios"] = (
        production_data["AJU_II_PA_PP_SUELD_EP"]
        + production_data["AJU_II_PA_TD_SUELD_ET"]
        + production_data["AJU_II_PA_TI_SUELD_ETA"]
        + production_data["AJU_II_PA_AP_AAS_AP"]
        + production_data["AJU_II_PP_PP_SUELD_OP"]
        + production_data["AJU_II_PP_TD_SUELD_OT"]
        + production_data["AJU_II_PP_TI_SUELD_OTA"]
        + production_data["AJU_II_PP_AP_AAS_PP"]
    )

    # operation of averange salary for perosnal
    production_data["sal_percapita"] = (
        production_data["sum_salarios"] / production_data["tot_empleo"]
    )

    # diference of production and sells
    production_data["pro-ven"] = (
        production_data["AJU_III_PE_PRODUCCION"] - production_data["total_ventas"]
    )

    # diference of inventory
    # production_data["previus_onvent"] =
    production_data["dif-inv"] = production_data["III_EX__VEXIS"] - production_data[
        "III_EX__VEXIS"
    ].shift(periods=1, fill_value=None)

    # inventory coeficient
    production_data["coeficiente"] = production_data.apply(
        lambda row: row["pro-ven"] / row["dif-inv"] if row["dif-inv"] != 0 else 0,
        axis=1,
    )

    production_data = production_data.pivot_table(
        index=["anio", "mes"],
        values=[
            "AJU_III_PE_PRODUCCION",
            "AJU_III_PE_VENTASIN",
            "AJU_III_PE_VENTASEX",
            "total_ventas",
            "III_EX__VEXIS",
            "sal_percapita",
            "tot_operativo",
            "tot_empleo",
            "dif-inv",
            "pro-ven",
            "coeficiente",
            "AJU_II_HORAS_HORDI_T",
            "AJU_II_HORAS_HEXTR_T",
        ],
    )

    # aplay fortmat for presentation of the table.
    # i use a lambda funtion, for each x put this format

    production_data["coeficiente"] = production_data["coeficiente"].apply(
        lambda x: "{:.2f}".format(x)
    )

    # Change name of colums
    production_data = production_data.rename(
        columns={
            "AJU_III_PE_PRODUCCION": "Produccion",
            "AJU_III_PE_VENTASIN": "Ventas_int",
            "AJU_III_PE_VENTASEX": "Ventas_ext",
            "III_EX__VEXIS": "Existen",
            "AJU_II_HORAS_HORDI_T":"Horas_Ord",
            "AJU_II_HORAS_HEXTR_T":"Horas_Ext",
        }
    )

    # reset the index of table
    production_data = production_data.reset_index()
    production_data = production_data.copy()

    # Create the column of Periodo
    production_data["Periodo"] = pd.to_datetime(
        production_data["anio"].astype(str) + "-" + production_data["mes"].astype(str),
        format="%Y-%m",
    )

    # Order columns
    prod_order = [
        "Periodo",
        "Produccion",
        "Ventas_int",
        "Ventas_ext",
        "total_ventas",
        "Existen",
        "tot_empleo",
        "tot_operativo",
        "sal_percapita",
        "pro-ven",
        "dif-inv",
        "coeficiente",
        "Horas_Ord",
        "Horas_Ext",
    ]

    production_data = production_data.reindex(columns=prod_order)

    # !format of columns - no funcionan
    # colums_number_format = [
    #     "Produccion",
    #     "Ventas_int",
    #     "Ventas_ext",
    #     "total_ventas",
    #     "Existen",
    #     "tot_empleo",
    #     "tot_operativo",
    #     "sal_percapita",
    #     "pro-ven",
    #     "dif-inv",
    # ]
    # production_data[colums_number_format] = production_data[colums_number_format].apply(
    #     lambda x: "{:,.2f}".format(x) if isinstance(x, (int, float)) else x
    # )

    return production_data


# * lines to try the code only activate to prove data
# producion_of_company = production(company_data, 438)
# print(producion_of_company)

# *Resume Tables of production
# funtion to resume production and sells per yeart
def resume_production(data):
    resume_table = data.groupby(data["Periodo"].dt.year).agg(
        {"Produccion": np.sum, "total_ventas": np.sum}
    )
    resume_table = resume_table.reset_index(drop = False)
    return resume_table

# *funtion to calculate hours per week
def resume_hours(data):
    for_drop = [
    "Produccion",
    "Ventas_int",
    "Ventas_ext",
    "total_ventas",
    "Existen",
    "tot_empleo",
    "sal_percapita",
    "pro-ven",
    "dif-inv",
    "coeficiente",
    ]
    final_mount = data
    final_mount = final_mount.drop(columns= for_drop)
    before_period = final_mount.iloc[-12]
    before_period = before_period.to_frame().T
    final_mount = final_mount.iloc[-2:]
    final_mount = pd.concat([before_period, final_mount ], axis=0)
    final_mount["promedio_30"] = ((final_mount["Horas_Ord"]+final_mount["Horas_Ext"])/30)/final_mount["tot_operativo"]
    final_mount["promedio_29"] = ((final_mount["Horas_Ord"]+final_mount["Horas_Ext"])/29)/final_mount["tot_operativo"]
    return final_mount


# This funtion calculate admin personal and production pertonal
def all_personal(company_data, company_nordem):
    company_data = company_data[company_data["id_numord"] == company_nordem]
    company_data = company_data.pivot_table(
        index=["anio", "mes"],
        values=[
            "id_numord",
            "II_PA_PP__NPERS_EP",
            "AJU_II_PA_PP_SUELD_EP",
            "II_PA_TD__NPERS_ET",
            "AJU_II_PA_TD_SUELD_ET",
            "II_PA_TI__NPERS_ETA",
            "AJU_II_PA_TI_SUELD_ETA",
            "II_PA_AP__AAEP",
            "AJU_II_PA_AP_AAS_AP",
            "II_PP_PP__NPERS_OP",
            "AJU_II_PP_PP_SUELD_OP",
            "II_PP_TD__NPERS_OT",
            "AJU_II_PP_TD_SUELD_OT",
            "II_PP_TI__NPERS_OTA",
            "AJU_II_PP_TI_SUELD_OTA",
            "II_PP_AP__APEP",
            "AJU_II_PP_AP_AAS_PP",
            "tot_empleo",
        ],
    )

    # averange salary per category
    company_averange_salary = company_data.copy()
    company_averange_salary["admin_per_dir"] = (
        company_averange_salary["AJU_II_PA_PP_SUELD_EP"]
        / company_averange_salary["II_PA_PP__NPERS_EP"]
    )
    company_averange_salary["admin_tem_dir"] = (
        company_averange_salary["AJU_II_PA_TD_SUELD_ET"]
        / company_averange_salary["II_PA_TD__NPERS_ET"]
    )
    company_averange_salary["admin_per_emp"] = (
        company_averange_salary["AJU_II_PA_TI_SUELD_ETA"]
        / company_averange_salary["II_PA_TI__NPERS_ETA"]
    )
    company_averange_salary["admin_per_apr"] = (
        company_averange_salary["AJU_II_PA_AP_AAS_AP"]
        / company_averange_salary["II_PA_AP__AAEP"]
    )
    company_averange_salary["pro_per_dir"] = (
        company_averange_salary["AJU_II_PP_PP_SUELD_OP"]
        / company_averange_salary["II_PP_PP__NPERS_OP"]
    )
    company_averange_salary["pro_tem_dir"] = (
        company_averange_salary["AJU_II_PP_TD_SUELD_OT"]
        / company_averange_salary["II_PP_TD__NPERS_OT"]
    )
    company_averange_salary["pro_per_emp"] = (
        company_averange_salary["AJU_II_PP_TI_SUELD_OTA"]
        / company_averange_salary["II_PP_TI__NPERS_OTA"]
    )
    company_averange_salary["pro_per_apr"] = (
        company_averange_salary["AJU_II_PP_AP_AAS_PP"]
        / company_averange_salary["II_PP_AP__APEP"]
    )

    """
        create table of administrative workers, 
        drop colums of the other categories, order columns and return this data
    """

    colums_to_delete_adm = [
        "AJU_II_PA_PP_SUELD_EP",
        "AJU_II_PA_TD_SUELD_ET",
        "AJU_II_PA_TI_SUELD_ETA",
        "AJU_II_PA_AP_AAS_AP",
        "AJU_II_PP_PP_SUELD_OP",
        "AJU_II_PP_TD_SUELD_OT",
        "AJU_II_PP_TI_SUELD_OTA",
        "AJU_II_PP_AP_AAS_PP",
        "tot_empleo",
        "II_PP_PP__NPERS_OP",
        "II_PP_TD__NPERS_OT",
        "II_PP_TI__NPERS_OTA",
        "II_PP_AP__APEP",
        "AJU_II_PP_AP_AAS_PP",
    ]

    company_admin_per = company_averange_salary.copy()
    company_admin_per = company_admin_per.drop(colums_to_delete_adm, axis=1)
    company_admin_per = company_admin_per.rename(
        columns={
            "II_PA_PP__NPERS_EP": "#_admin_per_dir",
            "II_PA_TD__NPERS_ET": "#_admin_tem_dir",
            "II_PA_TI__NPERS_ETA": "#_admin_tem_emp",
            "II_PA_AP__AAEP": "#_admin_ape",
        }
    )


    """ create table production workers,
    delete colums, order columns and create a table of production workers"""

    # colums to drop
    colums_to_delete_prd = [
        "II_PA_PP__NPERS_EP",
        "AJU_II_PA_PP_SUELD_EP",
        "II_PA_TD__NPERS_ET",
        "AJU_II_PA_TD_SUELD_ET",
        "II_PA_TI__NPERS_ETA",
        "AJU_II_PA_TI_SUELD_ETA",
        "II_PA_AP__AAEP",
        "AJU_II_PA_AP_AAS_AP",
        "AJU_II_PP_PP_SUELD_OP",
        "AJU_II_PP_TD_SUELD_OT",
        "AJU_II_PP_TI_SUELD_OTA",
        "AJU_II_PP_AP_AAS_PP",
        "tot_empleo",
        "admin_per_dir",
        "admin_tem_dir",
        "admin_per_emp",
        "admin_per_apr",
    ]

    company_prod_per = company_averange_salary.copy()
    company_prod_per = company_prod_per.drop(columns=colums_to_delete_prd, axis=1)
    company_prod_per = company_prod_per.rename(
        columns={
            "II_PP_PP__NPERS_OP": "#_prod_dir",
            "II_PP_TD__NPERS_OT": "#_prod_tem_dir",
            "II_PP_TI__NPERS_OTA": "#_prod_tem_emp",
            "II_PP_AP__APEP": "#_prod_apr",
        }
    )

    company_admin_per = company_admin_per.reset_index(drop=False)
    company_prod_per = company_prod_per.reset_index(drop=False)
    
    company_prod_per["Periodo"] = pd.to_datetime(
    company_prod_per["anio"].astype(str) + "-" + company_prod_per["mes"].astype(str),
    format="%Y-%m",
    )
    company_prod_per = company_prod_per.drop(["anio", "mes"], axis= 1)
    
    
    company_admin_per["Periodo"] = pd.to_datetime(
    company_admin_per["anio"].astype(str) + "-" + company_admin_per["mes"].astype(str),
    format="%Y-%m",
    )
    company_admin_per = company_admin_per.drop(["anio", "mes"], axis= 1)
    
    prod_per_order = [
        "Periodo",
        "#_prod_dir",
        "pro_per_dir",
        "#_prod_tem_dir",
        "pro_tem_dir",
        "#_prod_tem_emp",
        "pro_per_emp",
        "#_prod_apr",
        "pro_per_apr",
    ]
    company_prod_per = company_prod_per.reindex(columns=prod_per_order)
    
    # order de columns and gives new names
    admin_order_var = [
        "Periodo",
        "#_admin_per_dir",
        "admin_per_dir",
        "#_admin_tem_dir",
        "admin_tem_dir",
        "#_admin_tem_emp",
        "admin_per_emp",
        "#_admin_ape",
        "admin_per_apr",
    ]
    # company admin personal table finished
    company_admin_per = company_admin_per.reindex(columns=admin_order_var)

    return company_prod_per, company_admin_per


# * lines to try the code only activate to prove data
# personal_pro, personal_admin = all_personal(company_data, 438)
# print(personal_pro)
# print(personal_admin)