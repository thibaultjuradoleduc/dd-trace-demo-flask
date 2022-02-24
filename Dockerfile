FROM python:3
ADD flask_dd_trace.py /
ADD db_config.py /
ADD requirements.txt /
ENV DB_HOST mysql
ENV DB_USERNAME demo
ENV DB_PASSWORD demo
ENV DB_NAME demo
RUN pip install -r requirements.txt
CMD [ "python", "./flask_dd_trace.py" ]
