import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from layout.layout import serve_layout
from server.filter_database_callback import database_filter, back_button_callback
import pandas as pd
#from flask_limiter.util import get_remote_address
#from flask_limiter import Limiter
from server.common_callbacks import more_filters_button, reset_filters_button, reset_pagination
from server.incident_info_callback import incident_info_callback
from server.dynamic_dropdowns_callback import receiver_dynamic_dropdowns, initiator_dynamic_dropdowns
from server.download_data import download_data
import pickle
import faiss
from sentence_transformers import SentenceTransformer
import bleach

def clean_types(data):
    """Adding a variable cleaning the incident types to a "one-level" category for more meaningful analyses."""
    def translate_type(types):
        types = [t for t in types if isinstance(t, str)]

        type_mapping = {
            "Disruption": "DDoS/Defacement",
            "Data theft": "Data theft",
            "Data theft & Doxing": "Hack and leak",
            "Ransomware": "Ransomware"
        }

        sorted_types = sorted(types)

        if len(sorted_types) == 1:
            return type_mapping.get(sorted_types[0], sorted_types[0])
        elif len(sorted_types) == 2 and "Disruption" in sorted_types and "Hijacking with Misuse" in sorted_types:
            return "Wiper"
        elif len(sorted_types) > 1 and "Ransomware" in sorted_types:
            return "Ransomware"
        elif len(
                sorted_types) == 2 and "Data theft" in sorted_types and "Hijacking with Misuse" in sorted_types or "Hijacking without Misuse" in sorted_types:
            return "Data theft"
        else:
            return list(sorted_types)

    for incident in data:
        incident["incident_type_clean"] = translate_type(incident["incident_type"])

    for incident in data:
        if not isinstance(incident["incident_type_clean"], str):
            if "Data theft & Doxing" in incident["incident_type_clean"]:
                incident["incident_type_clean"] = "Hack and leak"
            elif "Data theft" in incident["incident_type_clean"]:
                incident["incident_type_clean"] = "Data theft"
            else:
                incident["incident_type_clean"] = "Other"
    return data


# ------------------------------------------------- READ DATA ---------------------------------------------------------
eurepoc_data = pd.read_csv("./data/eurepoc_dataset.csv")
eurepoc_data = eurepoc_data.set_index(eurepoc_data["ID"])


data_for_download = pd.read_csv("./data/eurepoc_dataset_download.csv")

full_data_dict = pickle.load(open("./data/full_data_dict.pickle", "rb"))
data_index = pickle.load(open("./data/full_data_dict_index_map.pickle", "rb"))

full_data_dict = clean_types(full_data_dict)

# Load the existing FAISS index and DataFrame
index = faiss.read_index("./data/eurepoc_index.index")
embedded_ids = pd.read_hdf("./data/eurepoc_embeddings_data_ids.h5", key="df_id")


# Initialize the SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

all_options = pickle.load(open("./data/all_options.pickle", "rb"))
receiver_name_dd_options = pickle.load(open("./data/receiver_names.pickle", "rb"))
initiator_name_dd_options = pickle.load(open("./data/initiator_names.pickle", "rb"))
offline_conflict_name_dd_options = pickle.load(open("./data/offline_conflict.pickle", "rb"))
weighted_cyber_intensity_dd_options = pickle.load(open("./data/weighted_cyber_intensity.pickle", "rb"))
number_of_attributions_dd_options = pickle.load(open("./data/number_of_attributions.pickle", "rb"))
all_options = all_options + receiver_name_dd_options + initiator_name_dd_options + offline_conflict_name_dd_options + weighted_cyber_intensity_dd_options + number_of_attributions_dd_options
all_options = set(all_options)

"""def validate_input(input):
    if input in all_options:
        if input:
            return bleach.clean(input)
    else:
        return None, print("Invalid input!")"""

def validate_input(input):
    if input and input in all_options:
        return bleach.clean(str(input))
    elif input is None:
        return None
    else:
        raise ValueError("Invalid input!")


def text_search(query):
    cleaned_query = bleach.clean(query)
    copied_ids = embedded_ids.copy()
    query_vector = model.encode([cleaned_query])
    k = 20
    top_k = index.search(query_vector, k)
    return [copied_ids['ID'][_id] for _id in top_k[1].tolist()[0]]


# These are the regional codes used for filtering the data by region
STATES_CODES = {
    "Africa (states)": "AFRICA",
    "Asia (states)": "ASIA",
    "Central America (states)": "CENTAM",
    "Central Asia (states)": "CENTAS",
    "Collective Security Treaty Organization (states)": "CSTO",
    "EU (member states)": "EU",
    "Eastern Asia (states)": "EASIA",
    "Europe (states)": "EUROPE",
    "Gulf Countries (states)": "GULFC",
    "Mena Region (states)":"MENA",
    "Middle East (states)": "MEA",
    "NATO (member states)": "NATO",
    "North Africa (states)": "NAF",
    "Northeast Asia (states)": "NEA",
    "Oceania (states)": "OC",
    "Shanghai Cooperation Organisation (states)": "SCO",
    "South Asia (states)": "SASIA",
    "South China Sea (states)": "SCS",
    "Southeast Asia (states)": "SEA",
    "Sub-Saharan Africa (states)":"SSA",
    "Western Balkans (states)": "WBALKANS"
}

#full_layout = serve_layout()

# ------------------------------------------------- APP -------------------------------------------------------------
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.icons.FONT_AWESOME]
)

server = app.server
app.layout = serve_layout

"""limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["120 per minute"]  # Set your desired rate limit
)
limiter.init_app(server)  # Initializing limiter with the Flask instance"""


# ------------------ CALLBACKS ------------------

@app.callback(
    Output('modal-status', 'children'),
    Input('close', 'n_clicks'),
)
def close_modal(n):
    if n is not None:
        return "false"
    return "true"

@app.callback(
    Output("collapse-radar-text", "is_open"),
    [Input("radar-collapse", "n_clicks")],
    [State("collapse-radar-text", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Common callbacks
more_filters_button(app)
reset_filters_button(app)
reset_pagination(app)
download_data(app, data_for_download, STATES_CODES, text_search, validate_input)

receiver_dynamic_dropdowns(app)
initiator_dynamic_dropdowns(app)

# database_filter callbacks
database_filter(app, eurepoc_data, STATES_CODES, text_search, validate_input)
back_button_callback(app)

#Display incident info
incident_info_callback(app, full_data_dict, data_index)


app.title = "EuRepoC Cyber Incidents TableView"


if __name__ == "__main__":
    app.run_server(host="0.0.0.0")
