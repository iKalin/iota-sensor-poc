# IOTA Sensor POC

Read sensor data from the public NetAtmo API and attach it to the IOTA Tangle.

## Installation

```
pip install -r requirements.txt
```

On Debian/Ubuntu you might need to install `libssl-dev`.

## Installation as a Snap

You can install the script as a [Snap](https://www.ubuntu.com/desktop/snappy) by doing:

```
sudo snap install iota-netatmo --channel=beta
```

This will expose a `iota-netatmo` command which you can call as if you were calling `poc.py` directly (See Usage below).

## Configuration

Configuration options can be specified via CLI or config file. CLI options have higher precendence than the ones specified in configuration file and can be use to override them.

### CLI arguments

  - `--config`: configuration file to read options from.
  - `--node`: node to connect to (defaults to http://localhost:14265/).
  - `--seed`: seed to use.
  - `--address`: address to send the data to.
  - `--tag`: identifying Tag for the stream
  - `--price`: price value to attach to the data.
  - `--client_id`: client_id to used to connect to the NetAtmo API.
  - `--client_secret`: client_secret used to connect to the NetAtmo API.
  - `--username`: username used to connect to the NetAtmo API.
  - `--password`: password used to connect to the NetAtmo API.
  - `--buffer-size`: how many NetAtmo responses to store locally before attaching them to the Tangle (defaults to 0)
  - `--buffer-directory`: directory to store NetAtmo responses before attaching them as a single chunk.


### Config file format

Most of the options can be specified on an config file. You can tell the script to read this file via the `--config` option.

Here's how your configuration file should look (`config.ini.dist`):

```
[iota]
node=http://localhost:14265
seed=AAAAAAAA
address=BBBBBBBB
tag=STREAMID
price=1234.5678
[sensor]
client_id=abcabcaabc
client_secret=defdefdef
username=name@localhost
password=123456
[buffer]
size=0
directory=./buffer/
```

## Usage

```
python poc.py --config configuration-file.ini
```

Alternatively, if you've installed the script as a snap, the equivalent call would be:

```
iota-netatmo --config configuration-file.ini
```

*Important Note for the snap version*: If you're using a configuration file with the snap version, the file would need to be located in your home directory.
This is because snaps are contained and only have access to [limited functionality](https://snapcraft.io/docs/reference/interfaces).

## TODO

- Handle expired NetAtmo tokens instead of requesting a new one each time.
- Validate tag's length.
- Add more NetAtmo API methods.
- Better errors for invalid characters in ini files.
