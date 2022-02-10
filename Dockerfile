FROM python:3.9.7

WORKDIR /root/Mikobot

COPY . .

RUN pip3 install --upgrade pip setuptools

RUN pip install -U -r requirements.txt

CMD ["python3","-m","Mikobot"] 
