from dash import dcc, html
import dash_bootstrap_components as dbc
from layout.filters import render_filters
from layout.datatable import body



def serve_layout():
    layout_full = dbc.Container(
        children=[
	    html.Link(rel='icon', href='./assets/eurepoc-logo.png'),	
            dcc.Location(id='url', refresh=False),
            dcc.Location(id='url-updater', refresh=True),
            dbc.Row([
                dbc.Col([
                    render_filters(),
                ]),
            ], id='filter-bar', style={}),
            dbc.Row([
                dbc.Col([
                    dbc.Button([
                        html.I(className="fa-solid fa-angles-left"),
                        "    Back to full table view",
                    ],
                        id="back-button",
                        n_clicks=0,
                        className="mb-3",
                        color="primary",
                    ),
                ], width=3)
            ], id='back-button-row', style={'display': 'none'}),
            dbc.Row([
                dbc.Col([
                    body
                ]),
            ]),
        ],
        fluid=True,
        style={"padding": '15px 40px'}
    )
    return layout_full