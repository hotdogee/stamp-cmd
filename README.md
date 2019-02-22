# stamp-cmd
A Command Line Interface (CLI) for Statistical Analysis of Metagenomic Profiles (STAMP)

[![BIOTOOLS](https://img.shields.io/badge/sponsored%20by-BIOTOOLS-orange.svg)](https://www.toolsbiotech.com/)
[![Docker Pulls](https://img.shields.io/docker/pulls/hotdogee/stamp-cmd.svg)][hub]
[![Docker Stars](https://img.shields.io/docker/stars/hotdogee/stamp-cmd.svg)][hub]
[![Docker Layers](https://images.microbadger.com/badges/image/hotdogee/stamp-cmd.svg)][hub]
[![Docker Version](https://images.microbadger.com/badges/version/hotdogee/stamp-cmd.svg)][hub]

Information regarding STAMP can be found at: http://kiwi.cs.dal.ca/Software/STAMP

# Docker Usage
```
$ docker run -t -v ${PWD}/example:/data --name stamp1 hotdogee/stamp-cmd -i otu.g.spf -g Grouping.txt -d /out
$ docker cp stamp1:/out .
$ docker container rm stamp1
```

# Local Usage
```
$ python stamp_cmd.py -h
usage: stamp_cmd.py [-h] -i PROFILE -g METADATA [-d OUTPUT] [-p PLOT]
                    [-t TABLE]

optional arguments:
  -h, --help            show this help message and exit
  -i PROFILE, --profile PROFILE
                        Path to the profile file
  -g METADATA, --metadata METADATA
                        Path to the group metadata file
  -d OUTPUT, --output OUTPUT
                        Output directory (default: output)
  -p PLOT, --plot PLOT  
                        Plot filename template (default: {g1}-vs-{g2}.psig.png)
  -t TABLE, --table TABLE
                        Table filename template (default: {g1}-vs-{g2}.test.xls)
```

# Docker build
```
$ docker build -f ./mkl/Dockerfile -t hotdogee/stamp-cmd:1.5.0 .
$ docker tag hotdogee/stamp-cmd:1.5.0 hotdogee/stamp-cmd:latest
$ docker push hotdogee/stamp-cmd
```

[hub]: https://hub.docker.com/r/hotdogee/stamp-cmd