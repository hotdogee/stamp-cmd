# stamp-cmd
A Command Line Interface (CLI) for Statistical Analysis of Metagenomic Profiles (STAMP)

Information regarding STAMP can be found at: http://kiwi.cs.dal.ca/Software/STAMP

# Usage
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
