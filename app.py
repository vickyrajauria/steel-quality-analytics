"""Interactive descriptive dashboard. Run: streamlit run app.py"""
from pathlib import Path
import pandas as pd
import streamlit as st
from src.pipeline import fault_summary

st.set_page_config(page_title='Steel Quality | Analyst Portfolio',page_icon='🏭',layout='wide')
ROOT=Path(__file__).resolve().parent
@st.cache_data
def load_data():
    return pd.read_csv(ROOT/'data/processed/faults_clean.csv')

st.title('Steel Quality Analytics')
st.caption('Manufacturing inspection portfolio • UCI Steel Plates Faults • SQL + Python')
st.info('These are labeled fault observations, not the full production population. Shares below are fault mix—not rejection rates. Pixel area is not financial loss or physical scrap area.')
try: df=load_data()
except FileNotFoundError:
    st.error('Run python -m src.pipeline first to prepare the data.');st.stop()
with st.sidebar:
    st.header('Explore the sample')
    steel=st.multiselect('Steel type',sorted(df.steel_type.unique()),default=sorted(df.steel_type.unique()))
    bands=st.multiselect('Thickness band (source units)', ['<=50','51-100','>100'],default=['<=50','51-100','>100'])
    st.caption('Thickness units are unspecified in the source. Bands are analyst-defined. Every chart uses the selected sample.')
selected=df[df.steel_type.isin(steel)&df.thickness_band.isin(bands)]
if selected.empty:
    st.warning('No observations match the filters. Select at least one steel type and thickness band.');st.stop()
s=fault_summary(selected)
c1,c2,c3,c4=st.columns(4)
c1.metric('Fault observations',f'{len(selected):,}')
c2.metric('Largest category',s.iloc[0].fault_type)
c3.metric('Largest category share',f'{s.iloc[0].record_share_pct:.1f}%')
c4.metric('Median defect pixel area',f'{selected.pixels_areas.median():,.1f}')
if len(selected)<100: st.warning('Small selected sample (<100). Treat differences as exploratory.')
a,b,c=st.tabs(['Fault priorities','Steel comparison','Explore records'])
with a:
    st.subheader('Recorded fault frequency')
    st.bar_chart(s.set_index('fault_type')['records'],color='#0f766e',sort=False)
    st.dataframe(s[['fault_type','records','record_share_pct','cumulative_share_pct','median_pixels','pixel_share_pct']].round(2),hide_index=True,width='stretch')
    st.subheader('Share of summed defect pixel areas')
    st.bar_chart(s.set_index('fault_type')['pixel_share_pct'],color='#d97706',sort=False)
    st.caption('Large pixel areas can dominate the sum. Use the median alongside totals. Neither measure establishes defect severity.')
with b:
    st.subheader('Within-steel fault mix (%)')
    mix=pd.crosstab(selected.steel_type,selected.fault_type,normalize='index')*100
    st.bar_chart(mix,stack=True)
    st.dataframe(mix.round(2),width='stretch')
    st.write('Selected observations by steel type')
    st.dataframe(selected.groupby('steel_type').size().rename('records'),width='stretch')
    st.caption('Different mixes are associations within this sample; they do not establish that one steel type is less reliable.')
with c:
    st.dataframe(selected,width='stretch',hide_index=True)
    st.download_button('Download filtered records',selected.to_csv(index=False),'filtered_faults.csv','text/csv')
st.divider()
st.markdown('**Suggested action:** investigate high-frequency categories and review the broad Other Faults label. Validate hypotheses with engineers and collect production denominators before estimating rates or savings.')
st.caption('Source: Buscema, Terzi & Tastle (2010), UCI Steel Plates Faults. DOI: 10.24432/C5J88N. Data: CC BY 4.0. No measured operational improvement is claimed.')
