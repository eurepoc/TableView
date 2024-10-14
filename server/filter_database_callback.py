from dash.dependencies import Input, Output, State
from server.filter_function import filter_datatable
import dash
import bleach

def database_filter(app, dataframe, states_codes, search_func, validation_func):
    # DataTable callback
    @app.callback(
        Output('row-count', 'children'),
        Output(component_id='datatable', component_property='data'),
        Output(component_id='datatable', component_property='tooltip_data'),
        Output(component_id='filter-bar', component_property='style'),
        Output(component_id='back-button-row', component_property='style'),
        Output(component_id="database-title", component_property="style"),
        Output(component_id='datatable', component_property='selected_rows'),
        Output(component_id='datatable-row', component_property='style'),
        Output(component_id='download_row', component_property='style'),
        Input(component_id='url', component_property='href'),
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
        Input(component_id='impact_indicator_dd', component_property='value'),
        Input(component_id='state_responsibility_dd', component_property='value'),
        Input(component_id='il_breach_dd', component_property='value'),
        Input(component_id='date-picker-range', component_property='start_date'),
        Input(component_id='date-picker-range', component_property='end_date'),
        Input('datatable', "page_current"),
        Input('datatable', "page_size"),
        Input('datatable', "sort_by")
    )
    def update_table(
            url,
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
            impact_indicator_filter,
            state_responsibility_filter,
            il_breach_filter,
            start_date_start,
            start_date_end,
            page_current,
            page_size,
            sort_by
    ):

        filtered_data_initial = dataframe

        type_filter = validation_func(type_filter)
        receiver_country_filter = validation_func(receiver_country_filter)
        #receiver_category_filter = validation_func(receiver_category_filter)
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
        impact_indicator_filter = validation_func(impact_indicator_filter)
        state_responsibility_filter = validation_func(state_responsibility_filter)
        il_breach_filter = validation_func(il_breach_filter)

        # Parse the 'url' Input if there was no dropdown change
        if url and '?' in url:
            params = dict([param.split('=') for param in url.split('?')[1].split('&')])
            incident_id = params.get('cyber_incident', 'All')
            incident_id = bleach.clean(incident_id)
        else:
            incident_id = "All"

        if incident_id != "All":
            filtered_data_initial = filtered_data_initial[filtered_data_initial['ID'] == int(incident_id)]
            tooltip_data = [{column: {'value': str(value), 'type': 'markdown'}
                             for column, value in row.items() if column not in ['initiator_name', 'receiver_name',
                             'context', 'start_date', "number_of_attributions", "number_of_political_responses",
                             "number_of_legal_responses", "zero_days", "radar_score_impact",
                             "radar_score_intensity", "radar_score_political", "radar_score_legal",
                             "radar_score_offline_conflict", "radar_score_attribution",
                             "legal_response_country", "impact_indicator", "weighted_cyber_intensity"]
                             }
                            for row in filtered_data_initial.to_dict('records')]

            data = filtered_data_initial.to_dict('records')

            return "", data, tooltip_data, {'display': 'none'}, {'margin-bottom': '20px'}, {'display': 'none'}, [0], {'display': 'none'}, {'display': 'none'}

        else:
            data, tooltip_data = filter_datatable(
                start_date_start,
                start_date_end,
                initiator_country_filter,
                type_filter,
                intensity_filter,
                attribution_number_filter,
                receiver_country_filter,
                receiver_category_filter,
                receiver_subcategory_filter,
                initiator_category_filter,
                initiator_subcategory_filter,
                attribution_basis_filter,
                receiver_name_filter,
                initiator_name_filter,
                search_filter,
                attribution_type_filter,
                cyber_conflict_issue_filter,
                offline_conflict_name_filter,
                impact_indicator_filter,
                state_responsibility_filter,
                il_breach_filter,
                states_codes,
                filtered_data_initial,
                search_func
            )

            if len(sort_by):
                dff = data.sort_values(
                        sort_by[0]['column_id'],
                        ascending=sort_by[0]['direction'] == 'asc',
                        inplace=False
                )
                      
                tooltip_data = [{column: {'value': str(value), 'type': 'markdown'}
                         for column, value in row.items() if column not in ['initiator_name', 'receiver_name',
                             'context', 'start_date', "number_of_attributions", "number_of_political_responses",
                             "number_of_legal_responses", "zero_days", "radar_score_impact",
                             "radar_score_intensity", "radar_score_political", "radar_score_legal",
                             "radar_score_offline_conflict", "radar_score_attribution",
                             "legal_response_country", "impact_indicator", "weighted_cyber_intensity"]
                         }
                        for row in dff.to_dict('records')]
                
            else:
                # No sort is applied
                dff = data

            nb_incidents = f"- showing {len(data)}/{len(filtered_data_initial)} cyber incidents"

            return nb_incidents, \
                dff.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records'), \
                tooltip_data, \
                {},\
                {'display': 'none'}, \
                {'margin-top': '0px', 'margin-bottom': '20px'}, \
                [], \
                {'margin-top': '0px', 'margin-bottom': '20px'}, \
                {'margin-bottom': '5px'}


def back_button_callback(app):
    @app.callback(
        Output(component_id='url-updater', component_property='search'),
        Input(component_id='back-button', component_property='n_clicks'),
    )
    def back_button(n_clicks):
        if n_clicks == 0:
            raise dash.exceptions.PreventUpdate
        else:
            return '?cyber_incident=All'
