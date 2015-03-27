# encoding: utf-8

import os

from gitinfo import gitinfo


def make_fmt(fg_color=None, bg_color=None,
             bold=False, italic=False, underline=False):

    _bold = [1] if bold else []
    _italic = [3] if italic else []
    _underline = [4] if underline else []

    _bg_color = [] if bg_color is None else [48, 5, bg_color]
    _fg_color = [] if fg_color is None else [38, 5, fg_color]

    fmt = sum([_bold, _italic, _underline, _bg_color, _fg_color], [])
    fmt = ';'.join(map(str, fmt))

    return fmt


def colorize(fmt, str):
    """returns the colorized string"""
    return '\[\x1b[%sm\]%s\[\x1b[0m\]' % (fmt, str)


def c(str, fg=None, bg=None, bold=False, italic=False, underline=False):
    """simplified version of colorize"""
    fmt = make_fmt(fg, bg, bold, italic, underline)
    return colorize(fmt, str)


def virtualenv():
    """returns the name of the virtualenv, or None"""
    env = os.environ.get('VIRTUAL_ENV', None)
    if env:
        return os.path.split(env)[1]
    else:
        return None


def formatgitinfo():
    branch_fmt = make_fmt(fg_color=256, bg_color=240, bold=True)
    bare_fmt = make_fmt(fg_color=256, bg_color=240, bold=True, italic=True)
    unstaged_fmt = make_fmt(fg_color=202, bg_color=240, bold=True)
    untracked_fmt = make_fmt(fg_color=202, bg_color=240, bold=True)
    staged_fmt = make_fmt(fg_color=48, bg_color=240, bold=True)
    upstream_fmt = make_fmt(fg_color=256, bg_color=240)

    """returns the colorized, formatted git info string"""
    gi = gitinfo()
    if gi is None:
        return ''

    sep = colorize(branch_fmt, ' ')

    if gi['bare']:
        fmt = bare_fmt
    else:
        fmt = branch_fmt

    branchinfo = gi['branch']
    if gi['rebase_desc']:
        branchinfo += '|' + gi['rebase_desc']

    ret = [colorize(fmt, branchinfo)]

    dirtyinfo = ''
    if gi['unstaged']:
        dirtyinfo += colorize(unstaged_fmt, '•')
    if gi['staged']:
        dirtyinfo += colorize(staged_fmt, '•')
    if gi['staged'] is None:
        dirtyinfo += colorize(unstaged_fmt, '#')
    if gi['untracked']:
        dirtyinfo += colorize(untracked_fmt, '⁃')
    if dirtyinfo:
        ret += [dirtyinfo]

    upstreaminfo = ''
    us = gi['upstream']
    if us:
        upstreaminfo += us['name']
        ahead, behind = us['ahead'], us['behind']
        if ahead:
            upstreaminfo += '+%s' % us['ahead']
        if behind:
            upstreaminfo += '-%s' % us['behind']
        if not ahead and not behind:
            upstreaminfo += '='

    if upstreaminfo:
        upstreaminfo = '(%s)' % upstreaminfo
        upstreaminfo = colorize(upstream_fmt, upstreaminfo)
        ret += [upstreaminfo]

    return sep + sep.join(ret) + sep


def simplegitinfo():
    """returns a simple git info string"""
    gi = gitinfo()
    if gi is None:
        return ''

    branchinfo = gi['branch']
    if gi['bare']:
        branchinfo += '[BARE]'
    if gi['rebase_desc']:
        branchinfo += '|' + gi['rebase_desc']

    ret = [branchinfo]

    dirtyinfo = ''
    if gi['unstaged']:
        dirtyinfo += '*'
    if gi['staged']:
        dirtyinfo += '+'
    if gi['staged'] is None:
        dirtyinfo += '#'
    if gi['untracked']:
        dirtyinfo += '%'
    if dirtyinfo:
        ret += [dirtyinfo]

    upstreaminfo = ''
    us = gi['upstream']
    if us:
        upstreaminfo += us['name']
        ahead, behind = us['ahead'], us['behind']
        if ahead:
            upstreaminfo += '+%s' % us['ahead']
        if behind:
            upstreaminfo += '-%s' % us['behind']
        if not ahead and not behind:
            upstreaminfo += '='

    if upstreaminfo:
        upstreaminfo = '(%s)' % upstreaminfo
        ret += [upstreaminfo]

    return ' '.join(ret)


def getprompt():
    user = c(' \u ', fg=256, bg=234)
    # host = c(' \h ', fg=144, bold=True)
    pwd = c(' \w ', fg=256, bg=236)
    _env = virtualenv()
    env = c(' %s ' % _env, fg=256, bg=238) if _env else ''

    return '%s%s%s%s\n> ' % (user, pwd, env, formatgitinfo())


def getsimpleprompt():
    env = virtualenv()
    git = simplegitinfo()

    env = 'virt: %s' % env if env else ''
    git = 'git: %s' % git if git else ''

    info = ('%s | %s' % (env, git)).strip(' |')
    if info:
        info = '\n%s\n' % info
    else:
        info = ''

    return '%s\u@\h:\w> ' % info


if __name__ == '__main__':
    if os.environ.get('PROMPT_STYLE') == 'simple':
        print getsimpleprompt()
    else:
        print getprompt()
