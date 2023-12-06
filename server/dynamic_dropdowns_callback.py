from dash.dependencies import Input, Output


def receiver_dynamic_dropdowns(app):
    @app.callback(
        Output('receiver_subcategory_dd', 'options'),
        Output('receiver_subcategory_dd', 'value'),
        Output('receiver_subcategory_dd', 'placeholder'),
        Input('receiver_category_dd', 'value')
    )
    def update_dropdown2(selected_option):
        if selected_option == 'State institutions / political system':
            options = [
                'All',
                'Civil service / administration',
                'Election infrastructure / related systems',
                'Government / ministries',
                'Intelligence agencies',
                'Judiciary',
                'Legislative',
                'Military',
                'Other (e.g., embassies)',
                'Police',
                'Political parties',
            ]
            placeholder = "Select..."

        elif selected_option == 'Critical infrastructure':
            options = [
                'All',
                'Chemicals',
                'Critical Manufacturing',
                'Defence industry',
                'Digital Provider',
                'Energy',
                'Finance',
                'Food',
                'Health',
                'Other',
                'Research',
                'Space',
                'Telecommunications',
                'Transportation',
                'Waste Water Management',
                'Water'
            ]
            placeholder = "Select..."

        elif selected_option == 'Social groups':
            options = [
                'All',
                'Advocacy / activists (e.g. human rights organizations)',
                'Criminal',
                'Ethnic',
                'Hacktivist',
                'Other social groups',
                'Political opposition / dissidents / expats',
                'Religious',
                'Terrorist'
            ]
            placeholder = "Select..."

        elif selected_option is None:
            options = []
            placeholder = "No subcategory for this category"

        else:
            options = []
            placeholder = "No subcategory for this category"

        return options, None, placeholder



def initiator_dynamic_dropdowns(app):
    @app.callback(
        Output('initiator_subcategory_dd', 'options'),
        Output('initiator_subcategory_dd', 'value'),
        Output('initiator_subcategory_dd', 'placeholder'),
        Input('initiator_category_dd', 'value')
    )
    def update_dropdown2(selected_option):
        if selected_option == 'Non-state-group':
            options = [
                'All',
                'Ethnic actors',
                'Religious actors',
                'Hacktivist(s)',
                'Criminal(s)',
                'Terrorist(s)',
                'Private technology companies / hacking for hire groups without state affiliation / research entities',
                'Other non-state groups',
            ]
            placeholder = "Select..."

        elif selected_option == 'Non-state actor, state-affiliation suggested':
            options = [
                'All',
                'Non-state-group, state-affiliation suggested (widely held view for the attributed initiator (group), but not invoked in this case)',
            ]
            placeholder = "Select..."

        elif selected_option is None:
            options = []
            placeholder = "No subcategory for this category"

        else:
            options = []
            placeholder = "No subcategory for this category"

        return options, None, placeholder
