# Ed&Co Automation Tool

Ed&Co is a network media on Instagram and Twitter that talks about the NBA and news. The authors creates posters to post on their social network and they did it by hand daily. This automation tool prevent them to check the NBA daily stats and fill the data on their Photoshop templates.

## Installation

Install [Python 3.9](https://www.python.org/downloads/release/python-390/)

In your project directory, open the command line and type :

```bash
pip install -r requirements.txt
```

All is set up, you are good to go.

## Usage

If you daily want to generate a new psd file with the NBA statistiques preloaded, type this command :

```bash
python edco.py
```

To generate the PSD file with a specific date :

```bash
python edco.py -D 20210208 #for 08/02/2021, please respect the format of 8 digits
python edco.py --date 20210208
```

## Note

Logos cannot be replaced automatically for now.
