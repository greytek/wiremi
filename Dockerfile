FROM python:3.9.4-slim

# Allow statements and log
ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY .. .
# Install production dependencies.
# Install the ODBC driver dependencies
RUN apt-get update && apt-get install -y gnupg2 curl
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

RUN pip install -r requirements.txt
# Run
ENTRYPOINT ["python", "main.py"]