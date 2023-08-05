import wx
import pandas as pd
from unidec.modules.isolated_packages.spreadsheet import *
from unidec.batch import UniDecBatchProcessor as BPEngine
from unidec.batch import *
from unidec.modules.html_writer import *


class HelpDlg(wx.Frame):
    def __init__(self, num=1, *args, **kw):
        super().__init__(*args, **kw)
        pathtofile = os.path.dirname(os.path.abspath(__file__))
        self.imagepath = os.path.join(pathtofile, "images")
        # print(pathtofile)
        # print(self.imagepath)
        if num == 1:
            self.help_frame()
        else:
            html = wx.html.HtmlWindow(self)
            html.SetPage("<html><body>You shouldn't see this!!! ERROR!!!!</body></html>")

    def help_frame(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title="Help", size=(600, 600))
        html = wx.html.HtmlWindow(self)

        html_str = "<html><body>" \
                   "<h1>Overview</h1><p>" \
                   "Welcome to the UniDec Processing Pipeline (UPP)! " \
                   "This module is designed to help you process, deconvolve, " \
                   "and extract specific information from your data. " \
                   "Expanding on the batch processing features present in UniDec from the beginning, " \
                   "it is designed to interface with Excel/CSV files so that you can connect it with your workflows. " \
                   "</p>" \
                   "<h2>Basic Features</h2> <h3>Opening A File</h3><p>" \
                   "Although you can type everything directly into UPP, " \
                   "we recommend you start by importing your information from " \
                   "an Excel/CSV file. " \
                   "After you have your file ready, you can open it by clicking the" \
                   " \"File > Open File\" button and selecting your file. " \
                   "You can also open a file by dragging and dropping it onto the window. " \
                   "After opening the file, you should see it populate the main window like a spreadsheet.</p>" \
                   "<h3>What Do You Need In the Spreadsheet?</h3>" \
                   "<p>All you need is to specify the \"Sample name\" column with the file path. " \
                   "However, there are other optional parameters that you can specifiy.</p>"

        html_str += array_to_html(basic_parameters, cols=["Parameter", "Required", "Description"], rows=None,
                                  colors=None, index=False)

        html_str += "<h3>Running UPP</h3><p>" \
                    "After you have opened your file, you can run UPP by clicking the \"Run\" button.</p> " \
                    "<p>There are two options to select to speed up the deconvolution and processing. " \
                    "The first is to use the already converted data. " \
                    "If you have already converted and averaged the data into a single spectrum," \
                    " you can select this option to skip the conversion step " \
                    "and speed up the program while you optimize the deconvolution.</p><p>" \
                    "The second option is to run the deconvolution engine. " \
                    "If you have already run the deconvolution engine on your data, " \
                    "you can select this option to skip the deconvolution step and speed up the program. " \
                    "This option is most useful if you have already deconvolved the data" \
                    " and want to adjust the peak matching or analysis.</p> "

        html_str += "<h3>Outputs</h3> <p>" \
                    "After running UPP, there are two key outputs. " \
                    "First, you will see one or more new tabs appear in the main window. " \
                    "These tabs will contain the results of the deconvolution and analysis. " \
                    "The results are saved to a \"results.xlsx\" file.</p> " \
                    "<p>Second, each deconvolution will generate an HTML reports that will be saved" \
                    " in the same directory as your data file in the _unidecfiles folder. " \
                    "You can open these reports in a web browser by clicking the \"Open All HTML Reports\" button. " \
                    "You can also open individual files by double clicking on individual cells.</p> "

        html_str += "<h3>Adjusting the Deconvolution Parameters</h3> <p>" \
                    "UPP will use the default UniDec parameters for deconvolution. " \
                    "However, you can adjust the deconvolution parameters " \
                    "by adding these optional rows in the spreadsheet: </p> "

        html_str += array_to_html(config_parameters, cols=["Parameter", "Required", "Description"], rows=None,
                                  colors=None, index=False)

        html_str += "<h2>Advanced Features</h2> <h3>Developing Workflows</h3><p>" \
                    "After you deconvolve your data, there are lots of things you can do with it. " \
                    "Because UPP is free and open-source, you can write in new functions and features " \
                    "that are customized for your workflow.</p> <p>For example, you could read in a column " \
                    "for \"Candidate Mass\" and search the peaks to if it is present. " \
                    "Take a look at the batch.py file on GitHub for ideas." \
                    "</p> <p>If you have new ideas for recipes, feel free to reach out for help. " \
                    "We are happy to help you develop your own recipes and workflows.</p> "

        html_str += "<h3>An Example Workflow: Check Correct Pairing</h3><p>" \
                    "Here is an example recipe that checks if the correct pairing of protein sequences is present. " \
                    "The column keyword of \"Sequence {n}\" defines a protein sequence " \
                    "were {n} is a number, such as \"Sequence 1\". " \
                    "Each sequence cell should give the amino acid sequence of the protein chain. </p> <p> " \
                    "Another key column is \"Correct{anything}\". UPP will look for a column with \"Correct\" in it. " \
                    "The \"Correct\" column should contain the correct pairing of the protein sequences. " \
                    "For example, if you have two protein sequences, \"Sequence 1\" and \"Sequence 2\", " \
                    "the \"Correct\" column should contain the pairing of the" \
                    " two sequences written as: \"Seq1+Seq2\". " \
                    "You can also other columns like \"Homodimer\" as a column header " \
                    "with similar definitions (Seq2+Seq2 for example) " \
                    "and UPP will check if the incorrect pairing is present. </p> <p> " \
                    "Finally, you can specify a Mod File to list potential sequence " \
                    "modifications (see more info below) and a \"Tolerance\" to specify the peak matching tolerance. " \
                    "Using all this information, the workflow will then search for the correct" \
                    " and incorrectly paired masses in the deconvolution results (with any possible modifications). " \
                    "If the correct pairing is present, it will color the peak green. " \
                    "If the incorrect pairing is present, it will color the peak red. " \
                    "If neither pairing is present (unknown), it will color the peak yellow. </p> <p> " \
                    "The final results spreadsheet will contain the percentage of the signal " \
                    "that is correct, incorrect, and unknown." \
                    "It will also give the percentage of correct and incorrect after ignoring the unknown. " \
                    "Additional details on keywords are provided below. "

        html_str += array_to_html(recipe_w, cols=["Parameter", "Required", "Description"], rows=None,
                                  colors=None, index=False)

        html_str += "</body></html>"

        html.SetPage(html_str)


class UPPApp(wx.Frame):
    """"""

    def __init__(self, nrows=2, ncolumns=2, title="UniDec Processing Pipeline"):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title=title, size=(1800, 600))
        self.use_decon = True
        self.use_converted = True
        self.bpeng = BPEngine()

        menu = wx.Menu()
        # Open File Menu
        open_file_menu_item = menu.Append(wx.ID_ANY, "Open File", "Open a CSV or Excel file")
        self.Bind(wx.EVT_MENU, self.on_load_file, open_file_menu_item)

        help_menu = wx.Menu()
        # Open File Menu
        help_manu_item = help_menu.Append(wx.ID_ANY, "Help Me!", "Open a help page")
        self.Bind(wx.EVT_MENU, self.on_help_page, help_manu_item)

        # Create the menubar
        menuBar = wx.MenuBar()
        menuBar.Append(menu, "&File")
        menuBar.Append(help_menu, "&Help")
        self.SetMenuBar(menuBar)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # Insert a button and bind it with a handler called on_run
        btn = wx.Button(panel, label="Run")
        btn.Bind(wx.EVT_BUTTON, self.on_run)
        hsizer.Add(btn, 0)

        # Insert a button for Open All HTML Reports and bind to function
        btn = wx.Button(panel, label="Open All HTML Reports")
        btn.Bind(wx.EVT_BUTTON, self.on_open_all_html)
        hsizer.Add(btn, 0)

        # Insert a static text of directory
        # hsizer.Add(wx.StaticText(panel, label="   Data Directory:", style=wx.ALIGN_CENTER_VERTICAL))
        # Insert a text box to read out the directory
        # self.dirtxtbox = wx.TextCtrl(panel, size=(400, -1))
        # hsizer.Add(self.dirtxtbox, 0, wx.EXPAND)
        # Add a button to set the directory
        # btn = wx.Button(panel, label="...")

        # Insert a static text of tolerance
        # hsizer.Add(wx.StaticText(panel, label="   Tolerance:", style=wx.ALIGN_CENTER_VERTICAL))
        # Insert a text box to read out the directory
        # self.tolbox = wx.TextCtrl(panel, size=(50, -1))
        # self.tolbox.SetValue("50")
        # hsizer.Add(self.tolbox, 0, wx.EXPAND)
        # hsizer.Add(wx.StaticText(panel, label="Da   ", style=wx.ALIGN_CENTER_VERTICAL))

        # Insert a checkbox to select whether to use already converted data
        self.useconvbox = wx.CheckBox(panel, label="Use Converted Data")
        hsizer.Add(self.useconvbox, 0, wx.EXPAND)
        self.useconvbox.SetValue(self.use_converted)

        # Insert a checkbox to select whether to use already deconvolved data
        self.usedeconbox = wx.CheckBox(panel, label="Deconvolve Data")
        hsizer.Add(self.usedeconbox, 0, wx.EXPAND)
        self.usedeconbox.SetValue(self.use_decon)

        sizer.Add(hsizer, 0, wx.ALL | wx.EXPAND)

        self.ss = SpreadsheetPanel(self, panel, nrows, ncolumns).ss
        self.ss.set_col_headers(["Sample name", "Data Directory"])
        sizer.Add(self.ss, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        self.Show()

    def on_run(self, event=None):
        print("Run button pressed")
        self.get_from_gui()
        self.bpeng.run_df(decon=self.use_decon, use_converted=self.use_converted)
        self.ss.set_df(self.bpeng.rundf)

    def load_file(self, filename):
        print("Loading File:", filename)
        self.bpeng.top_dir = os.path.dirname(filename)
        df = file_to_df(filename)
        self.ss.set_df(df)
        # dirname = os.path.dirname(filename)
        # self.set_dir_tet_box(dirname)

    def on_load_file(self, event):
        print("Load button pressed")
        # Create a file dialog
        with wx.FileDialog(self, "Open CSV or Excel File",
                           wildcard="CSV or Excel files (*.csv; *.xlsx; *.xls)|*.csv; *.xlsx; *.xls|"
                                    "CSV files (*.csv)|*.csv|"
                                    "Excel files (*.xlsx; *.xls)|*.xlsx; *.xls",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            # Show the dialog and retrieve the user response. If it is the OK response,
            # process the data.
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.load_file(pathname)

    # def set_dir_tet_box(self, dirname):
    #    self.dirtxtbox.SetValue(dirname)

    def get_from_gui(self):
        self.use_converted = self.useconvbox.GetValue()
        self.use_decon = self.usedeconbox.GetValue()

        # dirname = self.dirtxtbox.GetValue()
        # tol = self.tolbox.GetValue()
        # self.bpeng.data_dir = dirname
        # try:
        #    self.bpeng.tolerance = float(tol)
        # except Exception as e:
        #    print("Error with Tolerance Value. Using default value of 50 Da", e)
        #    self.bpeng.tolerance = 10
        #    self.tolbox.SetValue("10")

        self.ss.remove_empty()
        ssdf = self.ss.get_df()
        self.bpeng.rundf = ssdf

    def on_open_all_html(self, event):
        print("Open All HTML Reports button pressed")
        self.bpeng.open_all_html()

    def open_unidec(self, row):
        print("Opening in UniDec:", row)

    def on_help_page(self, event=None):
        print("Help button pressed")
        dlg = HelpDlg()
        dlg.Show()

    def on_exit(self, event=None):
        self.Close()


if __name__ == "__main__":
    app = wx.App()
    frame = UPPApp()
    frame.usedeconbox.SetValue(False)
    path = "C:\\Data\\Wilson_Genentech\\sequences_short.xlsx"

    frame.on_help_page()
    # exit()
    if False:
        frame.load_file(path)
        # frame.set_dir_tet_box("C:\\Data\\Wilson_Genentech\\Data")
        # print(df)
        frame.on_run()

    app.MainLoop()
