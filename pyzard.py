__author__ = 'kharekartik'
import json
import os
import platform

class Pyzard():
    """docstring for  Pyzard"""
    def __init__(self, os="none", version=-1):
        self.os = os
        self.version = version
        self.packages_list = []
        self.package_installer = "apt-get"

    def get_supported_distros(self):
        disto_file = open("distro.md","r")
        distro_list = disto_file.readlines()
        disto_file.close()
        return distro_list

    def get_linux_distribution(self):
        if(self.os == "none"):
            try:
                linux_distro = platform.linux_distribution()
                self.os = linux_distro[0].strip('"')
                self.version = linux_distro[1]
                print self.os + " " + self.version + " was found installed on your system"
                return linux_distro

            except Exception:
                print "Not supported for the current OS"

    def is_distro_supported(self):
        supported_distros = self.get_supported_distros()
        dist = self.os
        for dist in supported_distros:
            if self.os.lower() == str(dist).split(',')[0].lower() :
                return True
        print "Not supported for the current OS"
        return False

    def read_json(self, json_file):
        try:
            with open(json_file) as json_file:
                jsonAsDict = json.load(json_file)
                return jsonAsDict
        except Exception:
            print "Unable to read the current file.Does that even exist!"
 
    def get_installers(self, linux_distribution="Ubuntu"):
        distros_dict = self.read_json("installers.json")
        try:
            packages_list = distros_dict[linux_distribution]["packages"]
            package_installer = distros_dict[linux_distribution]["package-installer"]
            self.packages_list = packages_list
            self.package_installer = package_installer
            return package_installer, packages_list
        except KeyError:
            print "Key Error for: " + self.os
            similar_dist = self.get_similar_distro()
            if(similar_dist!=""):
                self.os = similar_dist
                print "packages not found for current OS.Trying installing packages for " + self.os
                return self.get_installers(self.os)
            else:
                print "Not supported for current OS"
 
    def get_similar_distro(self):
        distro_list = self.get_supported_distros()
        current_dist = self.os
        for dist in distro_list:
            dist_props = dist.split(',')
            if(current_dist.lower() == dist_props[0].lower() and dist_props[2]!="None" and dist_props[2]!="Self"):
                return dist_props[2].strip("\n")
            elif dist_props[2]=="None":
                return ""

    def get_dependencies(self, package):
        #TODO
        #checks for already installed dependencies and
        #return list of dependencies to be installed
        if(len(self.packages_list)):
            packages = self.packages_list
            if package in packages:
                if "requires" in packages[package]:
                    return packages[package]["requires"]
        return []
    
    def get_ppa(self, package):
        if(len(self.packages_list)):
            packages = self.packages_list
            if package in packages:
                if "ppa" in packages[package]:
                    return packages[package]["ppa"]
        return "None"

    def get_more_cmds(self, package):
        if(len(self.packages_list)):
            packages = self.packages_list
            if package in packages:
                if "cmds" in packages[package]:
                    return packages[package]["cmds"]
        return []

    def install_package(self, package):
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
        cmd = self.package_installer + ' install ' + package
        install_proc = os.system('echo %s | sudo %s' % (password, cmd))



    def install(self):
        distro = self.get_linux_distribution()
        if(self.is_distro_supported()):
            installer, packages= self.get_installers(self.os)
            packagesAsList = []
            package_index = 1
            for package in packages:
                print str(package_index) + " " + package
                package_index+=1
                packagesAsList.append(package)
            print ("To select package enter the package indices as space separated values or 0 to install all")

            selected_package = raw_input("Select Packages: ")
            packagesToBeInstalled = []
            if(selected_package!='0'):
                packagesToBeInstalled = selected_package.split(' ')
            else:
                for i in range(1, len(packagesAsList)+1):
                    packagesToBeInstalled.append(str(i))
    
            #password = raw_input("Enter SuperUser Password: ")

            for index in packagesToBeInstalled:
                try:
                   self.install_package(packagesAsList[int(index)-1])
                except Exception:
                    print "Sorry! Wasn't able to install "+packagesAsList[int(index)-1]



pyzard = Pyzard()
pyzard.install()        
