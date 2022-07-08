from os import listdir, system
import locale

locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")
texDir = "songs/tex/"
workDir = "songs/workdir/"

def gen_songbook():
    texfiles = sorted([file for file in listdir(texDir) if file.endswith(".tex")], key=locale.strxfrm)

    inp = open("songbook.def.tex", "r", encoding='utf-8')
    out = open("songbook.tex", "w", encoding='utf-8')

    for line in inp:
        if line == '-- Songs here --\n':
            for texfile in texfiles:
                replacement = '\\input{songs/tex/' + texfile + '}\n\\newpage\n'
                out.write(replacement)
        else:
            out.write(line)


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


def create_tex(lyrics, chords, title):
    begin_document = "\\subsection{" + title + "}\n\n\\begin{tabular}{l l}\n"
    end_document = "\\end{tabular}"
    texfile = texDir + title.replace(" ","_") + ".tex"
    with open(texfile, "w", encoding='utf-8') as out:
        out.write(begin_document)
        for i in range(len(lyrics)):
            out.write(lyrics_line_to_tex(lyrics[i]))
            out.write(chords_line_to_tex(chords[i]))
        out.write(end_document)


def gen_songs():
    for file in [file for file in listdir(workDir) if file.endswith(".txt")]:
        transform_txt(file)
        lyrics = []
        chords = []
        for line in open(workDir + file, "r", encoding='utf-8').readlines():
            if '::' in line:
                lyrics.append(line.split('::')[0].strip())
                chords.append(line.split('::')[1].strip().replace('#', '\\#'))
            else:
                lyrics.append(line)
                chords.append(line)
        
        create_tex(lyrics, chords, file[:-4])


def transform_txt(file):
    lyrics = []
    chords = []

    for line in open(workDir + file, "r", encoding='utf-8').readlines():
        if '::' in line:
            lyrics.append(line.split('::')[0])
            chords.append(line.split('::')[1].strip())
        else:
            lyrics.append(line)
            chords.append(line)
            
    adjust_txt = False
    fixed_length = len(lyrics[0])
    for l in lyrics:
        if l != '\n' and len(l) != fixed_length:
            adjust_txt = True

    if adjust_txt:
        print(file)
        lyrics = [l.strip() for l in lyrics]
        max = 0
        for l in lyrics:
            if len(l) > max:
                max = len(l)
        with open(workDir + file, "w", encoding='utf-8') as f:
            for i in range(0, len(lyrics)):
                if len(lyrics[i]) == 0:
                    f.write('\n')
                else:
                    f.write(lyrics[i].ljust(max + 10, ' ') + ' :: ' + chords[i] + '\n')
    

gen_songs()
gen_songbook()

system("pdflatex songbook.tex -halt-on-error")
system("pdflatex songbook.tex -halt-on-error")
system("pdflatex songbook.tex -halt-on-error")
# system("rm *.aux")
# system("rm *.log")
# system("rm *.toc")
# system("rm *.out")
# system("aws s3 cp songbook.pdf s3://piewoj/songbook.pdf")
# system("aws s3api put-object-tagging --bucket piewoj --key songbook.pdf --tagging 'TagSet={Key=public,Value=yes}'")