from vial import vim, register_function
from vial.utils import vimfunction

BRACKETS = (
    ('(', ')'),
    ('[', ']'),
    ('{', '}'),
    ('\'', '\''),
)

tail = []

def init():
    register_function('<SID>VialCrampClose(what)',  close)
    register_function('<SID>VialCrampLeave()', leave)
    register_function('<SID>VialCrampSkip()', skip)

    vim.command('inoremap <Plug>VialCrampLeave <c-r>=<SID>VialCrampLeave()<cr><esc>')
    vim.command('inoremap <Plug>VialCrampSkip <c-r>=<SID>VialCrampSkip()<cr>')

    for s, e in BRACKETS:
        vim.command('inoremap {0} {0}<c-r>=<SID>VialCrampClose("{1}")<cr>'.format(s, e))

    vim.command('inoremap " "<c-r>=<SID>VialCrampClose(\'"\')<cr>')

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
