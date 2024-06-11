# taAuthor
Create XML Author List using INSPIRE HEP format.

Recommended: add program to PATH (optional):
```bash
export PATH=$PATH:/full/path/to/taAuthor
```

Usage:
```bash
create_xml.py /full/path/to/authorlist.csv "Publication Reference"
```
"Publication Reference" can be an internal report number, arXiv number, ISBN, DOI, web destination, title, etc.

For more see:
```bash
create_xml.py --help 
```

TO DO:
Write ElementTree to CSV file.
