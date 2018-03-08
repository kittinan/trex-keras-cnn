# T-Rex Keras CNN

<p align="center">
  <a href="https://www.youtube.com/watch?v=oTCmk94YMvU" target="_BLANK">
    <img src="screenshot/screenshot.png" width="80%" />
  </a>
</p>


## T-rex game
[http://www.trex-game.skipser.com](http://www.trex-game.skipser.com)


### Install Requirement
```
pip install -r requirements.txt
```

Recommended to use Tensorflow-GPU as backend

## Instruction

### 1. Collect Data

Edit collect_data.py on this line

```python
im = ImageGrab.grab(bbox=(350,350,1000,480))
```

Change T-rex game screen position that match on your computer

run collect_data.py to collect screen capture and button you pressed (image file will store in img folder)
```
python collect_data.py
```

##### if screen capture too lag try install
```
sudo apt-get install scrot
```
