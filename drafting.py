import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# st.set_page_config(layout="wide")


# Load the data CSV file
season_stats = pd.read_csv("data/season_stats.csv")

# Load the names CSV file
teams_data = pd.read_csv("data/teams_data.csv")

# Load the dictionaries
conf_dict = pd.read_csv("data/conf_dict.csv")

measure_dict = pd.read_csv("data/measure_dict.csv")

# Merge the 2 datasets excluding 'TEAMNAME'
stats = pd.merge(
    season_stats, teams_data.drop(columns=["TEAMNAME"]), on="TEAMID", how="left"
)


# Pivoting the teams_stats dataframe
conf_columns = [col for col in stats.columns if col.startswith("CONF_")]

stats = stats.melt(
    id_vars=[col for col in stats.columns if col not in conf_columns],
    value_vars=conf_columns,
    var_name="CONFID",
    value_name="Value",
)
stats = stats[stats["Value"] == 1]


# Dropping the 'Value' column as it's no longer needed after filtering
stats.drop(columns=["Value"], inplace=True)

# Moving the 'CONFID' column to the second position
confid = stats.pop("CONFID")
stats.insert(1, "CONFID", confid)


# Choose the measure you want to plot
excluded_columns = ['SEASON', 'TEAMID', 'CONFID','WON_CONFERENCE', 'REGION', 'FIRSTD1SEASON', 'LASTD1SEASON']
measure_columns = [col for col in stats.columns if  col not in excluded_columns]


st.info("As this app's sole purpose now is to visualize statistics, please bear with us and make your selections. Either select one conference and then select teams; one or multiple to vizualize, \n or select two conferences to compare between both")


conf_selected_name = st.sidebar.multiselect("Choose one conference or multiple ones to compare", options=conf_dict['confname'])


# If the user makes one selection for the conference, make team selection to multiple

if len(conf_selected_name) == 1:

    # Get the conf_selected_id from the comf_dict associated with the name selected 
    conf_selected_id = conf_dict[conf_dict['confname'].isin(conf_selected_name)]['confid']


    # Get the conf id from our dataset
    conf = stats[stats['CONFID'].isin(conf_selected_id)]['CONFID'].unique()


    # Filtered dataset where it contains only the conference selected
    conf_df = stats[stats['CONFID'] == conf[0]]

    # Get the TEAMIDs for the selected conference
    conf_df_team_id = conf_df['TEAMID'].unique()


    # Filter teams_data to only include team assoicated with these TEAMIDs
    team_in_conf = teams_data[teams_data['TEAMID'].isin(conf_df_team_id)]



    team_selected = st.sidebar.multiselect(
    "Choose one or multiple teams", options=team_in_conf['TEAMNAME'].unique().tolist())

    # Get id of team_selected
    ti = team_in_conf[team_in_conf['TEAMNAME'].isin(team_selected)]['TEAMID'].values


    if team_selected:
        # Filter the dataset to the teams selected only
        conf_df = conf_df[conf_df["TEAMID"].isin(ti)]


        measure_selected_1 = st.sidebar.selectbox(
            "Choose one measure please",
            measure_dict["measure_name"],
            index=None,
            placeholder="Choose",
        )


        if measure_selected_1:
                measure = measure_dict[measure_dict["measure_name"] == measure_selected_1]["measure_id"].item()

                # Reset the indices to insert team name and conferenc name
                conf_df = conf_df.reset_index(drop=True)
                team_in_conf = team_in_conf.reset_index(drop=True)
                conf_dict = conf_dict.reset_index(drop=True)


                # Now assign the new columns of names

                conf_df['CONFNAME'] = conf_dict[conf_dict['confname'] == conf_selected_name[0]]['confname'].values[0]

                # Create a dictionary from team_in_conf with TEAMID as keys and TEAMNAME as values
                team_dict = dict(zip(team_in_conf['TEAMID'], team_in_conf['TEAMNAME']))

                # Use the dictionary to map TEAMID to TEAMNAME in conf_df
                conf_df['TEAMNAME'] = conf_df['TEAMID'].map(team_dict)

                measure = measure_dict[measure_dict["measure_name"] == measure_selected_1]["measure_id"].item()


                min_value = conf_df[measure].min()
                max_value = conf_df[measure].max()


                # Define the chart
                chart = alt.Chart(conf_df).mark_bar().encode(
                    x=alt.X("TEAMNAME:N", title="Team", sort="-y"),
                    y=alt.Y(
                        measure,
                        aggregate=measure_dict[measure_dict["measure_name"] == measure_selected_1]["measure_type"].item(),
                        type="quantitative",
                        scale=alt.Scale(domain=(0, max_value + 2)),
                        title=measure_selected_1
                    )
                )

                # Add a title to the chart
                chart = chart.properties(
                    title="Bar chart of " + measure_selected_1 + " for " + conf_selected_name[0] + " and the selected teams"
                )

                # Display the chart
                st.altair_chart(chart, use_container_width=True)


         
elif len(conf_selected_name) > 1:

    # Get the conf_selected_id from the comf_dict associated with the names selected 
    conf_selected_id = conf_dict[conf_dict['confname'].isin(conf_selected_name)]['confid']
    print("two", conf_selected_id)
    st.write("conf_selected_id", conf_selected_id)

    # Get the conf id from our dataset
    conf = stats[stats['CONFID'].isin(conf_selected_id)]['CONFID'].unique()
    conf
    print("three", conf)
    st.write("conf", conf)

    # Filtered dataset where it contains only the conference selected
    conf_df = stats[stats['CONFID'].isin(conf)]
    conf_df
    st.write("conf_df", conf_df)

    measure_selected_m = st.sidebar.selectbox(
        "Choose one measure please",
        measure_dict["measure_name"],
        index=None,
        placeholder="Choose",
    )
    st.write("measure_selected_m", measure_selected_m)

    if measure_selected_m:
                measure = measure_dict[measure_dict["measure_name"] == measure_selected_m]["measure_id"].item()
                print(measure)
                st.write("measure", measure)
                aggregate= measure_dict[measure_dict["measure_name"] == measure_selected_m]["measure_type"].item()
                st.write("aggregate", aggregate)



                # Initialize an empty list to store confname
                confname_list = []

                # Iterate over each row in conf_df
                for c in conf_df['CONFID']:

                    # Find the corresponding confname in conf_dict
                    confname = conf_dict[conf_dict['confid'] == c]['confname'].values[0]
                    # Append the confname to the list
                    confname_list.append(confname)

                # Add the confname_list as a new column to conf_df
                conf_df['CONFNAME'] = confname_list

                # default='warn' for See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy

                pd.options.mode.chained_assignment = None  

                st.write("conf_df", conf_df)

                measure = measure_dict[measure_dict["measure_name"] == measure_selected_m]["measure_id"].item()
                st.write("measure", measure)

                min_value = conf_df[measure].min()
                max_value = conf_df[measure].max()

                # Define the chart
                chart = alt.Chart(conf_df).mark_bar().encode(
                    x=alt.X("CONFNAME:N", title="Conference", sort="-y"),
                    y=alt.Y(
                        measure,
                        aggregate=measure_dict[measure_dict["measure_name"] == measure_selected_m]["measure_type"].item(),
                        type="quantitative",
                        scale=alt.Scale(domain=(0, max_value + 2)),
                        title=measure_selected_m
                    )
                )

                # Add a title to the chart
                chart = chart.properties(
                    title="Bar chart of " + measure_selected_m + " for " + "conf_selected_name" + " and the selected teams"
                )

                # Display the chart
                st.altair_chart(chart, use_container_width=True)
