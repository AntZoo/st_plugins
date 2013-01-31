import datetime
import sublime_plugin


class AddDateStampCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_snippet",\
        {"contents": "%s" % datetime.date.today().strftime("%Y-%m-%d")})


class AddTimeStampCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_snippet",\
        {"contents": "%s" % datetime.datetime.now().strftime("%H:%M")})


class AddDateTimeStampCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_snippet",\
        {"contents": "%s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})


class AddDatedCommentCommand(sublime_plugin.TextCommand):
    USER = "zue"
    COMMENT = "#"

    def run(self, edit):
        self.view.run_command("insert_snippet",\
        {"contents": self.COMMENT + " %s | " + self.USER + ": " % datetime.datetime.now().strftime("%Y-%m-%d")})
