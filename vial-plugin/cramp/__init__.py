from vial import vim, register_function
from vial.utils import get_key_code, get_ws, parse_keys

BRACKETS = (
    ('(', ')'),
    ('[', ']'),
    ('{', '}'),
    ('\'', '\''),
    ('"', '"'),
)

OPEN2CLOSE = dict(BRACKETS)

def init():
    register_function('<SID>BS()', backspace)
    register_function('<SID>CR()', cr)
    register_function('<SID>OpenClose(start)', open_close)

    vim.command('inoremap <Plug>VialCrampLeave <esc>')
    vim.command('inoremap <Plug>VialCrampSkip <c-g>U<right>')

    vim.command('inoremap <bs> <c-r>=<SID>BS()<cr><bs>')
    vim.command('inoremap <cr> <cr><c-r>=<SID>CR()<cr>')

    for s, e in BRACKETS:
        ss = s.replace('"', '\\"')
        ee = e.replace('"', '\\"')
        if s == e:
            vim.command('inoremap {0} {0}<c-r>=<SID>OpenClose("{1}")<cr>{0}<c-g>U<left>'.format(s, ss))
        else:
            vim.command('inoremap {0} {0}{1}<c-g>U<left>'.format(s, e))
            vim.command('inoremap {0} {0}<c-r>=<SID>OpenClose("{1}")<cr>'.format(e, ee))


def open_close(start):
    col = vim.current.window.cursor[1]

    try:
        rchar = vim.current.line[col]
    except IndexError:
        pass
    else:
        if rchar == start:
            return get_key_code('delete')

    return ''


def backspace():
    col = vim.current.window.cursor[1]

    try:
        lchar = vim.current.line[col-1]
        rchar = vim.current.line[col]
        if lchar in OPEN2CLOSE and OPEN2CLOSE[lchar] == rchar:
            return get_key_code('delete')
    except IndexError:
        pass

    return ''


def cr():
    line, col = vim.current.window.cursor
    buf = vim.current.buffer
    pline = buf[line-2]
    pspace = get_ws(pline)
    cline = buf[line-1]

    if pspace == get_ws(cline):
        return ''

    sline = cline.lstrip()
    if not sline or sline[0] not in (')', ']', '}'):
        return ''

    sline = pline.rstrip()
    if not sline or sline[-1] not in ('(', '[', '{'):
        return ''

    return parse_keys(' <cr><up><end><bs>')
