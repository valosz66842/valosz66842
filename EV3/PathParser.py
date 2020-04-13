import re
from . import path

COMMANDS = set('MmZzLlHhVvCcSsQqTtAa')
UPPERCASE = set('MZLHVCSQTA')

COMMAND_RE = re.compile("([MmZzLlHhVvCcSsQqTtAa])")
FLOAT_RE = re.compile("[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?")


def _tokenize_path(pathdef):
    for x in COMMAND_RE.split(pathdef):
        if x in COMMANDS:
            yield x
        for token in FLOAT_RE.findall(x):
            yield token


def parse_path(pathdef, current_pos=0j):
    elements = list(_tokenize_path(pathdef))
    elements.reverse()
    segments = path.Path()
    start_pos = None
    command = None
    while elements:
        if elements[-1] in COMMANDS:
            last_command = command  # Used by S and T
            command = elements.pop()
            absolute = command in UPPERCASE
            command = command.upper()
        else:
            if command is None:
                raise ValueError("Unallowed implicit command in %s, position %s" % (
                    pathdef, len(pathdef.split()) - len(elements)))
        if command == 'M':
            # Moveto command.
            x = elements.pop()
            y = elements.pop()
            pos = float(x) + float(y) * 1j
            if absolute:
                current_pos = pos
            else:
                current_pos += pos
            start_pos = current_pos
            command = 'L'
        elif command == 'Z':
            segments.append(path.Line(current_pos, start_pos))
            segments.closed = True
            current_pos = start_pos
            start_pos = None
            command = None  # You can't have implicit commands after closing.
        elif command == 'L':
            x = elements.pop()
            y = elements.pop()
            pos = float(x) + float(y) * 1j
            if not absolute:
                pos += current_pos
            segments.append(path.Line(current_pos, pos))
            current_pos = pos
        elif command == 'H':
            x = elements.pop()
            pos = float(x) + current_pos.imag * 1j
            if not absolute:
                pos += current_pos.real
            segments.append(path.Line(current_pos, pos))
            current_pos = pos
        elif command == 'V':
            y = elements.pop()
            pos = current_pos.real + float(y) * 1j
            if not absolute:
                pos += current_pos.imag * 1j
            segments.append(path.Line(current_pos, pos))
            current_pos = pos
        elif command == 'C':
            control1 = float(elements.pop()) + float(elements.pop()) * 1j
            control2 = float(elements.pop()) + float(elements.pop()) * 1j
            end = float(elements.pop()) + float(elements.pop()) * 1j
            if not absolute:
                control1 += current_pos
                control2 += current_pos
                end += current_pos

            segments.append(path.CubicBezier(current_pos, control1, control2, end))
            current_pos = end
        elif command == 'S':
            if last_command not in 'CS':
                control1 = current_pos
            else:
                control1 = current_pos + current_pos - segments[-1].control2
            control2 = float(elements.pop()) + float(elements.pop()) * 1j
            end = float(elements.pop()) + float(elements.pop()) * 1j
            if not absolute:
                control2 += current_pos
                end += current_pos
            segments.append(path.CubicBezier(current_pos, control1, control2, end))
            current_pos = end
        elif command == 'Q':
            control = float(elements.pop()) + float(elements.pop()) * 1j
            end = float(elements.pop()) + float(elements.pop()) * 1j
            if not absolute:
                control += current_pos
                end += current_pos
            segments.append(path.QuadraticBezier(current_pos, control, end))
            current_pos = end
        elif command == 'T':
            if last_command not in 'QT':
                control = current_pos
            else:
                control = current_pos + current_pos - segments[-1].control
            end = float(elements.pop()) + float(elements.pop()) * 1j
            if not absolute:
                end += current_pos
            segments.append(path.QuadraticBezier(current_pos, control, end))
            current_pos = end
        elif command == 'A':
            radius = float(elements.pop()) + float(elements.pop()) * 1j
            rotation = float(elements.pop())
            arc = float(elements.pop())
            sweep = float(elements.pop())
            end = float(elements.pop()) + float(elements.pop()) * 1j
            if not absolute:
                end += current_pos
            segments.append(path.Arc(current_pos, radius, rotation, arc, sweep, end))
            current_pos = end
    return segments