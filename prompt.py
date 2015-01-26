import subprocess
import os


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


user_fmt = make_fmt(66, bold=True)
host_fmt = make_fmt(144, bold=True)
pwd_fmt = make_fmt(215, bold=True)
clean_fmt = make_fmt(40, bold=True, italic=True)
dirty_fmt = make_fmt(9, bold=True, italic=True)
env_fmt = make_fmt(115, bold=True, italic=True)


def colorize(fmt, str):
    return '\[\x1b[%sm\]%s\[\x1b[0m\]' % (fmt, str)


def branch():
    try:
        out = subprocess.check_output(['git', 'status'],
                                      stderr=subprocess.STDOUT)
    except:
        return ''

    lines = out.splitlines()
    branch = lines[0][10:]

    if lines[-1] == 'nothing to commit, working directory clean':
        branch_fmt = clean_fmt
    else:
        branch_fmt = dirty_fmt

    return ' (%s)' % colorize(branch_fmt, branch)


def virtualenv():
    env = os.environ.get('VIRTUAL_ENV', None)
    if env:
        env = os.path.split(env)[1]
        return '(%s)' % colorize(env_fmt, env)
    else:
        return ''


user = colorize(user_fmt, '\u')
host = colorize(host_fmt, '\h')
pwd = colorize(pwd_fmt, '\w')
env = virtualenv()

# Print the new bash prompt
print '%s:%s%s%s$ ' % (user, pwd, branch(), env)
