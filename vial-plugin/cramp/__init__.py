from vial import vim, register_function
from vial.utils import vimfunction, get_key_code

BRACKETS = (
    ('(', ')'),
    ('[', ']'),
    ('{', '}'),
    ('\'', '\''),
    ('"', '"'),
)

OPEN2CLOSE = dict(BRACKETS)

tail = []
undo_breaked = False

def init():
    register_function('<SID>Close()',  close)
    register_function('<SID>Open(end)',  open)
    register_function('<SID>OpenClose(start)',  open_close)
    register_function('<SID>Leave()', leave)
    register_function('<SID>Skip()', skip)
    register_function('<SID>BS()', backspace)
    register_function('<SID>CR()', cr)
    register_function('<SID>BreakUndo()', break_undo)

    vim.command('inoremap <Plug>VialCrampLeave <c-r>=<SID>Leave()<cr><esc>')
    vim.command('inoremap <Plug>VialCrampSkip <c-r>=<SID>Skip()<cr>')

    vim.command('inoremap <bs> <c-r>=<SID>BS()<cr><bs>')
    vim.command('inoremap <cr> <c-r>=<SID>BreakUndo()<cr><cr><c-r>=<SID>CR()<cr>')

    for s, e in BRACKETS:
        ss = s.replace('"', '\\"')
        ee = e.replace('"', '\\"')

        if s == e:
            vim.command('inoremap {0} {0}<c-r>=<SID>OpenClose("{1}")<cr>'.format(s, ss))
        else:
            vim.command('inoremap {0} {0}<c-r>=<SID>Open("{1}")<cr>'.format(s, ee))
            vim.command('inoremap {0} {0}<c-r>=<SID>Close()<cr>'.format(e))


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
    undo_breaked = False
    if not tail:
        return ''

    pos = vim.current.window.cursor
    buf = vim.current.buffer
    line, col = pos
    result = ''
    for r in tail:
        if r == 'nl':
            result += get_key_code('cr') + get_key_code('c-d')
            buf[line-1] += buf[line].lstrip()
            del buf[line]
        else:
            modify_current_line(col, '', col + len(r))
            result += r

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

def get_ws(line):
    return line[:len(line) - len(line.lstrip())]

@vimfunction
def cr():
    line, col = vim.current.window.cursor
    buf = vim.current.buffer
    pline = buf[line-2]
    pspace = get_ws(pline)
    cline = buf[line-1]

    if pspace == get_ws(cline):
        return 

    sline = cline.lstrip()
    if not sline or sline[0] not in (')', ']', '}'):
        return

    sline = pline.rstrip()
    if not sline or sline[-1] not in ('(', '[', '{'):
        return

    if tail:
        tail.insert(0, 'nl')

    modify_current_line(col, '', len(cline))
    buf.append(pspace + cline[col:], line)

@vimfunction
def break_undo():
    global undo_breaked
    if not undo_breaked:
        undo_breaked = True
        return get_key_code('c-g') + 'u'



