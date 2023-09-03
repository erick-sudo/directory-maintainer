# Directory Maintainer

As a tools software engineer at a factory site, the Reporting and Data Team has asked for your assistance. They have generated a messy backlog of files as part of their work, and they'd like your help to categorize the files.

Right now, their team adds different files into one main backlog for later usage. As the number of files has grown, it's gotten harder and harder for their team to find the files they need.

Their current backlog has three types of files:

```
- .csv
- .log
- .txt
```

Your task is to write a program to help move the files in backlog into a more usable structure.

# Requirements

The Reporting and Data Team lead gave you the following requirements for the directory maintainer program:

*Target Directory*:
- The program needs to accept a path to a target directory as a command line argument
- That directory is the one that should be cleaned up

*File Categorisation*:
- Within the main folder, create a new folder for each file extension type.
- Move the files of each type into that folder.
- The folder name should be the file extension. (e.g. the `csv` folder should contain all the `.csv` files).

*Log Retention*:
- The data retention policy for logs states that you should only keep logs up to a specific `log-window` value. Your program should make sure that the `log` folder only keeps that number of files.
- The `log-window` will be passed into your program as a command line argument (this is handled by the starter code)
- For example - if the `log-window` is 5, then the folder should have the most recent 5 log files only -- the others should be deleted.
- The default retention policy is 30 days -- the default value of the argument is 30.
- Conveniently, log files are named starting with the date, formatted YYYYMMDD, so you should be able to sort them alphabetically to get the most recent ones.

*Large Files*:
- Within the txt folder, files with a size greater than a `size-threshold` should be moved into a separate directory inside `txt` called `large_txt_files`.
- The size threshold value will be an int value passed in as a command line
    argument, and represents a file size in KB.
- The default file size, if nothing is passed in, is 50KB.

If there are any other files in the directory, your program should print a message with the file name, but should not move the file. For example:

```
Unknown extension: Q3-board-mtg-final2-FINAL.pdf
```

## Use Case

A user would run your program like this:

```sh
python3 main.py ./directory/to/clean
```

And the program should organize the files in that directory.

The program should also accept command-line flags to control the log window and size threshold, per the
requirements above.

```sh
python3 main.py ./directory/to/clean --log-window=10 --size-threshold=20
```

## Starter Code

You've been provided with the argument-handling code that reads the `directory`, `--log-window`, and `--size-threshold` values from the command line. It calls the `clean_directory` function and passes in the values.

You need to implement the `clean_directory` function. It may be helpful to split the work into multiple helper functions.

 ## Output Snapshot

 If we have a directory that looks like the following:

```txt
- backlog
  - sheet_1.csv
  - sheet_2.csv
  - 20221002_component_x.log
  - employees_i.txt
  - employees_ii.txt
  - 20221003_component_y.log
  - 20221001_component_z.log
```

After running your program like this:

```sh
python3 main.py backlog
```

Afterwards, the directory should be structured like this:

```txt
- backlog
  - csv
    - sheet_1.csv
    - sheet_2.csv
  - log
    - 20221001_component_z.log
    - 20221002_component_x.log
    - 20221003_component_y.log
  - txt
    - employees_i.txt
    - large_txt_files
      - employees_ii.txt
```

 ## Hints

- It may be helpful to make backup copies of directories as you test your code,
     since if it works, it will actually move files around.
- Before you actually make the code move the files, it might be helpful to print
    out the files to be moved and their destinations, so that you can see that
    your logic will work correctly.
