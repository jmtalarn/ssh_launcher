# -*- coding: utf-8 -*-
#!/usr/bin/env python
from gi.repository import Gtk
import glob
import os
import logging
import yaml
import pprint
import webbrowser

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
# INIT DATA

with open("servers.yaml", 'r') as stream:
    servers = yaml.load(stream)

def run_console(server, pem):
    cmd_line = "ssh -i {} ec2-user@{}".format(pem, server)
    os.system("gnome-terminal -e 'bash -c \"" + cmd_line + " ; exec bash\"'")


class Handler:

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button):
        server_list = builder.get_object("servers_list")
        serverSelection = server_list.get_selection()
        serverStore = server_list.get_model()

        pems_list = builder.get_object("certificates_list")
        pemSelection = builder.get_object("certificates_list").get_selection()
        pemStore = pems_list.get_model()

        (model, tree_iter) = serverSelection.get_selected()
        if (tree_iter):
            server = model.get_value(tree_iter, 1)
        else:
            server = builder.get_object("entryTextIP").get_text()

        (model, tree_iter) = pemSelection.get_selected()
        if (tree_iter):
            pem = model.get_value(tree_iter, 1)
        else:
            pem = builder.get_object(
                "certificatechooser_button").get_filename()

        print("AWS Console running ssh to server:{} with pem:{}".format(server, pem))
        run_console(server, pem)

    def onWebOpenPressed(self,button):
        server_list = builder.get_object("servers_list")
        serverSelection = server_list.get_selection()

        (model, tree_iter) = serverSelection.get_selected()
        if (tree_iter):
            server = model.get_value(tree_iter, 1)
        else:
            server = builder.get_object("entryTextIP").get_text()

	webbrowser.open_new_tab("http://"+server+"/")

    def onClickChooseFile(self, *args):
        pemsSelection = builder.get_object("certificates_list").get_selection()
        pemsSelection.unselect_all()

    def onClickIPInput(self, *args):
        serversSelection = builder.get_object("servers_list").get_selection()
        serversSelection.unselect_all()

builder = Gtk.Builder()

builder.add_from_file(os.path.dirname(os.path.realpath(__file__))+"/dialog.glade")

builder.connect_signals(Handler())

window = builder.get_object("dialog1")


pems_tree = builder.get_object("certificates_list")


pemsStore = pems_tree.get_model()
for pem in sorted(glob.glob("/home/jmtalarn/.ssh/*.pem")):
    pemsStore.append([pem.replace('/home/jmtalarn/.ssh/', ''), pem])

servers_tree = builder.get_object("servers_list")

serversStore = servers_tree.get_model()
for key,data in sorted(servers.items()):
    logger.info("**"+key+"** "+data['name']+"["+data['ip']+"]")
    serversStore.append([data['name'], data['ip']] )


window.show_all()

Gtk.main()
