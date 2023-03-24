# eyeblink-detection

Welcome to eyeblink-detection, a small Python project that uses facial landmarks and mathematical calculations to detect eyeblinks. The project provides two options for running it: locally with Python or with Docker. It also includes a peak-finding algorithm to locate specific peaks and parameters to filter out noise and longer eyeblinks.



![screenshot-eyeblink](https://user-images.githubusercontent.com/34193118/79985450-4af7fd00-84b3-11ea-9b0c-143741f65adb.png)



# How to Run
There are two options for running the eyeblink detection program: with or without Docker.

## Option 1: Without Docker

1. Install the required packages by running the following commands:

```bash
apt-get update

apt-get install build-essential cmake \
libopenblas-dev liblapack-dev \
libx11-dev libgtk-3-dev \
python python-dev python-pip \
python3 python3-dev python3-pip

pip3 install --upgrade pip
```

2. Clone the repository and navigate to the directory:
```bash
git clone https://github.com/sobir-git/eyeblink-detection
cd eyeblink-detection/
```

3. Create a virtual environment and install the required Python packages:

```bash
python3 -m venv env
. env/bin/activate
python -m pip install -r requirements.txt
```

4. Run the program:
```bash
python detect_blinks.py
```

You can add the -g flag to display the graph of metrics:
```bash
python -g detect_blinks.py
```


## Option 2: With Docker

1. Clone the repository and navigate to the directory:
```bash
git clone https://github.com/sobir-git/eyeblink-detection
cd eyeblink-detection/
```
2. Build the Docker image:
```bash
docker build -t eyeblink-detection:latest .
```

3. Run the Docker container with specific access to webcam and X11 desktop:
```bash
xhost +

docker run -it \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --device=/dev/video0:/dev/video0 \
    eyeblink-detection:latest
```

# How It Works
The eyeblink detection program takes facial landmarks using the dlib library and computes the eye-area-over-distance metric.


![adr-measures](https://user-images.githubusercontent.com/34193118/79987710-716b6780-84b6-11ea-8d2a-973e31c0b846.png)

Mathematically, it is computed as:
```
ADR = (sqrt(S1) + sqrt(S2)) / (2*d)
```
where `S1` and `S2` are the areas of the left and right eyes, and `d` is the distance between the centers of the two eyes.

The program applies some preprocessing to this ADR metric, including SG smoothing using the [Savitzky–Golay filter](https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter), and baseline correction by running a median filter and then subtracting it from the signal.

The program then runs a peak-finding algorithm to locate specific peaks using Scipy's `scipy.signal.find_peaks` function. The peak-finding algorithm is controlled by parameters such as prominence and peak_width. The peak_width parameter is used to filter out super-fast eyeblinks which occur in <100ms duration as a result of noise in the data, as well as filter out super-long eyeblinks that can happen when one is drowsy and closes their eyes for a longer time (>500ms). Here is snapshot of the metrics and peak
detection in action (show if run with `-g` flag):
![graph](https://user-images.githubusercontent.com/34193118/79990247-7e3d8a80-84b9-11ea-875e-5af1ddf10bd8.png)


# Acknowledgments
This project is based on this tutorial by [Adrian Rosebrock](https://pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/). We also thank the developers of the [dlib](http://dlib.net/) and [OpenCV](https://opencv.org/) libraries for providing excellent computer vision tools.


