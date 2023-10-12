#!/bin/python3
import os
import locale

from parse import SongParser
from generate import generate_tex

TEX_DIR = "songs/tex/"
WORK_DIR = "songs/workdir/"
locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")


def gen_songbook(tex_files):
    inp = open("songbook.def.tex", "r", encoding='utf-8')
    out = open("songbook.tex", "w", encoding='utf-8')

    for line in inp:
        if line == '-- Songs here --\n':
            for tex_file in tex_files:
                replacement = f"\\input{{{TEX_DIR}{tex_file}}}\n\\newpage\n"
                out.write(replacement)
        else:
            out.write(line)


def main():
    for file in os.listdir(WORK_DIR):
        with open(f"{WORK_DIR}{file}", "r") as inp:
            parser = SongParser()
            for line in inp:
                parser.parse_line(line)

        title = file[:file.find(".txt")]
        title_with_underscores = title.replace(" ", "_")
        filepath = f"{TEX_DIR}{title_with_underscores}.tex"
        generate_tex(parser.tokens, title, filepath)

    tex_files = sorted([file for file in os.listdir(TEX_DIR)
                        if file.endswith(".tex")], key=locale.strxfrm)
    gen_songbook(tex_files)


if __name__ == "__main__":
    main()
