# novel-downloader
Novel-downloader is a simple Python 3 script to download web novel from  following sources:
1. https://lightnovelreader.org/

Currently, no support for other sources

Usage:
1. `$ python3 main.py https://lightnovelreader.org/i-reincarnated-but-will-try-to-live-without-using-my-cheat-ability` 
2. `$ python3 main.py https://lightnovelreader.org/i-reincarnated-but-will-try-to-live-without-using-my-cheat-ability -g https://lightnovelreader.org/i-reincarnated-but-will-try-to-live-without-using-my-cheat-ability/chapter-1`

_Variant 1_ - will assume that there are simple chapter numeration system

_Variant 2_ - option `[-g]` will receive list of chapters from any available chapter in the novel

After downloading you will have html-like file

To convert it to **epub** or other useful format simply add extension **.html** first

Then install <a href="https://pandoc.org/installing.html">pandoc</a> and use following code:
`$ pandoc -o "Novel name.epub" "Novel name.html"`

28-02-2022
