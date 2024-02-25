## M3U Category Matcher

Do you have IPTV provider who doesn't add categories to channels, but uses channels for it?
This script will attach channel-like categories to channels under them.
Example:

You have these 5 channels:
1. ### GENERAL ###
2. TV1 HD
3. TV2 HD
4. ### MUSIC ###
5. METAL LIVE TV HD

For example, if you provided `\#\#\# (.*) \#\#\#` regex:
This script will __remove__ channel with no. 1. and 5., then __attach__ categories:
- GENERAL (matched group from regex!) to channels 2, 3,
- MUSIC to channel 5.

### NOTE!
This script is in BETA phase. Please report any bugs!

### Based on
- argparse
- pathlib
- re
- [ipytv](https://github.com/Beer4Ever83/ipytv)

### Usage
```bash
python3 <path-to-script> -i "<m3u path>" -r "<regex to match>" (-v)
```

### Result
When everything is done, file is **OVERWRITTEN**!

### Example usage
```bash
python3 <path-to-script> -i "m3u_list.m3u" -r "\#\#\# (.*) \#\#\#"
```

### Available parameters
- -i/--input - absolute path to m3u+ file
- -r/--regex - regular expression used to match categories in channel names
- -v/--verbose - enable verbose mode
