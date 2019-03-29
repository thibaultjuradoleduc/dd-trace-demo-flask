FROM python:2
ADD flask_dd_trace.py /
ADD db_config.py /
ENV DB_HOST db_kikeyama-rds-mysql.cviighkaj1ry.us-east-1.rds.amazonaws.com
ENV DB_USERNAME <db_username>
ENV DB_PASSWORD <db_password>
ENV DB_NAME <db_name>
RUN pip install -r requirements.txt
CMD [ "python", "./flask_dd_trace.py" ]
