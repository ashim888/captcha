from distutils.core import setup
import py2exe

setup(
    version = "0.5",
    description = "Sample compile",
    name = "Spammer",
    options = {'py2exe':{'bundle_files':1,'compressed':True}},
    windows = ["beta_v1_with_tabs.py"],
    zipfile = None,
)