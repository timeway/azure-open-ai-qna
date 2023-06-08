FROM python:3.9.10-slim-buster
RUN apt-get update && apt-get install python-tk python3-tk tk-dev -y
COPY ./code/requirements.txt /usr/local/src/azure-open-ai-qna/requirements.txt
WORKDIR /usr/local/src/azure-open-ai-qna
RUN pip install -r requirements.txt
COPY ./code /usr/local/src/azure-open-ai-qna
EXPOSE 80
CMD ["streamlit", "run", "Home.py", "--server.port", "80", "--server.enableXsrfProtection", "false"]