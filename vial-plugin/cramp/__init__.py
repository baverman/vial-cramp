from vial import vim, register_function
from vial.utils import vimfunction

BRACKETS = (
    ('(', ')'),
    ('[', ']'),
    ('{', '}'),
    ('\'', '\''),
    ('"', '"'),
)

OPEN2CLOSE = dict(BRACKETS)

tail = []

def init():
    register_function('<SID>VialCrampClose()',  close)
    register_function('<SID>VialCrampOpen(end)',  open)
    register_function('<SID>VialCrampOpenClose(start)',  open_close)
    register_function('<SID>VialCrampLeave()', leave)
    register_function('<SID>VialCrampSkip()', skip)
    register_function('<SID>VialCrampBS()', backspace)

    vim.command('inoremap <Plug>VialCrampLeave <c-r>=<SID>VialCrampLeave()<cr><esc>')
    vim.command('inoremap <Plug>VialCrampSkip <c-r>=<SID>VialCrampSkip()<cr>')

    vim.command('inoremap <bs> <c-r>=<SID>VialCrampBS()<cr><bs>')

    for s, e in BRACKETS:
        ss = s.replace('"', '\\"')
        ee = e.replace('"', '\\"')

        if s == e:
            vim.command('inoremap {0} {0}<c-r>=<SID>VialCrampOpenClose("{1}")<cr>'.format(s, ss))
        else:
            vim.command('inoremap {0} {0}<c-r>=<SID>VialCrampOpen("{1}")<cr>'.format(s, ee))
            vim.command('inoremap {0} {0}<c-r>=<SID>VialCrampClose()<cr>'.format(e))


def modify_current_line(left, mid, right):
    l = vim.current.line
    vim.current.line = l[:left] + mid + l[right:]

@vimfunction
def close():
    col = vim.current.window.cursor[1]
    if col >= 1:
        try:
            end = vim.current.line[col-1]
            rchar = vim.current.line[col]
        except IndexError:
            pass
        else:
            if rchar == end:
                if tail and tail[0] == end:
                    tail.pop(0)

                modify_current_line(col, '', col + len(end))

    return ''

@vimfunction
def open_close(start):
    col = vim.current.window.cursor[1]

    try:
        rchar = vim.current.line[col]
    except IndexError:
        pass
    else:
        if rchar == start:
            if tail and tail[0] == start:
                tail.pop(0)

            modify_current_line(col, '', col + len(start))
            return ''

    tail.insert(0, start)
    modify_current_line(col, start, col)
    return ''

@vimfunction
def open(end):
    tail.insert(0, end)
    col = vim.current.window.cursor[1]
    modify_current_line(col, end, col)
    return ''

@vimfunction
def leave():
    if not tail:
        return ''

    col = vim.current.window.cursor[1]
    modify_current_line(col, '', col + len(tail))

    result = ''.join(tail)
    tail[:] = []

    return result

@vimfunction
def skip():
    col = vim.current.window.cursor[1]
    char = vim.current.line[col]
    modify_current_line(col, '', col + 1)

    if tail and tail[0] == char:
        tail.pop(0)

    return char

@vimfunction
def backspace():
    col = vim.current.window.cursor[1]

    try:
        lchar = vim.current.line[col-1]
        rchar = vim.current.line[col]
    except IndexError:
        return ''

    if tail and lchar in OPEN2CLOSE and OPEN2CLOSE[lchar] == rchar and rchar == tail[0]:
        modify_current_line(col, '', col + 1)
        tail.pop(0)

    return ''
