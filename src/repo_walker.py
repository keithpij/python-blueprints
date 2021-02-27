'''
This module contains tools to collect import data from Python code.

Note: 
Since there are a lot of file path creation tools in this module it is
important to use os.path.join becuase Windows and Mac have a different
way of constructing file paths.  Windows uses a backslash '\' and file paths
Linux and Apple use a forward slash '/'.  os.path.join will do the right
thing based on the current platform.
'''
import argparse
import json
import os
import sys


def find_repos(base_dir):
    '''
    This function will return a list of repos (directories) found in the base dir.
    It assumes that only folders which represent repos are in the base directory.
    '''
    repos = [os.path.join(base_dir, o) for o in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir,o))]
    repos.sort()
    return repos


def list_repos(base_dir):
    '''
    This function should be passed the root directory of a collection of related repositories.
    '''
    repo_list = find_repos(base_dir)
    for repo_dir in repo_list:
        print(repo_dir)
    print(len(repo_list))


def find_imports_for_all_repos(base_dir):
    repo_list = find_repos(base_dir)
    repo_map = {}
    for repo_dir in repo_list:
        print(repo_dir)
        module_map = find_imports_for_repo(repo_dir)
        repo_map[repo_dir] = module_map
    return repo_map


def find_imports_for_repo(repo_dir):
    '''
    This function should be passed the directory of a single repository.
    '''
    count = 0
    module_map = dict()

    for (sub_dir, dirs, files) in os.walk(repo_dir):
        for file_name in files:
            if file_name.endswith('.py'):
                count = count + 1

                file_path = sub_dir + os.sep + file_name
                fhand = open(file_path)

                # Loop through the file.
                all_modules = []
                for line in fhand:
                    line = line.strip()
                    if line.startswith('import '):
                        line = line[7:]
                        line_modules = line.split(',')
                        for module in line_modules:
                            if ' as ' in module:
                                module = module.split(' ')[0]
                        all_modules.append(module)

                fhand.close()
                module_map[file_name] = all_modules

    return module_map


if __name__ == '__main__':
    #BASE_DIR = '/Users/keithpij/code'

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--walk', help='Walk repos in the specified directory.')
    parser.add_argument('-l', '--list', help='List all repos in the specified directory.')
    args = parser.parse_args()

    if args.list:
        list_repos(args.list)
    if args.walk:
        repo_map  = find_imports_for_all_repos(args.walk)
        print(json.dumps(repo_map))
