__author__ = 'kharekartik'
import json
import os

with open("installers.json") as installers_file:
    print "Select package to install"
    installers = json.load(installers_file)
    package_index = 0;
    #selected_package = -1;
    packages = []
    for package in installers["Ubuntu"]:
        package_index+=1
        print str(package_index) + " " + package
        packages.append(package)
    selected_package = raw_input("Select Package: ")
    password = raw_input("Enter Password: ")
    command = 'apt-get install ' + packages[int(selected_package)]
    p = os.system('echo %s|sudo %s' % (password, command))
