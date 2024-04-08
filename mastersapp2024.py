import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
#from PIL import Image
#import plotly.graph_objs as go


df_rankings = pd.read_csv('2024_rankings.csv')





# Set the title and icon of the app
st.set_page_config(page_title="Masters 2024 Predictor", page_icon=":golf:", initial_sidebar_state="expanded")

linkedinlink = '[Andy Uttley - LinkedIn](https://www.linkedin.com/in/andrewuttley/)'
mediumlink = '[Andy Uttley - Medium Blog](https://andy-uttley.medium.com/)'

#Create header
st.write("""# MASTERS 2024 Predictor""")
st.write("""## How it works""")
st.write("Model your predicted winner by using the left side of the screen to apply weightings to different key metrics."
         "The current selections are those deemed most appropriate to the Masters based on recent outcomes.")

st.write("Here is the data being used. It is taken from multiple websites, some of which don't have full history or LIV players. Therefore assume there are quite a few errors in this data.")


#Bring in the data
data = pd.read_csv('Masters2024AppData.csv')
data



#Create and name sidebar
st.sidebar.header('Choose your weightings')

st.sidebar.write("""#### Choose your SG bias""")
def user_input_features():
    sgott = st.sidebar.slider('SG Off the Tee', 0, 100, 40, 5)
    sgt2g = st.sidebar.slider('SG Tee to Green', 0, 100, 60, 5)
    sga2g = st.sidebar.slider('SG Approach to Green', 0, 100, 90, 5)
    sgatg = st.sidebar.slider('SG Around the Green', 0, 100, 70, 5)
    sgputt = st.sidebar.slider('SG Putting', 0, 100, 80, 5)
    sgmasters = st.sidebar.slider('SG Masters History', 0, 100, 50, 5)
    sgtotal = st.sidebar.slider('SG Total', 0, 100, 30, 5)
    sgpar5 = st.sidebar.slider('SG Par 5s', 0, 100, 85, 5)
    sgpar4 = st.sidebar.slider('SG Par 4s', 0, 100, 30, 5)
    sgpar3 = st.sidebar.slider('SG Par 3s', 0, 100, 30, 5)



    user_data = {'SG OTT': sgott,
                     'SG T2G': sgt2g,
                     'SG A2G': sga2g,
                     'SG ATG': sgatg,
                     'SG Putt': sgputt,
                     'SG Total': sgtotal,
                     'SG Par 5': sgpar5,
                     'SG Par 4': sgpar4,
                     'SG Par 3': sgpar3,
                     'SG Masters': sgmasters}
    features = pd.DataFrame(user_data, index=[0])
    return features

df_user = user_input_features()

if st.sidebar.checkbox("Choose a recency bias"):
    def user_input_biased():
        thisyear = st.sidebar.slider('2024 weighting', 0, 100, 100, 5)
        lastyear = st.sidebar.slider('2023 weighting', 0, 100, 40, 5)
        biased_data = {'this year': thisyear/100,
                       'last year': lastyear/100}
        biased = pd.DataFrame(biased_data, index=[0])
        return biased


    df_user_biased = user_input_biased()

else:
    def user_input_biased():
        thisyear = 100
        lastyear = 40
        biased_data = {'this year': thisyear / 100,
                       'last year': lastyear / 100}
        biased = pd.DataFrame(biased_data, index=[0])
        return biased
    df_user_biased = user_input_biased()


st.write("## CURRENT CHOSEN WEIGHTINGS: ")
df_user









def results_output():
    sg_ott = (data['SG_OTT_2024']*df_user_biased['this year'][0] + data['SG_OTT_2023']*df_user_biased['last year'][0]) * df_user['SG OTT'][0] / 100
    sg_t2g = (data['SG_TeeToGreen_2024']*df_user_biased['this year'][0] + data['SG_TeeToGreen_2023']*df_user_biased['last year'][0]) * df_user['SG T2G'][0] / 100
    sg_a2g = (data['SG_A2G_2024']*df_user_biased['this year'][0]  + data['SG_A2G_2023']*df_user_biased['last year'][0]) * df_user['SG A2G'][0] / 100
    sg_atg = (data['SG_ATG_2024']*df_user_biased['this year'][0]  + data['SG_ATG_2023']*df_user_biased['last year'][0]) * df_user['SG ATG'][0] / 100
    sg_putt = (data['SG_Putting2024']*df_user_biased['this year'][0]  + data['SG_Putting2023']*df_user_biased['last year'][0]) * df_user['SG ATG'][0] / 100
    sg_total = (data['SG_Total_2024']*df_user_biased['this year'][0]  + data['SG_Total_2023']*df_user_biased['last year'][0]) * df_user['SG Total'][0]/100
    #missing some SG par data
    sgpar5 = (5 - data['Par5ScoringAvg_2023'] * df_user_biased['this year'][0] + 5 - data['Par5ScoringAvg_2023'] * df_user_biased['last year'][0]) * df_user['SG Par 5'][0] / 100
    sgpar4 = (4 - data['Par4ScoringAvg_2023'] * df_user_biased['this year'][0] + 4 - data['Par4ScoringAvg_2023'] * df_user_biased['last year'][0]) * df_user['SG Par 4'][0] / 100
    sgpar3 = (3 - data['Par3ScoringAvg_2023'] * df_user_biased['this year'][0] + 3 - data['Par3ScoringAvg_2023'] * df_user_biased['last year'][0]) * df_user['SG Par 3'][0] / 100
    #SG Masters diff calc
    sgmasters = (data['MastersWAvgSg']*((df_user_biased['last year'][0] + df_user_biased['this year'][0])/2) * df_user['SG Masters'][0]/100)

    results = {'Name': data['PLAYER NAME']
               , 'Total SG per round': (sg_ott + sg_t2g + sg_a2g + sg_atg + sg_putt + sgpar5 + sgpar4 + sgpar3 + sgmasters + (sg_total/9))
               , 'SG OTT Weighted': sg_ott
               , 'SG T2G Weighted': sg_t2g
               , 'SG A2G Weighted': sg_a2g
               , 'SG ATG Weighted': sg_atg
               , 'SG Putt Weighted': sg_putt
               , 'SG Par 5 Weighted': sgpar5
                , 'SG Par 4 Weighted': sgpar4
                , 'SG Par 3 Weighted': sgpar3
                , 'SG Masters': sgmasters
                 , 'SG Total': sg_total
               }
    resultpd = pd.DataFrame(results)
    resultpd.sort_values(by=['Total SG per round'], ascending=False, inplace=True)
    return resultpd

df_results  = results_output()



#Output rankings based on users selections
st.write(
    """
    ## CURRENT PREDICTION OUTPUT
    """
)

# use softmax to create the % probability
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return (e_x / e_x.sum(axis=0))*100

df_results['prediction'] = softmax(df_results['Total SG per round'])
df_results2 = df_results[['Name', 'prediction', 'Total SG per round']]
df_results2


df_results2['Est. Odds'] = ((100/df_results2['prediction']).astype(int)).astype(str)+'/1'
df_results2.reset_index(inplace=True)
df_results2.drop('index', axis=1, inplace=True)

winner = df_results2['Name'][0]
predperc = df_results2['prediction'][0]
st.markdown(f"The predicted winner is **{winner:}** who has a **{predperc:.2f}**% chance of winning")


#image of winner

try:
    winnerimage = Image.open(winner+'.jpg')
    st.image(winnerimage)
except:
    pass


st.write("## Full table of results")
st.write("Results are calculated using the weightings you have applied to historic scraped player data, and uses softmax to create a prediction. Softmax exponentiates each number and then divides each exponentiated value by the sum of all the exponentiated values. The resulting values are always between 0 and 1 and sum up to 1 (100% chance one of them will win), which makes them useful for representing probabilities.")


df_results2 = pd.merge(df_results2, df_rankings[['Name', 'Rank']], on='Name', how='left')
df_results2['Rank'] = pd.to_numeric(df_results2['Rank'], errors='coerce')
df_results2['Rank in Masters'] = np.arange(1, len(df_results2) + 1)
df_results2 = df_results2.rename(columns={'Rank': 'Current World Rank'})
df_results2['Current World Rank'] = pd.to_numeric(df_results2['Current World Rank'], errors='coerce')
df_results2['Current World Rank'] = df_results2['Current World Rank'].fillna(72)
df_results2['Rank in Masters'] = df_results2['Rank in Masters'].fillna(72)
df_results2['Rank Difference'] = df_results2['Rank in Masters'] - df_results2['Current World Rank']
# Get column list
cols = list(df_results2.columns)




# Reorder columns in dataframe
df_results2 = df_results2[cols]
st.dataframe(df_results2.drop('Total SG per round', axis=1))


