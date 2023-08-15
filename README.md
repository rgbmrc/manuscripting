# manuscripting

A command line tool easing the (painful) process of preparing scientific manuscripts.

## Installation

```
git clone https://github.com/rgbmrc/manuscripting.git
pip install ./manuscripting
```

## Usage

```
usage: manuscripting [-h] {enc,sub,bib} ...

positional arguments:
  {enc,sub,bib}
    enc          switch between text encodings
    sub          prepare submission
    bib          generate bibfile from source

options:
  -h, --help     show this help message and exit
```

#### tip: passing arguments from files via @
The following two lines are equivalent (`--` marks the start of positional arguments)
```
manuscripting @sub.args -- prl
manuscripting sub -exclude .gitignore *.args **/*.bib -- prl
```
provided the working directory contains a file `sub.args` which reads
```
sub
--exclude
.gitignore
*.args
**/*.bib
```

### `enc`: text encoding

```
usage: manuscripting enc [-h] {ascii,unicode} files [files ...]

positional arguments:
  {ascii,unicode}  encoding
  files            files to encode

options:
  -h, --help       show this help message and exit
```

__note__ regarding `.bib` files: 
JabRef can be configured to perform the conversion on cleanup;
one could also run
```
biber --tool --output_encoding=UTF-8 bibfile.bib
```
but this is slow and it heavily processes the source file, potentially with a disruptive outcome if the file is in BibTeX (rather than BibLaTeX) format.

### `bib`: managing bibliographies
Process and import references from one or more personal BibTeX or BibLaTeX files (e.g. [JabRef](https://www.jabref.org/) libraries).
```
usage: manuscripting bib [-h] [-o [OMIT ...]] [-j] [-a MAX_AUTHORS] source [dest]

positional arguments:
  source                source bib file
  dest                  destination bib file [default: same as source file name]

options:
  -h, --help            show this help message and exit
  -o [OMIT ...], --omit [OMIT ...]
                        fields to be omitted
  -j, --only-journal    omit eprint field for published papers
  -a MAX_AUTHORS, --max-authors MAX_AUTHORS
                        maximum number of authors, if more 'et al' is used
```

### `sub`: preparing submissions
Prepare a zipped archive for uploads to submission servers.
```
usage: manuscripting sub [-h] [-n] [--exclude EXCLUDE] [-b] [-i] subname [projname]

positional arguments:
  subname             submission name
  projname            project name [default: QCD_spectrum]

options:
  -h, --help          show this help message and exit
  -n, --no-build      do not build the project beforehand
  --exclude EXCLUDE   regex matching files to exclude
  -b, --bibliography  embed referenced bib entries
  -i, --input         embed inputted tex files
```
