# TodoReview
A SublimeText 3 plugin for reviewing todo (any other) comments within your code.

**Check the issues for upcoming features**

This is a fork of [@robcowie's](https://github.com/robcowie) SublimeTodo. Unfortunately, it doesn't have ST3 support and he is unable to maintain it any longer. Additionally, this includes [@dnatag's](https://github.com/dnatag) ST3 fork, which allowed me to get everything fixed relatively quickly.


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
Once the list is generated, as a swift coder, you must naturally want to navigate it with your keyboard, right? Well you are in luck!

By pressing the `up` or `down` keys, you are able to swiftly navigate the results. If you are a VIM user, you can also use `j` and `k` respectably. Once you have navigated to the result you want, simply press `enter` to open the result in a new tab, while going to the corresponding line.

In the event you would like to clear your selection, you may do so by pressing `c`.

##Color Scheme
One new feature that wasn't on SublimeTodo is the ability to tag and prioritize tasks (or whatever you are searching for). For the initial release, you are able to use `@priority`, `@critical` or `[priority]`, `[critical]` to keep track of your more important tasks. Right now, this only turns it a unique color, but down the line, the system will actually sort results with a priority hierarchy.

Additionally, you can tag tasks using something like `@tomorrow` or `@bug`. These are only example, anything following the `@` sign, before a space, will be highlighted accordingly. If you are like me, you also would like one more option, just in the event something really needs to stand out, perhaps a reference link, etc. You can also use `[Comment]` or `[Need To Test]` for another type of reference as needed. Unlike tags with the `@` sign, you can use spaces between brackets.

The way that these are colored depends on your color scheme. It's been a pain point of sublime text for quite some time that plugins are unable to influence the color scheme without some manual edits. I use and would recommend the [Tomorrow Night](https://github.com/theymaybecoders/sublime-tomorrow-theme) color scheme. However, if you are not, here are the corresponding colors these tags will be:

- **Titles** Same color as a *string*
- **Line Numbers** Same color as a *function*
- **Priority** same color as a *variable*
- **Bracket Tags** same color as a *class*
- **@ Tags** same color as a *keyword*

These may change in the future, but for now, this is the best way of to handle highlighting differences.


# License
All of SublimeTODO is licensed under the MIT license.

Copyright (c) 2014 Jonathan Delgado

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
