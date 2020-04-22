# eyeblink-detection

# How to run

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
You can optionally create virual environment first
```bash
# optional
python3 -m venv env
. env/bin/activate
```

Then run
```
pip3 -m pip install -r requirements.txt
```

# 4. Run
```bash
python3 detect_blinks.py
```
