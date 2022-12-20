import ETL

# We will test the extraction , transformation and try to get some insights in this file
data_from_api = ETL.get_data_API(
    'https://opendata.paris.fr/api/records/1.0/search/?dataset=coronavirus-commercants-parisiens-livraison-a-domicile&q=&facet=code_postal&facet=type_de_commerce&facet=fabrique_a_paris&facet=services&rows=2503')

print("json response is ", data_from_api)

# ************ from json to dataframe : ************

df = ETL.retrieve_fields_from_json(data_from_api)
print(df)

# ************ what is null ?  ************
# true stands for non null values, false for null values => NaN

ETL.visualize_null_values(dataFrame=df)

# ************ eliminate and fill ************


# each missing value will get "no {nameOfCulmn} provided"
df = ETL.eliminating_null_values(dataFrame=df)
print(df)
print("****Columns data types are **** \n ", df.dtypes)

# ************ insight 1 : mail validation ************
taille_tab = len(df)
nbr_mail_valid = ETL.valid_mail_by_regex(df)
pr_mail = ETL.pourcentage(nbr_mail_valid,taille_tab)

# ************ insight 2 : Links validation ************

nbr_links_valid = ETL.valid_link_by_regex(df)
pr_links = ETL.pourcentage(nbr_links_valid , taille_tab)


# ************ insight 3 : Home delivery ************
nbr_Home_delivery = ETL.Home_Delivery_count(df)
per_delivery = ETL.pourcentage(nbr_Home_delivery, taille_tab)


products_list = [['number of entreprises proceeding with Home delivery ',nbr_Home_delivery, per_delivery],
                 ['number of entreprises having websites ',nbr_links_valid , pr_links ],
                 ['number of businesses using mail',nbr_Home_delivery, per_delivery]]

df_insights = ETL.pd.DataFrame (products_list, columns = ['insights', 'number','pourcentage'])
#print(df_insights)