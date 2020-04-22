FROM jjanzic/docker-python3-opencv

# install dlib

RUN apt-get update && \
  apt-get install -y build-essential cmake \
  libopenblas-dev liblapack-dev \
  libx11-dev libgtk-3-dev \
  python python-dev python-pip \
  python3-dev python3-pip \
  && pip3 install --upgrade pip \
  && pip3 install numpy imutils scipy matplotlib dlib 



WORKDIR /
RUN apt-get install git && \
  git clone https://github.com/sobir-git/eyeblink-detection && \


WORKDIR /eyeblink-detection/

ENTRYPOINT ["python3", "detect_blinks.py"]


# runs using
# docker run -it --rm  --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY blink-detector:latest