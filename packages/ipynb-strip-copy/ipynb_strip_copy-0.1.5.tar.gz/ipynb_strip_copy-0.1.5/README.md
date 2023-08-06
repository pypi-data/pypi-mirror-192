# ipynb_strip_copy is deprecated

Please use [snip-copy](https://github.com/matthigger/snip_copy) instead.  Note that snip-copy doesn't contain the functionality of the `--sum-pts` flag here (planned as a separate repo, will update this message when complete).

# Description

Command line tool to detect text in a jupyter notebook cell and process
accordingly (remove the cell, clear its contents or snip a section). Our
motivation is to allow users to maintain a "rubric" `ipynb` file from
which the "solution" and "student" copies can be created quickly.

## Installation

    pip install ipynb_strip_copy

## Quick-Start

Open
up [demo_rubric.ipynb](https://github.com/matthigger/ipynb_strip_copy/blob/main/demo_rubric.ipynb)
and use the
command line interface via the jupyter magic command `!`:

    !python -m ipynb_strip_copy demo_rubric.ipynb

## Usage

Commands are explicitly written into the jupyter notebook's markdown or code cells and have the form:

    #! rm: student, sol

The command above implies the removal of its containing cell when
the 
- `<orig_file_name>_student.ipynb`
- `<orig-file-name>_sol.ipynb`

outputs are created via `python -m ipynb_strip_copy demo_rubric.ipynb`. The text of any command (i.e. `#! rm: student, sol` is removed in all outputs).

### `#! rm`

Removes the cell entirely

### `#! clear`

Clears cell of any contents

### `#! snip-start` / `#! snip-end`

Snips a section of text within the cell. For example:

    # here be starter code, given to students on assignment
    x = defaultdict(list)
    
    #! snip-start: student
    # solution
    #! snip-end: student

will generate output `<orig_file_name>_student.ipynb` whose corresponding cell
contains only:

    # here be starter code, given to students on assignment
    x = defaultdict(list)

## Counting Points

If the `--sum-pts` flag is passed (i.e. `!python -m ipynb_strip_copy demo_rubric.ipynb --sum-pts`) then we'll search markdown cells for "problems" and print a list of problems, their associated points and the total points for the whole assignment:

    | question              |   points |
    |:----------------------|---------:|
    | problem: example      |      123 |
    | part: another example |       28 |
    | total                 |      151 |


- points must be integers
- A problem is defined by the first match of regular expression: `(part|problem).+\(\d+ *(points|pts)[^\(]*\)` on a line where we map characters to their lowercase version beforehand.  See [test_case_points.ipynb](test/test_case_points.ipynb) for some examples.