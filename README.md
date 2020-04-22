# eyeblink-detection

![screenshot-eyeblink](https://user-images.githubusercontent.com/34193118/79985450-4af7fd00-84b3-11ea-9b0c-143741f65adb.png)


# How to run
There are two options. With an without Docker.


## 1. Install requirements

```bash
apt-get update

apt-get install build-essential cmake \
libopenblas-dev liblapack-dev \
libx11-dev libgtk-3-dev \
python python-dev python-pip \
python3 python3-dev python3-pip

pip3 install --upgrade pip
```

## 2. Clone the repo
```bash
git clone https://github.com/sobir-git/eyeblink-detection
cd eyeblink-detection/
```

## 3. Install requirements.txt
We are creating a virtual environment and installing the required python packages (mainly dlib, opencv, scipy).

```bash
python3 -m venv env
. env/bin/activate
python -m pip install -r requirements.txt
```

## 4. Run
```bash
python detect_blinks.py
```

You can add `-g` flag to display the graph of metrics.
```bash
python -g detect_blinks.py
```


# Run using Docker

## 1. Clone the repo
```bash
git clone https://github.com/sobir-git/eyeblink-detection
cd eyeblink-detection/
```

## 2. Build docker image
```bash
docker build -t eyeblink-detection:latest .
```
Wait for some time. It may take 5-10 minutes.

## 3. Run docker image
Run the following command, giving the container specific access to webcam and X11 desktop.

```bash
docker run -it \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --device=/dev/video0:/dev/video0 \
    eyeblink-detection:latest
```

