# Sublime Text Plugins

These are the plugins I have made for myself. You may or may not find something (anything?) useful here. I'll update the README with descriptions as needed.

## datetimestamp.py
This one is for date/timestamping your files. It contains four commands that you can bind to key shortcuts or stick in the context menu. They are:

- add_date_stamp: inserts 2013-01-31;
- add_time_stamp: inserts 13:31;
- add_date_time_stamp: inserts 2013-01-31 13:31;
- add_dated_comment: inserts # 2013-01-31 | zue: 

You may want to modify the last one, it has two variables that are easy to change. USER is your username ("zue" in my case), COMMENT is your symbol that comments a line ("#" in my case).

## create4glcontents.py
This one scans your currently opened file for function names, inserts an md5 hash beneath them and then inserts a table of contents on the line the cursor is in. You have to look inside and set a couple of variables for it to work for you, but it's nicely commented and it should be fairly easy to set them. The function checks not to insert duplicate md5's and recreates the ToC each time it is called, deleting the old one.

To add the command use create_contents.

## createpervariables.py
This plugin scans your .per file for variables in the screen form, and inserts a block in the form of:

```
ATTRIBUTES
    firstVariable  = FORMONLY.
    secondVariable = FORMONLY.
    thirdVariable  = FORMONLY.
END
```

You can modify the REGEXPs and tabsize in the script.
