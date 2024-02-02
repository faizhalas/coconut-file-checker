import streamlit as st
import pandas as pd

st.set_page_config(
     page_title="File Checker",
     page_icon="🥥",
     layout="wide"
)
st.title('🥥 File Checker')

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


def reset_data():
     st.cache_data.clear()

#===check filetype===
@st.cache_data(ttl=3600)
def get_ext(extype):
    extype = uploaded_file.name
    return extype
     
#===upload===
@st.cache_data(ttl=3600)
def upload(extype):
    keywords = pd.read_csv(uploaded_file)
    return keywords

@st.cache_data(ttl=3600)
def conv_txt(extype):
    col_dict = {'TI': 'Title',
            'SO': 'Source title',
            'DE': 'Author Keywords',
            'ID': 'Keywords Plus'}
    keywords = pd.read_csv(uploaded_file, sep='\t', lineterminator='\r')
    keywords.rename(columns=col_dict, inplace=True)
    return keywords


st.subheader('Put your file here...')

#===read data===
uploaded_file = st.file_uploader("Choose your a file", type=['csv','txt'], on_change=reset_data)

if uploaded_file is not None:
    extype = get_ext(uploaded_file)
    if extype.endswith('.csv'):
        data = upload(extype) 
                  
    elif extype.endswith('.txt'):
        data = conv_txt(extype)

    col1, col2 = st.columns(2)
    
    with col1:
        #===check keywords===  
        keycheck = list(data.columns)
        keycheck = [k for k in keycheck if 'Keyword' in k]
        container1 = st.container(border=True)
        
        if not keycheck:
            container1.subheader('❌ Keyword Stem', divider='red')
            container1.write("Unfortunately, you don't have a column containing keywords in your data. Please check again. If you want to use it in another column, please rename it to 'Keywords'.")
        else:
            container1.subheader('✔️ Keyword Stem', divider='blue')
            container1.write('Congratulations! You can use Keywords Stem')
            
        #===check any obj===
        coldf = sorted(data.select_dtypes(include=['object']).columns.tolist())
        container2 = st.container(border=True)
                
        if not coldf:
            container2.subheader('❌ Topic Modeling', divider='red')
            container2.write("Unfortunately, you don't have a column containing object in your data. Please check again.")
        else:
            container2.subheader('✔️ Topic Modeling', divider='blue')
            container2.write('Congratulations! You can use Topic Modeling')

    with col2:            
        #===bidirected===    
        container3 = st.container(border=True)
                
        if not keycheck:
            container3.subheader('❌ Bidirected Network', divider='red')
            container3.write("Unfortunately, you don't have a column containing keywords in your data. Please check again. If you want to use it in another column, please rename it to 'Keywords'.")
        else:
            container3.subheader('✔️ Bidirected Network', divider='blue')
            container3.write('Congratulations! You can use Bidirected Network')
    
        #===Visualization===
        if 'Publication Year' in data.columns:
                   data.rename(columns={'Publication Year': 'Year', 'Citing Works Count': 'Cited by',
                                         'Publication Type': 'Document Type', 'Source Title': 'Source title'}, inplace=True)
    
        col2check = ['Document Type','Source title','Cited by','Year']
        miss_col = [column for column in col2check if column not in data.columns]
        container4 = st.container(border=True)
        
        
        if not miss_col:
            container4.subheader('✔️ Sunburst', divider='blue')
            container4.write('Congratulations! You can use Sunburst')
        else:
            container4.subheader('❌ Sunburst', divider='red')
            miss_col_str = ', '.join(miss_col)
            container4.write(f"Unfortunately, you don't have: {miss_col_str}. Please check again.")
