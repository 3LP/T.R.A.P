# UI
# Imort modules
import os,pygtk
from gi.repository import Gtk, Vte
from gi.repository import GLib, Gdk
from gi.repository import GObject
from gi.repository import GtkSource
import numpy as np
import sys
pygtk.require('2.0')

# Graphical User Interface
# Global
StatusBar = Gtk.Statusbar()
source = GtkSource.View()
buffer = source.get_buffer()
terminal = Vte.Terminal()
class MainWindow(Gtk.Window):
    file_tag = 'NoFileLoaded!'
    # Open File function
    def open_file(menuitem, user_param):
        chooser = Gtk.FileChooserDialog(title="Open a file",action=Gtk.FileChooserAction.OPEN, buttons=(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
        chooser.set_default_response(Gtk.ResponseType.OK)
        filter = Gtk.FileFilter()
        filter2 = Gtk.FileFilter()
        filter2.set_name("All Files")
        filter2.add_pattern("*.*")
        chooser.add_filter(filter2)
        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            global file_tag
            file_tag = filename
            textbuffer = source.get_buffer()
            print "Opened File: " + filename
            StatusBar.push(0,"Opened File: " + filename)
            index = filename.replace("\\","/").rfind("/") + 1
            window.set_title(filename[index:] + " - PyPad")
            file = open(filename, "r")
            text = file.read()
            textbuffer.set_text(text)
            file.close()
            chooser.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            chooser.destroy()
            chooser.destroy()
    def save_file(menuitem,user_param):
            textbuffer = source.get_buffer()
            StatusBar.push(0,"Saved File: " + file_tag)
            index = file_tag.replace("\\","/").rfind("/") + 1
            text = textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter(),False)
            window.set_title(file_tag[index:] + " - PyPad")
            file = open(file_tag, "w")
            file.write(text)
            file.close()

    def save_file_as(menuitem,user_param):
        chooser = Gtk.FileChooserDialog(title="Save file",action=Gtk.FileChooserAction.SAVE, buttons=(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_SAVE,Gtk.ResponseType.OK))
        chooser.set_default_response(Gtk.ResponseType.OK)
        filter = Gtk.FileFilter()
        filter.set_name("Text Files")
        filter.add_mime_type("text/data")
        chooser.add_filter(filter)
        filter2 = Gtk.FileFilter()
        filter2.set_name("All Files")
        filter2.add_pattern("*.*")
        chooser.add_filter(filter2)
        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            textbuffer = source.get_buffer()
            print "Saved File: " + filename
            StatusBar.push(0,"Saved File: " + filename)
            index = filename.replace("\\","/").rfind("/") + 1
            text = textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter(),False)
            window.set_title(filename[index:] + " - PyPad")
            file = open(filename, "w")
            file.write(text)
            file.close()
            chooser.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            chooser.destroy()
            chooser.destroy()

    def __init__(self):
        Gtk.Window.__init__(self)
        # Window title and Icon
        self.set_title("MaeTrics")
    # Vertical Box
        self.box = Gtk.VBox(homogeneous=False, spacing=0)
        self.add(self.box)
        # Menu
        menu = Gtk.MenuBar()
        filemenu = Gtk.Menu()
        filem = Gtk.MenuItem("File")
        # Import
        imenu = Gtk.Menu()
        importm = Gtk.MenuItem("T.R.A.P")
        importm.set_submenu(imenu)
        inews = Gtk.MenuItem("Import T.R.A.P#1...")
        ibookmarks = Gtk.MenuItem("Import T.R.A.P#2...")
        imenu.append(inews)
        imenu.append(ibookmarks)
        openm = Gtk.MenuItem("Open")
        savem = Gtk.MenuItem("Save")
        saveasm = Gtk.MenuItem("Save As")
        exit = Gtk.MenuItem("Exit")
        openm.connect("activate",self.open_file)
        saveasm.connect("activate",self.save_file_as)
        savem.connect("activate",self.save_file)
        exit.connect("activate", Gtk.main_quit)
        filemenu.append(importm)
        filemenu.append(openm)
        filemenu.append(savem)
        filemenu.append(saveasm)
        filemenu.append(exit)
        filem.set_submenu(filemenu)
        menu.append(filem)
        # Source View
        source.set_show_line_numbers(True)
        terminal.set_encoding("UTF-8")
        terminal.fork_command_full(Vte.PtyFlags.DEFAULT,os.environ['HOME'],["/bin/sh"],[],GLib.SpawnFlags.DO_NOT_REAP_CHILD,None,None,)
        # Scrolled Text Window
        scrolledwindow1 = Gtk.ScrolledWindow()
        scrolledwindow1.set_hexpand(True)
        scrolledwindow1.set_vexpand(True)
        scrolledwindow1.set_border_width(10)
        scrolledwindow2 = Gtk.ScrolledWindow()
        scrolledwindow1.add(source)
        scrolledwindow2.add(terminal)
        # Vertical Pane
        vpaned = Gtk.VPaned()
        vpaned.add1(scrolledwindow1)
        vpaned.add2(scrolledwindow2)
        # Pack everything in vertical box
        self.box.pack_start(menu, False, False, 0)
        self.box.pack_start(vpaned, True, True, 0)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()




window = MainWindow()
Gtk.main()

