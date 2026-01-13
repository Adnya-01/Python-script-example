import os
import json
import shutil
from subprocess import PIPE, run
import sys

# what we are looking for in the names of the directories
GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go", "build"]


# find paths of all the game directories from the source directory
def find_all_game_paths(source):
    game_paths = []

    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)

        break
    return game_paths



# get only name of the game stripping the "game" aspect
def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)
    return new_names




def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)



# copy files form source to destination and overwrite if it already exists
# recursive copy
def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)



# create json file with metadata about the games
def make_json_metadata_file(path, game_dirs):
    data = {
        "gamenames": game_dirs,
        "numberofgames": len(game_dirs)
    }

    with open(path, "w") as f:
        json.dump(data,f)

# compile go code in a directory (only the first one)
def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break
        break

    if code_file_name is None:
        return
    
    # make command go build filename
    command = GAME_COMPILE_COMMAND + [code_file_name]
    run_command(command, path)

def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)

    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print("Compile result: ", result)

    # change dir back to cwd we were in before we changed dir
    os.chdir(cwd)

def main(source, target):
    # cwd = directory we ran this python file from
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)
    new_game_dirs = get_name_from_paths(game_paths, "_game")

    create_dir(target_path)

    # loop through all of the paths and run the copy function
    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path)


    json_path = os.path.join(target, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)




if __name__ == "__main__":
    # to get command line arguments
    args = sys.argv
    

    # make sure you have correct number of args: filename, source and target
    if len(args) != 3:
        raise Exception("You must pass a source and target directory only.")

    #strip off name of the python file and just get the source and target
    source, target = args[1:]
    main(source, target)

