# TodoReview
A SublimeText 3 plugin for reviewing todo (any other) comments within your code.

**Check the issues for upcoming features**

This is a fork of @robcowie's SublimeTodo. Unfortunatly, he is unable to maintain it any longer. Additionally, this includes @dnatag's ST3 fork, which allowed me to get this thing fixed relatively quickly. This package will be actively maintained, and is in full working condition for ST3. ST2 will not be supported as the original SublimeTODO should cover you.


# Install
**To be updated once on Package Control.**

# Config


## Adding comment patterns
You can use any RegExp pattern to search by, leaving a lot of room for customization. Each pattern will generate a different group in the results page. For a lean install, only `TODO` comes in the default config. Use the example below to add your own patterns for searching.

**It is important to note that at least one named group must be provided and will be used to group the comments in the results**

```javascript
"patterns": {
    "TODO": "TODO[\\s]*?:+(?P<todo>.*)$",
    "NOTE": "NOTE[\\s]*?:+(?P<note>.*)$",
    "FIXME": "FIX ?ME[\\s]*?:+(?P<fixme>\\S.*)$",
    "CHANGED": "CHANGED[\\s]*?:+(?P<changed>\\S.*)$"
}
```


## Case Sensitive
By default, searching is not case sensitive. If you would like it to force case, you can add the following to your config.

```javascript
    "case_sensitive": true
```



## Excluding files and folders
Obviously, some files or folders might need to be excluded from your search. An example would be your `.git` folder, which has tons of files that will take time to search, with results you most likely will not want.

To exclude directories, add the directory name to `exclude_folders`. Please note, this is not a glob or RegExp field. A preset for your `.git` folder has already been added for you. An example of this:

```javascript
    "exclude_folders": [
        ".git",
        "node_modules"
    ]
```

Additionally, if you would like to exclude individual files, you can base the exclusion on name or glob pattern through `exclude files`. Example of this:

```javascript
"exclude_files": [
    "*.md",
    "dontsearch.txt"
]
```



# Usage
Simply open your Sublime Text 3 Command Pallet and find the `TodoReview: Generate List` command. This will, as the name explains, generate your TODO List. You can then use these results to jump to the corresponding result.

## Navigating results
**Documenation coming after new schema**


#Contributing
All contributions are welcome. I would like to keep this project lean as possible, and not stray to far from the core competency of reviewing comments. Updates will mostly come from maintenence and new features. As far as issues go, please feel free to submit them, but I offer no warranty on this software.


# License
All of SublimeTODO is licensed under the MIT license.

Copyright (c) 2014 Jonathan Delgado

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
