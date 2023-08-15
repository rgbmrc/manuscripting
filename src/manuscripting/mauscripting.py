import fileinput
import re
import subprocess
import shutil
import sys
from importlib import resources
from itertools import chain
from pathlib import Path


def enc(encoding, files):
    accents = resources.read_text("manuscripting", "accents.txt").splitlines()
    accents = {a[0]: f"{{{a[1:]}}}" for a in accents}
    if encoding == "unicode":
        accents = {v: k for k, v in accents.items()}
    for line in fileinput.input(files=files, inplace=True):
        for a in accents.items():
            line = line.replace(*a)
        sys.stdout.write(line)


def bib(source, dest, omit, max_authors, only_journal):
    if not dest:
        dest = Path(source).name
    if max_authors:
        max_authors_regex = re.compile(
            "(author[\s=]*\{{{0})(?:{0}){{{1},}}.+?\}}".format(
                ".+? and ", max_authors - 2
            )
        )
    omit = "|".join(map("({})".format, omit or ["?!"]))
    omit = f"\s+({omit})"
    with open(source, "r") as source:
        with open(dest, "w") as dest:
            for line in source:
                m = re.match("@(\w+)", line)
                if m is not None:
                    type = m.group(1).lower()
                if re.match(omit, line):
                    continue
                if max_authors:
                    line = max_authors_regex.sub(r"\1others}", line)
                if only_journal:
                    raise NotImplementedError()
                    if type != "article" or not re.match("\s+eprint", line):
                        pass
                dest.write(line)


def sub(subname, projname, no_build, exclude, bibliography, input):
    projname = Path(projname)
    dest = Path(f"submissions/{projname}_{subname}/")
    dest.mkdir(parents=True, exist_ok=True)

    # collect relevant resources (using git)
    exclude = set(chain.from_iterable(Path().glob(e) for e in exclude))
    files = subprocess.check_output(["git", "ls-files"], text=True).splitlines()
    files = map(Path, files)
    files = {f for f in files if not f in exclude}
    tex_file = projname.with_suffix(".tex")
    bbl_file = projname.with_suffix(".bbl")
    if no_build:
        pass
    else:
        subprocess.run(["latexmk", "-interaction=nonstopmode", str(tex_file)])
    if bibliography:
        bibliography = open(bbl_file).read()
    else:
        files.add(bbl_file)
        bibliography = rf"\input{{{bbl_file}}}"

    # copy files in a flat directory structure
    nestings = {}
    for f in files:
        f_str = str(f).replace("/", "_")
        f_flat = Path(f_str)
        if len(f.parts) > 1:
            nestings[str(f.with_suffix(""))] = str(f_flat.with_suffix(""))
        shutil.copy(f, dest / f_flat)
        print(f_flat)

    # update references to nested files
    for line in fileinput.input(files=dest.glob("*.tex"), inplace=True):
        for nf in nestings.items():
            line = line.replace(*nf)
        sys.stdout.write(line)

    # handle \bibliogrpahy and \input commands
    inputs_files = set()
    for line in fileinput.input(files=[dest / tex_file], inplace=True):
        m = re.match(r"\\bibliography\{.+?\}", line)
        if bibliography and m:
            # just in case smth preceeds or follows \bibliography{}
            line = line[: m.start()] + bibliography + line[m.end() :]
        if input:
            while m := re.search(r"\\input\{(.+?)\}", line):
                f = Path(m.group(1)).with_suffix(".tex")
                line = line[: m.start()] + f.read_text() + line[m.end() :]
                inputs_files.add(f)
        sys.stdout.write(line)
    for f in inputs_files:
        f.unlink()

    # zip
    shutil.make_archive(dest, "zip", dest)
