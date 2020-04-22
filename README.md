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


# How it works

It takes the facial landmarks using dlib library. It computes eye-area-over-distance metric which is
the technically the average of square roots of both eye areas divided by the distance between them.

![adr-measures](https://user-images.githubusercontent.com/34193118/79987710-716b6780-84b6-11ea-8d2a-973e31c0b846.png)

Mathematically computed as 
```
ADR = (sqrt(S1) + sqrt(S2)) / (2*d)
```
where `S1` and `S2` are the areas of the left and right eyes and `d` is the distance between the centers of the two eyes.

We apply some preprocessing this ADR metric:
- SG smoothing (using [Savitzky–Golay filter](https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter))
- Baseline correction (by running a median filter and then subtracting it from the signal)

Then we run a peak finding algorithm to locate specific peaks. For this we use Scipy's `scipy.signal.find_peaks`
function. The peak finding algorithm is controlled by parameters such as `prominence` and `peak_width`. 
Using the parameter `peak_width` we will control filter out *super-fast eyeblinks* which occure in <100ms duration 
as a result of noise in the data, as well as we filter out *super-long eyeblinks* 
which can happen when one is drowsy and closes eyes for longer time (>500ms). Here is snapshot of the metrics and peak
detection in action (show if run with `-g` flag):
![graph](https://user-images.githubusercontent.com/34193118/79990247-7e3d8a80-84b9-11ea-875e-5af1ddf10bd8.png)
