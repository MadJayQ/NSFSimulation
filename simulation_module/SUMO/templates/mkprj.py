# mkprj.py
# Author: Quentin Goss
# Last Modified: 01/23/2019
#
# Makes a blank SUMO project to specified location (default ./)
import optparse
import os
import shutil

def main():
    options = get_option()
        
    # path of this file
    abs_path = os.path.dirname(os.path.abspath(__file__))
    
    # Move to the work folder
    os.chdir(options.dir)
    os.system('mkdir ' + options.name_prj)
    os.chdir(options.dir + options.name_prj)
    os.system('mkdir data')
    os.system('mkdir ' + options.name_mod)
    
    # Add the template stuff to the data directory
    os.chdir('./data')
    copy_file(abs_path + '/project/data/blank.net.xml',options.name_prj + '.net.xml')
    if options.is_poly:
        copy_file(abs_path + '/project/data/blank.poly.xml',options.name_prj + '.poly.xml')
    copy_file(abs_path + '/project/data/blank.rou.xml',options.name_prj + '.rou.xml')
    copy_file(abs_path + '/project/data/blank.settings.xml',options.name_prj + '.settings.xml')
    sumo_cfg(abs_path + '/project/data/blank.sumocfg',options.name_prj + '.sumocfg',options.name_prj,options.is_poly)
    
    # Setup the first module
    os.chdir('../' + options.name_mod)
    copy_file(abs_path + '/project/ex0/runner.py','runner.py')
    copy_file(abs_path + '/project/ex0/core.py','core.py')
    copy_file(abs_path + '/project/ex0/run.bat','run.bat')
    copy_file(abs_path + '/project/ex0/run.nogui.bat','run.nogui.bat')
    config_py(abs_path + '/project/ex0/config.py','config.py',options.name_prj,options.sumo_tools)
    
    # hhh
    if False:
        shutil.copytree('./project',options.dir + options.name_prj)
        
        os.chdir(options.dir + options.name_prj)
        os.system('dir')
# end def main

def get_option():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("-d","--dir",type="string",default="./", help="Directory to place project [default ./]",dest="dir")
    opt_parser.add_option('-n','--name',type="string",default=None, help="Project name",dest="name_prj")
    opt_parser.add_option('-m','--module_name',type="string",default='ex0', help="First module name [default ex0]", dest='name_mod')
    opt_parser.add_option('-p','--polygon',action="store_true",dest='is_poly', default=False, help='Add polygon files and setting. [default FALSE]')
    opt_parser.add_option('-t','--sumo_tools',type="string",default="C:/Program Files (x86)/Eclipse/Sumo/tools", help="The location of the SUMO tools dirctory [default C:/Program Files (x86)/Eclipse/Sumo/tools]",dest="sumo_tools")
    
    options, args = opt_parser.parse_args()

    if options.name_prj == None:
        raise Exception('Project name cannot be None.')
    
    return options
# end def get_options

def copy_file(src,dst):
    with open(src,'r') as fsrc:
        with open(dst,'w') as fdst:
            for line in fsrc:
                fdst.write(line)
# end def copy_file

def sumo_cfg(src,dst,prj,is_poly):
    with open(src,'r') as fsrc:
        with open(dst,'w') as fdst:
            for line in fsrc:
                if "<net-file" in line:
                    fdst.write('\t\t<net-file value="' + prj + '.net.xml" />\n')
                    continue
                elif "<route-files" in line:
                    fdst.write('\t\t<route-files value="' + prj + '.rou.xml" />\n')
                    continue
                elif "<additional-files" in line:
                    if not is_poly:
                        continue
                    else:
                        fdst.write('\t\t<additional-files value="' + prj + '.poly.xml" /> <!-- OPTIONAL -->\n')
                        continue
                elif "<gui-settings-file" in line:
                    fdst.write('\t\t<gui-settings-file value="' + prj + '.settings.xml" />\n')
                    continue
                else:
                    fdst.write(line)
                    continue
# end sumo_cfg

def config_py(src,dst,prj,sumo_tools):
    with open(src,'r') as fsrc:
        with open(dst,'w') as fdst:
            for line in fsrc:
                if "s_project_name =" in line:
                    fdst.write("s_project_name = '" + prj + "'\n")
                    continue
                elif "s_sumo_tools_dir =" in line:
                    fdst.write("s_sumo_tools_dir = '" + sumo_tools + "'\n")
                    continue
                elif "#      ex0 configuration" in line:
                    fdst.write("#      " + prj + " configuration")
                    continue
                else:
                    fdst.write(line)
                    continue
# end def config_py

main()
