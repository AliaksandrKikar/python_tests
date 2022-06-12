FROM python:3.9
ADD ./python_tack
WORKDIR /python_tack
COPY test_DB_AdventureWorks2017.py ./
RUN pip install -r requirements.txt
CMD ["python", "./test_DB_AdventureWorks2017.py"]