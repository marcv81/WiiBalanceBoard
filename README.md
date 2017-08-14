# Setup

## Dependencies

    conda create --name WiiBalanceBoard python=3.6
    source activate WiiBalanceBoard
    conda install --channel vpython vpython==7.1.2
    pip install python-uinput==0.11.2

## Run

    python main.py /dev/input/jsN

