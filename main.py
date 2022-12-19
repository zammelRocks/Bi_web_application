import ETL
# function file
import altair as alt
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from PIL import Image

if __name__ == '__main__':
    # ************ URL ************

    data_from_api = ETL.get_data_API(
        'https://opendata.paris.fr/api/records/1.0/search/?dataset=coronavirus-commercants-parisiens-livraison-a-domicile&q=&facet=code_postal&facet=type_de_commerce&facet=fabrique_a_paris&facet=services&rows=2503')

    # print("json response is ", data_from_api)

    # ************ from json to dataframe : ************

    df = ETL.retrieve_fields_from_json(data_from_api)
    # print(df)

    # ************ what is null ?  ************
    # true stands for non null values, false for null values => NaN

    # ETL.visualize_null_values(dataFrame=df)

    # ************ eliminate and fill ************

    # each missing value will get "no {nameOfCulmn} provided"
    df = ETL.eliminating_null_values(dataFrame=df)
    # print(df)




    ################################################
    ########## Frontend Visualization ##############
    ################################################

    st.set_page_config(page_title="Test technique", page_icon=":tada", layout="wide")

    # lottie_coding
    lottie_coding = ETL.load_lottieur1("https://assets1.lottiefiles.com/packages/lf20_uzvwjpkq.json")

    # Header section

    with st.container():
        left_col, right_col = st.columns(2)
        with left_col:
            image = Image.open('assets/Quanticfy.png')
            st.image(image, width=300)
        with right_col:
            st.subheader("Hi QuanticFy Team :wave:")
            st.title("This is our work ")



    with st.container():
        st.write("---")
    with st.container():
        st.title("Introduction")
        left_column, right_column = st.columns(2)

        with left_column:
            st.header("Theme: Commerce et tourisme")
            st.subheader("Subject: Acheter à Paris - Commerçants parisiens - Retrait de commande ou livraison")

        with right_column:
            st_lottie(lottie_coding, height=400, key="coding")

    with st.sidebar:
        selected = option_menu(
            menu_title="Sections",
            options=["1-Home" , "2-DataSet", "3-Visualisations"],
            icons=["house" , "bi-table", "graph-up"],
            menu_icon="cast",
            default_index=0,
            orientation="Vertical",
        )

    if selected == "Home":
        st.title(f"You have selected {selected}")
    if selected == "DataSet":
        st.title(f"You have selected {selected}")
    if selected == "Visualisations":
        st.title(f"You have selected {selected}")

    with st.container():
        st.title("dataSet")
    # streamlit charts & frames display
    st.title("This is the data frame we used")
    st.dataframe(df)

    with st.container():
        st.title("Charts & Matrix")

    st.subheader('chart 1 : repartition des services par rapport type de commerce')
    plot1 = alt.Chart(df).mark_bar().encode(

        x='type_de_commerce', y='services'
    )
    st.write(plot1)

    # ************ CrossTable : find correlation between ype of Commerce and services given  ************
    st.subheader('chart 2: répartition numérique des services')
    CrossTab = ETL.Corr_typeB_services(df)
    st.dataframe(CrossTab)
    st.line_chart(CrossTab)

    st.subheader('chart 3: répartion des commerçants par rapport au type de commerce')
    # group businesses by domain/Activity
    nbr_business_per_domain = df.groupby(['type_de_commerce'])['nom_du_commerce'].count()
    nbr_frame = nbr_business_per_domain.to_frame()
    st.line_chart(nbr_frame)
