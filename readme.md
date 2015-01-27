# TodoReview
A SublimeText plugin for reviewing todo (and other) comments within your code.

![ScreenShot](http://i.imgur.com/0kTJ3cU.png)

**Check the issues for upcoming features**

This is a fork of [@robcowie's](https://github.com/robcowie) SublimeTodo. Unfortunately, it doesn't have ST3 support and he is unable to maintain it any longer. Additionally, this includes [@dnatag's](https://github.com/dnatag) ST3 fork, which allowed me to get everything fixed relatively quickly.


# Install

#### [Package Control](https://sublime.wbond.net/) (Recommended)
TodoReview is accessible on Package Control. If you do not have Package Control, follow these [instructions](https://sublime.wbond.net/installation) to install it, it's extremely useful. Once you have it installed, just bring up your command pallet, type in `Install Package` then, on the next prompt, `TodoReview` and you are set!

#### Git Clone
If you are forking this project, or for whatever reason do not want to use Package Control, you can install this package this old fashion way. First, figure out where your packages directory is by going to (Preferences -> Browse Packages) - then just run git clone as normal.


# Usage
Simply open your Sublime Text Command Pallet and find the `TodoReview: Project Files` command. This will generate your TODO List using all files that are currently in your project, except the ones which are excluded in your settings. If you would like to also include your open files within the search, you can use the `TodoReview: Project and Open Files` command; it's that easy! You can then use these results to jump to the corresponding result. Additionally, you can right click a file or folder in your sidebar and select TodoReview to limit your search.

## Navigating results
Once the list is generated, as a swift coder, you must naturally want to navigate it with your keyboard, right? Well you are in luck!

By pressing the `up` or `down` keys, you are able to swiftly navigate the results. If you are a VIM user, you can also use `j` and `k` respectably. You can also use `page up` or `page down` to skip 10 lines at a time. Once you have navigated to the result you want, simply press `enter` to open the result in a new tab, while going to the corresponding line. You can also refresh the list at any time by pressing `r`, it uses the same arguments as the last search.

## Priorities
New in 2.1.0, results are now fully indexed and sorted. You can now add something like `(0)` to anywhere in your todo's to assign a priority of `0`. This will work with any number up to 99. Todo's are then sorted with the lowest number first; all matches that don't have priorities will be assigned a priority of 100. Here is some example output:

```
// Tuesday 09/30/14 at 10:46AM - 27 files in 0.16 secs

## TODO (5)
1. 3.0.0.txt:3   Press `r` to refresh! (1)
2. readme.md:1   Take a screenshot
3. readme.md:2   Document goodies
4. 3.0.0.txt:1   Make sure @tags work
5. 3.0.0.txt:2   Other [formatting] too

## TEST (2)
1. 3.0.0.txt:4   (2) Priorities work?
2. 3.0.0.txt:5   Read from buffer
```

## Color Scheme
You can tag tasks using something like `@tomorrow` or `@bug`. These are only example, anything following the `@` sign, before a space, will be highlighted accordingly. If you are like me, you also would like one more option, just in the event something really needs to stand out, perhaps a reference link, etc. You can also use `[Comment]` or `[Need To Test]` for another type of reference as needed. Unlike tags with the `@` sign, you can use spaces between brackets.

The way that these are colored depends on your color scheme. It's been a pain point of sublime text for quite some time that plugins are unable to influence the color scheme without some manual edits. I use and would recommend the [Tomorrow Night](https://github.com/theymaybecoders/sublime-tomorrow-theme) color scheme. However, if you are not, here are the corresponding colors these tags will be:

- **Report Headers** are the same color as a *comment*
- **Pattern Titles** are the same color as a *string*
- **Line Numbers** are the same color as a *function*
- **Priority** are the same color as a *variable*
- **Bracket Tags** are the same color as a *class*
- **@Tags** are the same color as a *keyword*

These may change in the future, but for now, this is the best way of to handle highlighting differences.


# Config
Global configuration can be set within the standard package settings menu (Preferences -> Package Settings -> TodoReview) however, this plugin also offers project specific settings. To override your global settings on a project basis, edit your `.sublime-project` file accordingly, more information on settings below:

```javascript
{
    "folders": [],
    "settings": {
        "todoreview": {
            "exclude_folders": [
                "*.git"
            ]
        }
    }
}

```

## Adding comment patterns
You can use any RegExp pattern to search by, leaving a lot of room for customization. Each pattern will generate a different group in the results page. For a lean install, only `TODO` comes in the default config. Use the example below to add your own patterns for searching. For more information on regex, please visit [Regex 101](http://regex101.com) and try the default patterns out.

**It is important to note that at least one named group must be provided and will be used to group the comments in the results**

```javascript
"patterns": {
    "TODO": "TODO[\\s]*?:[\\s]*(?P<todo>.*)$",
    "NOTE": "NOTE[\\s]*?:[\\s]*(?P<note>.*)$",
    "FIXME": "FIX ?ME[\\s]*?:[\\s]*(?P<fixme>.*)$",
    "CHANGED": "CHANGED[\\s]*?:[\\s]*(?P<changed>.*)$"
}
```

## Comment pattern weight
In case you want a non-alphabetical sort of the patterns, you can use the `patterns_weight` setting. There are some very important notes about this setting. Firstly, the key MUST be upper case, or the setting will not work. The key must also match the pattern named group. The value can be either a number or string, it is just evaluated as an alphabetical override. All patterns not mentioned will retain the same alphabetical weight versus the new values. Example:

```javascript
"patterns_weight": {
	"NOTE": 3,
    "TEST": "z"
}

//Order:
//Note
//Fixme
//Todo
//Test
```

## Excluding files and folders
Obviously, some files or folders might need to be excluded from your search. An example would be your `.git` folder, which has tons of files that will take time to search, with results you most likely will not want.

To exclude directories, add the directory name to `exclude_folders`. This is a glob field, so make sure to add wildcards where needed. A preset for your `.git` folder has already been added for you. An example of this:

```javascript
"exclude_folders": [
    "*.git*",
    "*node_modules*"
]
```

Additionally, if you would like to exclude individual files, you can base the exclusion on name or glob pattern through `exclude files`. Example of this:

```javascript
"exclude_files": [
    "*.sublime-workspace",
    "*.sublime-project"
]
```

## Include Directories
Though it may be unnecessary for most, I've also included a setting to override the default path, allowing for only specific folders to be searched. This is NOT a glob setting, rather absolute paths to the folders you would like searched, possibly even outside of your project. Please note, this setting is overridden by a `paths` argument being passed to the command; for example, the sidebar shortcut will still operate as normal, independent of this setting. Example of this:

```javascript
"include_paths": [
    "~/currentproject/folder",
    "~/Users/Jonathan/anotherfolder"
]
```

## Case Sensitive
By default, searching is not case sensitive. If you would like it to force case, you can add the following to your config. This defaults to `false`.

```javascript
"case_sensitive": true
```

## Encoding
If you are planning on using any non UTF-8 characters in your comments, you may need to change this setting to your file encodings for a project. Please note, this setting doesn't affect currently opened files, since Sublime Text handles the encoding on buffered files. All files that need to be opened are done so though python, this setting directly affects the encoding as files are opened. The default is `utf-8`.

```javascript
"encoding": "western-258"
```

## Include folders in results
If you have a large project with repeating file names, it is sometimes useful to also have the file's folder displayed in the results. This would turn the result `index.js:1` to `lib/index.js:1`. Results are sorted alphabetically to group folders and files together. Please note that results are sorted by priority first. This defaults to `false`.

Additionally, if you choose to include folders in your report, you may also specify the folder depth for your report paths.

```javascript
"render_include_folder": true,
"render_folder_depth": 5
```

## Align results
TodoReview now automatically aligns the comments for you, calculating the largest result and aligning the rest accordingly. The system default for maximum spaces is `50`, which prevents a single file with an abnormally long length completely ruining your results. You can change this setting by editing `render_maxspaces`

```javascript
"render_maxspaces": 100
```

## Report Header
if you ever feel the overwhelming urge to either remove or edit the standard report header, you can now do so by editing `render_header_format` and `render_header_date`. Both use standard regex replacement to create the report header. Setting the `render_header_format` to a blank string will completely remove the header all together. Example:

```javascript
"render_header_format": "%d - %c files in %t secs",
"render_header_date": "%A %m/%d/%y at %I:%M%p"
```

- **%d** - the formatted date string
- **%c** - the total file count
- **%t** - the total time count
- The date formatting can be found in the [Python Documentation](https://docs.python.org/2/library/datetime.html)

## Custom Skip Lines
If you would like to skip more (or less) than 10 lines at a time when using `page up` or `page down`, we have a setting for you! These defaults to `10`.

```javascript
"navigation_forward_skip": 10,
"navigation_backward_skip": 10
```

# Arguments
The TodoReview search engine takes a number of arguments to better find what you are looking for. These are automatically generated on a number of sugar functions, such as using the sidebar or command pallet, but you can also create your own keybinds to utilize them.

- `paths` - An array of paths to search
- `open_files` - Boolean to include open files
- `open_files_only` - Boolean to restrict search to open files
- `settings` - A settings object; this will override ALL project settings.


# License

The MIT License (MIT)

Copyright (c) 2014 Jonathan Delgado

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
