#
# gtkui.py
#
# Copyright (C) 2016-2017 Noam <noamgit@gmail.com>
# https://github.com/noam09
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#

try:
    from deluge.log import LOG as log
except Exception as e:
    print 'Telegramer: Exception - %s' % str(e)

try:
    import gtk
    import deluge.common
    from common import get_resource
    from deluge.ui.client import client
    import deluge.component as component
    from deluge.plugins.pluginbase import GtkPluginBase
except ImportError as e:
    log.error('Telegramer: Import error - %s', str(e))

class GtkUI(GtkPluginBase):
    def enable(self):
        self.glade = gtk.glade.XML(get_resource("config.glade"))
        self.glade.signal_autoconnect({
            "on_button_test_clicked":self.on_button_test_clicked,
            "on_button_save_clicked":self.on_button_save_clicked,
            "on_button_reload_clicked":self.on_button_reload_clicked
        })
        component.get("Preferences").add_page("Telegramer", self.glade.get_widget("prefs_box"))
        component.get("PluginManager").register_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").register_hook("on_show_prefs", self.on_show_prefs)

    def disable(self):
        component.get("Preferences").remove_page("Telegramer")
        component.get("PluginManager").deregister_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").deregister_hook("on_show_prefs", self.on_show_prefs)

    def on_apply_prefs(self):
        log.debug("Telegramer: applying prefs for Telegramer")
        config = {
            "telegram_notify_added":self.glade.get_widget("telegram_notify_added").get_active(),
            "telegram_notify_finished":self.glade.get_widget("telegram_notify_finished").get_active(),
            "telegram_token":self.glade.get_widget("telegram_token").get_text(),
            "telegram_user":self.glade.get_widget("telegram_user").get_text(),
            "telegram_users":self.glade.get_widget("telegram_users").get_text(),
            "wol_address":self.glade.get_widget("wol_address").get_text(),
            "wol_inteface":self.glade.get_widget("wol_inteface").get_text(),
            "cat1":self.glade.get_widget("cat1").get_text(),
            "dir1":self.glade.get_widget("dir1").get_text(),
            "cat2":self.glade.get_widget("cat2").get_text(),
            "dir2":self.glade.get_widget("dir2").get_text(),
            "cat3":self.glade.get_widget("cat3").get_text(),
            "dir3":self.glade.get_widget("dir3").get_text()
        }
        client.telegramer.set_config(config)

    def on_show_prefs(self):
        client.telegramer.get_config().addCallback(self.cb_get_config)

    def cb_get_config(self, config):
        "callback for on show_prefs"
        self.glade.get_widget("telegram_notify_added").set_active(config["telegram_notify_added"])
        self.glade.get_widget("telegram_notify_finished").set_active(config["telegram_notify_finished"])
        self.glade.get_widget("telegram_token").set_text(config["telegram_token"])
        self.glade.get_widget("telegram_user").set_text(config["telegram_user"])
        self.glade.get_widget("telegram_users").set_text(config["telegram_users"])
        self.glade.get_widget("wol_address").set_text(config["wol_address"])
        self.glade.get_widget("wol_inteface").set_text(config["wol_inteface"])
        self.glade.get_widget("cat1").set_text(config["cat1"])
        self.glade.get_widget("dir1").set_text(config["dir1"])
        self.glade.get_widget("cat2").set_text(config["cat2"])
        self.glade.get_widget("dir2").set_text(config["dir2"])
        self.glade.get_widget("cat3").set_text(config["cat3"])
        self.glade.get_widget("dir3").set_text(config["dir3"])

    def on_button_test_clicked(self, Event=None):
        client.telegramer.telegram_do_test()

    def on_button_save_clicked(self, Event=None):
        self.on_apply_prefs()

    def on_button_reload_clicked(self, Event=None):
        client.telegramer.restart_telegramer()
