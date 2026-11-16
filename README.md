LOANDESK LIBRARY SIMULATOR
==========================

A comprehensive command-line application built in Python that acts 
as a library assistant. It manages reading-list requests, tracks 
the library's physical book holdings, and processes batch operations.

The project demonstrates advanced Object-Oriented Programming, 
including data encapsulation, JSON file persistence, custom error 
handling, and complex algorithmic logic for inventory management.


OVERVIEW
--------

The application operates in two distinct modes:
  1. Interactive Mode: Users can enter commands continuously to view 
     requests, check gaps, manage books, and lend out collections.
  2. Single Command Mode: Users can execute a single command directly 
     from the terminal and exit immediately.

The core of this application involves several key algorithms: a Planning 
Analysis to find requests the desk can lend, a Gap Analysis to list missing 
copies for a request, and a Lending flow that marks copies as borrowed.

The desk works from copy counts only. It does not record due dates, 
fines, or patron names. A title is available when copies are still 
on the shelf:
    on the shelf = copies - borrowed


HOW TO RUN
----------

1. Ensure you have Python 3 installed.

2. Run a single command:
   python main.py <command>

3. Enter interactive mode:
   python main.py manage


SUPPORTED COMMANDS
------------------

Commands are case-insensitive. Request names and book titles are matched 
case-insensitively. Names containing spaces must be enclosed in double 
quotes (e.g., "Monday Seminar").

  * Application Mode:
    manage
      Enters the interactive command loop.

  * Request Commands:
    request list
      Prints a simple, numbered list of all request names, in file order.
    
    request view "<request_name>"
      Prints the request name and the books it needs, with the required 
      quantity of each title. (Shows the request itself, not the live shelf).
    
    request gap "<request_name>"
      Performs a gap analysis and prints each title that is short, 
      together with the missing quantity.
    
    request lend "<request_name>"
      Lends the request if every title has enough copies on the shelf. 
      Increases `borrowed` by the needed quantity for each title. `copies` 
      stays the same. If any title is short, reports the missing copies 
      and leaves the holdings unchanged.

  * Holdings (Books) Commands:
    books add "<title>" <quantity>
      Adds the quantity to that title's `copies`. If the title is not in 
      the holdings yet, creates it with `borrowed` set to 0. The quantity 
      must be a positive integer.
    
    books return "<title>" <quantity>
      Subtracts the quantity from `borrowed`. Fails with an error if the 
      quantity is greater than the number currently borrowed, leaving that 
      title unchanged. `copies` stays the same. Returning a title that is 
      not in the holdings fails in the same way.
    
    books process <filepath>
      Reads a text file and executes each line sequentially. Lines have the 
      form: ADD "<title>" <quantity> or RETURN "<title>" <quantity>. 
      Blank lines are ignored. One failing line does not undo earlier lines 
      and does not stop the rest of the file.

  * Analysis Command:
    plan
      Prints every request that can be lent from the current shelf, in 
      file order. A request can be lent when, for every title, 
      `copies - borrowed` is at least the quantity the request needs.

  * Interactive-Only Command:
    exit
      Saves the holdings and terminates the interactive session.


THE SHELF RULE
--------------

Availability is always computed from the two stored numbers:
  * On the shelf = `copies - borrowed`.
  * `plan`, `request gap`, and `request lend` all use that shelf count.
  * The shortfall for a title is `need - (copies - borrowed)` when the 
    need is greater than the shelf count.
  * `books add` changes `copies` only.
  * `books return` changes `borrowed` only.
  * A successful `request lend` adds each needed quantity to `borrowed` 
    and does not change `copies`.
  * The requests file is never modified.


PROJECT STRUCTURE
-----------------

  Main Application:
    - main.py                   : Entry point and argument parser.

  Source Code (loandesk/):
    - requests.py               : The Request class (data model).
    - holdings.py               : The Holdings class (inventory logic).
    - loan_desk_manager.py      : The core controller class managing 
                                  state, commands, and I/O.

  Data & Configuration:
    - config.json               : Points to the data and report files.
    - requests.json             : Sample reading-list requests.
    - holdings.json             : Initial state of the library inventory.
    - batch_commands.txt        : Sample batch file for the process command.


LICENSE
-------

This program is provided as-is for educational and demonstration
purposes. Use and modify it freely.