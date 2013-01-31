import sublime_plugin
import re


class ExtractPerVariablesCommand(sublime_plugin.TextCommand):
    VARIABLES = "[\|\[]\s*(\w*)\s*"
    REGION = "\{[\n\r]{0,2}(?:.*[\n\r]{0,2})*?\}"
    TAB_SPACES = 4

    def run(self, edit):
        reg = self.view.find_all(self.REGION)
        self.view.insert(edit, self.view.sel()[-1].end(), "ATTRIBUTES\n")
        vars = re.findall(self.VARIABLES, self.view.substr(reg[0]))
        vars = self.formatVariables(vars)
        self.view.insert(edit, self.view.sel()[-1].end(), "\n".join(vars))
        self.view.insert(edit, self.view.sel()[-1].end(), "\nEND")

    def formatVariables(self, vars):
        max_len = 0
        formatted_vars = []
        for v in vars:
            if len(v) > max_len:
                max_len = len(v)
        for v in vars:
            if len(v) < max_len:
                formatted_vars += [" " * self.TAB_SPACES + v + \
                                " " * (max_len - len(v)) + " = FORMONLY."]
            else:
                formatted_vars += [" " * self.TAB_SPACES + v + " = FORMONLY."]
        return formatted_vars
