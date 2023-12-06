from dash.dependencies import Input, Output, State
from dash import callback_context as ctx


def refresh_url(app):
    @app.callback(Output('url-updater', 'search'),
                  [Input('incident_type_dd', 'value'),
                   Input('receiver_country_dd', 'value'),
                   Input('receiver_category_dd', 'value'),
                   Input('initiator_country_dd', 'value'),
                   Input('initiator_category_dd', 'value'),
                   Input('attribution_basis_dd', 'value'),
                   Input('receiver_name_dd', 'value'),
                   Input('initiator_name_dd', 'value'),
                   Input('search', 'value'),
                   Input('attribution_type_dd', 'value'),
                   Input("attribution_number_dd", "value"),
                   Input("cyber_conflict_issue_dd", "value"),
                   Input("offline_conflict_name_dd", "value"),
                   Input("intensity_dd", "value"),
                   Input('date-picker-range', 'start_date'),
                   Input('date-picker-range', 'end_date')],
                  [State('url-updater', 'search')])
    def update_url(*args):
        # If the callback was not triggered by the initial load of the application
        if ctx.triggered:
            # Get the id of the input that triggered the callback
            input_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # If the callback was triggered by a dropdown
            if input_id in ['incident_type_dd', 'receiver_country_dd', 'receiver_category_dd',
                            'initiator_country_dd', 'initiator_category_dd', 'attribution_basis_dd',
                            'receiver_name_dd', 'initiator_name_dd', 'search',
                            'attribution_type_dd', 'attribution_number_dd',
                            'cyber_conflict_issue_dd', 'offline_conflict_name_dd',
                            'intensity_dd', 'date-picker-range']:
                return '?cyber_incident=All'

        # If the callback was triggered by the initial load of the application,
        # or by something else, don't change the URL
        return args[-1]
