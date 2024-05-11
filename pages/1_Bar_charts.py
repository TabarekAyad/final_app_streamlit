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
    season_stats, teams_data, on="TEAMID", how="left"
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


# Moving the 'CONFID' column
stats.insert(1, "CONFID", stats.pop("CONFID"))

# Merge the dataframes and drop the redundant column
stats = pd.merge(
    stats, conf_dict, left_on="CONFID", right_on="confid", how="left"
).drop(columns="confid")

stats.rename(columns={"confname": "CONFNAME"}, inplace=True)

# Moving the 'CONFID' column
stats.insert(2, "CONFNAME", stats.pop("CONFNAME"))

# Moving the 'TEAMNAME' column
stats.insert(4, "TEAMNAME", stats.pop("TEAMNAME"))


# Choose the measure you want to plot
excluded_columns = ['SEASON', 'TEAMID', 'CONFID','WON_CONFERENCE', 'REGION', 'FIRSTD1SEASON', 'LASTD1SEASON']
measure_columns = [col for col in stats.columns if  col not in excluded_columns]


st.info("As this app's sole purpose now is to visualize statistics, please bear with us and make your selections. Either select one conference and then select teams; one or multiple to vizualize, \n or select conferences to compare.\n *Please note that this app allows you to visualize and download the results from the horizontal 3 dots on the top of your screen to your right")

start_season = stats['SEASON'].min()

end_season = stats['SEASON'].max()

season_range = st.slider(
    "You can choose which year to start from and which year to end with",
    start_season, end_season, (start_season, end_season))

stats = stats[stats["SEASON"].between(season_range[0], season_range[1])]

conf_selected_name = st.sidebar.multiselect("Choose one conference or multiple ones to compare", options=stats['CONFNAME'].unique())


# If the user makes one selection for the conference, make team selection to multiple

if len(conf_selected_name) == 1:

    # Filtered dataset where it contains only the conference selected
    conf_df = stats[stats['CONFNAME'].isin(conf_selected_name)]

    team_selected_1 = st.sidebar.multiselect(
    "Choose one or multiple teams", options=conf_df['TEAMNAME'].unique())

    if team_selected_1:
        # Filter the dataset to the teams selected only

        conf_df = conf_df[conf_df["TEAMNAME"].isin(team_selected_1)]

        measure_selected_1 = st.sidebar.selectbox(
            "Choose one measure please",
            measure_dict["measure_name"],
            index=None,
            placeholder="Choose",
        )


        if measure_selected_1:
                
                measure = measure_dict[measure_dict["measure_name"] == measure_selected_1]["measure_id"].item()
                
                min_value = conf_df[measure].min()
                max_value = conf_df[measure].max()

                # Define the chart
                chart = alt.Chart(conf_df).mark_bar().encode(
                    x=alt.X("TEAMNAME:N", title="Team", sort="-y"),
                    y=alt.Y(
                        measure,
                        aggregate=measure_dict[measure_dict["measure_name"] == measure_selected_1]["measure_type1"].item(),
                        type="quantitative",
                        scale=alt.Scale(domain=(0, max_value + 2)),
                        title=measure_selected_1
                    )
                )

                # Add a title to the chart
                chart = chart.properties(
                    title="Bar chart of " + measure_selected_1 + " for " + conf_selected_name[0] +
                    " and the selected team(s)"
                )

                # Display the chart
                st.altair_chart(chart, use_container_width=True)


         
elif len(conf_selected_name) > 1:

    # Filtered dataset where it contains only the conference selected

    conf_df = stats[stats['CONFNAME'].isin(conf_selected_name)]

    entity = st.sidebar.radio(
        "Do you want to compare between conferences or teams of these conferences?",
        ["Teams", "Conferences"], index=0,
        captions = ["This will show conferences names alone", "This will show teams names alone"])

    if entity == "Teams":

        team_selected_m = st.sidebar.multiselect("Choose one or multiple teams", options=conf_df['TEAMNAME'].unique())

        if team_selected_m:
              
        # Filter the dataset to the teams selected only

            conf_df = conf_df[conf_df["TEAMNAME"].isin(team_selected_m)]

            measure_selected_m_1 = st.sidebar.selectbox("Choose one measure please", measure_dict["measure_name"], index=None, placeholder="Choose")

            if measure_selected_m_1:
                
                measure = measure_dict[measure_dict["measure_name"] == measure_selected_m_1]["measure_id"].item()
                
                min_value = conf_df[measure].min()
                max_value = conf_df[measure].max()

                # Define the chart
                chart = alt.Chart(conf_df).mark_bar().encode(
                    x=alt.X("TEAMNAME:N", title="Team", sort="-y"),
                    y=alt.Y(
                        measure,
                        aggregate=measure_dict[measure_dict["measure_name"] == measure_selected_m_1]["measure_type1"].item(),
                        type="quantitative",
                        scale=alt.Scale(domain=(0, max_value + 2)),
                        title=measure_selected_m_1
                    )
                )

                # Add a title to the chart
                chart = chart.properties(
                    title="Bar chart of " + measure_selected_m_1 + " for " + conf_selected_name[0] + " and the selected team(s)"
                )

                # Display the chart
                st.altair_chart(chart, use_container_width=True)



    else:

        # Filtered dataset where it contains only the conference selected

        conf_df = stats[stats['CONFNAME'].isin(conf_selected_name)]

        measure_selected_m_m = st.sidebar.selectbox(
            "Choose one measure please",
            measure_dict["measure_name"],
            index=None,
            placeholder="Choose",
        )

        if measure_selected_m_m:
                    
            measure = measure_dict[measure_dict["measure_name"] == measure_selected_m_m]["measure_id"].item()

            aggregate= measure_dict[measure_dict["measure_name"] == measure_selected_m_m]["measure_type1"].item()

            min_value = conf_df[measure].min()
            max_value = conf_df[measure].max()

            # Define the chart
            chart = alt.Chart(conf_df).transform_calculate(
            CONFNAME_SHORT="replace(datum.CONFNAME, ' Conference', '')"
            ).mark_bar().encode(
            x=alt.X("CONFNAME_SHORT:N", title="Conference", sort="-y"),
            y=alt.Y(
                measure,
                aggregate=measure_dict[measure_dict["measure_name"] == measure_selected_m_m]["measure_type1"].item(),
                type="quantitative",
                scale=alt.Scale(domain=(0, max_value + 2)),
                title=measure_selected_m_m
                )
            )


            # Add a title to the chart
            chart = chart.properties(
            title="Bar chart of " + measure_selected_m_m + " for the selected conferences and the selected teams"
            )

            # Display the chart
            st.altair_chart(chart, use_container_width=True)

