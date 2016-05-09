2048 in TKinter
===============
A simple 2048 clone in Python TKinter.

![demo](demo.png)

## Usage

```python
from py2048 import runApp
runApp()
```

## Dependencies

tkinter (with Tcl/Tk 8.6)

## Installation

via `pip`:
```bash
pip install git+https://github.com/weihanglo/py2048.git
# or
pip install https://github.com/weihanglo/py2048/archive/master.zip
```

via `git clone`:
```bash
git clone https://github.com/weihanglo/py2048.git
cd py2048
python3 setup.py install
```

If you have some trouble in importing tkinter, try following commands.
```
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/CentOS
sudo dnf install python3-tkinter
```

## Tests

All tests are passed under:
- Python 3.5.1 with OSX 10.11.4, 
- Python 3.4.3 with Fedora 23,
- Python 3.4.2 with Debian 8.

To test the logical part, clone and run the commands:
```
python3 setup.py test
```

## Authors

- [Weihang Lo](https://github.com/weihanglo)
