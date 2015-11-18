# encoding: utf-8

from __future__ import print_function

import subprocess
import os

import six


def isdir(base, path):
    return os.path.isdir(os.path.join(base, path))


def isfile(base, path):
    return os.path.isfile(os.path.join(base, path))


def islink(base, path):
    return os.path.islink(os.path.join(base, path))


def readfile(base, path):
    try:
        with open(os.path.join(base, path)) as f:
            return f.read().strip()
    except:
        return ''


def convert(s):
    if s == 'true':
        return True
    elif s == 'false':
        return False
    return s


def cmd(params):
    with open(os.devnull, 'w') as devnull:
        try:
            output = subprocess.check_output(params, stderr=devnull)
            exit_code = 0
        except subprocess.CalledProcessError as err:
            output = err.output
            exit_code = err.returncode

    if six.PY3:
        output = output.decode('utf-8')
    return output, exit_code


def gitinfo():
    params = ['git', 'rev-parse', '--git-dir', '--is-inside-git-dir',
              '--is-bare-repository', '--is-inside-work-tree',
              '--short', 'HEAD']
    repo_info, rev_parse_exit_code = cmd(params)

    if not repo_info:
        return None

    repo_info = tuple([convert(i) for i in repo_info.split()])
    if rev_parse_exit_code != 0:
        repo_info += (None,)
    g, inside_gitdir, bare_repo, inside_worktree, short_sha = repo_info

    r = None
    b = ''
    step = ''
    total = ''
    detached = False

    if isdir(g, 'rebase-merge'):
        b = readfile(g, 'rebase-merge/head-name')
        step = readfile(g, 'rebase-merge/msgnum')
        total = readfile(g, 'rebase-merge/end')

        if isfile(g, '/rebase-merge/interactive'):
            r = 'REBASE-i'
        else:
            r = 'REBASE-m'
    else:
        if isdir(g, 'rebase-apply'):
            step = readfile(g, 'rebase-apply/next')
            total = readfile(g, 'rebase-apply/last')
            if isfile(g, 'rebase-apply/rebasing'):
                b = readfile(g, 'rebase-apply/head-name')
                r = 'REBASE'
            elif isfile(g, 'rebase-apply/applying'):
                r = 'AM'
            else:
                r = 'AM/REBASE'
        elif isfile(g, 'MERGE_HEAD'):
            r = 'MERGING'
        elif isfile(g, 'CHERRY_PICK_HEAD'):
            r = 'CHERRY-PICKING'
        elif isfile(g, 'REVERT_HEAD'):
            r = 'REVERTING'
        elif isfile(g, 'BISECT_LOG'):
            r = 'BISECTING'

        if b:
            pass
        elif islink(g, 'HEAD'):
            b = cmd(['git', 'symdolic-ref', 'HEAD'])[0]
        else:
            head = readfile(g, 'HEAD')
            if not head:
                return None
            b = head[5:] if head[:5] == 'ref: ' else head
            if head == b:
                detached = True
                params = ['git', 'describe', '--contains', '--all', 'HEAD']
                b, retcode = cmd(params)
                if retcode:
                    b = short_sha
                b = '(%s)' % b

    if step and total:
        r = '%s %s/%s' % (r, step, total)

    w = False
    i = False
    s = False
    u = False
    c = False
    p = None

    if inside_gitdir:
        if bare_repo:
            c = True
        else:
            b = 'GIT_DIR!'

    elif inside_worktree:
        params = ['git', 'diff', '--no-ext-diff', '--quiet', '--exit-code']
        retcode = cmd(params)[1]
        if retcode:
            w = True
        if short_sha:
            params = ['git', 'diff-index', '--cached', '--quiet', 'HEAD', '--']
            retcode = cmd(params)[1]
            if retcode:
                i = True
        else:
            i = None

        params = ['git', 'rev-parse', '--verify', '--quiet', 'refs/stash']
        retcode = cmd(params)[1]
        if retcode == 0:
            s = True

        params = ['git', 'ls-files', '--others', '--exclude-standard',
                  '--error-unmatch', '--', ':/*']
        retcode = cmd(params)[1]
        if retcode == 0:
            u = True

        params = ['git', 'rev-list', '--count', '--left-right',
                  '@{upstream}...HEAD']
        count = cmd(params)[0]

        if not count:
            p = None
        else:
            up, local = tuple(map(int, count.split()))
            params = ['git', 'rev-parse', '--abbrev-ref', '@{upstream}']
            name = cmd(params)[0].strip()
            p = {'name': name, 'behind': up, 'ahead': local}

    b = b[11:] if b[:11] == 'refs/heads/' else b

    return {'branch': b,
            'detached': detached,
            'bare': c,
            'unstaged': w,
            'staged': i,
            'stash': s,
            'untracked': u,
            'rebase_desc': r,
            'upstream': p}


def main():
    for k, v in gitinfo().items():
        print('%s: %s' % (k, v))


if __name__ == '__main__':
    main()
