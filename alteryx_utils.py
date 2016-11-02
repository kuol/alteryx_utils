# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os

def main():
    destination = "C:\Users\kliu\Downloads"
    copy_alteryx(dst = destination, install_type = "non_admin")


# run workflows in batch mode ----
def run_workflows(path = './workflows'):
    files = os.listdir(path)
    for f in files:
        cmd = 'AlteryxEngineCmd.exe ' + f    
        return_code = os.system(cmd)
        print f + ": " + str(return_code)
    
    
    
# copy & install Alteryx ----
def copy_alteryx(dst,
                 repo_path = "\\\\DEN-IT-FILE-07\\BuildRepo", 
                 branch = "Predictive_Dev",
                 install_type = "admin"):
    """Copy Alteryx installation file to user appointed directory
    
    Args:
        dst: A string of the directory path you want to copy the file to.
        repo_path: A string of the Alteryx BuildRepo path.
        branch: A string of branch name, default to "Predictive_Dev"
        install_type: A string of 4 options: 'admin', 'non_admin', 'gallery' 
            and 'server'
    
    Returns:
        0 if copy successes, 1 if copy fails.
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
    src = "\\".join([repo_path, latest, "Alteryx", install_file])
    
    cmd = "copy " + '"' + src + '" ' + dst
    return os.system(cmd)

if __name__ == '__main__':
    main()

