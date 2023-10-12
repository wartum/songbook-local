LINE, VERSE_SEPARATOR, TABLE_SEPARATOR = range(3)
MAX_PAGE_LINES = 60


class Token:
    def __init__(self, type, value):
        self.type = type

        if self.type == LINE:
            sp = value.split("::")
            self.lyrics = sp[0].strip()
            self.chords = sp[1].strip()
            self.chords = self.chords.replace("#", "\\#")
            if self.lyrics.startswith("+"):
                self.refrain = True
                self.lyrics = self.lyrics[1:]
            else:
                self.refrain = False

    def __str__(self):
        ret = "< " + str(self.type) + ", "
        if self.type == LINE:
            ret += self.lyrics + " | " + self.chords
        elif self.type == VERSE_SEPARATOR:
            ret += "NEW VERSE"
        else:
            ret += "< Unknown token >"
        ret += " >"
        return ret


class SongParser:
    def __init__(self):
        self.page_lines = 0
        self.tokens = []

    def parse_line(self, line):
        self.page_lines += 1
        line = line.strip()
        if len(line) == 0:
            self.tokens.append(Token(VERSE_SEPARATOR, line))
        elif "::" in line:
            self.tokens.append(Token(LINE, line))

        if self.page_lines > MAX_PAGE_LINES:
            self.add_table_separator()

    def add_table_separator(self):
        separators = [tk for tk in self.tokens if tk.type == VERSE_SEPARATOR]
        if len(separators) > 0:
            last_sep = separators[-1]
            last_sep.type = TABLE_SEPARATOR
            self.page_lines = len(self.tokens) - self.tokens.index(last_sep) - 1
