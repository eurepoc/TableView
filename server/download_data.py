from dash.dependencies import Input, Output
from dash import dcc, ctx, callback
import pandas as pd
import io
from datetime import datetime as dt
from server.filter_function import filter_datatable
import urllib.parse


def all_to_none(value):
    if value == "All":
        return None
    else:
        return value


def download_data(app, df, states_codes, search_func, validation_func):
    @app.callback(
        Output("download-dataframe-csv", "data"),
        Input("download-button", "n_clicks"),
        Input(component_id='incident_type_dd', component_property='value'),
        Input(component_id='receiver_country_dd', component_property='value'),
        Input(component_id='receiver_category_dd', component_property='value'),
        Input(component_id='receiver_subcategory_dd', component_property='value'),
        Input(component_id='initiator_country_dd', component_property='value'),
        Input(component_id='initiator_category_dd', component_property='value'),
        Input(component_id='initiator_subcategory_dd', component_property='value'),
        Input(component_id='attribution_basis_dd', component_property='value'),
        Input(component_id='receiver_name_dd', component_property='value'),
        Input(component_id='initiator_name_dd', component_property='value'),
        Input(component_id='search', component_property='value'),
        Input(component_id='attribution_type_dd', component_property='value'),
        Input(component_id="attribution_number_dd", component_property="value"),
        Input(component_id="cyber_conflict_issue_dd", component_property="value"),
        Input(component_id="offline_conflict_name_dd", component_property="value"),
        Input(component_id="intensity_dd", component_property="value"),
        Input(component_id='date-picker-range', component_property='start_date'),
        Input(component_id='date-picker-range', component_property='end_date'),
        prevent_initial_call=True,
    )
    def func(n_clicks,
            type_filter,
            receiver_country_filter,
            receiver_category_filter,
            receiver_subcategory_filter,
            initiator_country_filter,
            initiator_category_filter,
            initiator_subcategory_filter,
            attribution_basis_filter,
            receiver_name_filter,
            initiator_name_filter,
            search_filter,
            attribution_type_filter,
            attribution_number_filter,
            cyber_conflict_issue_filter,
            offline_conflict_name_filter,
            intensity_filter,
            start_date_start,
            start_date_end):

        type_filter = validation_func(type_filter)
        receiver_country_filter = validation_func(receiver_country_filter)
        receiver_category_filter = validation_func(receiver_category_filter)
        receiver_subcategory_filter = validation_func(receiver_subcategory_filter)
        initiator_country_filter = validation_func(initiator_country_filter)
        initiator_category_filter = validation_func(initiator_category_filter)
        initiator_subcategory_filter = validation_func(initiator_subcategory_filter)
        attribution_basis_filter = validation_func(attribution_basis_filter)
        receiver_name_filter = validation_func(receiver_name_filter)
        initiator_name_filter = validation_func(initiator_name_filter)
        attribution_type_filter = validation_func(attribution_type_filter)
        attribution_number_filter = validation_func(attribution_number_filter)
        cyber_conflict_issue_filter = validation_func(cyber_conflict_issue_filter)
        offline_conflict_name_filter = validation_func(offline_conflict_name_filter)
        intensity_filter = validation_func(intensity_filter)

        if "download-button" == ctx.triggered_id:

            filtered_data_initial = df.copy()

            if start_date_start == "2000-01-01" and start_date_end == str(dt.now().date()):
                start_date = None
                end_date = None
            else:
                start_date = pd.to_datetime(start_date_start).strftime('%Y-%m-%d')
                end_date = pd.to_datetime(start_date_end).strftime('%Y-%m-%d')

            if initiator_country_filter == "All countries":
                initiator_country_filter = None

            type_filter = all_to_none(type_filter)
            intensity_filter = all_to_none(intensity_filter)
            attribution_number_filter = all_to_none(attribution_number_filter)
            receiver_category_filter = all_to_none(receiver_category_filter)
            receiver_subcategory_filter = all_to_none(receiver_subcategory_filter)
            initiator_category_filter = all_to_none(initiator_category_filter)
            initiator_subcategory_filter = all_to_none(initiator_subcategory_filter)
            attribution_basis_filter = all_to_none(attribution_basis_filter)
            receiver_name_filter = all_to_none(receiver_name_filter)
            initiator_name_filter = all_to_none(initiator_name_filter)
            attribution_type_filter = all_to_none(attribution_type_filter)
            cyber_conflict_issue_filter = all_to_none(cyber_conflict_issue_filter)
            offline_conflict_name_filter = all_to_none(offline_conflict_name_filter)

            if intensity_filter:
                intensity_filter = str(intensity_filter)
            if attribution_number_filter:
                attribution_number_filter = str(attribution_number_filter)

            region_filter = None

            if receiver_country_filter:
                if receiver_country_filter == "Global (states)":
                    receiver_country_filter = None
                elif "(states)" in receiver_country_filter and receiver_country_filter != "Global (states)":
                    state = receiver_country_filter
                    if receiver_country_filter in states_codes:
                        region_filter = states_codes[state]
                        receiver_country_filter = None
                elif receiver_country_filter == "EU (member states)":
                    receiver_country_filter = None
                    region_filter = "EU(MS)"
                elif receiver_country_filter == "NATO (member states)":
                    receiver_country_filter = None
                    region_filter = "NATO"
                else:
                    receiver_country_filter = receiver_country_filter

            # Define input filters in dictionary
            input_filters = {
                'incident_type': type_filter,
                'receiver_country': receiver_country_filter,
                "receiver_category": receiver_category_filter,
                "receiver_category_subcode": receiver_subcategory_filter,
                "initiator_country": initiator_country_filter,
                "initiator_category": initiator_category_filter,
                "initiator_category_subcode": initiator_subcategory_filter,
                "attribution_basis": attribution_basis_filter,
                "receiver_name": receiver_name_filter,
                "initiator_name": initiator_name_filter,
                "attribution_type": attribution_type_filter,
                "number_of_attributions": attribution_number_filter,
                "cyber_conflict_issue": cyber_conflict_issue_filter,
                "offline_conflict_issue_subcode": offline_conflict_name_filter,
                "weighted_cyber_intensity": intensity_filter,
                "receiver_region": region_filter,
            }

            if search_filter:
                results = search_func(search_filter)
                filtered_data = filtered_data_initial[filtered_data_initial["ID"].isin(results)]
                filtered_data = filtered_data.set_index("ID").loc[results].reset_index()

                if start_date and end_date:
                    filtered_data = filtered_data.loc[(filtered_data['start_date'] >= start_date)
                                                      & (filtered_data['start_date'] <= end_date)]
                for col, val in input_filters.items():
                    if val is not None:
                        filtered_data[col] = filtered_data[col].fillna('').astype(str)
                        filtered_data = filtered_data.loc[filtered_data[col].str.contains(val, regex=False)]

            else:
                filtered_data = pd.DataFrame.from_dict(filtered_data_initial)
                if start_date and end_date:
                    filtered_data = filtered_data.loc[(filtered_data['start_date'] >= start_date)
                                                      & (filtered_data['start_date'] <= end_date)]
                for col, val in input_filters.items():
                    if val is not None:
                        filtered_data[col] = filtered_data[col].fillna('').astype(str)
                        filtered_data = filtered_data.loc[filtered_data[col].str.contains(val, regex=False)]

            return dcc.send_data_frame(filtered_data.to_excel, f"eurepoc_data_{dt.now().strftime('%Y-%m-%dT%H:%M')}.xlsx", index=False, engine='openpyxl')
