'''
Copyright 2018 Giacomo Benso

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
 documentation files (the "Software"), to deal in the Software without restriction, including without limitation
  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
   and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies
 or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import PIL.Image
import PIL.ImageTk
import tkinter
import json
import getopt
from collections import Counter
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import httpagentparser
from graphviz import Digraph


# map continent abbreviation to continent name
continents = {'AF': 'Africa', 'AS': 'Asia', 'EU': 'Europe', 'NA': 'North America', 'SA': 'South America',
                  'OC': 'Oceania', 'AN': 'Antarctica'}

# map country abbreviation to continent abbreviation
cntry_to_cont = {'AF': 'AS', 'AX': 'EU', 'AL': 'EU', 'DZ': 'AF', 'AS': 'OC', 'AD': 'EU', 'AO': 'AF', 'AI': 'NA',
                     'AQ': 'AN', 'AG': 'NA', 'AR': 'SA', 'AM': 'AS', 'AW': 'NA', 'AU': 'OC', 'AT': 'EU', 'AZ': 'AS',
                     'BS': 'NA', 'BH': 'AS', 'BD': 'AS', 'BB': 'NA', 'BY': 'EU', 'BE': 'EU', 'BZ': 'NA', 'BJ': 'AF',
                     'BM': 'NA', 'BT': 'AS', 'BO': 'SA', 'BQ': 'NA', 'BA': 'EU', 'BW': 'AF', 'BV': 'AN', 'BR': 'SA',
                     'IO': 'AS', 'VG': 'NA', 'BN': 'AS', 'BG': 'EU', 'BF': 'AF', 'BI': 'AF', 'KH': 'AS', 'CM': 'AF',
                     'CA': 'NA', 'CV': 'AF', 'KY': 'NA', 'CF': 'AF', 'TD': 'AF', 'CL': 'SA', 'CN': 'AS', 'CX': 'AS',
                     'CC': 'AS', 'CO': 'SA', 'KM': 'AF', 'CD': 'AF', 'CG': 'AF', 'CK': 'OC', 'CR': 'NA', 'CI': 'AF',
                     'HR': 'EU', 'CU': 'NA', 'CW': 'NA', 'CY': 'AS', 'CZ': 'EU', 'DK': 'EU', 'DJ': 'AF', 'DM': 'NA',
                     'DO': 'NA', 'EC': 'SA', 'EG': 'AF', 'SV': 'NA', 'GQ': 'AF', 'ER': 'AF', 'EE': 'EU', 'ET': 'AF',
                     'FO': 'EU', 'FK': 'SA', 'FJ': 'OC', 'FI': 'EU', 'FR': 'EU', 'GF': 'SA', 'PF': 'OC', 'TF': 'AN',
                     'GA': 'AF', 'GM': 'AF', 'GE': 'AS', 'DE': 'EU', 'GH': 'AF', 'GI': 'EU', 'GR': 'EU', 'GL': 'NA',
                     'GD': 'NA', 'GP': 'NA', 'GU': 'OC', 'GT': 'NA', 'GG': 'EU', 'GN': 'AF', 'GW': 'AF', 'GY': 'SA',
                     'HT': 'NA', 'HM': 'AN', 'VA': 'EU', 'HN': 'NA', 'HK': 'AS', 'HU': 'EU', 'IS': 'EU', 'IN': 'AS',
                     'ID': 'AS', 'IR': 'AS', 'IQ': 'AS', 'IE': 'EU', 'IM': 'EU', 'IL': 'AS', 'IT': 'EU', 'JM': 'NA',
                     'JP': 'AS', 'JE': 'EU', 'JO': 'AS', 'KZ': 'AS', 'KE': 'AF', 'KI': 'OC', 'KP': 'AS', 'KR': 'AS',
                     'KW': 'AS', 'KG': 'AS', 'LA': 'AS', 'LV': 'EU', 'LB': 'AS', 'LS': 'AF', 'LR': 'AF', 'LY': 'AF',
                     'LI': 'EU', 'LT': 'EU', 'LU': 'EU', 'MO': 'AS', 'MK': 'EU', 'MG': 'AF', 'MW': 'AF', 'MY': 'AS',
                     'MV': 'AS', 'ML': 'AF', 'MT': 'EU', 'MH': 'OC', 'MQ': 'NA', 'MR': 'AF', 'MU': 'AF', 'YT': 'AF',
                     'MX': 'NA', 'FM': 'OC', 'MD': 'EU', 'MC': 'EU', 'MN': 'AS', 'ME': 'EU', 'MS': 'NA', 'MA': 'AF',
                     'MZ': 'AF', 'MM': 'AS', 'NA': 'AF', 'NR': 'OC', 'NP': 'AS', 'NL': 'EU', 'NC': 'OC', 'NZ': 'OC',
                     'NI': 'NA', 'NE': 'AF', 'NG': 'AF', 'NU': 'OC', 'NF': 'OC', 'MP': 'OC', 'NO': 'EU', 'OM': 'AS',
                     'PK': 'AS', 'PW': 'OC', 'PS': 'AS', 'PA': 'NA', 'PG': 'OC', 'PY': 'SA', 'PE': 'SA', 'PH': 'AS',
                     'PN': 'OC', 'PL': 'EU', 'PT': 'EU', 'PR': 'NA', 'QA': 'AS', 'RE': 'AF', 'RO': 'EU', 'RU': 'EU',
                     'RW': 'AF', 'BL': 'NA', 'SH': 'AF', 'KN': 'NA', 'LC': 'NA', 'MF': 'NA', 'PM': 'NA', 'VC': 'NA',
                     'WS': 'OC', 'SM': 'EU', 'ST': 'AF', 'SA': 'AS', 'SN': 'AF', 'RS': 'EU', 'SC': 'AF', 'SL': 'AF',
                     'SG': 'AS', 'SX': 'NA', 'SK': 'EU', 'SI': 'EU', 'SB': 'OC', 'SO': 'AF', 'ZA': 'AF', 'GS': 'AN',
                     'SS': 'AF', 'ES': 'EU', 'LK': 'AS', 'SD': 'AF', 'SR': 'SA', 'SJ': 'EU', 'SZ': 'AF', 'SE': 'EU',
                     'CH': 'EU', 'SY': 'AS', 'TW': 'AS', 'TJ': 'AS', 'TZ': 'AF', 'TH': 'AS', 'TL': 'AS', 'TG': 'AF',
                     'TK': 'OC', 'TO': 'OC', 'TT': 'NA', 'TN': 'AF', 'TR': 'AS', 'TM': 'AS', 'TC': 'NA', 'TV': 'OC',
                     'UG': 'AF', 'UA': 'EU', 'AE': 'AS', 'GB': 'EU', 'US': 'NA', 'UM': 'OC', 'VI': 'NA', 'UY': 'SA',
                     'UZ': 'AS', 'VU': 'OC', 'VE': 'SA', 'VN': 'AS', 'WF': 'OC', 'EH': 'AF', 'YE': 'AS', 'ZM': 'AF',
                     'ZW': 'AF'}


class ViewerException(Exception):
    """ Exception specific for the viewer class """
    def __init__(self, message):
        self.message = message


class Viewer:
    """ Class to perform all the operations on the json file """

    def __init__(self,file):
        self.location = file

    def traverse(self, searchBy, subject, *id : str):
        """
        high order function used by all the tasks.

        this function iterates through the json file and returns a list of tuples containing
        the values retrieved depending on the arguments passed.

        Paremeters
        ----------
        searchBy : string
            Key to search for in each line of the json file
        subject : string
            Key to retrieve in each line of the json file (the value will be added to the list to return)
        *id : string
            Multiple arguments, these are the values to be compared with the values of the 'searchBy' key.
            for each of the values that matches, the value of the 'subject' key is added to the list to be returned
            together with the matching value.

        Returns
        -------
        list
            A list of tuples containing the values mathced by the parameters
        """
        table = []
        with open(self.location, 'r') as fl:
            for line in fl:
                r = json.loads(line)
                #if the keys are in the line and the event is read
                if searchBy in r and subject in r and r['event_type'] == 'read':
                    for x in id: # for each of the ids passed as arguments
                        if r[searchBy] == x:
                            table.append((x,r[subject]))
        return table

    def viewBy(self, searchBy, subject, id1):
        """
        This function is a 'wrapper' function for the traverse function.

        Paremeters
        ----------
        searchBy : string
            Key to search for in each line of the json file
        subject : string
            Key to retrieve in each line of the json file (the value will be added to the list to return)
        *id : string
            this is the value to be compared with the value of the 'searchBy' key.
            if the value matches, the 'subject' key is added to the list to be returned.

        Returns
        -------
        list
            A list of containing the valuse that match the parameters
        """
        table = self.traverse(searchBy, subject, id1)
        return [x[1] for x in table] #return only first part of the tuple

    def sortByPopularity(self, arr):
        """
        This function is a sorting function.

        Paremeters
        ----------
        arr : list
            list to be sorted

        Returns
        -------
        list
            A dictionary containing the top 10 values in the list sorted by popularity
        """
        return dict(list(Counter([x[1] for x in arr]).most_common())[:10])

    def generateGraph(self, table, inputDoc, inputReader = None):
        """
        Function to generate a graphviz graph from a list.

        Paremeters
        ----------
        table : list
            list containing the data to be put into the graph
        inputDoc : string
            document passed as input, will be highlighted in green
        inputReader : string
            optional reader passed as input, will be highlighted in green

        Returns
        -------
        list
            the graph for visualization of the result
        """
        dot = Digraph(comment='Also Likes Graph')
        ids = set([x[0] for x in table])
        docs = set([x[1] for x in table])
        for x in ids:
            if(x == inputReader):
                dot.node(x, x[-4:], style='filled', fillcolor='green', shape = 'rectangle')
            else:
                dot.node(x, x[-4:], shape = 'rectangle')
        for x in docs:
            if (x == inputDoc):
                dot.node(x, x[-4:], style='filled', fillcolor='green')
            else:
                dot.node(x, x[-4:])
        for x in table:
            dot.edge(x[0],x[1])
        return dot

    def likesFun(self, documentID, readerID = None):
        """
        Function for the also-likes functionality.

        Paremeters
        ----------
        documentID: string
            the document to use as input
        readerID: string
            optional argument denoting the reader to use as input

        Returns
        -------
        set
            a set of tuples (reader,document)
        """
        hasRead = False
        table = set(self.viewBy('env_doc_id', 'visitor_uuid', documentID)) #traverse to find readers
        if readerID != None and readerID in table: #check if input reader has read the input document
            table.remove(readerID)
            hasRead = True
        tmp = set(self.traverse('visitor_uuid', 'env_doc_id', *table)) #traverse to find documents for readers
        if hasRead:
            tmp.add((readerID, documentID))
        return tmp

    def alsoLikes(self, documentID, sortingFun, readerID = None):
        """
        Also-likes functionality (task 4d).

        Paremeters
        ----------
        documentID: string
            the document to use as input
        sortingFun: function
            function to use to sort the result
        readerID: string
            optional argument denoting the reader to use as input

        Returns
        -------
        dictionary
            A dictionary containing the valuse in the list sorted by the sorting function
        """
        tmp = self.likesFun(documentID, readerID)
        docs = [x for x in tmp if x[1] != documentID] #remove input document
        return sortingFun(docs)

    def alsoLikesGraph(self, documentID, readerID = None):
        """
        Also-likes functionality with graph generation (task 5).

        Paremeters
        ----------
        documentID: string
            the document to use as input
        readerID: string
            optional argument denoting the reader to use as input

        Returns
        -------
        set
            the graph generated by the generateGraph function
        """
        tmp = self.likesFun(documentID, readerID)
        return self.generateGraph(tmp, documentID, readerID) #create graph

    def produceOutput(self, type, id, rd = None):
        """
        Function used to retreive the correct task depending on the parameter passed.

        Paremeters
        ----------
        type: string
            the task number to be performed
        id: string
            the 'id' to be used to search in the json file
        rd: string
            the optional 'id' to be used to search in the json file (needed for the optional reader)

        Returns
        -------
        dictionary
            the result of the search in the json file performed by the function corresponding to the task
        """
        if type == '2a':
            return Counter(self.viewBy('env_doc_id', 'visitor_country', id))
        elif type == '3a':
            return Counter(self.viewBy('env_doc_id', 'visitor_useragent', id))
        elif type == '2b':
            table = self.viewBy('env_doc_id','visitor_country', id)
            return Counter([continents.get(cntry_to_cont.get(x)) for x in table])
        elif type == '3b':
            table = self.viewBy('env_doc_id', 'visitor_useragent', id)
            return Counter([httpagentparser.detect(x)['browser']['name'] for x in table]) #httpagentparser
        elif type == '4d':
            return dict(self.alsoLikes(id, self.sortByPopularity, rd))
        elif type == '4ds': #4d returning last 4 of docIDS (radability purposes)
            return dict([(x[-4:], y) for (x, y) in self.alsoLikes(id, self.sortByPopularity, rd).items()])
        elif type == '5':
            return self.alsoLikesGraph(id, rd)
        else:
            raise ViewerException('Task ' + type + ' undefined')


class MainPage(tkinter.Frame):
    """ GUI class """

    def __init__(self, fileName, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.viewer = Viewer(fileName)

        self.radioButtonValue = StringVar()
        self.radioButtonValue.set('2a')

        # figure for histograms
        self.fig = Figure(figsize=(4, 4), dpi=100)
        self.subplot = self.fig.add_subplot(111)
        self.subplot.bar([], [], color='g')
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=YES)

        #canvas for png graph
        self.canvas2 = Canvas(self)

        self.fm0 = Frame(self)
        self.fm1 = Frame(self.fm0)
        self.fmHidden = Frame(self.fm0)
        self.label = Label(self.fm1, text="Document UUID:")
        self.label.pack(side=tkinter.TOP, fill=tkinter.BOTH, padx=10, pady=10)
        self.textbox = Entry(self.fm1)
        self.textbox.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=YES, padx=5)
        self.fm1.pack(side=tkinter.LEFT, expand=YES,fill=tkinter.BOTH)

        self.label2 = Label(self.fmHidden, text="Optional Reader UUID:")
        self.label2.pack(side=tkinter.TOP, fill=tkinter.BOTH, padx=10, pady=10)
        self.textbox2 = Entry(self.fmHidden)
        self.textbox2.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=YES, padx=5)

        self.fmButton = Frame(self.fm0)
        self.visualButton = Button(self.fmButton, fg="black", text="Visualise",
                                   command = lambda :self.visualiseContent(self.textbox.get(), self.radioButtonValue.get()))
        self.visualButton.pack(side=tkinter.BOTTOM, pady=5, padx=10)
        self.fmButton.pack(side=tkinter.RIGHT,fill=tkinter.BOTH)
        self.fm0.pack(side=tkinter.TOP, fill=tkinter.BOTH, padx=10)

        self.labelRadio = Label(self, text="About the Document:")
        self.labelRadio.pack(side=tkinter.TOP, fill=tkinter.BOTH, padx=(0,75), pady=10)

        # Radiobuttons
        self.fm2 = Frame(self)
        self.byCountry = Radiobutton(self.fm2, text="Visitors by Country", variable = self.radioButtonValue,
                                     value='2a', command = lambda : self.secondTextBox())
        self.byCountry.pack(side=tkinter.LEFT, padx=5)
        self.byContinent = Radiobutton(self.fm2, text="Visitors by Continent", variable = self.radioButtonValue,
                                       value='2b', command = lambda : self.secondTextBox())
        self.byContinent.pack(side=tkinter.LEFT, padx=5)
        self.byBrowserString = Radiobutton(self.fm2, text="Visitors by Browser-extended", variable=self.radioButtonValue,
                                           value='3a', command = lambda : self.secondTextBox())
        self.byBrowserString.pack(side=tkinter.LEFT, padx=5)
        self.fm2.pack(side=tkinter.TOP, padx=(0,75))
        self.fm3 = Frame(self)
        self.byBrowser = Radiobutton(self.fm3, text="Visitors by Browser", variable=self.radioButtonValue,
                                     value='3b',command = lambda : self.secondTextBox())
        self.byBrowser.pack(side=tkinter.LEFT, padx=5)
        self.alsoLikes = Radiobutton(self.fm3, text="Also-Liked Documents", variable=self.radioButtonValue,
                                     value='4ds', command = lambda : self.secondTextBox())
        self.alsoLikes.pack(side=tkinter.LEFT, padx=5)
        self.alsoLikesGraph = Radiobutton(self.fm3, text="Also-Liked Documents Graph", variable=self.radioButtonValue,
                                          value='5', command=lambda: self.secondTextBox())
        self.alsoLikesGraph.pack(side=tkinter.LEFT, padx=5)
        self.fm3.pack(side=tkinter.TOP, padx=(0,75))

    def secondTextBox(self):
        """ hide or show the optional readerID entry textbox """
        if self.radioButtonValue.get() == '4ds' or self.radioButtonValue.get() == '5' :
            self.fmHidden.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=YES)
        else:
            self.fmHidden.pack_forget()

    def visualiseContent(self, documentID : str, value):
        """
        Visualise the result of the functions performed by the viewr in the GUI.

        Paremeters
        ----------
        documentID: string
            the document id to be passed as input to the json file
        value: string
            the task number
        """
        if len(documentID.strip()) != 0:
            if len(self.textbox2.get().strip()) != 0 : # if we have a readerID
                diction = self.viewer.produceOutput(value, documentID.strip(), self.textbox2.get().strip())
            else:
                diction = self.viewer.produceOutput(value, documentID.strip())
            if isinstance(diction, dict):
                self.canvas2.pack_forget() #if png graph is packed, unpack it
                self.canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=YES)
                self.subplot.clear()
                self.subplot.bar(list(diction.keys()), diction.values(), color='g')
                self.canvas.draw()
            else:
                diction.format = 'png' # change output to png
                diction.render('alsolikes.dot')
                self.canvas.get_tk_widget().pack_forget() # if histogram is packed, unpack it
                self.img = PIL.ImageTk.PhotoImage(PIL.Image.open("alsolikes.dot.png")) #embed png graph in GUI
                self.canvas2.configure(height=self.img.height(), width=self.img.width())
                self.canvas2.create_image(0, 0, anchor="nw",image=self.img)
                self.canvas2.pack(side=tkinter.BOTTOM, pady=(0, 80), expand=YES, )
        else:
            print("Invalid Input")


if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "gu:d:t:f:") #get the arguments
    except getopt.GetoptError:
        print('usage: <program -u user_uuid -d doc_uuid -t task_id -f file_name>')
        print('or <program -g -f file_name>')
        sys.exit(2)

    #variables needed (command line arguments)
    graphic = False
    filename = userID = docID = task = None

    for opt, arg in opts: # check which arguments are passed
        if opt == '-g':
           graphic = True
        elif opt == '-f':
            filename = arg
        elif opt == '-u':
            userID = arg
        elif opt == '-d':
            docID = arg
        elif opt == '-t':
            task = arg

    if filename is not None and filename[-5:] == '.json': #check string finishes with ".json"
        try:
            if graphic == True: # use GUI
                root = Tk()
                root.geometry('850x600')
                root.title("Visualisator")
                myGUI = MainPage(filename, root).pack(side="top", fill="both", expand=True)
                root.mainloop()
            elif docID is not None and task is not None: # use command line
                try:
                    viewer = Viewer(filename)
                    if task == '2a' or task == '2b' or task == '3a' or task == '3b' or task == '4d':
                        tmp = viewer.produceOutput(task, docID, userID)
                        print(docID + " --> " + str(dict(tmp)))
                    else:
                        dot = viewer.produceOutput(task, docID, userID)
                        dot.format = 'ps'
                        dot.render('alsolikes.dot') #try view true?
                        print('graph generated in .dot and .ps in the current folder')
                except ViewerException as e:
                    print (e.message)
                    print("Task must be 2a, 2b, 3a, 3b, 4d or 5")
                    sys.exit(2)
            else:
                print('usage: program -u user_uuid -d doc_uuid -t task_id -f file_name')
                print("doc_uuid and task_id are needed")
                sys.exit(2)
        except IOError:
            print(filename + " Not Found!")
            sys.exit(2)
    else:
        print('usage: program -u user_uuid -d doc_uuid -t task_id -f file_name')
        print("file_name must be a valid json file")
        sys.exit(2)