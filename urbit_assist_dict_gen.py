# after cloning the docs repo, run in the repo's parent directory

'''
Definition of PATH_CONFIG
--------------------------
[
  {
    "path" : "/home/mbc/projects/docs/hoon/reference/rune/",
    "parse_here" : true,
    "recursive" : false,
    "parser" : "one_char_rune"
  },
  {
    "path" : "/home/mbc/projects/docs/hoon/reference/rune/",
    "parse_here" : false,
    "recursive" : true,
    "parser" : "two_char_rune"
  },
  {
    "path" : "/home/mbc/projects/docs/hoon/reference/stdlib/",
    "parse_here" : true,
    "recursive" : true,
    "parser" : "library"
  }
]
'''

import json
import mistune
import os

# configuration attributes
PATH = '/home/mbc/projects/hoon-assist-emacs'
PARSE_HERE = 'parse_here'
RECURSIVE = 'recursive'
PARSER = 'parser'

# i/o constants
READ = 'r'
WRITE = 'w'
PATH_CONFIG = 'path_config.json'
DICTIONARY = 'hoon-dictionary.json'

# types of parsers
ONE_CHAR_RUNE = 'one_char_rune'
TWO_CHAR_RUNE = 'two_char_rune'
LIBRARY = 'library'

def key_doc_mapping(key_doc_tuple):
    return { 'keys' : [key_doc_tuple[0]], 'doc' : mistune.markdown(key_doc_tuple[1])}


def rune_key_parser(path, position):
    # parsing runes only differs by one index position
    header = '---'
    identifier = 'title:'
    separator = ' '

    f = open(path, READ)
    f_data = f.read()
    f.close()

    key = f_data.split(header)[1].split(identifier)[1].strip().split(separator)[position]
    documentation = f_data.split(header)[2]

    return (key, documentation)

def one_char_rune_parser(path):
    return key_doc_mapping(rune_key_parser(path, 1))


def two_char_rune_parser(path):
    return key_doc_mapping(rune_key_parser(path, 0))


def library_parser(path):
    entry_identifier = '### '
    dry_arm_identifier = '++'
    wet_arm_identifer = '+-'
    title_header = '# '

    f = open(path, READ)
    f_data = f.read()
    f.close()

    arm_doc_list = []

    arm_list = f_data.split(entry_identifier)[1:]
    for arm in arm_list:
        # maybe not necessary, but if an index error is thrown due to no dry
        # arm identifer then try a wet one, otherwise forget about it
        try:
            key = arm.split('\n')[0].split(dry_arm_identifier)[1][:-1]
        except:
            try:
                key = arm.split('\n')[0].split(wet_arm_identifier)[1][:-1]
            except:
                continue

        # need to change format from h3 to h1
        arm = title_header + arm
        arm_doc_list.append(key_doc_mapping((key, arm)))

    return arm_doc_list


def call_parser(path, parse_here, recursive, parser):
    '''
        + Get the list of everything in the current path
        + If parsing this directory, parse all files in this directory and
          add the results to the list
        + If parsing recursively, make the recursive call where path is each
          subdirectory, parser is the parser, and parse_here and recursive are
          always true because parse_here only applies to the root directory and
          recursive must be true if we're making a recursive call. Add results
          from the recursive call to the list
        + Return the results
    '''
    dict_list = []
    dir_list = os.listdir(path)

    if parse_here:
        for file in dir_list:
            full_name = os.path.join(path, file)
            if os.path.isfile(full_name):
                result = parser(full_name)

                # a different data type will be returned depending on whether
                # the libray or rune function is being used
                if isinstance(result, list) and len(result) != 0:
                    dict_list += result
                else:
                    dict_list.append(parser(full_name))

    if recursive:
        for file in dir_list:
            full_name = os.path.join(path, file)
            if os.path.isdir(full_name):
                result = call_parser(full_name, True, True, parser)
                if len(result) != 0:
                    dict_list += result

    return dict_list


def get_parser(parser_name):
    if parser_name == ONE_CHAR_RUNE:
        return one_char_rune_parser
    elif parser_name == TWO_CHAR_RUNE:
        return two_char_rune_parser
    elif parser_name == LIBRARY:
        return library_parser
    else:
        return None


def extract_data(path_info):
    # figure out which parser to use
    parser = get_parser(path_info[PARSER])
    if parser == None:
        return []

    # call the function that will traverse the directory structure
    return call_parser(path_info[PATH], path_info[PARSE_HERE], path_info[RECURSIVE], parser)


def get_path_config(filename):
    config_file = open(filename, READ)
    config_data = config_file.read()
    config_file.close()
    return json.loads(config_data)


def write_dict_file(key_list, filename):
    dict_file = open(filename, WRITE)
    # make it readable
    dict_file.write(json.dumps(key_list, indent=2))
    dict_file.close()


def main():
    # grab the configuration and read it into a dict
    path_config = get_path_config(PATH_CONFIG)

    # the dictionary to eventually stringify write to the dictionary file
    dict_list = []

    # add the keys from each path in the configuration to the dictionary list
    for entry in path_config:
        dict_list += extract_data(entry)

    # clean up any that slipped through
    for entry in reversed(dict_list):
        if entry == []:
            dict_list.remove(entry)

    # write out the finished file
    write_dict_file(dict_list, DICTIONARY)

if __name__ == '__main__':
    main()
