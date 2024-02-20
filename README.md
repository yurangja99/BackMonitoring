# BackMonitoring

**Don't care other people!**: Do If another person (except yourself!) appears, quickly hide the current window!

### Prerequisites
- Windows 10 or newer

### Installation
First, clone this project. 

```commandline
git clone https://github.com/yurangja99/BackMonitoring.git
```

Then, install required packages. 

```commandline
conda create -n back-monitoring python=3.9
conda activate back-monitoring
pip install pypiwin32
pip install opencv-python
pip install face_detection@git+https://github.com/elliottzheng/face-detection
```

To use gpu, follow the [instruction](https://pytorch.org/get-started/locally/) to install torch. 

Finally, run `main.py` for use. 
You can set some configurations in `config` in `main.py`. 

```commandline
python main.py
```

### Acknowledgements
- I used `face_detection` implementation by [elliottzheng et al.](https://github.com/elliottzheng/face-detection)
