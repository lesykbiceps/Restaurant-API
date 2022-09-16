FROM python
WORKDIR /usr/src/app
COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt
# copy project
COPY . /usr/src/app

# Ensure the path here is correct
ENV FLASK_APP /app/run.py

CMD ["python","run.py"]
