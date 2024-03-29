#! /usr/bin/env python

# Check for root user login
import os, sys
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\n")

# Get your username (not root)
import pwd
uname=pwd.getpwuid(1000)[0]

# The remastering process uses chroot mode.
# Check to see if this script is operating in chroot mode.
# /home/mint directory only exists in chroot mode
is_chroot = os.path.exists('/home/mint')
dir_develop=''
if (is_chroot):
	dir_develop='/usr/local/bin/develop'
	dir_user = '/home/mint'
else:
	dir_develop='/home/' + uname + '/develop'
	dir_user = '/home/' + uname

# Everything up to this point is common to all Python scripts called by shared-*.sh
# =================================================================================

def message (string):
    os.system ('echo ' + string)

# Replace text in a file        
def change_text (filename, text_old, text_new):
    text=open(filename, 'r').read()
    text = text.replace(text_old, text_new)
    open(filename, "w").write(text)

# THIS IS THE SCRIPT FOR REPLACING THE DEFAULT LMDE DISPLAY MANAGER WITH A LIGHTER ONE.
message ('===============================')
message ('BEGIN REPLACING DISPLAY MANAGER')

# Install LightDM
message ('INSTALLING lightdm and lightdm-gtk-greeter')
os.system ('apt-get install -qq lightdm lightdm-gtk-greeter')
os.system ('dpkg-reconfigure lightdm')

# ============================
# Configure LightDM
# http://arcticdog.wordpress.com/2012/02/08/customising-the-lightdm-gtk-greeter/

import shutil

def remove_file (filename):
    if (os.path.exists(filename)):
        os.remove(filename)

# Change the LightDM wallpaper
src = dir_develop + '/ui-login/etc_lightdm/lightdm-gtk-greeter.conf'
dest = '/etc/lightdm/lightdm-gtk-greeter.conf'
message ('REPLACING ' + dest)
shutil.copyfile(src, dest)

# Auto-login as user 'mint'
src = dir_develop + '/ui-login/etc_lightdm/lightdm.conf'
dest = '/etc/lightdm/lightdm.conf'
message ('REPLACING ' + dest)
shutil.copyfile(src, dest)

# Disable auto-login if not in chroot mode
if (not (is_chroot)):
    filename = '/etc/lightdm/lightdm.conf'
    text_old = '\nautologin'
    text_new = '\n# autologin'
    change_text (filename, text_old, text_new)

# Implement auto-login (copied from the GDM autologin file)
src = dir_develop + '/ui-login/etc_pam.d/lightdm-autologin'
dest = '/etc/pam.d/lightdm-autologin'
message ('REPLACING ' + dest)
shutil.copyfile(src, dest)

# Change the LightDM login box
src = dir_develop + '/ui-login/usr_share_lightdm-gtk-greeter/greeter.ui'
dest = '/usr/share/lightdm-gtk-greeter/greeter.ui'
message ('REPLACING ' + dest)
shutil.copyfile(src, dest)


message ('FINISHED REPLACING DISPLAY MANAGER')
message ('==================================')
