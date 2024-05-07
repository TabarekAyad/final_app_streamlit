if len(conf_selected) == 1:
    conf = conf_dict[conf_dict["conf_value"] == conf_selected[0]]["conf_key"].item()
    conf_df = teams_data[teams_data[conf].isin([1])]
    team_selected = st.multiselect(
        "Choose one or multiple teams", options=conf_df["TEAMNAME"].unique().tolist()
    )
    if team_selected:
        conf_df = conf_df[conf_df["TEAMNAME"].isin(team_selected)]
        measure_selected_1 = st.sidebar.selectbox(
            "Choose one measure please",
            measure_dict["measure_value"],
            index=None,
            placeholder="Choose",
        )
        if measure_selected_1:
            agg_func_selected = st.sidebar.selectbox(
                "Which aggregate function associated with the measure did you choose from the below?",
                ["mean", "median", "std", "sum"],
                index=None,
                placeholder="Choose",
            )
            if agg_func_selected:
                measure = measure_dict[
                    measure_dict["measure_value"] == measure_selected_1
                ]["measure_key"].item()
                min_value = conf_df[measure].min()
                max_value = conf_df[measure].max()
                x = alt.X("TEAMNAME:N", title="Team", sort="-y")
                y = alt.Y(
                    measure,
                    aggregate=agg_func_selected,
                    type="quantitative",
                    scale=alt.Scale(domain=(0, max_value + 2)),
                    title=measure_selected_1,
                )
                chart = alt.Chart(conf_df).mark_bar().encode(x=x, y=y)
                st.altair_chart(chart, use_container_width=True)
elif len(conf_selected) > 1:
    conf = [
        conf_dict[conf_dict["conf_value"] == conf_val]["conf_key"].item()
        for conf_val in conf_selected
    ]
    conf_df = pd.concat([teams_data[teams_data[c].isin([1])] for c in conf])
    measure_selected_m = st.sidebar.selectbox(
        "Choose one measure please",
        measure_dict["measure_value"],
        index=None,
        placeholder="Choose",
    )
    if measure_selected_m:
        agg_func_selected = st.sidebar.selectbox(
            "Which aggregate function associated with the measure did you choose from the below?",
            ["mean", "median", "std", "sum"],
            index=None,
            placeholder="Choose",
        )
        if agg_func_selected:
            measure = measure_dict[measure_dict["measure_value"] == measure_selected_m][
                "measure_key"
            ].item()
            min_value = conf_df[measure].min()
            max_value = conf_df[measure].max()
            x = alt.X("TEAMNAME:N", title="Team", sort="-y")
            y = alt.Y(
                measure,
                aggregate=agg_func_selected,
                type="quantitative",
                scale=alt.Scale(domain=(0, max_value + 2)),
                title=measure_selected_m,
            )
            chart = alt.Chart(conf_df).mark_bar().encode(x=x, y=y)
            st.altair_chart(chart, use_container_width=True)

'''

# Create a dictionary for measures with 'None' as the value for each key
# Choose the measure you want to plot
excluded_columns = ['SEASON', 'TEAMID','WON_CONFERENCE', 'REGION', 'TEAMNAME', 'FIRSTD1SEASON', 'LASTD1SEASON']
stats_columns = [col for col in teams_stats.columns if not col.startswith('CONF_') and col not in excluded_columns]

measures_dict = {key: None for key in stats_columns}

print(measures_dict)

# Save the dictionary to a file
with open('confs_dict.csv', 'wb') as f:
    pickle.dump(confs_dict, f)

with open('measures_dict.csv', 'wb') as f:
    pickle.dump(measures_dict, f)


# 1 Errors:
# No module named 'Home'
# ImportError: attempted relative import with no known parent package


# file1.py
import pandas as pd

def create_dataframe():
    # Create your DataFrame here
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    return df

# file2.py
from file1 import create_dataframe

df = create_dataframe()
print(df)




# file1.py
import pandas as pd

def create_dataframe():
    # Create your DataFrame here
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    return df

# app.py
import streamlit as st
from file1 import create_dataframe

df = create_dataframe()
st.write(df)




# file1.py
import pandas as pd

def create_dataframe():
    # Create your DataFrame here
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    return df

def filter_dataframe(df):
    # Filter your DataFrame here
    filtered_df = df[df['A'] == 1]
    return filtered_df


# app.py
import streamlit as st
from file1 import create_dataframe, filter_dataframe

df = create_dataframe()
filtered_df = filter_dataframe(df)

st.write("Original DataFrame:")
st.write(df)

st.write("Filtered DataFrame:")
st.write(filtered_df)




# 2

import pandas as pd
import streamlit as st

# Add the caching decorator
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)
    return df

# Load the data CSV files
season_stats = load_data("data/season_stats.csv")
teams_data = load_data("data/teams_data.csv")
conf_dict = load_data("data/conf_dict.csv")
measure_dict = load_data("data/measure_dict.csv")

# Merge the 2 datasets
teams_stats = pd.merge(season_stats, teams_data, on='TEAMID', how='left')

def get_dataframes():
    return season_stats, teams_data, conf_dict, measure_dict, teams_stats


from Home import get_dataframes

# Get the dataframes
season_stats, teams_data, conf_dict, measure_dict, teams_stats = get_dataframes()

# Now you can use the dataframes in this file


import sys
sys.path.append('/path/to/your/module/directory')

export PYTHONPATH="${PYTHONPATH}:/path/to/your/module/directory"

from . import my_module




#3.

import pandas as pd

def load_cached_dataframes():
    # Dictionary to store the loaded dataframes
    cached_dataframes = {}

    # List of file paths for the cached CSV files
    cached_files = ['cached_data1.csv', 'cached_data2.csv', 'cached_data3.csv']  # Add your file names here

    # Load each cached CSV file as a dataframe and store it in the dictionary
    for file_path in cached_files:
        df_name = file_path.split('.')[0]  # Extract dataframe name from file name
        cached_dataframes[df_name] = pd.read_csv(file_path)

    return cached_dataframes



import pandas as pd

def load_cached_dataframes():
    # Dictionary to store the loaded dataframes
    cached_dataframes = {}

    # List of file paths for the cached CSV files
    cached_files = [
        '/path/to/cached_data1.csv', 
        '/path/to/cached_data2.csv', 
        '/path/to/cached_data3.csv'
    ]  # Add the full file paths here

    # Load each cached CSV file as a dataframe and store it in the dictionary
    for file_path in cached_files:
        df_name = file_path.split('/')[-1].split('.')[0]  # Extract dataframe name from file path
        cached_dataframes[df_name] = pd.read_csv(file_path)

    return cached_dataframes


#4.
#Pickle

import pickle

# ... your code to convert CSV to DataFrames ...

# Cache the DataFrames
with open('dataframe_cache.pkl', 'wb') as f:
  pickle.dump(dataframe1, f)
  pickle.dump(dataframe2, f)
  # ... pickle more DataFrames if needed ...



import pickle

# Load the DataFrames
with open('dataframe_cache.pkl', 'rb') as f:
  dataframe1 = pickle.load(f)
  dataframe2 = pickle.load(f)
  # ... load more DataFrames if needed ...

# Use the loaded DataFrames
print(dataframe1.head())
print(dataframe2.tail())


#5.
#Joblib

from joblib import dump

# ... your code to convert CSV to DataFrames ...

# Cache the DataFrames
dump(dataframe1, 'dataframe1.joblib')
dump(dataframe2, 'dataframe2.joblib')
# ... dump more DataFrames if needed ...



from joblib import load

# Load the DataFrames
dataframe1 = load('dataframe1.joblib')
dataframe2 = load('dataframe2.joblib')
# ... load more DataFrames if needed ...

# Use the loaded DataFrames
print(dataframe1.head())
print(dataframe2.tail())

'''