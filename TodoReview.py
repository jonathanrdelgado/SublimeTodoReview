'''
SublimeTodoReview
A SublimeText 3 plugin for reviewing todo (any other) comments within your code.

@author Jonathan Delgado (Initial Repo by @robcowie and ST3 update by @dnatag)
'''

from collections import namedtuple
from datetime import datetime
from itertools import groupby
from os import path, walk
import sublime_plugin
import threading
import sublime
import functools
import fnmatch
import re

Message = namedtuple('Message', 'type, msg')


def do_when(conditional, callback, *args, **kwargs):
    if conditional():
        return callback(*args, **kwargs)
    sublime.set_timeout(functools.partial(do_when, conditional, callback, *args, **kwargs), 50)

class ThreadProgress(object):
    def __init__(self, thread, message, success_message, file_counter):
        self.thread = thread
        self.message = message
        self.success_message = success_message
        self.file_counter = file_counter
        self.addend = 1
        self.size = 8
        sublime.set_timeout(lambda: self.run(0), 100)

    def run(self, i):
        if not self.thread.is_alive():
            if hasattr(self.thread, 'result') and not self.thread.result:
                sublime.status_message('')
                return
            sublime.status_message(self.success_message)
            return
        before = i % self.size
        after = (self.size - 1) - before
        sublime.status_message('%s [%s=%s] (%s files scanned)' % (self.message, ' ' * before, ' ' * after, self.file_counter))
        if not after:
            self.addend = -1
        if not before:
            self.addend = 1
        i += self.addend
        sublime.set_timeout(lambda: self.run(i), 100)

class TodoExtractor(object):
    def __init__(self, dirpaths, filepaths, file_counter):
        self.dirpaths = dirpaths
        self.filepaths = filepaths
        self.patterns = settings.get('patterns', {})
        self.file_counter = file_counter
        self.ignored_dirs = settings.get('exclude_folders', [])
        self.ignored_files = [fnmatch.translate(patt) for patt in settings.get('exclude_files', [])]

    def iter_files(self):
        seen_paths_ = []

        for filepath in self.filepaths:
            pth = path.realpath(path.abspath(filepath))
            if pth not in seen_paths_:
                seen_paths_.append(pth)
                yield pth

        for dirpath in self.dirpaths:
            dirpath = path.abspath(dirpath)
            for dirpath, dirnames, filenames in walk(dirpath):
                for dir in self.ignored_dirs:
                    if dir in dirnames:
                        dirnames.remove(dir)

                for filepath in filenames:
                    pth = path.join(dirpath, filepath)
                    pth = path.realpath(path.abspath(pth))
                    if pth not in seen_paths_:
                        seen_paths_.append(pth)
                        yield pth

    def filter_files(self, files):
        exclude_patterns = [re.compile(patt) for patt in self.ignored_files]

        for filepath in files:
            if any(patt.search(filepath) for patt in exclude_patterns):
                continue
            yield filepath

    def search_targets(self):
        return self.filter_files(self.iter_files())

    def extract(self):
        message_patterns = '|'.join(self.patterns.values())
        case_sensitivity = 0 if settings.get('case_sensitive', False) else re.IGNORECASE
        patt = re.compile(message_patterns, case_sensitivity)
        patt_priority = re.compile(r'\(([0-9]{1,2})\)')
        for filepath in self.search_targets():
            try:
                f = open(filepath, 'r', encoding='utf-8')
                for linenum, line in enumerate(f):
                    for mo in patt.finditer(line):
                        # Remove the non-matched groups
                        matches = [Message(msg_type, msg) for msg_type, msg in mo.groupdict().items() if msg]
                        for matchi in matches:
                            priority = patt_priority.search(matchi.msg)

                            if priority:
                                priority = int(priority.group(0).replace('(', '').replace(')', ''))
                            else:
                                priority = 100

                            yield {
                                'filepath': filepath,
                                'linenum': linenum + 1,
                                'match': matchi,
                                'priority': priority
                            }
            except (IOError, UnicodeDecodeError):
                f = None
            finally:
                self.file_counter.increment()
                if f is not None:
                    f.close()

class RenderResultRunCommand(sublime_plugin.TextCommand):
    def run(self, edit, formatted_results, file_counter):
        active_window = sublime.active_window()
        existing_results = [v for v in active_window.views() if v.name() == 'TodoReview' and v.is_scratch()]
        if existing_results:
            result_view = existing_results[0]
        else:
            result_view = active_window.new_file()
            result_view.set_name('TodoReview')
            result_view.set_scratch(True)
            result_view.settings().set('todo_results', True)

        hr = u'+ {0} +'.format('-' * 56)
        header = u'{hr}\n| TodoReview @ {0:<43} |\n| {1:<56} |\n{hr}\n'.format(datetime.now().strftime('%A %m/%d/%y at %I:%M%p'), u'{0} files scanned'.format(file_counter), hr=hr)

        result_view.erase(edit, sublime.Region(0, result_view.size()))
        result_view.insert(edit, result_view.size(), header)

        regions_data = [x[:] for x in [[]] * 2]

        # Result sections
        for linetype, line, data in formatted_results:
            # edit = result_view.begin_edit()
            insert_point = result_view.size()
            result_view.insert(edit, insert_point, line)
            if linetype == 'result':
                rgn = sublime.Region(insert_point, result_view.size())
                regions_data[0].append(rgn)
                regions_data[1].append(data)
            result_view.insert(edit, result_view.size(), u'\n')

        result_view.add_regions('results', regions_data[0], '')

        d_ = dict(('{0},{1}'.format(k.a, k.b), v) for k, v in zip(regions_data[0], regions_data[1]))
        result_view.settings().set('result_regions', d_)

        result_view.assign_syntax('Packages/TodoReview/TodoReview.hidden-tmLanguage')
        result_view.settings().set('line_padding_bottom', 2)
        result_view.settings().set('line_padding_top', 2)
        result_view.settings().set('word_wrap', False)
        result_view.settings().set('command_mode', True)
        active_window.focus_view(result_view)

class WorkerThread(threading.Thread):

    def __init__(self, extractor, callback, file_counter):
        self.extractor = extractor
        self.callback = callback
        self.file_counter = file_counter
        threading.Thread.__init__(self)

    def run(self):

        todos = self.extractor.extract()
        formatted = list(self.format(todos))

        sublime.set_timeout(functools.partial(self.callback, formatted, self.file_counter), 10)

    def format(self, messages):
        messages = sorted(messages, key=lambda m: (m['priority'], m['match'].type))

        for message_type, matches in groupby(messages, key=lambda m: m['match'].type):
            matches = list(matches)
            if matches:
                yield ('header', u'\n## {0} ({1})'.format(message_type.upper(), len(matches)), {})
                for idx, m in enumerate(matches, 1):
                    msg = m['match'].msg

                    if settings.get('render_include_folder', False):
                        filepath = path.dirname(m['filepath']).replace('\\', '/').split('/')
                        filepath = filepath[len(filepath) - 1]  + '/' + path.basename(m['filepath'])
                    else:
                        filepath = path.basename(m['filepath'])
                    spaces = ' '*(settings.get('render_spaces', 1) - len(filepath + ':' + str(m['linenum'])))
                    line = u"{idx}. {filepath}:{linenum}{spaces}{msg}".format(idx=idx, filepath=filepath, linenum=m['linenum'], spaces=spaces, msg=msg)
                    yield ('result', line, m)

class FileScanCounter(object):

    def __init__(self):
        self.ct = 0
        self.lock = threading.RLock()

    def __call__(self, filepath):
        self.increment()

    def __str__(self):
        with self.lock:
            return '%d' % self.ct

    def increment(self):
        with self.lock:
            self.ct += 1

    def reset(self):
        with self.lock:
            self.ct = 0

class TodoReviewCommand(sublime_plugin.TextCommand):
    def run(self, edit, paths=False, open_files=False):
        global settings
        filepaths = []

        settings = sublime.load_settings('TodoReview.sublime-settings')
        window = self.view.window()

        if open_files:
            filepaths = [view.file_name() for view in window.views() if view.file_name()]

        if not paths:
            paths = window.folders()
        else:
            for p in paths:
                if path.isfile(p):
                    filepaths.append(p)

        file_counter = FileScanCounter()
        extractor = TodoExtractor(paths, filepaths, file_counter)

        worker_thread = WorkerThread(extractor, self.render_formatted, file_counter)
        worker_thread.start()
        ThreadProgress(worker_thread, 'Finding TODOs', '', file_counter)

    def render_formatted(self, rendered, counter):
        self.view.run_command("render_result_run", {"formatted_results": rendered, "file_counter": str(counter)})

class NavigateResults(sublime_plugin.TextCommand):
    DIRECTION = {'forward': 1, 'backward': -1}
    STARTING_POINT = {'forward': -1, 'backward': 0}

    def __init__(self, view):
        super(NavigateResults, self).__init__(view)

    def run(self, edit, direction):
        view = self.view
        settings = view.settings()
        results = self.view.get_regions('results')
        if not results:
            sublime.status_message('No results to navigate')
            return

        selection = int(settings.get('selected_result', self.STARTING_POINT[direction]))
        selection = selection + self.DIRECTION[direction]
        try:
            target = results[selection]
        except IndexError:
            target = results[0]
            selection = 0

        settings.set('selected_result', selection)
        target = target.cover(target)
        view.add_regions('selection', [target], 'selected', 'dot')
        view.show(target)

class ClearSelection(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.erase_regions('selection')
        self.view.settings().erase('selected_result')

class GotoComment(sublime_plugin.TextCommand):

    def __init__(self, *args):
        super(GotoComment, self).__init__(*args)

    def run(self, edit):
        selection = int(self.view.settings().get('selected_result', -1))
        selected_region = self.view.get_regions('results')[selection]
        data = self.view.settings().get('result_regions')['{0},{1}'.format(selected_region.a, selected_region.b)]
        new_view = self.view.window().open_file(data['filepath'])
        do_when(lambda: not new_view.is_loading(), lambda:new_view.run_command("goto_line", {"line": data['linenum']}))
