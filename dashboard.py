import streamlit as st
import psycopg2
con = psycopg2.connect(
    host="Scanner.berta.corp",
    database="postgres",
    user="postgres",
    password="frgthy")
#con.autocommit = True
cur = con.cursor()

# Title
st.title("Dashboard for scanner/BERTA")

# slider
 
# first argument takes the title of the slider
# second argument takes the starting of the slider
# last argument takes the end number
level = st.slider("Select the days to refresh", 1, 30)
 
# print the level
# format() is used to print value
# of a variable at a specific position
st.text('Selected: {}'.format(level))


# Create a button, that when clicked, shows a text
if(st.button("Refresh")):
    cur.execute("select count(*) from scantable where dateandtime>=(now()::date+ INTERVAL '-{} day'); ".format(str(level)))
    number_str  = cur.fetchall()
    number=number_str[0][0]
    st.text(("Number of scans for today ", number))



    
