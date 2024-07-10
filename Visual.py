import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from Langchain import search_result

# Custom CSS for page background and other styles
page_bg_img = """
<style>
body {
    background-color: #FCF2CB;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
.st-bd {
    background: rgba(0,0,0,0);
}
</style>
"""

# Streamlit app configuration
st.set_page_config(
    page_title="Flipkart Product Suggestion",
    page_icon="OIP.jpg",
    layout="wide",
    initial_sidebar_state="auto"
)

# Injecting custom CSS for background
st.markdown(page_bg_img, unsafe_allow_html=True)

# Loading data
products = pd.read_csv('products.csv')
reviews = pd.read_csv('revi.csv')
mean = reviews.groupby('p_id').mean(numeric_only=True)
colors = ["gold", "mediumturquoise", "darkorange", "lightgreen"]
star='<span style="font-size:150%;color:#F9C906">&starf;</span>'
# Options for user to choose
option = st.selectbox("Choose option", ["All product analysis", "Langchain suggestion"])

# Handling different options
if option == "All product analysis":
    for i in range(len(products)):
        col1, col2, col3 = st.columns([1, 1, 1])
        st.write('---')  # Horizontal line to separate rows
        row_data = products.iloc[i]
        pid = row_data["p_id"]
        
        # Column 1: Product Image and Price
        with col1:
            st.markdown(f"<img src={row_data['img']} width='300' height='500' style='padding-bottom:1cm;align-items:center'>", unsafe_allow_html=True)
            st.write(f"""<p style="text-align:center;font-size:20px;background-color:red;border-radius: 10px;
                     font-weight:600;color: #fff">₹ {row_data["price"]}</p>""",unsafe_allow_html=True)
        
        # Column 2: Product Name, Specifications, and Star Ratings
        with col2:
            st.markdown(f"<h2>{row_data['product_name']}</h2>", unsafe_allow_html=True)
            st.markdown(f"""<p style="color: #fff;padding: 1px 6px 1px 6px; display: inline-block;
                        border-radius: 10px;font-weight: 500;font-size: 15px;vertical-align: middle;
                        background-color: #388e3c"><span style="font-size:150%;color:#fff">&starf;
                        </span>{row_data["Star"]}</p>""",unsafe_allow_html=True)
            specification=(row_data['Specification']).replace('[','').replace(']',"").replace("'","").split(',')
            for i in specification:
                st.markdown(f"&#x25C8;&nbsp; &nbsp; {i}", unsafe_allow_html=True)
            st.markdown(f"Star Ratings:", unsafe_allow_html=True)
            st.markdown(f"""<p style='text-align:left'>{star*5}&nbsp;&nbsp;<span>{row_data['5_star']}</span><br>
                        {star*4}&nbsp;&nbsp;<span>{row_data['4_star']}</span><br>
                        {star*3}&nbsp;&nbsp;<span>{row_data['3_star']}</span><br>
                        {star*2}&nbsp;<span>{row_data['2_star']}</span><br>
                        {star*1}&nbsp;<span>{row_data['1_star']}</span><br>
                        </p>""",unsafe_allow_html=True)
        # Column 3: Sentiment Analysis and Product Suggestion
        with col3:
            st.markdown(f"""<p style="text-align: center;font-weight:800;
                        color:"red">Sentiment Analysis<br>with<br>Product Suggestion percentage</p>""",unsafe_allow_html=True)
            st.markdown("<p style='padding-top:3cm'></p>",unsafe_allow_html=True)
            categories = ['Positive', 'Negative', 'Neutral']
            values = [mean["Positive"][pid], mean["Negative"][pid], mean["neutral"][pid]]
            fig = go.Figure(data=[go.Pie(labels=categories, values=values, textinfo='label+percent', 
                                         marker=dict(colors=colors))])
            fig.update_traces(hoverinfo='label+percent+name')
            fig.update_layout(showlegend=False, height=300)
            # Product suggestion based on reviews
            compound = mean["compound"][pid]
            percentage = round((compound + 1) * 50)
            fig.add_trace(go.Pie(values=[100, 0],hole=0.7,marker_colors=["lightgrey", "white"],textinfo='none',hoverinfo='none'))
            fig.add_trace(go.Pie(values=[percentage, 100 - percentage],hole=0.7,marker_colors=["dodgerblue", "white"],textinfo='none',
                            hoverinfo='none'))
            fig.update_layout(showlegend=False,margin=dict(t=0, b=0, l=0, r=0),shapes=[dict(type="circle",x0=0.5, y0=0.5, x1=0.5, y1=0.5,
                                line=dict(color="white", width=3),)],annotations=[dict(text=f"{percentage}%",x=0.5, y=0.5,font_size=20,
                                showarrow=False)])
            st.plotly_chart(fig,use_container_width=True)

#Search based suggestion
elif option == "Langchain suggestion":
    st.write("Please enter valid search based on mobiles")
    search = st.text_input("Enter")
    if search:
        dg = search_result(search)
        if 'output' in dg:
            st.write(dg['output'])
        else:
            st.write("No results found.")
    else:
        st.write("Please enter a valid search term.")

