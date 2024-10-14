from dash.dependencies import Input, Output
from dash import html
import plotly.graph_objects as go
import pickle
from server.incident_info_function import create_modal_text


# Reading files for radar chart
average_scores_across_incidents = pickle.load(open("./data/average_scores_across_incidents.pickle", "rb"))


def incident_info_callback(app, data_dict, index):
    @app.callback(
        Output('datatable_info', 'children'),
        Output('general_info_incident', 'children'),
        Output('incident_radar', 'figure'),
        Output('datatable_url', 'children'),
        [Input('datatable', 'data'),
         Input('datatable', 'selected_rows')]
    )
    def display_selected_row(data, selected_rows):

        if selected_rows is not None and len(selected_rows) > 0:

            row_data = data[selected_rows[0]]
            incident_title = f'{row_data["name"]}'
            incident_url = f'https://eurepoc.eu/table-view/?cyber_incident={row_data["ID"]}'
            general_info_text = create_modal_text(
                data=data_dict,
                index=index,
                derived_virtual_data=row_data
            )

            # Radar chart
            incident_radar_figures = {
                '<b>Impact indicator</b>': float(row_data["radar_score_impact"])if row_data["radar_score_impact"] is not None else 0,
                '<b>Cyber intensity</b>':  float(row_data["radar_score_intensity"]) if row_data["radar_score_intensity"] is not None else 0,
                '<b>Offline conflict intensity</b>': float(row_data["radar_score_offline_conflict"]) if row_data["radar_score_offline_conflict"] is not None else 0,
                '<b>Attribution time</b>': float(row_data["radar_score_attribution"]) if row_data["radar_score_attribution"] is not None else 0,
                "<b>Number of political responses</b>": float(row_data["radar_score_political"]) if row_data["radar_score_political"] is not None else 0,
                "<b>Number of legal responses</b>": float(row_data["radar_score_legal"]) if row_data["radar_score_legal"] is not None else 0,
                "<b>Impact indicator</b>": float(row_data["radar_score_impact"]) if row_data["radar_score_impact"] is not None else 0
            }

            fig = go.Figure(data=go.Scatterpolar(
                r=[value for value in average_scores_across_incidents.values()] + [average_scores_across_incidents['<b>Impact indicator</b>']],
                theta=[key for key in average_scores_across_incidents.keys()] + ['<b>Impact indicator</b>'],
                mode='lines+markers',
                fill='none',
                line=dict(width=3, color='rgba(0, 44, 56, 0.5)'),
                marker=dict(size=10, color='rgba(0, 44, 56, 0.5)'),
                name="Average across all incidents",
                hovertemplate='Indicator: %{theta}<br>'
                              'Scaled score: %{r:.2f}<extra></extra>'
            ))

            fig.add_trace(go.Scatterpolar(
                r=[value for value in incident_radar_figures.values()] + [incident_radar_figures['<b>Impact indicator</b>']],
                theta=[key for key in incident_radar_figures.keys()] + ['<b>Impact indicator</b>'],
                mode='lines+markers',
                fill='none',
                line=dict(width=3, color='#CC0130'),
                marker=dict(size=10, color='#CC0130'),
                name="Selected incident",
                hovertemplate='Indicator: %{theta}<br>'
                              'Scaled score: %{r:.2f}<extra></extra>'
            ))

            fig.update_layout(
                polar=dict(
                    bgcolor='rgba (0, 0, 0, 0)',
                    radialaxis=dict(
                        visible=True,
                        range=[0, 4],
                        tickmode='linear',
                        dtick=1,
                        showticklabels=True,
                        gridcolor="rgba (0, 44, 56, 0.4)",
                        gridwidth=1,
                        linewidth=1,
                        linecolor="rgba (0, 44, 56, 0.4)",
                    ),
                    angularaxis=dict(
                        showticklabels=True,
                        gridcolor="rgba (0, 44, 56, 0.4)",
                        gridwidth=1,
                        linewidth=1,
                        linecolor="rgba (0, 44, 56, 0.4)",
                    )
                ),
                font=dict(
                    family="Lato",
                    color="#002C38",
                ),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.18,
                ),
                margin=dict(l=0, r=0, t=25, b=25, pad=0),
                dragmode=False
            )
            return incident_title, general_info_text, fig, incident_url

        else:

            incident_title = ""
            incident_url = ""
            general_info_text = html.Span([
                    html.I(
                        className="fa-solid fa-arrow-pointer",
                        style={'margin-right': '0.5rem'}
                    ),
                    ' Select an incident using the select buttons in the first column of the table above to display more information.'
                ], style={'text-align': 'center', 'font-size': '1.2rem', 'color': '#CC0130'})


            fig = go.Figure(data=go.Scatterpolar(
                r=[value for value in average_scores_across_incidents.values()] + [
                    average_scores_across_incidents['<b>Impact indicator</b>']],
                theta=[key for key in average_scores_across_incidents.keys()] + ['<b>Impact indicator</b>'],
                mode='lines+markers',
                fill='none',
                line=dict(width=3, color='rgba(0, 44, 56, 0.6)'),
                marker=dict(size=10, color='rgba(0, 44, 56, 0.6)'),
                name="Average across all incidents",
                hovertemplate='Indicator: %{theta}<br>'
                              'Scaled score: %{r:.2f}<extra></extra>'
            ))

            fig.update_layout(
                polar=dict(
                    bgcolor='rgba (0, 0, 0, 0)',
                    radialaxis=dict(
                        visible=True,
                        range=[0, 4],
                        tickmode='linear',
                        dtick=1,
                        showticklabels=True,
                        gridcolor="rgba (0, 44, 56, 0.4)",
                        gridwidth=1,
                        linewidth=1,
                        linecolor="rgba (0, 44, 56, 0.4)",
                    ),
                    angularaxis=dict(
                        showticklabels=True,
                        gridcolor="rgba (0, 44, 56, 0.4)",
                        gridwidth=1,
                        linewidth=1,
                        linecolor="rgba (0, 44, 56, 0.4)",
                    )
                ),
                font=dict(
                    family="Lato",
                    color="#002C38",
                ),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.18,
                ),
                margin=dict(l=0, r=0, t=25, b=25, pad=0),
                dragmode=False
            )

            return incident_title, general_info_text, fig, incident_url