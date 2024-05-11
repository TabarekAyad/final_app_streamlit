import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')



# Add the caching decorator
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)
    return df

# Load the data CSV file
season_stats = load_data('data/season_stats.csv')

# Load the names CSV file
teams_data = load_data('data/teams_data.csv')

# Merge the 2 datasets
teams_stats = pd.merge(season_stats, teams_data, on='TEAMID', how='left')

# Load the dictionaries
conf_dict = load_data('data/conf_dict.csv')

measure_dict = load_data('data/measure_dict.csv')

#teams_stats['SEASON'] = teams_stats['SEASON'].str.replace(',', '')
#teams_stats['TEAMID'] = teams_stats['TEAMID'].str.replace(',', '')
#teams_stats['SEASON'] = pd.to_datetime(teams_stats['SEASON'], format='%Y')
#ACC = teams_stats[teams_stats['CONF_ACC'] == 1]

st.title("NCAA March Madness")
st.subheader("Using Streamlit to build a website showing visualizations of NCAA March Madness")

st.markdown("""*Please note that this app allows you to visualize and download the results""")

st.markdown("""
            
            NCAA March Madness is the annual college basketball tournament organized by the National Collegiate Athletic Association (NCAA). It\'s a single-elimination tournament played each spring in the United States, featuring 68 college basketball teams from the Division I level of the NCAA, to determine the national championship.

            """)


st.image('data/ncaa_logo.jpg', caption='NCAA logo')


st.markdown("""
            
            The tournament was created in 1939 and has become one of the most famous annual sporting events in the United States. The tournament consists of several rounds, named the First Four, First Round, Second Round, Sweet Sixteen, Elite Eight, Final Four, and the National Championship.

            """)



st.markdown("""
            
            The "March Madness" name is derived from the particularly intense and exciting games that often occur during the tournament, many of which are played in March. The tournament is widely regarded as one of the most exciting events in sports due to its single-elimination format, which means any team could potentially be eliminated at any stage.

            """)


st.image('data/march_madness_logo.jpeg', caption='March Madness Logo')


st.markdown("""
            Source: \n
            [NCAA bracket for March Madness](https://www.ncaa.com/march-madness-live/bracket) \n
            [NCAA Logo](https://dbukjj6eu5tsf.cloudfront.net/ncaa.org/images/2021/7/14/NCAA_Disk.jpg) \n
            [March Madness Logo](https://www.ncaa.org/images/2021/9/29/March_Madness.jpg?width=942&quality=80&format=jpg) \n
            
            """)

with st.expander('About Streamlit'):
     st.markdown(
                """

                Streamlit is a free and open-source Python library that allows you to rapidly build and share beautiful machine learning and data science web apps. It's designed specifically for data scientists and machine learning engineers. 

                With Streamlit, you can create stunning-looking applications with only a few lines of code. It's especially useful for people with no front-end knowledge as it requires no experience with HTML, JavaScript, or CSS. 

                Streamlit allows you to build an app in a few lines of code with its simple API¹. You can add widgets, which is as simple as declaring a variable. It also allows you to deploy your apps directly from Streamlit, making it easy to share, manage, and deploy your apps¹.

                It's compatible with the majority of Python libraries (e.g., pandas, matplotlib, seaborn, plotly, Keras, PyTorch, SymPy (latex)). This makes it a powerful tool for creating interactive web applications for machine learning and data science.

                Source:\n
                (1) [Streamlit • A faster way to build and share data apps](https://streamlit.io/) \n
                (2) [Python Tutorial: Streamlit DataCamp](https://www.datacamp.com/tutorial/streamlit) \n
                (3) [Streamlit in 3 Minutes. Streamlit is an open-source Python](https://medium.com/data-and-beyond/streamlit-d357935b9c) \n
                (4) [Streamlit documentation](https://main--streamlit-docs.netlify.app/)


                ### Want to learn how to use it?

                - Check out [streamlit.io](https://streamlit.io)
                - Jump into the [documentation](https://docs.streamlit.io)
                - Ask a question in their [community forums](https://discuss.streamlit.io)

            """
            )
     st.image('https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png', width=250)

with st.expander('About Altair: the library we used to visualize our data'):
     st.markdown(
                """

                Altair is a declarative statistical visualization library for Python. It’s built on top of the Vega and Vega-Lite visualization grammars, which describe the visual appearance and interactivity of visualizations in a JSON format.

                Some key features of Altair:

                Declarative: In Altair, you declare links between data columns and visual encoding channels, such as the x-axis, y-axis, and color. The rest of the plot details are handled automatically.
                Consistent API: Altair provides a simple, friendly, and consistent API, which makes it easier to create a wide range of statistical visualizations.
                Based on Vega-Lite: Altair visualizations are built on top of Vega-Lite, a high-level grammar of interactive graphics. This allows for a high degree of customizability and interactivity in the visualizations.

                Source:\n
                (1) [Vega-Altair: Declarative Visualization in Python](https://altair-viz.github.io/) \n
                (2) [Altair in Python Tutorial: Data Visualizations](https://www.datacamp.com/tutorial/altair-in-python) \n

            """
            )


with st.expander('The data used'):
     st.dataframe(season_stats)
     st.dataframe(teams_data)

