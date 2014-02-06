# Sublime TODOs

A Sublime Text 2 plugin to extract and list TODO comments from open files and 
project folders.

Take a look at [this screencast](http://webdesign.tutsplus.com/tutorials/applications/quick-tip-streamline-your-todo-lists-in-sublime-text-2/) (courtesy of Shannon Huffman) for an overview.


# Install

The preferred method is to use the [Sublime Package Manager](http://wbond.net/sublime_packages/package_control). Alternatively, checkout from github:

```sh
$ cd Sublime Text 2/Packages
$ git clone https://robcowie@github.com/robcowie/SublimeTODO.git
```

# Config

All plugin configuration must be placed in user or project-specific settings inside a `todo` object, for example;

```javascript
{
    // other user config ...
    "todo": {
        "patterns": {}
    }
}
```

See an example user settings file [here](https://gist.github.com/2049887).


## Adding comment patterns

Extraction uses regular expressions that return one match group 
representing the message. Default patterns are provided for `TODO`, `NOTE`, `FIXME` 
and `CHANGED` comments.
To override or provide more patterns, add `patterns` to user settings, e.g.

```javascript
"patterns": {
    "TODO": "TODO[\\s]*?:+(?P<todo>.*)$",
    "NOTE": "NOTE[\\s]*?:+(?P<note>.*)$",
    "FIXME": "FIX ?ME[\\s]*?:+(?P<fixme>\\S.*)$",
    "CHANGED": "CHANGED[\\s]*?:+(?P<changed>\\S.*)$"
}
```

Note that the pattern _must_ provide at least one named group which will be used to group the comments in results.

By default, searching is not case sensitive. You can change this behaviour by adding 

    "case_sensitive": true

to the todo settings object.


## Excluding files and folders

Global settings `folder_exclude_patterns`, `file_exclude_patterns` and `binary_file_patterns` are excluded from search results.

To exclude further directories, add directory names (not glob pattern or regexp) to `folder_exclude_patterns` in todo settings:

```javascript
"todo": {
    "folder_exclude_patterns": [
        "vendor", 
        "tmp"
    ]
}
```

To add file excludes, add glob patterns to `file_exclude_patterns`:

```javascript
"file_exclude_patterns": [
    "*.css"
]
```


## Results title

Override the results view title by setting `result_title`

```javascript
"result_title": "TODO Results"
```

# Usage

`Show TODOs: Project and open files` scans all files in your project
`Show TODOs: Open files only` scans only open, saved files
Both are triggered from the command palette. No default key bindings are provided.

## Navigating results

Results can be navigated by keyboard and mouse:

 * `n`ext, `p`revious, `c`lear, `enter`
 * `alt-double click` (`shift-double click` in Linux)

 Note that due to the lack of support for context in mousemaps right now,
 alt-double click will trigger in _any_ document, though it should be a no-op.

# License

All of SublimeTODO is licensed under the MIT license.

Copyright (c) 2012 Rob Cowie <szaz@mac.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
