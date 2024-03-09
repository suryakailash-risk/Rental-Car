import pandas as pd
from datetime import datetime
import streamlit as st
import extra_streamlit_components as stx
import streamlit as st
from streamlit_chat import message
import time

st.sidebar.title('Select the Type of Database')

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
footer = """
<style>
footer {
    visibility: hidden;
}
footer:after {
    content:'Your Custom Text';
    visibility: visible;
    display: block;
    position: relative;
    #background-color: red;
    padding: 5px;
    top: 2px;
} </style>"""



options = ['Select Database','MySQL - AWS(RDS)']

selected_option = st.sidebar.selectbox('Select an Database:', options)

if selected_option=="MySQL - AWS(RDS)":
    import mysql.connector

    # try:
    connection = mysql.connector.connect(
                host='mohitamode.c7ww0086ajus.us-east-1.rds.amazonaws.com',
                user='admin',
                password='12345678',
                database='mm_team02_01'
            )

    if connection.is_connected():
                db_info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_info)
    st.title(f'You selected: {selected_option} database')
    cursor = connection.cursor()
    selected_option = stx.tab_bar(data=[
    stx.TabBarItemData(id=1, title="Query", description="Run SQL Query"),
    stx.TabBarItemData(id=2, title="Run", description="View Data Dynamically"),
], default=1)
    if  selected_option == '1':
        dictionarydata={
            "select Query":{'id':"0"},
            "Average rental duration for each car model":{'id':"1","Query":"""SELECT Car_model, AVG(DATEDIFF(Rental_enddate, Rental_startdate)) AS avg_rental_duration
                                                                                FROM rental_details
                                                                                JOIN car ON rental_details.Car_id = car.Car_id
                                                                                GROUP BY Car_model;"""},
            "Total revenue generated from rentals for each car brand":{'id':"2","Query":"""SELECT Car_brand, CONCAT('$', FORMAT(SUM(Estimated_cost), 2)) AS total_revenue
                                                                                            FROM rental_details
                                                                                            JOIN car ON rental_details.Car_id = car.Car_id
                                                                                            GROUP BY Car_brand;"""},
                       
            "Calculate the total number of rentals and average rental cost per customer:":{'id':'6','Query':"""SELECT c.Customer_id, c.Customer_fname, c.Customer_lname, c.Customer_phone, c.Customer_license, COUNT(*) AS total_rentals, AVG(rd.Estimated_cost) AS avg_rental_cost
FROM rental_details rd
JOIN customer c
ON c.Customer_id= rd.Customer_id
GROUP BY Customer_id;
                                                                                                        """},
            "Each rental month and year, total estimated cost for that month":{'id':'7','Query':"""SELECT 
                                                                                                                    CASE 
                                                                                                                        WHEN MONTH(Rental_startdate) = 1 THEN 'January'
                                                                                                                        WHEN MONTH(Rental_startdate) = 2 THEN 'February'
                                                                                                                        WHEN MONTH(Rental_startdate) = 3 THEN 'March'
                                                                                                                        WHEN MONTH(Rental_startdate) = 4 THEN 'April'
                                                                                                                        WHEN MONTH(Rental_startdate) = 5 THEN 'May'
                                                                                                                        WHEN MONTH(Rental_startdate) = 6 THEN 'June'
                                                                                                                        WHEN MONTH(Rental_startdate) = 7 THEN 'July'
                                                                                                                        WHEN MONTH(Rental_startdate) = 8 THEN 'August'
                                                                                                                        WHEN MONTH(Rental_startdate) = 9 THEN 'September'
                                                                                                                        WHEN MONTH(Rental_startdate) = 10 THEN 'October'
                                                                                                                        WHEN MONTH(Rental_startdate) = 11 THEN 'November'
                                                                                                                        WHEN MONTH(Rental_startdate) = 12 THEN 'December'
                                                                                                                    END AS rental_month,
                                                                                                                    YEAR(Rental_startdate) AS rental_year,
                                                                                                                    SUM(Estimated_cost) AS monthly_revenue
                                                                                                                FROM 
                                                                                                                    rental_details
                                                                                                                GROUP BY 
                                                                                                                    rental_month, rental_year
                                                                                                                ORDER BY 
                                                                                                                    monthly_revenue DESC;
                                                                                                                """},
            "car model with the highest average mileage per rental hour":{'id':'8','Query':"""SELECT Car_model, AVG(Car_milage / Rental_total_hrs) AS avg_mileage_per_hour
                                                                                                            FROM car
                                                                                                            JOIN rental_details ON car.Car_id = rental_details.Car_id
                                                                                                            GROUP BY Car_model
                                                                                                            ORDER BY avg_mileage_per_hour DESC;
                                                                                                            """},
            "Calculate the total revenue generated from rentals for each customer":{'id':'9','Query':"""SELECT 
                                                                                                                    rd.Customer_id,
                                                                                                                    c.Customer_fname,
                                                                                                                    c.Customer_lname,
                                                                                                                    SUM(rd.Estimated_cost) AS Total_Revenue,
                                                                                                                    count(rd.Rental_id) As Total_Booked
                                                                                                                FROM 
                                                                                                                    rental_details rd
                                                                                                                JOIN 
                                                                                                                    customer c ON rd.Customer_id = c.Customer_id
                                                                                                                GROUP BY 
                                                                                                                    rd.Customer_id, c.Customer_fname, c.Customer_lname;"""},
            "SP - Get Customer Rental Details":{'id':"3","Query":"""call GetCustomerRentalDetails"""},
            "SP - Calculate Total Revenue":{'id':"4","Query":"""call CalculateTotalRevenue"""},
            "SP - Get Customer Rental History":{'id':"5","Query":"""call GetCustomerRentalHistory"""}
                        
                        
        }
        queryoption = list(dictionarydata.keys()) 
        selected_option_query = st.selectbox('Select an SQL Query:', queryoption)
        querydata=dictionarydata[selected_option_query]
        if   ((selected_option_query in dictionarydata.keys()) and (querydata['id']=='1')):
            
            time.sleep(1)
            message("""Hey!!
                    Give me Average rental duration for each car model.
                    Query and Output""") 
            time.sleep(1)
            message("""Hello I am MSD bot!
                    Query that is going to run is :""", is_user=True)  # align's the message to the right
            time.sleep(1)
            st.title("Query")
            st.text_area(label=" ",value="""WITH exc AS (
                                                        SELECT Car_model, AVG(DATEDIFF(Rental_enddate, Rental_startdate)) AS avg_rental_duration
                                                        FROM rental_details
                                                        JOIN car ON rental_details.Car_id = car.Car_id
                                                        GROUP BY Car_model
                                                    )
                                                    SELECT * FROM exc
                                                    where Car_model='{car_model}';""",height=150, disabled=True)
            query = """
                SELECT DISTINCT Car_model FROM car;
                """
            cursor.execute(query)
            car_model_data = cursor.fetchall()
            car_models_list = [model[0] for model in car_model_data]
            # car_models_list = ['None', '*', *car_models_list]
            car_model=st.selectbox('Select an Car Model:',car_models_list, index=0)
            if st.button("Submit Query1"):
                query = f"""
                        WITH exc AS (
                            SELECT Car_model, AVG(DATEDIFF(Rental_enddate, Rental_startdate)) AS avg_rental_duration
                            FROM rental_details
                            JOIN car ON rental_details.Car_id = car.Car_id
                            GROUP BY Car_model
                        )
                        SELECT * FROM exc
                        where Car_model='{car_model}';
                                    """
                cursor.execute(query)
                rows = cursor.fetchall()
                df=pd.DataFrame(rows)
                st.title("Data from the Database")
                df.columns=['car model','Avg Rental Duration']
                st.dataframe(df, height=100, width=650)
                st.balloons()
                st.toast('Hooray! This Query is a successful!', icon="✅")
        elif ((selected_option_query in dictionarydata.keys()) and (querydata['id']=='2')):
            time.sleep(1)
            message("""Hey!!
                    Give me Find the total revenue generated from rentals for each car brand:
                    Query and Output""") 
            time.sleep(1)
            message("""Hello I am MSD bot!
                    Query that is going to run is :""", is_user=True)  # align's the message to the right
            time.sleep(1)
            st.title("Query")
            st.text_area(label=" ",value="""WITH exc AS (
                        SELECT Car_brand, CONCAT('$', FORMAT(SUM(Estimated_cost), 2)) AS total_revenue
                        FROM rental_details
                        JOIN car ON rental_details.Car_id = car.Car_id
                        GROUP BY Car_brand)
                        select * from exc
                        where Car_brand = '{Car Brand}';""",height=150, disabled=True)
            query = """
                SELECT DISTINCT Car_brand FROM car;
                """
            cursor.execute(query)
            Car_brand_data = cursor.fetchall()
            Car_brand_list = [model[0] for model in Car_brand_data]
            Car_brand=st.selectbox('Select an Database:',Car_brand_list)
            if st.button("Submit1"):
                query = f"""
                        WITH exc AS (
                        SELECT Car_brand, CONCAT('$', FORMAT(SUM(Estimated_cost), 2)) AS total_revenue
                        FROM rental_details
                        JOIN car ON rental_details.Car_id = car.Car_id
                        GROUP BY Car_brand)
                        select * from exc
                        where Car_brand = '{Car_brand}';
                                """
                cursor.execute(query)
                rows = cursor.fetchall()
                st.title("Data from the Database")
                df=pd.DataFrame(rows)
                df.columns=['Car Brand','Total Revenue in USA $']
                st.dataframe(df, height=300, width=650)
                st.balloons()
                st.toast('Hooray! This Query is a successful!', icon="✅")
        elif ((selected_option_query in dictionarydata.keys()) and (querydata['id']=='3')):
            time.sleep(1)
            message("""Hey!!
                    Run a Stored procedure to Get Customer Rental Details By ID
                    Query and Output""") 
            time.sleep(1)
            message("""Hello I am MSD bot!
                    Query that is going to run is :""", is_user=True)  # align's the message to the right
            time.sleep(1)
            st.title("Query")
            st.text_area(label=" ",value='''call GetCustomerRentalDetails(<< Enter Customer ID>>);''', disabled=True)
            Customer_ID = st.number_input('Enter a number', value=0, min_value=0, max_value=100, step=1)
            st.write('You entered:', Customer_ID)
            if st.button("Submit"):
                query = f"call GetCustomerRentalDetails({Customer_ID});"
                cursor.execute(query)
                rows = cursor.fetchall()
                df=pd.DataFrame(rows)
                df.columns=['First Name','Last Name','Email','Total Rental','Total Rent paid']
                st.dataframe(df, height=300, width=650)
                st.snow()
        elif ((selected_option_query in dictionarydata.keys()) and (querydata['id']=='4')):
            st.write("Query")
            st.write('''call CalculateTotalRevenue("2023/12/30","2024/01/01");''')
            startdate = st.date_input('Select a start date')
            st.write('You Start entered:', startdate)
            enddate = st.date_input('Select a end date')
            st.write('You End entered:', enddate)
            if st.button("Submit"):
            
                # startdate = datetime.strptime(startdate, '%Y-%m-%d')
                startdate = startdate.strftime('%Y/%m/%d')
                # enddate = datetime.strptime(enddate, '%Y-%m-%d')
                enddate = enddate.strftime('%Y/%m/%d')
                print(enddate,"hi")

                st.write(startdate , enddate)
                query = f"""call CalculateTotalRevenue("{str(startdate)}","{str(enddate)}");"""
                cursor.execute(query)
                rows = cursor.fetchall()
                df=pd.DataFrame(rows)
                df.columns=['Total Revenue']
                st.dataframe(df, height=300, width=650)
        elif ((selected_option_query in dictionarydata.keys()) and (querydata['id']=='5')):
            st.write("Query")
            st.write('''call GetCustomerRentalHistory(<<Customer ID>>);''')
            Customer_ID = st.number_input('Enter a number', value=0, min_value=0, max_value=100, step=1)
            st.write('You entered:', Customer_ID)
            if st.button("Submit"):
                query = f"""call GetCustomerRentalHistory({Customer_ID})"""
                cursor.execute(query)
                rows = cursor.fetchall()
                df=pd.DataFrame(rows)
                df.columns=['Customer Firstname','Customer Lastname', 'Email','Estimated_cost','Car_model']
                st.dataframe(df, height=300, width=650)
        elif ((selected_option_query in dictionarydata.keys()) and (querydata['id']=='6')):
            st.title("Query")
            st.text_area(label=" ",value="""SELECT c.Customer_id, c.Customer_fname, c.Customer_lname, c.Customer_phone, c.Customer_license, COUNT(*) AS total_rentals, AVG(rd.Estimated_cost) AS avg_rental_cost
FROM rental_details rd
JOIN customer c
ON c.Customer_id= rd.Customer_id
GROUP BY Customer_id;""",height=150, disabled=True)
            if st.button("Submit"):
                query = f"""SELECT c.Customer_id, c.Customer_fname, c.Customer_lname, c.Customer_phone, c.Customer_license, COUNT(*) AS total_rentals, AVG(rd.Estimated_cost) AS avg_rental_cost
FROM rental_details rd
JOIN customer c
ON c.Customer_id= rd.Customer_id
GROUP BY Customer_id;
"""
                cursor.execute(query)
                rows = cursor.fetchall()
                df=pd.DataFrame(rows)
                df.columns=['Customer_id','Customer_fname', 'Customer_lname','Customer_phone','Customer_license','total_rentals', 'avg_rental_cost']
                st.dataframe(df, height=300, width=650)
        elif ((selected_option_query in dictionarydata.keys()) and (querydata['id']=='7')):
            time.sleep(1)
            message("""Hey!!
                    Calculate the total revenue generated from rentals for each month of the year.
                    Query and Output""") 
            time.sleep(1)
            message("""Hello I am MSD bot!
                    Query that is going to run is :""", is_user=True)  # align's the message to the right
            time.sleep(1)
            st.title("Query")
            st.text_area(label=" ",value="""SELECT 
                            CASE 
                                WHEN MONTH(Rental_startdate) = 1 THEN 'January'
                                WHEN MONTH(Rental_startdate) = 2 THEN 'February'
                                WHEN MONTH(Rental_startdate) = 3 THEN 'March'
                                WHEN MONTH(Rental_startdate) = 4 THEN 'April'
                                WHEN MONTH(Rental_startdate) = 5 THEN 'May'
                                WHEN MONTH(Rental_startdate) = 6 THEN 'June'
                                WHEN MONTH(Rental_startdate) = 7 THEN 'July'
                                WHEN MONTH(Rental_startdate) = 8 THEN 'August'
                                WHEN MONTH(Rental_startdate) = 9 THEN 'September'
                                WHEN MONTH(Rental_startdate) = 10 THEN 'October'
                                WHEN MONTH(Rental_startdate) = 11 THEN 'November'
                                WHEN MONTH(Rental_startdate) = 12 THEN 'December'
                            END AS rental_month,
                            YEAR(Rental_startdate) AS rental_year,
                            SUM(Estimated_cost) AS monthly_revenue
                        FROM 
                            rental_details
                        GROUP BY 
                            rental_month, rental_year
                        ORDER BY 
                            monthly_revenue DESC;
                        """,height=150, disabled=True)
            query = f"""SELECT 
                            CASE 
                                WHEN MONTH(Rental_startdate) = 1 THEN 'January'
                                WHEN MONTH(Rental_startdate) = 2 THEN 'February'
                                WHEN MONTH(Rental_startdate) = 3 THEN 'March'
                                WHEN MONTH(Rental_startdate) = 4 THEN 'April'
                                WHEN MONTH(Rental_startdate) = 5 THEN 'May'
                                WHEN MONTH(Rental_startdate) = 6 THEN 'June'
                                WHEN MONTH(Rental_startdate) = 7 THEN 'July'
                                WHEN MONTH(Rental_startdate) = 8 THEN 'August'
                                WHEN MONTH(Rental_startdate) = 9 THEN 'September'
                                WHEN MONTH(Rental_startdate) = 10 THEN 'October'
                                WHEN MONTH(Rental_startdate) = 11 THEN 'November'
                                WHEN MONTH(Rental_startdate) = 12 THEN 'December'
                            END AS rental_month,
                            YEAR(Rental_startdate) AS rental_year,
                            SUM(Estimated_cost) AS monthly_revenue
                        FROM 
                            rental_details
                        GROUP BY 
                            rental_month, rental_year
                        ORDER BY 
                            monthly_revenue DESC;"""
            cursor.execute(query)
            rows = cursor.fetchall()
            df=pd.DataFrame(rows)
            # df.columns=['Customer Firstname','Customer Lastname', 'Email','Estimated_cost','Car_model']
            st.dataframe(df, height=300, width=650)
            import matplotlib.pyplot as plt
            # Create a bar plot using matplotlib
            plt.figure(figsize=(10,5))
            plt.pie(df[2], labels=df[0], autopct='%1.1f%%')
            plt.title('Monthly Values')

            # Display the plot with Streamlit
            st.pyplot(plt)
        elif ((selected_option_query in dictionarydata.keys()) and (querydata['id']=='8')):
            time.sleep(1)
            message("""Hey!!
                    Give me Total revenue generated from rentals for each car brand.
                    Query and Output""") 
            time.sleep(1)
            message("""Hello I am MSD bot!
                    Query that is going to run is :""", is_user=True)  # align's the message to the right
            time.sleep(1)
            st.title("Query")
            st.text_area(label=" ",value="""SELECT Car_model, AVG(Car_milage / Rental_total_hrs) AS avg_mileage_per_hour
                                            FROM car
                                            JOIN rental_details ON car.Car_id = rental_details.Car_id
                                            GROUP BY Car_model
                                            ORDER BY avg_mileage_per_hour DESC;""",height=150, disabled=True)
            if st.button("Submit"):
                query = f"""SELECT Car_model, AVG(Car_milage / Rental_total_hrs) AS avg_mileage_per_hour
                            FROM car
                            JOIN rental_details ON car.Car_id = rental_details.Car_id
                            GROUP BY Car_model
                            ORDER BY avg_mileage_per_hour DESC;"""
                cursor.execute(query)
                rows = cursor.fetchall()
                df=pd.DataFrame(rows)
                # df.columns=['Customer Firstname','Customer Lastname', 'Email','Estimated_cost','Car_model']
                st.dataframe(df, height=300, width=650)
        elif ((selected_option_query in dictionarydata.keys()) and (querydata['id']=='9')):
            time.sleep(1)
            st.title("Query")
            st.text_area(label=" ",value="""SELECT 
       rd.Customer_id,
       c.Customer_fname,
       c.Customer_lname,
       SUM(rd.Estimated_cost) AS Total_Revenue,
       count(rd.Rental_id) As Total_Booked
   FROM 
       rental_details rd
   JOIN 
       customer c ON rd.Customer_id = c.Customer_id
   GROUP BY 
       rd.Customer_id, c.Customer_fname, c.Customer_lname;""",height=150, disabled=True)
            if st.button("Submit"):
                query = f"""SELECT 
       rd.Customer_id,
       c.Customer_fname,
       c.Customer_lname,
       SUM(rd.Estimated_cost) AS Total_Revenue,
       count(rd.Rental_id) As Total_Booked
   FROM 
       rental_details rd
   JOIN 
       customer c ON rd.Customer_id = c.Customer_id
   GROUP BY 
       rd.Customer_id, c.Customer_fname, c.Customer_lname;"""
                cursor.execute(query)
                rows = cursor.fetchall()
                df=pd.DataFrame(rows)
                # df.columns=['Customer Firstname','Customer Lastname', 'Email','Estimated_cost','Car_model']
                st.dataframe(df, height=300, width=650)

    elif selected_option =='2':
        
        st.title("Database Queries")
        query=st.text_area(label="Enter Query",value="""select * from car""",height=150)

        if st.button("Submit"):
                cursor.execute(query)
                rows = cursor.fetchall()
                df=pd.DataFrame(rows)
                st.title("Data from the Database")
                st.dataframe(df, height=100, width=650)
elif  selected_option=="Select Database":
     st.write('You Need to select database')
