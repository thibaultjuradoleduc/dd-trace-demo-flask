FROM python:2
ADD flask_dd_trace.py /
ADD db_config.py /
ENV DB_HOST <DB_HOST>
ENV DB_USERNAME <DB_USERNAME>
ENV DB_PASSWORD <DB_PASSWORD>
ENV DB_NAME <DB_NAME>
RUN pip install -r requirements.txt
CMD [ "python", "./flask_dd_trace.py" ]
