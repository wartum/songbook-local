from parse import LINE, VERSE_SEPARATOR, TABLE_SEPARATOR

MAX_PAGE_LINES = 60


def generate_tex(tokens, title, filepath):
    with open(filepath, "w") as out:
        generate_single_column_tex(tokens, title, out)


def find_page_separators(tokens):
    if len(tokens) <= MAX_PAGE_LINES:
        return

    verse_separators = []
    for i in range(len(tokens)):
        if tokens[i].type == VERSE_SEPARATOR:
            tup = (tokens[i], i)
            verse_separators.append(tup)

    previous_s = verse_separators[0]
    for s in verse_separators[1:]:
        if s[1] >= MAX_PAGE_LINES:
            previous_s[0].type = TABLE_SEPARATOR
            break
        previous_s = s


def generate_single_column_tex(tokens, title, fd):
    find_page_separators(tokens)
    fd.write(f"\\subsection{{{title}}}\n\n")
    fd.write("\\begin{tabular}[t]{l l}\n")
    for tk in tokens:
        if tk.type == LINE:
            if tk.refrain is True:
                fd.write(f"    \\textbf{{{tk.lyrics}}} & {tk.chords} \\\\\n")
            else:
                fd.write(f"    {tk.lyrics} & {tk.chords} \\\\\n")
        elif tk.type == VERSE_SEPARATOR:
            fd.write("\n    & \\\\\n\n")
        elif tk.type == TABLE_SEPARATOR:
            fd.write("\\end{tabular}\n\\begin{tabular}[t]{l l}\n")
    fd.write("\\end{tabular}")
