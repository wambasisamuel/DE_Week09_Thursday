FROM python:3.9.16-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PYTHONWARNINGS="ignore"
ENV DEBIAN_FRONTEND="noninteractive"
ENV TZ='Africa/Nairobi'

WORKDIR /project

COPY requirements.txt .

RUN  apt-get -y update && apt-get -y --no-install-recommends install tzdata cron netcat
RUN pip install --upgrade pip &&  pip install --no-cache-dir -r requirements.txt

COPY . .
#CMD ["nc", "-lk", "1337"]
#CMD ["cron", "-f"]
#HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "/project/visualize.py", "--server.port=8501", "--server.address=0.0.0.0"]
