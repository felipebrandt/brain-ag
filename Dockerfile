FROM python:3.9
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /
EXPOSE 5000

COPY . /


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "main.py", "-h", "0.0.0.0", "-p", "5000"]
