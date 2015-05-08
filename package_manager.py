__author__ = 'kharekartik'

import os

class Package_Manager():
	def get_dependencies(self, package):
		if "requires" in package:
			return package["requires"]
		return []

	def get_ppa(self, package):
		if "ppa" in package:
		    return package["ppa"]
		return "none"

	def get_more_cmds(self, package):
		if "cmds" in package:
		    return package["cmds"]
		return []

	def install_package(self, package, package_installer):
		#TODO
		print "Installing " + package
		dependencies = self.get_dependencies(package)
		ppa = self.get_ppa(package)
		cmds = self.get_more_cmds(package)
		for dependency in dependencies:
		    "Found dependency: " + dependency
		    self.install_package(dependency)
		if(ppa!="none"):
		    os.system("sudo add-apt-repository %s" % ppa)
		    os.system("sudo apt-get update")
		for cmd in cmds:
		    os.system(cmd)
		cmd = package_installer + ' install ' + package
		install_proc = os.system('sudo %s' % (cmd))
