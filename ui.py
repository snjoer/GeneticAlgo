import os
import wx
from ga2values import *

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title='Genetic Algo', size=(800, 450))

        self.panel = wx.Panel(self)
        self.left_panel = wx.Panel(self.panel)
        self.middle_panel = wx.Panel(self.panel)
        self.right_panel = wx.Panel(self.panel)
        self.key_word = ''
        self.path = ''
        self.bin_path = ''

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.GridBagSizer(5, 1)
        middle_sizer =wx.GridBagSizer(5, 1)
        right_sizer =wx.GridBagSizer(5, 1)
        self.panel.SetSizer(sizer)
        self.left_panel.SetSizer(left_sizer)
        self.middle_panel.SetSizer(middle_sizer)
        self.right_panel.SetSizer(right_sizer)
        count = wx.StaticText(self.left_panel,
                label='Stable Count')
        self.count_box = wx.TextCtrl(self.left_panel,
                style=wx.TE_PROCESS_ENTER)
        population = wx.StaticText(self.left_panel,
                label='Population')
        self.pop_box = wx.TextCtrl(self.left_panel,
                style=wx.TE_PROCESS_ENTER)
        cross_ratio = wx.StaticText(self.left_panel,
                label='Cross Ratio')
        self.cr_box = wx.TextCtrl(self.left_panel,
            style=wx.TE_PROCESS_ENTER)
        vary_ratio = wx.StaticText(self.left_panel,
                label='Vary Ratio')
        self.vr_box = wx.TextCtrl(self.left_panel,
                style=wx.TE_PROCESS_ENTER)
        origin = wx.StaticText(self.middle_panel,
                label='Origin:')
        _bin = wx.StaticText(self.right_panel,
                label='Bin:')
        self.grLabel = wx.StaticText(self.left_panel,
                label='Generation: Null')
        self.thLabel = wx.StaticText(self.left_panel,
                label='Threshold: Null')
        start_button = wx.Button(self.left_panel, label='Start')
        bestTh_button = wx.Button(self.left_panel, label='BestThreshold')
        display_button = wx.Button(self.left_panel, label='Display')
        exit_button = wx.Button(self.left_panel, label='Exit')
        
        self.img = wx.EmptyImage(512,512)
        self.img = self.img.Scale(self.img.GetWidth()/2, self.img.GetHeight()/2).ConvertToBitmap()
        import_button = wx.Button(self.middle_panel, label="Import an image")
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, self.img)
        self.bin_img = self.img
        self.binImgCtrl = wx.StaticBitmap(self.right_panel, wx.ID_ANY, self.bin_img)
    
        sizer.Add(self.left_panel)
        sizer.Add(self.middle_panel)
        sizer.Add(self.right_panel)
        left_sizer.Add(count, pos=(1, 1))
        left_sizer.Add(self.count_box, pos=(2,1))
        left_sizer.Add(population, pos=(3, 1))
        left_sizer.Add(self.pop_box, pos=(4, 1))
        left_sizer.Add(cross_ratio, pos=(5, 1))
        left_sizer.Add(self.cr_box, pos=(6, 1))
        left_sizer.Add(vary_ratio, pos=(7, 1))
        left_sizer.Add(self.vr_box, pos=(8, 1))
        left_sizer.Add(start_button, pos=(9, 1))
        left_sizer.Add(bestTh_button, pos=(15, 1))
        left_sizer.Add(display_button, pos=(10, 1))
        left_sizer.Add(exit_button, pos=(11, 1))
        left_sizer.Add(self.grLabel, pos=(12, 1))
        left_sizer.Add(self.thLabel, pos=(13, 1))
        middle_sizer.Add(origin, pos=(1, 1))
        middle_sizer.Add(import_button, pos=(2,1))
        middle_sizer.Add(self.imageCtrl, pos=(3, 2))
        right_sizer.Add(_bin, pos=(1, 0))
        right_sizer.Add(self.binImgCtrl, pos=(3, 0))

        self.Bind(wx.EVT_BUTTON, self.start, start_button)
        self.Bind(wx.EVT_BUTTON, self.bestThreshold, bestTh_button)
        self.Bind(wx.EVT_BUTTON, self.display, display_button)
        self.Bind(wx.EVT_BUTTON, self.exit, exit_button)
        self.Bind(wx.EVT_BUTTON, self.importImage, import_button)

    def importImage(self, event):
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(),
                "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.path = dialog.GetPath()
            self.img = wx.Image(self.path, wx.BITMAP_TYPE_JPEG)
            w, h = self.img.GetWidth(), self.img.GetHeight()
            self.w, self.h = self.adjustSize(w, h)
            self.img = self.img.Scale(self.w/2, self.h/2).ConvertToBitmap()
            self.imageCtrl.SetBitmap(self.img)
            self.bin_img = self.img
            self.binImgCtrl.SetBitmap(self.bin_img)
            self.panel.Refresh()

    def start(self, event):
        self.count = self.count_box.GetValue().encode('utf-8')
        self.population = self.pop_box.GetValue().encode('utf-8')
        self.cross_ratio = self.cr_box.GetValue().encode('utf-8')
        self.vary_ratio = self.vr_box.GetValue().encode('utf-8')
        if self.count == "" or self.population == "" or self.cross_ratio == "" or self.vary_ratio == "" or self.path == "":
            box = wx.MessageDialog(None, 'Input incomplete!', 'Input Error!', wx.OK)
            box.ShowModal()
            box.Destroy()
            return 
        self.count = int(self.count)
        self.population = int(self.population)
        self.cross_ratio = float(self.cross_ratio)
        self.vary_ratio = float(self.vary_ratio)
        dataValid = True
        if self.population <= 0:
            box = wx.MessageDialog(None, 'Invalid population!', 'Input Error!', wx.OK)
            dataValid = False
        if self.cross_ratio < 0 or self.cross_ratio > 1:
            box = wx.MessageDialog(None, 'Invalid cross ratio!', 'Input Error!', wx.OK)
            dataValid = False
        if self.vary_ratio < 0 or self.vary_ratio > 1:
            box = wx.MessageDialog(None, 'Invalid vary ratio!', 'Input Error!', wx.OK)  
            dataValid = False
        if dataValid == False:
            box.ShowModal()
            box.Destroy()
            return
        self.bin_path, self.gr, self.th = main(self.path, self.count, self.population, \
                self.cross_ratio, self.vary_ratio)
        self.grLabel.SetLabel('Generation: ' + str(self.gr))
        self.thLabel.SetLabel('Threshold: ' + str(self.th))
    
    def bestThreshold(self, event):
        if self.path == '':
            box = wx.MessageDialog(None, 'No input image!', 'Input Error!', wx.OK)
            box.ShowModal()
            box.Destroy()
            return
        self.bin_path, self.th = naiveFindBestThreshold(self.path)
        self.grLabel.SetLabel('Generation: 0')
        self.thLabel.SetLabel('Threshold: ' + str(self.th))

    def display(self, event):
        if self.bin_path == '':
            box = wx.MessageDialog(None, 'Nothing to display!', 'Display Error!', wx.OK)
            box.ShowModal()
            box.Destroy()
            return
        self.bin_img = wx.Image(self.bin_path, wx.BITMAP_TYPE_JPEG)
        self.bin_img = self.bin_img.Scale(self.w/2, self.h/2).ConvertToBitmap()
        self.binImgCtrl.SetBitmap(self.bin_img)
        self.panel.Refresh()

    def exit(self, event):
        self.Destroy()
    
    def adjustSize(self, w, h):
        if w > 512 or h > 512:
                if w > h:
                    h = 512.0 * h / w 
                    w = 512 
                else:
                    w = 512.0 * w / h 
                    h = 512 
        return w, h	
if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
