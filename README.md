# NYT Crossword Downloader

These are a couple of old hacky scripts I wrote back when I got my Remarkable
table. The script downloads the latest puzzles from NYT as PDFs, and syncs them
with the Remarkable tablet using [RCU](http://www.davisr.me/projects/rcu/) -
This has NOT been tested with latest versions of the Remarkable nor RCU.

By default it will download the last two weeks of puzzles. It will not download
a file twice if the file exists in the `crosswords` folder.

## Caveats

- This script is not affiliated with the NYT at all, and use of this script is
  at your own risk. Although I haven't been permanently banned, I have run into
  issues where their bot detection blocked m
- Tested with python 3.8.10. If you are using `pyenv`, then it should
  automatically choose the right version.

## Usage

1. `git clone https://github.com/nikwithak/nyt_crossword_downloader.git`
2. `cd nyt_crossword_downloader`

- TODO: Add login / authentication to the script so these next steps aren't
  necessary.

3. Log in to https://www.nytimes.com/crosswords/ in your browser.
4. Open Developer Tools in your browser (Control+Shift+I)
5. Open the Network tab.
6. Refresh the page, and find the requestin the Network tab, and copy the
   contents of the `Cookie: `header, starting with with `nyt-` and ending in
   `nyt-geo=US`
7. Paste the contents of the Cookie header into a file called "nyt_cookies.txt"
8. run `python ./fetch_crosswords.py`

## Support

This script is provided with no warranty or guarantees. If you have questions or
run into issues, please
[file an Issue](https://github.com/nikwithak/nyt_crossword_downloader/issues/new/choose).
