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
    register_function('<SID>VialCrampClose(what)',  close)
    register_function('<SID>VialCrampLeave()', leave)
    register_function('<SID>VialCrampSkip()', skip)
    register_function('<SID>VialCrampBS()', backspace)

    vim.command('inoremap <Plug>VialCrampLeave <c-r>=<SID>VialCrampLeave()<cr><esc>')
    vim.command('inoremap <Plug>VialCrampSkip <c-r>=<SID>VialCrampSkip()<cr>')

    vim.command('inoremap <bs> <c-r>=<SID>VialCrampBS()<cr><bs>')

    for s, e in BRACKETS:
        if e == '"':
            e = '\\"'

        vim.command('inoremap {0} {0}<c-r>=<SID>VialCrampClose("{1}")<cr>'.format(s, e))


@vimfunction
def close(what):
    tail.insert(0, what)
    col = vim.current.window.cursor[1]
    vim.current.line = vim.current.line[:col] + what + vim.current.line[col:]
    return ''

@vimfunction
def leave():
    if not tail:
        return ''

    col = vim.current.window.cursor[1]
    vim.current.line = vim.current.line[:col] + vim.current.line[col+len(tail):]

    result = ''.join(tail)
    tail[:] = []

    return result

@vimfunction
def skip():
    col = vim.current.window.cursor[1]
    char = vim.current.line[col]
    vim.current.line = vim.current.line[:col] + vim.current.line[col+1:]

    if tail and tail[0] == char:
        tail.pop(0)

    return char

@vimfunction
def backspace():
    col = vim.current.window.cursor[1]
    lchar = vim.current.line[col-1]
    rchar = vim.current.line[col]

    if tail and lchar in OPEN2CLOSE and OPEN2CLOSE[lchar] == rchar and rchar == tail[0]:
        vim.current.line = vim.current.line[:col] + vim.current.line[col+1:]
        tail.pop(0)

    return ''
