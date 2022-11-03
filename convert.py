from os import listdir
import locale


def main():
    locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")
    tex_dir = "songs/tex/"
    work_dir = "songs/workdir/"

    # Find all txt
    txt_files = [file for file in listdir(work_dir) if file.endswith(".txt")]

    # Check and fix the txt file formatting
    for file in txt_files:
        transform_txt(work_dir + "\\" + file)

    # Transform txt to tex
    for file in txt_files:
        txt2tex(work_dir + file, tex_dir + file.replace(".txt", ".tex").replace(" ", "_"))

    # Find all tex
    tex_files = sorted([file for file in listdir(tex_dir) if file.endswith(".tex")], key=locale.strxfrm)

    # Generate songbook as tex
    gen_songbook(tex_files)

def transform_txt(file_path):
    lyrics, chords = extract_lines_from_txt(file_path)
    max_lyrics_line_length = max([len(lyric) for lyric in lyrics])
    with open(file_path, "w", encoding='utf-8') as f:
        for i in range(0, len(lyrics)):
            if len(lyrics[i]) == 0:
                f.write('\n')
            else:
                f.write(lyrics[i].ljust(max_lyrics_line_length + 5, ' ') + ' :: ' + chords[i] + '\n')


def txt2tex(txt_file_path, tex_file_path):
    title = txt_file_path.split("/")[-1][:-4]
    lyrics, chords = extract_lines_from_txt(txt_file_path)
    chords = [c.replace('#', '\\#') for c in chords]
    layout = "single_column"

    for line in lyrics:
        if "---" in line:
            layout = "two_columns"

    if layout == "single_column":
        begin_document = "\\subsection{" + title + "}\n\n\\begin{tabular}{l l}\n"
        end_document = "\\end{tabular}"

        with open(tex_file_path, "w", encoding='utf-8') as out:
            out.write(begin_document)
            for i in range(len(lyrics)):
                out.write(lyrics_line_to_tex(lyrics[i]))
                out.write(chords_line_to_tex(chords[i]))
            out.write(end_document)
    else:
        begin_document = "\\subsection{" + title + "}\n\n\\begin{tabular}{l l l l}\n"
        end_document = "\\end{tabular}"
        left_lyrics, right_lyrics, left_chords, right_chords = side_lines(lyrics, chords)

        with open(tex_file_path, "w", encoding='utf-8') as out:
            out.write(begin_document)
            for i in range(len(lyrics)):
                out.write(lyrics_line_to_tex(lyrics[i]))
                out.write(chords_line_to_tex(chords[i]))
            out.write(end_document)


def extract_lines_from_txt(file_path):
    lyrics = []
    chords = []

    for line in open(file_path, "r", encoding='utf-8').readlines():
        if '::' in line:
            lyrics.append(line.split('::')[0])
            chords.append(line.split('::')[1].strip())
        else:
            lyrics.append(line)
            chords.append(line)

    return [lyric.strip() for lyric in lyrics], chords


def lyrics_line_to_tex(line):
    if len(line) > 0 and line[0] == "+":
        return "\t\\textbf{" + line[1:] + "}\n"
    elif len(line) > 0 and line == "===":
        return "\t\\end{tabular}\n\t\\newpage\n\t\\begin{tabular}{l l}\n"
    else:
        return "\t" + line + "\n"


def chords_line_to_tex(line):
    if len(line) > 0 and line == "===":
        return ""
    else:
        return "\t&" + line + "\\\\\n"


def gen_songbook(tex_files):
    inp = open("songbook.def.tex", "r", encoding='utf-8')
    out = open("songbook.tex", "w", encoding='utf-8')

    for line in inp:
        if line == '-- Songs here --\n':
            for tex_file in tex_files:
                replacement = '\\input{songs/tex/' + tex_file + '}\n\\newpage\n'
                out.write(replacement)
        else:
            out.write(line)


def side_lines(lyrics, chords):
    ll = []
    rl = []
    lc = []
    rc = []
    after_token = False
    for i in range(len(lyrics)):
        if lyrics[i].strip() == "---":
            after_token = True
            continue
        if after_token:
            rl.append(lyrics[i])
            rc.append(chords[i])
        else:
            ll.append(lyrics[i])
            lc.append(chords[i])
    return ll, rl, lc, rc


if __name__ == "__main__":
    main()
