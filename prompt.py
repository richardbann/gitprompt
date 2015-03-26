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


user_fmt = make_fmt(fg_color=256, bg_color=234)
host_fmt = make_fmt(144, bold=True)
pwd_fmt = make_fmt(fg_color=256, bg_color=236)
env_fmt = make_fmt(fg_color=256, bg_color=238)

branch_fmt = make_fmt(fg_color=256, bg_color=240, bold=True)
bare_fmt = make_fmt(fg_color=256, bg_color=240, bold=True, italic=True)
unstaged_fmt = make_fmt(fg_color=9, bg_color=240, bold=True)
untracked_fmt = make_fmt(fg_color=9, bg_color=240, bold=True)
staged_fmt = make_fmt(fg_color=48, bg_color=240, bold=True)
upstream_fmt = make_fmt(fg_color=256, bg_color=240)


def colorize(fmt, str):
    return '\[\x1b[%sm\]%s\[\x1b[0m\]' % (fmt, str)


def virtualenv():
    env = os.environ.get('VIRTUAL_ENV', None)
    if env:
        return os.path.split(env)[1]
    else:
        return None


def formatgitinfo():
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

    ret = [colorize(fmt, gi['branch'])]

    dirtyinfo = ''
    if gi['unstaged']:
        dirtyinfo += colorize(unstaged_fmt, '.')
    if gi['staged']:
        dirtyinfo += colorize(staged_fmt, '.')
    if gi['staged'] is None:
        dirtyinfo += colorize(unstaged_fmt, '#')
    if gi['untracked']:
        dirtyinfo += colorize(untracked_fmt, '?')
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


user = colorize(user_fmt, ' \u ')
host = colorize(host_fmt, ' \h ')
pwd = colorize(pwd_fmt, ' \w ')

_env = virtualenv()
env = colorize(env_fmt, ' %s ' % _env) if _env else ''


print '%s%s%s%s\n> ' % (user, pwd, env, formatgitinfo())
