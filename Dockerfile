FROM jjanzic/docker-python3-opencv

# # Replace 1000 with your user / group id
# RUN export uid=1000 gid=1000 && \
#     mkdir -p /home/developer && \
#     echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
#     echo "developer:x:${uid}:" >> /etc/group && \
#     echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
#     chmod 0440 /etc/sudoers.d/developer && \
#     chown ${uid}:${gid} -R /home/developer


# install dlib dependencies
RUN apt-get update && \
  apt-get install -y build-essential cmake \
  pkg-config libatlas-base-dev libboost-python-dev \
  libopenblas-dev liblapack-dev libboost-all-dev \
  libx11-dev libgtk-3-dev wget \
  python python-dev python-pip \
  python3 python3-dev python3-pip \
  && pip3 install --upgrade pip \
  && pip3 install numpy imutils scipy matplotlib dlib

# # installdlib
# RUN wget http://dlib.net/files/dlib-19.6.tar.bz2 && \
# 	tar xvf dlib-19.6.tar.bz2 && \
# 	cd dlib-19.6/ &&\
# 	mkdir build && \
# 	cd build && \
# 	cmake .. && \
# 	cmake --build . --config Release && \
# 	sudo make install && \
# 	sudo ldconfig &&\
# 	cd .. &&\
# 	pkg-config --libs --cflags dlib-1

# RUN  # move to dlib's root directory
# 	cd dlib-19.6 &&\
# 	python setup.py install &&\
# 	# clean up(this step is required if you want to build dlib for both Python2 and Python3)
# 	rm -rf dist &&\
# 	rm -rf tools/python/build  &&\
# 	rm python_examples/dlib.so 


# WORKDIR /
# RUN apt-get install git && \
# git clone https://github.com/sobir-git/eyeblink-detection

ADD ./* /eyeblink-detection/

WORKDIR /eyeblink-detection/


ENTRYPOINT ["python3", "detect_blinks.py"]



# runs using
# docker run -it --rm  --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY blink-detector:latest


# docker run -it \
#     --user=$USER \
#     --env="DISPLAY" \
#     --volume="/etc/group:/etc/group:ro" \
#     --volume="/etc/passwd:/etc/passwd:ro" \
#     --volume="/etc/shadow:/etc/shadow:ro" \
#     --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
#     --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
#     blink-detector:latest2


# docker run -it \
#     --env="DISPLAY" \
#     --env="QT_X11_NO_MITSHM=1" \
#     --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
#     blink-detector:latest2
# export containerId=$(docker ps -l -q)