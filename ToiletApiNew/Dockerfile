FROM osgeo/gdal:ubuntu-small-latest
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until
RUN apt-get update -y
RUN apt-get install -y python
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev libpq-dev

# set work directory
WORKDIR /usr/src/ToiletApiNew
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
