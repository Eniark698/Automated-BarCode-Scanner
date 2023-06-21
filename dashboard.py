import streamlit as st
import psutil
import time
import plotly.express as px
import pandas as pd
import numpy as np


def create_chart():
    # Sample data
    data = {'Fruit': ['Apples', 'Oranges', 'Bananas'],
            'Amount': [10, 15, 7]}

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Create a Plotly Express bar chart
    fig = px.bar(df, x='Fruit', y='Amount', title='Fruit Count')

    return fig






def get_system_info():
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    memory_total = memory_info.total / (1024.0 ** 3)  # convert bytes to GB
    memory_used = memory_info.used / (1024.0 ** 3)
    memory_percent = memory_info.percent
    return cpu_percent, memory_total, memory_used, memory_percent

def main():
    st.title('PC Monitoring Dashboard')

    cpu_placeholder = st.empty()
    memory_placeholder = st.empty()
    cpu_placeholder_1 = st.empty()
    memory_placeholder_1 = st.empty()
    st.plotly_chart(create_chart())

    while True:
        cpu_percent, memory_total, memory_used, memory_percent = get_system_info()
        cpu_placeholder.metric(label="CPU Usage", value=f"{cpu_percent}%", delta=None)
        memory_placeholder.metric(label="Memory Usage", value=f"{memory_used:.2f} GB / {memory_total:.2f} GB", delta=f"{memory_percent}%")
         # Gather current system data
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent

        # Create new bar charts with the current data
        cpu_chart = cpu_placeholder_1.bar_chart(data=[cpu_percent], width=20)
        memory_chart = memory_placeholder_1.bar_chart(data=[memory_percent], width=20)

    # Set a delay between loops

        time.sleep(10)

if __name__ == "__main__":
    main()
