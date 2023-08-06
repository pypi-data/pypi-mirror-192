# Cinetone

A python CLI tool for generating color palettes from a given video file. 

## Installation

Install it from pypi using : 

```
pip install cinetone
```

## Usage

The tool can be run from the command line using the following syntax:

```
cinetone [-h] [-o OUTPUT] [-sc SKIPCOUNT] video_file
```
- `video_file: Path to the video file to be decoded (required)`
- `-o, --output: Places the output in the specified file. Saves into out.png by default`
- `-sc, --skipcount: Specifies the frames to skip while processing. Default value is 50`
- `-h, --help: View help`

## Dependencies

- imageio[ffmpeg]