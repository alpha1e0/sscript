
import sublime, sublime_plugin

import os
import subprocess



class MdToHtmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("subdone.sublime-settings")

        cmdFile = settings.get("pandoc_cmd_file")
        cmdFile = cmdFile if cmdFile else "pandoc"

        #pluginPath = sublime.packages_path()
        pluginPath = os.path.dirname(os.path.realpath(__file__))

        templateFile = settings.get("pandoc_template_file")
        if not templateFile:
            templateFile = os.path.join(pluginPath, "data", \
                "pandoc-template", "template.html")
        templateFileArg = "\"" + templateFile + "\""

        cssFile = settings.get("pandoc_css_file")
        if not cssFile:
            self._cssFile = os.path.join(pluginPath, "data", \
                "pandoc-template", "template.css")
        cssFileArg = "\"" + self._cssFile + "\""

        toc = settings.get("pandoc_toc")
        if toc:
            tocDepth = settings.get("pandoc_toc_depth")
            tocDepth = tocDepth if tocDepth else 3
            self._tocArg = "--toc --toc-depth={0}".format(tocDepth)
        else:
            self._tocArg = ""

        sourceFileName = self.view.file_name()
        sourceFileNameArg = "\"" + sourceFileName + "\""

        outputFileName = os.path.basename(sourceFileName) + ".html"
        outputPath = settings.get("pandoc_output_path")
        outputPath = outputPath if outputPath else os.path.dirname(sourceFileName)
        outputFileArg = "\"" + os.path.join(outputPath, outputFileName) + "\""

        cmd = " ".join([cmdFile, "--from markdown", "--to html", \
            "--template", templateFileArg, "--css", cssFileArg, \
            "-s --self-contained", self._tocArg, sourceFileNameArg, \
            "--output", outputFileArg])
        debug(cmd)

        try:
            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            sublime.error_message(str(err.output))

