# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
from subprocess import Popen, PIPE

def main():
    destination = "C:\\Users\\kliu\\Downloads"
    install_src = copy_alteryx(dst = destination)
    install_dst = "C:\\Program Files\\Alteryx\\bin\\"
    log_path = destination + '\\' + 'alteryx_install.log'   
    pred_src = copy_predictive(dst = destination)
    install_alteryx(install_src, install_dst, log_path)
    install_predictive(pred_src)
     


# run workflows in batch mode ----
def run_workflows(path = './workflows'):
    alteryx_bin = "C:\\Program Files\\Alteryx\\bin\\AlteryxEngineCmd.exe"
    files = [os.path.join(path,x) for x in os.listdir(path) if x.endswith(".yxmd")]
    for f in files:
        cmd = quote(alteryx_bin) + ' ' + f    
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        output, errors = proc.communicate()
        print("Output:")
        print("="*50)
        print(output.decode('utf-8', errors="ignore"))
        print("Errors:")
        print("="*50)
        print(errors.decode('utf-8', errors="ignore"))
        #return_code = os.system(cmd)
        #print(f + ": " + str(return_code))
    
def quote(s):
    return '"' + s + '"'  
    
# copy & install Alteryx ----
def copy_alteryx(dst,
                 repo_path = "\\\\DEN-IT-FILE-07\\BuildRepo", 
                 branch = "EmCap", #"Predictive_Dev",
                 install_type = "admin"):
    """Copy Alteryx installation file to user appointed directory
    
    Args:
        dst: A string of the directory path you want to copy the file to.
        repo_path: A string of the Alteryx BuildRepo path.
        branch: A string of branch name, default to "Predictive_Dev"
        install_type: A string of 4 options: 'admin', 'non_admin', 'gallery' 
            and 'server'
    
    Returns:
        Path of the installation exe file. 
    """
    install_dict = {'admin': 'AlteryxInstallx64',
                    'non_admin': 'AlteryxNonAdminInstall',
                    'gallery': 'AlteryxGalleryInstall',
                    'server': 'AlteryxServerInstall'}
    dirs = os.listdir(repo_path)
    all_versions =  [x for x in dirs if branch in x]
    latest = all_versions[-1]
    src = "\\".join([repo_path, latest, "Alteryx"])
    files = os.listdir(src)
    install_file = [x for x in files if install_dict[install_type] in x][0]
    src += "\\" + install_file
    
    cmd = "copy " + quote(src) + ' ' + dst
    err_code = os.system(cmd)
    if err_code:
        print("Error: failed to copy the latest Alteryx build")
        print("Copy command is: " + cmd)
        return
    return dst + '\\' + install_file

def copy_predictive(dst,
                 repo_path = "\\\\DEN-IT-FILE-07\\BuildRepo", 
                 branch = "Predictive_Dev",
                 install_type = "admin"):
    """Copy Predictive installation file to user appointed directory
    
    Args:
        dst: A string of the directory path you want to copy the file to.
        repo_path: A string of the Alteryx BuildRepo path.
        branch: A string of branch name, default to "Predictive_Dev"
        install_type: A string of 4 options: 'admin', 'non_admin', 'gallery' 
            and 'server'
    
    Returns:
        Path of the installation exe file. 
    """
    install_dict = {'admin': 'RInstaller',
                    'non_admin': 'RNonAdminInstall',
                    'rre': 'RREInstaller'}
    dirs = os.listdir(repo_path)
    all_versions =  [x for x in dirs if branch in x]
    latest = all_versions[-1]
    src = "\\".join([repo_path, latest, "R"])
    files = os.listdir(src)
    install_file = [x for x in files if install_dict[install_type] in x][0]
    src += "\\" + install_file 
    
    cmd = "copy " + quote(src) + ' ' + dst
    err_code = os.system(cmd)
    if err_code:
        print("Error: failed to copy the latest Alteryx build")
        print("Copy command is: " + cmd)
        return
    return dst + '\\' + install_file

def install_alteryx(src, dst = None, silent = True, log_file = None):
    """ Install Alteryx
    
    Args:
        src: string, the path of the installation exe file.
        dst: (optional) string, where you want Alteryx to be installed.
        silient: boolean, if you want to have conversation window during install
        log_file: (optional) string, where you want to save the log file.
    
    Returns:
        None
    """
    cmd = [quote(src)]
    if silent:
        cmd.append('/s')
    if dst:
        cmd.append('TARGETDIR=' + quote(dst))
    if log_file:
        cmd.append('/l=' + quote(log_file))
    
    cmd = quote(' '.join(cmd))
    err_code = os.system(cmd)
    if err_code:
        print("Error: failed to install Alteryx")
        print("Installation command used is: " + cmd)
        if log_file:
            print("See the log file: " + log_file + " for the details")  
 
def install_predictive(src, silent = True):
    cmd = src
    if silent:
        cmd += " /s"
    cmd = quote(cmd)
    err_code = os.system(cmd)
    if err_code:
        print("Error: failed to install Alteryx")
        print("Installation command used is: " + cmd)
    
if __name__ == '__main__':
    main()

