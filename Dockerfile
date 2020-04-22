FROM python:3.7


RUN apt-get update  &&\
	apt-get install -y \
		build-essential \
		cmake \
		libopenblas-dev \
		liblapack-dev \
		libx11-dev \
		libgtk-3-dev \
		python python-dev python-pip \
		python3 python3-dev python3-pip

ADD ./* /app/
WORKDIR /app/

RUN pip install dlib
RUN pip install jupyter matplotlib numpy imutils opencv-python pandas scipy

ENTRYPOINT ["python", "detect_blinks.py"]



