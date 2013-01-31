import sublime_plugin
import sublime
import hashlib
import re
import datetime


class CreateContentsCommand(sublime_plugin.TextCommand):
    '''
    This plugin will scan the current view for function names,
    add an md5 sum on the next line after the function name
    and create a table of contents on the line where
    the cursor is placed.

    You need to set three variables to make this work with
    your language:
    1. CONTENTS is the title of the table of contents;
    2. FUNCTION_REGEXP is the regexp that will find your functions
                (note that the part that you want to show up
                on the table of contents and that will be used
                to make the md5 hash should be enclosed in brackets);
    3. COMMENT is a string, consisting of a symbol that is used for
                one line comments in your language.

    The code assumes that the cursor is placed on a blank line
    and that the CONTENTS and COMMENT variables do not contain
    any special characters that you would need to escape in a regexp.
    '''
    CONTENTS = "OBSAH"
    FUNCTION_REGEXP = "^#*\s*?FUNCTION\s*(.*?)\(.*"
    COMMENT = "#"

    def run(self, edit):
        self.cont_dict = {}
        id = 0
        regions = self.view.find_all(self.FUNCTION_REGEXP, sublime.IGNORECASE)
        for r in reversed(regions):
            try:
                found = re.search(self.FUNCTION_REGEXP, self.view.substr(r)).group(1)
                md = self.calculate_md5(found)
                self.cont_dict[id] = [found, md]
                id += 1
                self.insert_md5_undoubled(r, md)
            except AttributeError:
                pass
        self.delete_contents()
        self.insert_contents_tabbed(self.cont_dict)

    def insert_contents_tabbed(self, contents):
        max_len = 0
        for li in contents:
            if len(contents[li][0]) > max_len:
                max_len = len(contents[li][0])
        for li in contents:
            if len(contents[li][0]) < max_len:
                contents[li] = [contents[li][0] + (" ") * (max_len - len(contents[li][0])), contents[li][1]]
        edit = self.view.begin_edit()
        try:
            self.view.insert(edit, self.view.sel()[-1].end(), self.COMMENT + " " + self.CONTENTS + " (%s):\n" % datetime.datetime.now().strftime("%Y-%m-%d"))
            for i in range(len(contents) - 1, -1, -1):
                self.view.insert(edit, self.view.sel()[-1].end(), self.COMMENT + " " + contents[i][0] + " " + contents[i][1] + "\n")
        finally:
            self.view.end_edit(edit)

    def insert_md5_undoubled(self, region, md):
        if not self.view.find_all("^" + self.COMMENT + "\s" + md, sublime.IGNORECASE):
            edit = self.view.begin_edit()
            try:
                self.view.insert(edit, region.end(), "\n" + self.COMMENT + " " + md)
            finally:
                self.view.end_edit(edit)

    def calculate_md5(self, st):
        return hashlib.md5(st.encode('utf8')).hexdigest()

    def delete_contents(self):
        to_delete = self.view.find_all("^" + self.COMMENT + " " + self.CONTENTS + " \(\d{4}-\d{2}-\d{2}\):[\n\r]{1,2}(?:^" + self.COMMENT + "\s\w+\s+\w+[\n\r]{1,2})*")
        if to_delete:
            edit = self.view.begin_edit()
            try:
                for r in to_delete:
                    self.view.erase(edit, r)
            finally:
                self.view.end_edit(edit)
