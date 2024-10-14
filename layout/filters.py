from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from datetime import date
from datetime import datetime as dt
import pickle

def make_break(num_breaks):
    br_list = [html.Br()] * num_breaks
    return br_list

def shorten_option_text(file):
    options = pickle.load(open(f"./data/{file}.pickle", "rb"))
    options = [
        {'label': opt[:40] + '...' if len(opt) > 40 else opt, 'value': opt} for opt in options
    ]
    return options

filters_info_popover = dbc.Popover(
    "This table enables you to search through individual cyber incidents in our database and see all codings associated with each incident.",
    target="filters_info",
    body=True,
    trigger="hover",
)

incident_type_popover = dbc.Popover(
    "Depicts the cyber incident(s) type concerning the reported consequences for the target(s): \
    Data theft, data theft with doxing, disruption, hijacking without misuse, and hijacking with misuse.",
    target="incident_type_dd_info",
    body=True,
    trigger="hover",
)

initiator_country_popover = dbc.Popover(
    "Describes a) the country of origin of the attributed initiating actor and b) the categorization \
    of the actor. Both terms apply to the incident’s planning and/or executing party. The latter can \
    also be a cyber proxy. The term “country“ – as applied to the selection list – comprises states, \
    provinces, and territories. This designation does not reflect an official position regarding the \
    status of a given country or region.",
    target="initiator_country_dd_info",
    body=True,
    trigger="hover",
)

receiver_country_popover = dbc.Popover(
    "Describes a) the country of origin of the targeted entities and b) the respective actor \
    categorization. The term “country“ – as applied to the selection list – comprises states, \
    provinces, and territories. This designation does not reflect an official position regarding \
    the status of a given country or region.",
    target="receiver_country_dd_info",
    body=True,
    trigger="hover",
)

cyber_intensity_popover = dbc.Popover(
    html.Span([
        "Our Cyber Intensity Indicator measures the severity of a cyber incident. This is achieved by evaluating the duration \
        of the incident itself and of its effects, as well as the scope and type of targets. Scores range from 1-15.\
        For more information on the methodology see ",
        html.A("here", href="https://www.eurepoc.eu/methodology", target="_blank"),
        "."
    ]),
    target="cyber_intensity_dd_info",
    body=True,
    trigger="hover",
)

offline_conflict_popover = dbc.Popover(
    html.Span([
        "Only relevant for cyber incidents that indicated direct links to offline-conflicts. Conflict names are based on the ",
        html.A("HIIK Conflict Barometer", href="https://hiik.de/hiik/methodology/?lang=en", target="_blank"),
        "."
    ]),
    target="offline_conflict_dd_info",
    body=True,
    trigger="hover",
)


# Reading in the dropdown menu options saved as pickle files
incident_type_dd_options = pickle.load(open("./data/incident_type_dd.pickle", "rb"))
receiver_countries_dd_options = pickle.load(open("./data/receiver_countries_dd.pickle", "rb"))
initiator_country_dd_options = pickle.load(open("./data/initiator_country_dd.pickle", "rb"))

initiator_category_dd_options = [
    {'label': 'All', 'value': "All"},
    {'label': 'State', 'value': 'State'},
    {'label': 'Non-state actor, state-affiliation suggested', 'value': 'Non-state actor, state-affiliation suggested'},
    {'label': 'Non-state-group', 'value': 'Non-state-group'},
    {'label': 'Individual hacker(s)', 'value': 'Individual hacker(s)'},
    {'label': 'Other', 'value': 'Other'},
    {'label': 'Unknown', 'value': 'Unknown'}
]

receiver_categories_dd_options = [
    {'label': 'All', 'value': "All"},
    {'label': 'State institutions / political system', 'value': 'State institutions / political system'},
    {'label': 'International / supranational organisation', 'value': 'International / supranational organization'},
    {'label': 'Critical infrastructure', 'value': 'Critical infrastructure'},
    {'label': 'Social groups', 'value': 'Social groups'},
    {'label': 'Corporate Targets (non-critical)',
     'value': 'Corporate Targets (corporate targets only coded if the respective company is not part of the critical infrastructure definition)'},
    {'label': 'End user(s) / specially protected groups', 'value': 'End user(s) / specially protected groups'},
    {'label': 'Media', 'value': 'Media'},
    {'label': 'Science', 'value': 'Science'},
    {'label': 'Education', 'value': 'Education'},
    {'label': 'Other', 'value': 'Other'},
    {'label': 'Unknown', 'value': 'Unknown'},
]

il_breach_dd_options = [
    {'label': 'All', 'value': "All"},
    {'label': 'Cyber espionage', 'value': 'Cyber espionage'},
    {'label': 'Human rights', 'value': 'Human rights'},
    {'label': 'Diplomatic / consular law', 'value': 'Diplomatic / consular law'},
    {'label': 'Air law', 'value': 'Air law'},
    {'label': 'Law of the sea', 'value': 'Law of the sea'},
    {'label': 'Space law', 'value': 'Space law'},
    {'label': 'International telecommunication law', 'value': 'International telecommunication law'},
    {'label': 'International peace', 'value': 'International peace'},
    {'label': 'Armed conflict', 'value': 'Armed conflict'},
    {'label': 'Due diligence', 'value': 'Due diligence'},
    {'label': 'Sovereignty', 'value': 'Sovereignty'},
    {'label': 'Law of treaties (pacta sunt servanda)', 'value': 'Law of treaties (pacta sunt servanda)'},
    {'label': 'Good faith', 'value': 'Good faith'},
    {'label': 'Self-determination', 'value': 'Self-determination'},
    {'label': 'International criminal law', 'value': 'International criminal law'},
    {'label': 'Aid and development', 'value': 'Aid and development'},
    {'label': 'Disaster management', 'value': 'Disaster management'},
    {'label': 'International economic law', 'value': 'International economic law'},
    {'label': 'Intellectual property law', 'value': 'Intellectual property law'},
    {'label': 'International organizations', 'value': 'International organizations'},
    {'label': 'Other', 'value': 'Other'}
]

state_responsibility_indicator_dd_options = [
    {'label': 'All', 'value': "All"},
    {'label': 'None/Negligent', 'value': 'None/Negligent'},
    {'label': 'Indirect', 'value': 'Indirect (knowingly sanctioning / ordering / ideological / material support by official members of state entities/agencies/units for officially non-state-actors)'},
    {'label': 'Direct', 'value': 'Direct (official members of state entities / agencies / units responsible)'},
]

impact_indicator_labels_dd_options = [
    {'label': 'All', 'value': "All"},
    {'label': 'Minor', 'value': 'Minor'},
    {'label': 'Low', 'value': 'Low'},
    {'label': 'Medium', 'value': 'Medium'},
    {'label': 'High', 'value': 'High'},
    {'label': 'Very high', 'value': 'Very high'},
]

attribution_basis_dd_options = shorten_option_text("attribution_basis_dd")
attribution_type_dd_options = shorten_option_text("attribution_type")

# Updating
receiver_name_dd_options = shorten_option_text("receiver_names")
initiator_name_dd_options = shorten_option_text("initiator_names")
offline_conflict_name_dd_options = pickle.load(open("./data/offline_conflict.pickle", "rb"))
cyber_conflict_issue_dd_options = pickle.load(open("./data/cyber_conflict_issue.pickle", "rb"))
weighted_cyber_intensity_dd_options = pickle.load(open("./data/weighted_cyber_intensity.pickle", "rb"))
#impact_indicator_value_dd_options = pickle.load(open("./data/impact_indicator.pickle", "rb"))
number_of_attributions_dd_options = pickle.load(open("./data/number_of_attributions.pickle", "rb"))
#number_of_legal_responses_dd_options = pickle.load(open("./data/number_of_political_responses.pickle", "rb"))
#number_of_political_responses_dd_options = pickle.load(open("./data/number_of_legal_responses.pickle", "rb"))

def render_filters():
    filters = dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(
                            className="fa-solid fa-filter",
                            style={
                                'font-size': '25px',
                                "display": "inline-block",
                                "margin-right": "10px",
                                'color': '#CC0130'
                            }
                        ),
                        html.Span([
                            html.H3("Filters", style={'display': 'inline-block'}),
                            html.I(
                                id="filters_info",
                                className="fa-regular fa-circle-question",
                                style={
                                    'text-align': 'center',
                                    'font-size': '12px',
                                    'color': '#002C38',
                                    'right': '-14px', 'top': '-2px',
                                    'position': 'absolute'
                                },
                            ),
                        ], style={'position': 'relative'}),
                        filters_info_popover
                    ]),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Label('Date of cyber incidents'),
                                    dcc.DatePickerRange(
                                        id='date-picker-range',
                                        min_date_allowed=date(2000, 1, 1),
                                        max_date_allowed=dt.now().date(),
                                        start_date=date(2000, 1, 1),
                                        end_date=dt.now().date(),
                                        display_format='D/M/YYYY',
                                        style={
                                            'width': '100%',
                                            'color': 'rgb(0, 44, 56)',
                                            'font-size': '8px'
                                        },
                                        className="dash-bootstrap",
                                    )
                                ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4,),
                                dbc.Col([
                                    html.Div([
                                        html.Span([
                                            html.Label('Type of cyber incidents'),
                                            html.I(
                                                id="incident_type_dd_info",
                                                className="fa-regular fa-circle-question",
                                                style={
                                                    'text-align': 'center',
                                                    'font-size': '12px',
                                                    'color': '#002C38',
                                                    'right': '-14px', 'top': '-2px',
                                                    'position': 'absolute'
                                                },
                                            ),
                                            incident_type_popover
                                        ], style={'position': 'relative'}),
                                        dcc.Dropdown(
                                            id='incident_type_dd',
                                            options=[
                                             {"label": "All", "value": "All"},
                                             {"label": "Data theft", "value": "Data theft"},
                                             {"label": "Data theft & Doxing", "value": "Data theft & Doxing"},
                                             {"label": "Disruption", "value": "Disruption"},
                                             {"label": "Hijacking with Misuse",
                                              "value": "Hijacking with Misuse"},
                                             {"label": "Hijacking without Misuse",
                                              "value": "Hijacking without Misuse"},
                                             {"label": "Ransomware", "value": "Ransomware"},
                                            ],
                                            value="All",
                                        ),
                                    ], className="pt-3 pt-md-0"),
                                ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                dbc.Col([
                                    html.Div([
                                        html.Label('Search through incident name and description: '),
                                        dbc.Input(
                                            id="search",
                                            placeholder="Search...",
                                            type="text",
                                            debounce=True,
                                        ),
                                    ], className="pt-3 pt-md-0"),
                                ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                            ], style={'margin-top': '10px'}),
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.Span([
                                            html.Label('Country of origin of initiator(s)'),
                                            html.I(
                                                id="initiator_country_dd_info",
                                                className="fa-regular fa-circle-question",
                                                style={
                                                    'text-align': 'center',
                                                    'font-size': '12px',
                                                    'color': '#002C38',
                                                    'right': '-14px', 'top': '-2px',
                                                    'position': 'absolute'
                                                },
                                            ),
                                            initiator_country_popover
                                        ], style={'position': 'relative'}),
                                        dcc.Dropdown(id='initiator_country_dd',
                                                     options=initiator_country_dd_options),
                                    ], className="pt-3 pt-md-0"),
                                ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                dbc.Col([
                                    html.Div([
                                        html.Label('Initiator category'),
                                        dcc.Dropdown(id='initiator_category_dd',
                                        options=initiator_category_dd_options),
                                    ], className="pt-3 pt-md-0"),
                                ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                dbc.Col([
                                    html.Div([
                                        html.Label('Initiator subcategory'),
                                        dcc.Dropdown(id='initiator_subcategory_dd'),
                                    ], className="pt-3 pt-md-0"),
                                ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                            ], style={'margin-top': '10px'}),
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.Span([
                                            html.Label('Receiver country'),
                                            html.I(
                                                id="receiver_country_dd_info",
                                                className="fa-regular fa-circle-question",
                                                style={
                                                    'text-align': 'center',
                                                    'font-size': '12px',
                                                    'color': '#002C38',
                                                    'right': '-14px', 'top': '-2px',
                                                    'position': 'absolute'
                                                },
                                            ),
                                            receiver_country_popover
                                        ], style={'position': 'relative'}),
                                        dcc.Dropdown(id='receiver_country_dd',
                                                     options=receiver_countries_dd_options,
                                                     value="Global (states)",
                                                     clearable=False),
                                    ], className="pt-3 pt-md-0"),
                                ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                dbc.Col([
                                    html.Div([
                                        html.Label('Receiver category'),
                                        dcc.Dropdown(id='receiver_category_dd',
                                                     options=receiver_categories_dd_options),
                                    ], className="pt-3 pt-md-0"),
                                ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                dbc.Col([
                                    html.Div([
                                        html.Label('Receiver subcategory'),
                                             dcc.Dropdown(id='receiver_subcategory_dd'),
                                    ], className="pt-3 pt-md-0"),
                                ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                            ], style={'margin-top': '10px'}),
                            dbc.Collapse([
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            html.Label('Initiator name'),
                                            dcc.Dropdown(id='initiator_name_dd', options=initiator_name_dd_options),
                                        ], className="pt-3 pt-md-0"),
                                    ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                    dbc.Col([
                                        html.Div([
                                            html.Label('Receiver name'),
                                            dcc.Dropdown(id='receiver_name_dd', options=receiver_name_dd_options),
                                        ], className="pt-3 pt-md-0"),
                                    ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                    dbc.Col([
                                        html.Div([
                                            html.Span([
                                                html.Label('Cyber Intensity score'),
                                                html.I(
                                                    id="cyber_intensity_dd_info",
                                                    className="fa-regular fa-circle-question",
                                                    style={
                                                        'text-align': 'center',
                                                        'font-size': '12px',
                                                        'color': '#002C38',
                                                        'right': '-14px', 'top': '-2px',
                                                        'position': 'absolute'
                                                    },
                                                ),
                                                cyber_intensity_popover
                                            ], style={'position': 'relative'}),
                                            dcc.Dropdown(id='intensity_dd', options=weighted_cyber_intensity_dd_options),
                                        ], className="pt-3 pt-md-0"),
                                    ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                ], style={'margin-top': '10px'}),
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            html.Span([
                                                html.Label('Related offline conflict'),
                                                html.I(
                                                    id="offline_conflict_dd_info",
                                                    className="fa-regular fa-circle-question",
                                                    style={
                                                        'text-align': 'center',
                                                        'font-size': '12px',
                                                        'color': '#002C38',
                                                        'right': '-14px', 'top': '-2px',
                                                        'position': 'absolute'
                                                    },
                                                ),
                                                offline_conflict_popover
                                            ], style={'position': 'relative'}),
                                            dcc.Dropdown(
                                                id='offline_conflict_name_dd',
                                                options=offline_conflict_name_dd_options
                                            )
                                        ], className="pt-3 pt-md-0"),
                                    ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                    dbc.Col([
                                        html.Div([
                                            html.Label('Cyber conflict issue'),
                                            dcc.Dropdown(id='cyber_conflict_issue_dd',options=cyber_conflict_issue_dd_options),
                                        ], className="pt-3 pt-md-0"),
                                    ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                    dbc.Col([
                                        html.Div([
                                            html.Label('Number of attributions'),
                                            dcc.Dropdown(id='attribution_number_dd',
                                                         options=number_of_attributions_dd_options),
                                        ], className="pt-3 pt-md-0"),
                                    ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                ], style={'margin-top': '10px'}),
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            html.Label('Attribution basis'),
                                            dcc.Dropdown(id='attribution_basis_dd',options=attribution_basis_dd_options),
                                        ], className="pt-3 pt-md-0"),
                                        ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                    dbc.Col([
                                        html.Div([
                                            html.Label('Attribution type'),
                                            dcc.Dropdown(id='attribution_type_dd',options=attribution_type_dd_options),
                                        ], className="pt-3 pt-md-0"),
                                    ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                    dbc.Col([
                                        html.Div([
                                            html.Label('Impact indicator'),
                                            dcc.Dropdown(id='impact_indicator_dd', options=impact_indicator_labels_dd_options),
                                        ], className="pt-3 pt-md-0"),
                                    ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                ], style={'margin-top': '10px'}),
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            html.Label('State responsibility indicator'),
                                            dcc.Dropdown(id='state_responsibility_dd',
                                                         options=state_responsibility_indicator_dd_options),
                                        ], className="pt-3 pt-md-0"),
                                    ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                    dbc.Col([
                                        html.Div([
                                            html.Label('International Law Breach'),
                                            dcc.Dropdown(id='il_breach_dd', options=il_breach_dd_options),
                                        ], className="pt-3 pt-md-0"),
                                    ], xs=12, sm=12, md=4, lg=4, xl=4, xxl=4),
                                ], style={'margin-top': '10px'}),
                            ],
                                id="collapse",
                                is_open=False
                            ),
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        dbc.Button(
                                            html.B("Show/hide more filters"),
                                            id="collapse-button",
                                            className="mb-3",
                                            color="link",
                                            n_clicks=0,
                                            style={
                                                'color': 'rgb(0, 44, 56)',
                                                'text-align': 'center'
                                            },
                                        ),
                                        *make_break(1),
                                        dbc.Button("Reset selection", id="reset", className="mb-3", n_clicks=0,
                                                   color="light")
                                    ], style={'text-align': 'center', "margin-bottom": "10px"}),
                                ]),
                            ]),
                        ]),
                    ]),
                ])
            ])
        ])
    ], style={'margin-top': '20px', 'margin-bottom': '20px'})
    return filters
