import pandas as pd
from datetime import datetime as dt
import bleach


def all_to_none(value):
    if value == "All":
        return None
    else:
        return value


def filter_datatable(
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
    search_func,
    show_only_sent_to_database
):
    
    if show_only_sent_to_database:
        filtered_data_initial = filtered_data_initial.loc[(filtered_data_initial["status"] != "Open")]
        print(filtered_data_initial.head(2))
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
    impact_indicator_filter = all_to_none(impact_indicator_filter)
    state_responsibility_filter = all_to_none(state_responsibility_filter)
    il_breach_filter = all_to_none(il_breach_filter)

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
        "impact_indicator": impact_indicator_filter,
        "state_responsibility_indicator": state_responsibility_filter,
        "IL_breach_indicator": il_breach_filter,
    }


    if search_filter and len(search_filter) > 550:
        search_filter = None

    if search_filter:
        search_filter = bleach.clean(search_filter)
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

        tooltip_data = [{column: {'value': str(value), 'type': 'markdown'}
                         for column, value in row.items() if column not in ['initiator_name', 'receiver_name',
                             'context', 'start_date', "number_of_attributions", "number_of_political_responses",
                             "number_of_legal_responses", "zero_days", "radar_score_impact",
                             "radar_score_intensity", "radar_score_political", "radar_score_legal",
                             "radar_score_offline_conflict", "radar_score_attribution",
                             "legal_response_country", "impact_indicator", "weighted_cyber_intensity"]
                         }
                        for row in filtered_data.to_dict('records')]

        #data = filtered_data.to_dict('records')

        return filtered_data, tooltip_data

    else:
        filtered_data = pd.DataFrame.from_dict(filtered_data_initial)
        if start_date and end_date:
            filtered_data = filtered_data.loc[(filtered_data['start_date'] >= start_date)
                                              & (filtered_data['start_date'] <= end_date)]
        for col, val in input_filters.items():
            if val is not None:
                filtered_data[col] = filtered_data[col].fillna('').astype(str)
                filtered_data = filtered_data.loc[filtered_data[col].str.contains(val, regex=False)]

        tooltip_data = [{column: {'value': str(value), 'type': 'markdown'}
                         for column, value in row.items() if column not in ['initiator_name', 'receiver_name',
                             'context', 'start_date', "number_of_attributions", "number_of_political_responses",
                             "number_of_legal_responses", "zero_days", "radar_score_impact",
                             "radar_score_intensity", "radar_score_political", "radar_score_legal",
                             "radar_score_offline_conflict", "radar_score_attribution",
                             "legal_response_country", "impact_indicator", "weighted_cyber_intensity"
                         ]
                         }
                        for row in filtered_data.to_dict('records')]

        #data = filtered_data.to_dict('records')

        return filtered_data, tooltip_data
