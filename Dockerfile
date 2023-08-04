# Use an official Ubuntu runtime as a parent image
FROM python:3.11.4-slim-bullseye

# Set the working directory in the container to /app
WORKDIR /app

ADD . /app
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Update apt-get and install packages
RUN apt-get update && apt-get install -y \
libzbar0  supervisor \
 && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir tendo pyzbar psycopg2-binary psutil Pillow pytz streamlit plotly matplotlib 

EXPOSE 8501

#RUN  streamlit run /app/dashboard.py --server.port 8501 --server.baseUrlPath /scanner/dashboard/ --server.enableCORS false --server.enableXsrfProtection false
# Run app.py when the container launches
CMD ["/usr/bin/supervisord"]