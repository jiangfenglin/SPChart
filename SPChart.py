import os
import wx
import wx.lib.filebrowsebutton as filebrowse
import wx.grid
import wx.lib.buttons as buttons
#import wx.lib.plot as plot
#from matplotlib.backends import backend_wxagg     
#from matplotlib.figure import Figure   
import matplotlib
matplotlib.use("WXAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
from matplotlib.lines import Line2D
import matplotlib.colors as colors
from matplotlib.collections import LineCollection
import Splib as splib


#File menu
IDM_OpenFile = wx.NewId()

#Char menu
IDM_ZSmith =  wx.NewId()
IDM_YSmith =  wx.NewId()
IDM_Polar = wx.NewId()
IDM_LogMag = wx.NewId()
IDM_Numeric =  wx.NewId()


#Function menu
IDM_TDR = wx.NewId()
IDM_Phase =wx.NewId()
IDM_MixMode = wx.NewId()


#Curve Menu
IDM_AllOn = wx.NewId()
IDM_AllOff = wx.NewId()
IDM_Reflections = wx.NewId() 
IDM_Transmissions = wx.NewId()
IDM_Isolations = wx.NewId()
IDM_CustomCurve = wx.NewId()

#Options Menu
IDM_ChartSetting = wx.NewId()


#Help Menu
IDM_Content = wx.NewId()
IDM_About = wx.NewId()



class MyFrame(wx.MDIParentFrame):
    def __init__(self, *args, **kwargs):
        wx.MDIParentFrame.__init__(self, *args, **kwargs)
        self.SetIcon(wx.Icon("icons/icon.ico",wx.BITMAP_TYPE_ICO))
        self.Maximize()
        self.CreateMenuBar()
        self.CreateTopToolBar()
        self.statusBar = self.CreateStatusBar()
        self.BindEvents()

    def CreateMenuBar(self):
        #File Menu
        menu_File = wx.Menu()
        menu_File.Append(IDM_OpenFile,"&Open\tCtrl-O","Open File")

        #Chart Menu
        menu_Chart = wx.Menu()

        #item = wx.MenuItem(menu_Chart,IDM_ZSmith,"Z Smith","Z Smith")
        #item.SetBitmap(wx.Bitmap("icons/ZSmith.png",wx.BITMAP_TYPE_PNG))
        #menu_Chart.AppendItem(item)

        #item = wx.MenuItem(menu_Chart,IDM_YSmith,"Y Smith","Y Smith")
        #item.SetBitmap(wx.Bitmap("icons/YSmith.png",wx.BITMAP_TYPE_PNG))
        #menu_Chart.AppendItem(item)

        #item = wx.MenuItem(menu_Chart,IDM_Polar,"Polar","Polar")
        #item.SetBitmap(wx.Bitmap("icons/Polar.png",wx.BITMAP_TYPE_PNG))
        #menu_Chart.AppendItem(item)

        item = wx.MenuItem(menu_Chart,IDM_LogMag,"Log Mag","Log Mag")
        item.SetBitmap(wx.Bitmap("icons/LogMag.png",wx.BITMAP_TYPE_PNG))
        menu_Chart.AppendItem(item)
        
        item = wx.MenuItem(menu_Chart,IDM_Numeric,"Numeric","Numeric")
        item.SetBitmap(wx.Bitmap("icons/Numeric.png",wx.BITMAP_TYPE_PNG))
        menu_Chart.AppendItem(item)


        #Menu Function
        menu_Function =  wx.Menu()
        menu_Function.Append(IDM_MixMode,"MixMode","MixMode")
        menu_Function.Append(IDM_TDR,"TDR","TDR")
        menu_Function.Append(IDM_Phase,"Phase","Phase")

        #Curve Menu
        menu_Curve = wx.Menu()
        item = wx.MenuItem(menu_Chart,IDM_AllOn,"All On","All On")
        item.SetBitmap(wx.Bitmap("icons/AllOn.png",wx.BITMAP_TYPE_PNG))
        menu_Curve.AppendItem(item)        

        item = wx.MenuItem(menu_Chart,IDM_AllOff,"All Off","All Off")
        item.SetBitmap(wx.Bitmap("icons/AllOff.png",wx.BITMAP_TYPE_PNG))
        menu_Curve.AppendItem(item)        


        item = wx.MenuItem(menu_Chart,IDM_Reflections,"Reflections","Reflections")
        item.SetBitmap(wx.Bitmap("icons/Reflections.png",wx.BITMAP_TYPE_PNG))
        menu_Curve.AppendItem(item)        

        item = wx.MenuItem(menu_Chart,IDM_Transmissions,"Transmissions","Transmissions")
        item.SetBitmap(wx.Bitmap("icons/Transmissions.png",wx.BITMAP_TYPE_PNG))
        menu_Curve.AppendItem(item)        

        item = wx.MenuItem(menu_Chart,IDM_Isolations,"Isolations","Isolations")
        item.SetBitmap(wx.Bitmap("icons/Isolations.png",wx.BITMAP_TYPE_PNG))
        menu_Curve.AppendItem(item)        

        item = wx.MenuItem(menu_Chart,IDM_CustomCurve,"Custom Curve","Custom Curve")
        item.SetBitmap(wx.Bitmap("icons/CustomCurve.png",wx.BITMAP_TYPE_PNG))
        menu_Curve.AppendItem(item)  
        

        
        #Options Menu
        menu_Options =  wx.Menu()
        menu_Options.Append(IDM_ChartSetting,"ChartSetting","ChartSetting")

        #Help Menu
        menu_Help =  wx.Menu()
        menu_Help.Append(IDM_Content,"Content","Content")
        menu_Help.Append(IDM_About,"About","About")


        #Menu bar 
        menuBar = wx.MenuBar()
        menuBar.Append(menu_File, "F&ile")
        menuBar.Append(menu_Chart, "&Chart")
        menuBar.Append(menu_Function, "&Function")
        menuBar.Append(menu_Curve, "C&urve")
        menuBar.Append(menu_Options, "&Options")
        menuBar.Append(menu_Help, "&Help")
    
        self.SetMenuBar(menuBar)
        


    def CreateTopToolBar(self):
        tb = self.CreateToolBar() 
        tb.AddSimpleTool(IDM_OpenFile, wx.Bitmap("icons/FileOpen.ico",wx.BITMAP_TYPE_ICO), "Open File","Open a file")
        tb.AddSeparator()
        
        tb.AddSimpleTool(IDM_CustomCurve, wx.Bitmap("icons/CustomCurve.png",wx.BITMAP_TYPE_PNG), "Custom Curve","Custom Curve")
        tb.AddSeparator()

        tb.AddSimpleTool(IDM_MixMode, wx.Bitmap("icons/MixMode.png",wx.BITMAP_TYPE_PNG), "Mix Mode","Mix Mode")

        tb.Realize()
        #pass
    def BindEvents(self):
        
        self.Bind(wx.EVT_MENU, self.OnOpenFile, id = IDM_OpenFile)
        self.Bind(wx.EVT_MENU, self.OnPhase, id = IDM_Phase)
        self.Bind(wx.EVT_MENU, self.OnAllOn, id = IDM_AllOn)
        self.Bind(wx.EVT_MENU, self.OnAllOff, id = IDM_AllOff)
        self.Bind(wx.EVT_MENU, self.OnReflections, id = IDM_Reflections)
        self.Bind(wx.EVT_MENU, self.OnTransmission, id = IDM_Transmissions)
        self.Bind(wx.EVT_MENU, self.OnIsolations, id = IDM_Isolations)
        self.Bind(wx.EVT_MENU, self.OnChartSetting, id = IDM_ChartSetting)
        self.Bind(wx.EVT_MENU, self.OnChartSetting, id = IDM_CustomCurve)
        self.Bind(wx.EVT_MENU, self.OnMixMode, id =IDM_MixMode)
        self.Bind(wx.EVT_MENU, self.OnContent, id =IDM_Content)
        self.Bind(wx.EVT_MENU, self.OnAbout, id =IDM_About)


    def OnOpenFile(self,event):
        filepath = wx.FileSelector("Open SnP file", default_path="", 
                default_filename="", default_extension="",
                wildcard="All files (*.*)|*.*",
               flags=0, parent=None,x=-1, y=-1)        
        if filepath:
            #win = SubFrame(self, -1, filepath)
            spara = splib.SPara(filepath)
            win = SeCanvesFrame(self, -1, filepath,dim=spara.GetDimension(),data=spara.GetdBSe())



    def OnPhase(self,event):
        subframe = self.GetActiveChild()
        if subframe is not None:
            #subframe.ClearCurve()
            filepath = subframe.GetTitle()
            spara = splib.SPara(filepath)
            axes_label = ["%s - Phase" %filepath,"Frequency(GHz)","Angle(deg)"]
            win = SeCanvesFrame(self, -1, filepath,spara.GetDimension(),spara.GetAngSe(),axes_label)

    def OnAllOff(self,event):
        subframe = self.GetActiveChild()
        if subframe is not None:
            subframe.ClearCurve()

    def OnAllOn(self,event):
        subframe = self.GetActiveChild()
        if subframe is not None:
            subframe.DrawAllCurve()
    
    def OnReflections(self,event):
        subframe = self.GetActiveChild()
        if subframe is not None:
            subframe.DrawReflectionCurve()

    def OnTransmission(self,event):
        subframe = self.GetActiveChild()
        if subframe is not None:
            subframe.DrawTransmissionCurve()

    def OnIsolations(self,event):
        subframe = self.GetActiveChild()
        if subframe is not None:
            subframe.DrawIsolationCurve()


    def OnChartSetting(self,event):
        #print event.GetId()
        #print IDM_CustomCurve,IDM_ChartSetting
        subframe = self.GetActiveChild()
        if subframe is not None:
            #dim = int(os.path.splitext(subframe.GetTitle())[-1][2:-1])
            dim = subframe.dim
            mod = subframe.mod
            #splist = subframe.axes.get_legend_handles_labels()[1] 

        
            dlg  = ChartSetting(self,-1,"Chart Setting",size= (400,300),dim=dim,mod=mod)
            dlg.CenterOnParent()
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                splist = dlg.GetValue()
                subframe.DrawCurve(splist)
            dlg.Destroy()

    def OnMixMode(self,event):
        dlg  = MixModeDlg(self,-1,"Mixed mode S-paramters")
        dlg.CenterOnParent()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            #print dlg.GetChartType()
            portmap = dlg.GetPortMap()
            splist =  dlg.GetCurveList()
            filepath = dlg.GetFilepath()
            
            spara = splib.SPara(filepath)
            if dlg.GetChartType() == "Grid dB-Mag":
                data=spara.GetMixdB4P(portmap)
                axes_label = ["%s - MixMode Magnitude" %filepath,"Frequency(GHz)","Mag(dB)"]
            else:
                data=spara.GetMixAng4P(portmap)
                axes_label = ["%s - MixMode Angle" %filepath,"Frequency(GHz)","Angle(deg)"]
            
            win = MixCanvesFrame(self, -1, filepath,dim=spara.GetDimension()/2,data=data,axes_label=axes_label)
            win.DrawCurve(splist)

    def OnContent(self,event):
        os.startfile("rc\\SPchartHelpdoc.chm")

    def OnAbout(self,event):
        info = wx.AboutDialogInfo()
        info.Name = "SPChart"
        info.Version = "Rev:0.0"
        info.Copyright = "(C) 2011 Signal-integrity.org"
        info.Description = "SPChart is a free S-parameter viewer, it also support mix mode s-parameter(4 port)."
           
        info.WebSite = ("http://www.signal-integrity.org", "SPChart home page")
        info.Developers = [ "Aaron Lee(leeooox@gmail.com)"]

        info.License = "It's free for any purpose even commercial, but please keep the signature."
        wx.AboutBox(info)


 
class CanvsFrameBase(wx.MDIChildFrame):
    """
    mod is chart mod, it could be:"MagSe","dBSe","AngSe","MagMix","AngMix","TDRSe",,"TDRDiff"
    """
    def __init__(self, parent,ID,title,data=None,axes_label=None):

        wx.MDIChildFrame.__init__(self, parent,ID,title)
        self.data = data
        if axes_label is None:
            self.axes_title = self.GetTitle()
            self.axes_xlabel = "Frequency(GHz)"
            self.axes_ylabel = "Mag(dB)"
        else:
            self.axes_title = axes_label[0]
            self.axes_xlabel = axes_label[1]
            self.axes_ylabel = axes_label[2]

            
        #GUI layout
        self.Maximize()
        panel = wx.Panel(self, -1, style=wx.CLIP_CHILDREN) 
        self.canvas = FigureCanvas(panel, -1, Figure())
        toolbar = NavigationToolbar2Wx(self.canvas)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        
        sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        sizer.Add(toolbar, 0, wx.EXPAND|wx.RIGHT)
        


        self.canvas.mpl_connect('motion_notify_event', self.UpdateStatusBar)


    def GetSPindex(self,s):
        pass

    def DrawAllCurve(self):
        pass

    def DrawReflectionCurve(self):
        pass

    def DrawTransmissionCurve(self):
        pass

    def DrawIsolationCurve(self):
        pass

    def ClearCurve(self):
        self.axes = self.canvas.figure.gca()
        self.axes.cla()
        self.canvas.draw() 

    def DrawCurve(self,splist):
        self.axes = self.canvas.figure.gca()
        self.axes.set_position([0.05,0.05,0.85,0.9])
        self.axes.cla()

        freq = self.data[0]
        markevery = int(freq.shape[0]/10)+1
        cnt = 0
        for sp in splist:
            legend = sp
            line  = Line2D(freq,self.data[self.GetSPindex(sp)],label =sp,c=self.GenColor(cnt),marker=self.GenMarker(cnt),markersize=8,markevery=markevery)
            self.axes.add_line(line)
            cnt+=1

        self.axes.legend(bbox_to_anchor=(1,1), loc="upper left")
        self.axes.set_title(self.axes_title)
        self.axes.set_xlabel(self.axes_xlabel)
        self.axes.set_ylabel(self.axes_ylabel)
        self.axes.grid(True,linestyle='-', linewidth=1)  #Open grid
        self.axes.set_cursor_props(1,"r") #
        self.axes.autoscale_view()

        self.canvas.draw() 
        
        cursor = Cursor(self.axes, useblit=True, color='red', linewidth=1 ) 
        


    def GenColor(self,i):
        #colormap = ['b','g','r','c','m','y','k']
        f = open("rc\\ColorMap.txt")
        colormap = f.readlines()

        return colormap[i%len(colormap)].strip()



    def GenMarker(self,i):
        markermap = "+*,.1234<>DH^_dhopsvx|"
        return markermap[i%len(markermap)]

    def UpdateStatusBar(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            self.GetParent().statusBar.SetStatusText(( "x= " + str(x) +
                                           "  y=" +str(y) ),0)


class SeCanvesFrame(CanvsFrameBase):
    def __init__(self, parent,ID,title,dim=4,data=None,axes_label=None):
        CanvsFrameBase.__init__(self, parent,ID,title,data,axes_label)

        self.dim = dim
        #print self.dim
        self.mod = "se"
        self.DrawAllCurve()

    def GetSPindex(self,s):
        i = int(s[1:-1])
        j = int(s[-1])
        return (i-1)*self.dim + j

    def DrawAllCurve(self):
        splist = []
        for i in range(1, self.dim + 1):
            for j in range(1, self.dim + 1):
                legend = "S%s%s" %(i,j)
                splist.append(legend)
        self.DrawCurve(splist)

    def DrawReflectionCurve(self):
        splist = []
        for i in range(1,self.dim + 1):
            legend = "S%s%s" %(i,i)
            splist.append(legend)
        self.DrawCurve(splist)

    def DrawTransmissionCurve(self):
        splist = []
        for i in range(1, self.dim + 1):
            for j in range(i+1, self.dim + 1):
                legend = "S%s%s" %(j,i)
                splist.append(legend)
        self.DrawCurve(splist)

    def DrawIsolationCurve(self):
        splist = []
        for i in range(1, self.dim + 1):
            for j in range(i+1, self.dim + 1):
                legend = "S%s%s" %(i,j)
                splist.append(legend)
        self.DrawCurve(splist)

class MixCanvesFrame(CanvsFrameBase):
    def __init__(self, parent,ID,title,dim=4,data=None,axes_label=None):
        CanvsFrameBase.__init__(self, parent,ID,title,data,axes_label)

        self.dim = dim
        self.mod = "mix"
        #self.DrawAllCurve()

    def GetSPindex(self,s):
        type = s[1:3]#cc,cd,dc,dd
        co = {"cc":0,"cd":1,"dc":2,"dd":3}
        i = int(s[4:5])
        j = int(s[-2])
        return  (self.dim**2)*co[type] + (i-1)*self.dim + j

    def DrawAllCurve(self):
        splist = []
        for i in range(1, self.dim + 1):
            for j in range(1, self.dim + 1):
                for t in ["cc","cd","dc","dd"]:
                    legend = "S%s[%s,%s]" %(t,i,j)
                    splist.append(legend)
        self.DrawCurve(splist)

    def DrawReflectionCurve(self):
        splist = []
        for i in range(1,self.dim + 1):
            for t in ["cc","cd","dc","dd"]:
                legend = "S%s[%s,%s]" %(t,i,i)
                splist.append(legend)
        self.DrawCurve(splist)

    def DrawTransmissionCurve(self):
        splist = []
        for i in range(1, self.dim + 1):
            for j in range(i+1, self.dim + 1):
                for t in ["cc","cd","dc","dd"]:
                    legend = "S%s[%s,%s]" %(t,j,i)
                    splist.append(legend)
        self.DrawCurve(splist)

    def DrawIsolationCurve(self):
        splist = []
        for i in range(1, self.dim + 1):
            for j in range(i+1, self.dim + 1):
                for t in ["cc","cd","dc","dd"]:
                    legend = "S%s[%s,%s]" %(t,i,j)
                    splist.append(legend)
        self.DrawCurve(splist)

class ChartSetting(wx.Dialog):
    def __init__(self, parent,ID,title,dim,mod,size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self, parent,ID,title,size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE)
        

        sizer = wx.BoxSizer(wx.VERTICAL)
        nb = wx.Notebook(self,-1)
        sizer.Add(nb)


        panel_curve = wx.Panel(nb,-1,size=(400,300))
        nb.AddPage(panel_curve , "Curve")

        CurveList = []
        for i in range(1, dim + 1):
            for j in range(1, dim + 1):
                if mod == "se":
                    legend = "S%s%s" %(i,j)
                    CurveList.append(legend)
                elif mod == "mix":
                    for t in ["cc","cd","dc","dd"]:
                        legend = "S%s[%s,%s]" %(t,i,j)
                        CurveList.append(legend)
                
        
        self.chk_sp = wx.CheckListBox(panel_curve, -1, (0, 0), wx.DefaultSize, CurveList)
        
        spchked_list = self.GetParent().GetActiveChild().axes.get_legend_handles_labels()[1] 
        self.chk_sp.SetCheckedStrings(spchked_list) 

        
        btnsizer = wx.StdDialogButtonSizer()
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        
        
        btnsizer.AddButton(btn)


        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def GetValue(self):
        return self.chk_sp.GetCheckedStrings()


class MixModeDlg(wx.Dialog):
    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        self.SetSize((550,500))
        self.fbb = filebrowse.FileBrowseButton(
            self, -1, (0,0),size=(450, -1),labelText="File",
            changeCallback = self.fbbCallback
            )
        wx.StaticText(self,-1,"Port mapping",(20,40))
        self.gd_portmap =  PortMapGrid(self,-1,(0,60),(220,300))


        wx.StaticText(self,-1,"Chart Type",(260,40))
        self.cmb_charttype = wx.ComboBox(self, -1, "Grid dB-Mag", (260, 60), 
                             (160, -1), ["Grid dB-Mag","Grid Angle"],
                             wx.CB_DROPDOWN|wx.CB_READONLY)
     

        wx.StaticText(self,-1,"Curves",(260,90))
        self.clb_splist = wx.CheckListBox(self, -1, (260, 110), (160,250))


        posy = 110
        self.btn_spfilter = []
        for b in ["CC","CD","DC","DD"]:
            btn = buttons.GenToggleButton(self, -1, "All %s's" %b,(440,posy))
            posy += 30
            self.btn_spfilter.append(btn)
            btn.Bind(wx.EVT_BUTTON,self.OnSPFilter)
            


        wx.Button(self, wx.ID_OK,"OK",(100,400))
        wx.Button(self, wx.ID_CANCEL,"Cancel",(200,400))

    def OnSPFilter(self,evt): 
        btn = evt.GetEventObject()
        chk = evt.GetIsDown()
        filter = btn.GetLabel()[4:-2].lower()
        
        i = 0
        for item in self.clb_splist.GetItems():
            if item.find(filter) != -1:
                self.clb_splist.Check(i,chk)
            i += 1

    def fbbCallback(self, evt):
        filepath = self.fbb.GetValue()
        try:
            dim = int(os.path.splitext(filepath)[-1][2:-1])
        except:
            dlg = wx.MessageDialog(self, 'A invalid file!\nPlease use a snp file.',
                               'Error',
                               wx.OK | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
            
        else:
            if dim <0:#!=4:
                dlg = wx.MessageDialog(self, 'Only support 4 port S-paramter',
                               'Error',
                               wx.OK | wx.ICON_INFORMATION
                               )
                dlg.ShowModal()
                dlg.Destroy()
            else:
                self.gd_portmap.DeleteRows(0,self.gd_portmap.GetNumberRows())
                self.gd_portmap.AppendRows(dim/2)
                for i in range(0,dim/2):
                    self.gd_portmap.SetCellValue(i,0,str(2*i+1))
                    self.gd_portmap.SetCellValue(i,1,str(2*i+2))

                #add checklist
                spitemlist = []
                for i in range(1,dim/2+1):
                    for j in range(1,dim/2+1):
                        spitemlist.append("Scc[%s,%s]" %(i,j))
                        spitemlist.append("Scd[%s,%s]" %(i,j))
                        spitemlist.append("Sdc[%s,%s]" %(i,j))
                        spitemlist.append("Sdd[%s,%s]" %(i,j))

                self.clb_splist.SetItems(spitemlist)
                self.clb_splist.SetCheckedStrings(spitemlist)

                #Set toggle buttons
                for btn in self.btn_spfilter:
                    btn.SetToggle(True)


    def GetChartType(self):
        return self.cmb_charttype.GetValue()

    def GetPortMap(self):
        pmap = []
        for i in range(self.gd_portmap.GetNumberRows()):
            for j in range(self.gd_portmap.GetNumberCols()):
                pmap.append(int(self.gd_portmap.GetCellValue(i,j)))

        return pmap
    
    def GetCurveList(self):
        return self.clb_splist.GetCheckedStrings()

    def GetFilepath(self):
        return self.fbb.GetValue()

class PortMapGrid(wx.grid.Grid):
    def __init__(self, *args, **kwargs):
        wx.grid.Grid.__init__(self, *args, **kwargs)
        self.CreateGrid(16,2)
        collabel = ["IP port+","IP port-"]
        self.SetRowLabelSize(40)
        for col in range(2):
            self.SetColLabelValue(col,collabel[col])



if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame(None,title="SPChart",size=(800,600))
    frame.Show()
    app.MainLoop()
