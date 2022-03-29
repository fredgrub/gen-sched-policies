import os
from subprocess import check_call, STDOUT
from tabnanny import check

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

BUILD_ROOT = '/opt'
TARGET_DIR = '/opt/simgrid'
CLONE_DIR = 'simgrid-313'
SIMGRID_URL = 'https://framagit.org/simgrid/simgrid.git'
SIMGRID_VERSION = 'v3_13'

def install_dependencies():
    print(bcolors.OKGREEN + bcolors.BOLD + "Installing dependencies" + bcolors.ENDC)
    sys_wide_cmd = [
        'sudo', 'apt-get', 'install', '-y',
        'python3', 'git', 'gcc-4.8', 'g++-4.8',
        'g++', 'cmake', 'libboost-context-dev',
        'libboost-dev', 'doxygen', 'transfig'
        ]
    python_cmd = [
        'sudo', 'apt-get', 'install', '-y',
        'python3-numpy', 'python3-scipy', 'python3-matplotlib'
        ]

    print('=> Updating system')
    check_call(['sudo' 'apt-get', 'update', '-y'],
     stdout=open(os.devnull,'wb'), stderr=STDOUT)
    print('=> Installing system-wide dependencies')
    check_call(sys_wide_cmd, 
     stdout=open(os.devnull,'wb'), stderr=STDOUT)
    print('=> Installing python3 dependencies')
    check_call(python_cmd,
     stdout=open(os.devnull,'wb'), stderr=STDOUT)

def main():
    print(bcolors.OKBLUE + bcolors.BOLD +
     "-- AWS SIMGRID Setup Script --" + bcolors.ENDC)
    
    # install dependencies
    install_dependencies()

    print(bcolors.OKGREEN + bcolors.BOLD +
    "Building simgird" + bcolors.ENDC)

    print('=> Prepare (1/3)')
    os.chdir(BUILD_ROOT)
    check_call(['sudo', 'rm', '-f', TARGET_DIR],
     stdout=open(os.devnull,'wb'), stderr=STDOUT)
    check_call(['ln' '-s', CLONE_DIR, TARGET_DIR],
     stdout=open(os.devnull,'wb'), stderr=STDOUT)
    
    print('=> Clone (2/3)')
    check_call([
        'sudo', 'git', 'clone', '-b', SIMGRID_VERSION,
        '--single-branch', SIMGRID_URL, CLONE_DIR
        ],
         stdout=open(os.devnull,'wb'), stderr=STDOUT)
    
    print('=> Build (3/3)')
    os.chdir(TARGET_DIR)
    check_call([
        'sudo', 'cmake', '-DBUILD_SHARED_LIBS=OFF',
        '-DCMAKE_INSTALL_PREFIX=%s'%TARGET_DIR,
        ])
    check_call([
        'sudo', 'make', '&&', 'make', 'check',
        '&&', 'make', 'install'
        ])
    check_call([
        'sudo', 'ln', '-s', '/opt/simgrid/lib/libsimgrid.so',
        '/usr/lib/libsimgrid.so', '&&', 'ln', '-s',
        '/opt/simgrid/lib/libsimgrid.so.3.13',
        '/usr/lib/libsimgrid.so.3.13'
        ])
    print(bcolors.OKBLUE + bcolors.BOLD +
    "Finished" + bcolors.ENDC)
    

if __name__ == "__main__":
    main()