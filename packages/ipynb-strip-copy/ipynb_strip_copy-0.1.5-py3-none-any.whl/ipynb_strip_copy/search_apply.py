from collections import defaultdict
from copy import copy
import re

from ipynb_strip_copy.command import all_command

ORIG_CMD_STRIP = 'ORIGINAL-CMD-STRIPPED'


def search_command(cell_text, s_cmd_start='\n?[ ]*#!', s_cmd_end='\n'):
    """ finds all commands, parses suffix

    >>> cell_text = r'012345#!some-command-here: suffix1, suffix2END'
    >>> cell_text_out, command_dict = search_command(cell_text,
    ...     s_cmd_end='END') # doctest doesn't like newlines
    >>> cell_text_out
    '012345'
    >>> command_dict
    {'suffix1': [('some-command-here', 6)], 'suffix2': [('some-command-here', 6)]}

    Args:
        cell_text (str): text of a jupyter cell
        s_cmd_start (str): start of any command
        s_cmd_end (str): end of any command

    Returns:
        cell_text (str): text of jupyter cell (all commands removed)
        command_dict (dict): keys are suffix, values are command_list.  a
            command_list is a list of (cmd_text, idx) tuples.  cmd_text are the
            observed commands and idx refers to their found location in
            the returned cell_text
    """

    # keys are suffix, values are list of (cmd_text, idx)
    command_dict = defaultdict(list)

    while True:
        match_start = re.search(s_cmd_start, cell_text)
        if match_start is None:
            break

        idx_start = match_start.start()
        match_end = re.compile(s_cmd_end).search(cell_text,
                                                 pos=match_start.end())

        if match_end is None:
            # assume command goes to end of text
            idx_end = len(cell_text)
        else:
            idx_end = match_end.end()

        # store command and remove from cell_text
        s_cmd_full = cell_text[idx_start: idx_end]
        cell_text = cell_text[:idx_start] + cell_text[idx_end:]

        # parse command
        cmd, suffix_csv = s_cmd_full.split(':')
        cmd = cmd.split(' ')[-1].strip()
        for suffix in suffix_csv.split(','):
            command_dict[suffix.strip()].append((cmd, idx_start))

    return cell_text, dict(command_dict)


def apply_command(cell_text, command_dict):
    """ applies a list of commands to cell_text

    note: assumes all commands are commutative (snip, rm-cell, clear-cell are)

    Args:
        cell_text (str): text of jupyter cell (all commands removed)
        command_dict (dict): keys are suffix

    Returns:
        suffix_text_dict (dict): keys are suffixes, values are text of all
            commands applied
    """
    assert ORIG_CMD_STRIP not in command_dict.keys()

    suffix_text_dict = {ORIG_CMD_STRIP: cell_text}
    for suffix, command_list in command_dict.items():
        _cell_text = copy(cell_text)
        for command in all_command:
            # find locations which refer to command
            _command_list = [(cmd, idx) for (cmd, idx) in command_list
                             if command.s_target in cmd]

            # apply command
            if _command_list:
                _cell_text = command.apply(_cell_text, _command_list)

            if _cell_text is None:
                # not great design ... but cell remove returns cell_text=None
                break

        suffix_text_dict[suffix] = _cell_text

    return suffix_text_dict


def search_apply_command(cell_text):
    _cell_text, command_dict = search_command(cell_text)
    return apply_command(_cell_text, command_dict)
