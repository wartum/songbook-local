from parse import LINE, VERSE_SEPARATOR, TABLE_SEPARATOR


begin_table = "\\begin{tabular}[t]{l l}\n"
end_table = "\\end{tabular}\n"


def start_song_tex(title):
    return f"\\subsection{{{title}}}\n\n"


def line_token_to_tex(tk):
    if tk.refrain is True:
        return f"    \\textbf{{{tk.lyrics}}} & {tk.chords} \\\\\n"
    else:
        return f"    {tk.lyrics} & {tk.chords} \\\\\n"


def verse_separator_token_to_tex(tk):
    return "\n    & \\\\\n\n"


def table_separator_token_to_tex(tk):
    return f"{end_table}{begin_table}"


def generate_tex(tokens, title, filepath):
    fd = open(filepath, "w")
    fd.write(start_song_tex(title))
    fd.write(begin_table)
    for tk in tokens:
        if tk.type == LINE:
            fd.write(line_token_to_tex(tk))
        elif tk.type == VERSE_SEPARATOR:
            fd.write(verse_separator_token_to_tex(tk))
        elif tk.type == TABLE_SEPARATOR:
            fd.write(table_separator_token_to_tex(tk))
    fd.write(end_table)
    fd.close()
