
import streamlit as st
import pandas as pd

def recommend_colleges_v2(user_percentile, user_rank, user_category, df):
    df['Category'] = df['Category'].astype(str).str.strip().str.lower()
    user_category = user_category.strip().lower()
    # Build filter conditions
    cond = (df['Category'] == user_category)
    if user_percentile is not None:
        cond = cond & (df['Percentile Cutoff (Min)'] <= user_percentile)
    if user_rank is not None:
        cond = cond & (df['Merit List Rank Cutoff (Min)'] >= user_rank)
    eligible_colleges = df[cond].copy()
    if eligible_colleges.empty:
        return pd.DataFrame(columns=df.columns)
    eligible_colleges = eligible_colleges.sort_values('Percentile Cutoff (Min)', ascending=False)
    return eligible_colleges[['College Name', 'Branch/Discipline', 'Category', 'Percentile Cutoff (Min)', 'Merit List Rank Cutoff (Min)']]

st.title('MHT-CET College & Branch Eligibility Bot')
st.write('Enter your details to see eligible colleges and branches based on 2024-25 cutoffs. You must specify your category. Percentile and/or rank are optional.')

cutoffs_df = pd.read_csv('cet_cap_2024_25_cutoffs.csv', skiprows=1)

category = st.selectbox('Category (required)', sorted(cutoffs_df['Category'].dropna().unique()))

percentile = st.number_input('MHT-CET Percentile (optional)', min_value=0.0, max_value=100.0, value=None, step=0.01, format="%f")
rank = st.number_input('State Merit List Rank (optional)', min_value=1, max_value=200000, value=None, step=1, format="%d")

if st.button('Show Eligible Colleges & Branches'):
    # Convert None values for percentile/rank if not entered
    p = percentile if percentile != 0.0 else None
    r = rank if rank != 1 else None
    results = recommend_colleges_v2(p, r, category, cutoffs_df)
    if results.empty:
        st.warning('No colleges found matching your criteria. Try changing your inputs.')
    else:
        st.success(f'Found {len(results)} eligible college-branch combinations!')
        st.dataframe(results)
