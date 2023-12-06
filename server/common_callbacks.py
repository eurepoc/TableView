from dash.dependencies import Input, Output, State
from datetime import datetime as dt


def more_filters_button(app):
    @app.callback(
        Output("collapse", "is_open"),
        [Input("collapse-button", "n_clicks")],
        [State("collapse", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open


def reset_filters_button(app):
    @app.callback(
        Output('receiver_country_dd', 'value'),
        Output('initiator_country_dd', 'value'),
        Output('date-picker-range', 'start_date'),
        Output('date-picker-range', 'end_date'),
        Output('incident_type_dd', component_property='value'),
        Output('receiver_category_dd', component_property='value'),
        Output('initiator_category_dd', component_property='value'),
        Output('attribution_basis_dd', component_property='value'),
        Output('receiver_name_dd', component_property='value'),
        Output('initiator_name_dd', component_property='value'),
        Output('search', component_property='value'),
        Output('attribution_type_dd', component_property='value'),
        Output("attribution_number_dd", component_property="value"),
        Output("cyber_conflict_issue_dd", component_property="value"),
        Output("offline_conflict_name_dd", component_property="value"),
        Output("intensity_dd", component_property="value"),
        #Output('datatable', "sort_by"),
        #Output('datatable', "page_current"),
        Input("reset", "n_clicks")
    )
    def on_button_click(n_clicks):
        if n_clicks is not None:
            return \
                "Global (states)", \
                    None, \
                    "2000-01-01", \
                    dt.now().date(), \
                    None, None, None, None, None, None, None, None, None, None, None, None


def reset_pagination(app):
    @app.callback(
        Output('datatable', "sort_by"),
        Output('datatable', "page_current"),
        Input('receiver_country_dd', 'value'),
        Input('initiator_country_dd', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('incident_type_dd', component_property='value'),
        Input('receiver_category_dd', component_property='value'),
        Input('initiator_category_dd', component_property='value'),
        Input('attribution_basis_dd', component_property='value'),
        Input('receiver_name_dd', component_property='value'),
        Input('initiator_name_dd', component_property='value'),
        Input('search', component_property='value'),
        Input('attribution_type_dd', component_property='value'),
        Input("attribution_number_dd", component_property="value"),
        Input("cyber_conflict_issue_dd", component_property="value"),
        Input("offline_conflict_name_dd", component_property="value"),
        Input("intensity_dd", component_property="value"),
        Input("reset", "n_clicks")
    )
    def on_button_click(*args):
        return [], 0



def get_total_incidents(app, df):
    @app.callback(
        Output('row-count', 'children'),
        [Input('datatable', 'data')]
    )
    def update_row_count(data):
        return f"- showing {len(data)}/{len(df)} cyber incidents"
