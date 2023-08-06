
def shortener(text, max_width, break_idx):
    if len(text) <= max_width:
        return text
    length_2nd_half = max_width - (break_idx + 2)
    if length_2nd_half <= 1:
        return text[:break_idx] + '...'
    else:
        return text[:break_idx] + '..' + text[-(length_2nd_half):]


class TextBoxPrinter:
    def __init__(self, left_col=20, right_col=30):
        """"""
        self._left_col = left_col
        self._right_col = right_col
        self._full_width = left_col + right_col + 7
        self._horizontal = '|' + '-' * self._full_width + '|'
        self._blank_line = '|' + ' ' * self._full_width + '|'

    def sprint(self, pkt):
        return '\n'.join(
            [self.horizontal_line(),
             self.full_width_centered(pkt.trans_id()),
             self.blank_line()] +
            self.packet_status(pkt) +
            self.packet_sprint(pkt) +
            [self.horizontal_line()]
        )

    def horizontal_line(self):
        return self._horizontal

    def blank_line(self):
        return self._blank_line

    def full_width_centered(self, text):
        return '| ' + text.center(self._full_width - 2) + ' |'

    def full_width_right(self, text):
        return '| ' + text.rjust(self._full_width - 3) + '  |'

    def full_width_left(self, text):
        return '|  ' + text.ljust(self._full_width - 3) + ' |'

    def label_value_line(self, label, value):
        label = shortener(label, (self._left_col - 1), 9)
        value = shortener(value, (self._right_col - 1), 9)
        return f'| {label:>{self._left_col}} ->  {value:<{self._right_col}} |'

    def packet_status(self, pkt):
        return [self.full_width_left(f'length: {pkt.length_in_bytes()} bytes')]

    def packet_sprint(self, pkt):
        if pkt.nested_packet is None:
            return (self.header_sprint(pkt) +
                    self.payload_sprint(pkt) +
                    self.trailer_sprint(pkt))
        else:
            return (self.header_sprint(pkt) +
                    self.packet_sprint(pkt.nested_packet) +
                    self.trailer_sprint(pkt))


    def header_sprint(self, pkt):
        header_fields = pkt.get_header_field_list()
        if len(header_fields):
            wrap = (self._full_width - 18) // 3
            return (self.field_list_sprint(pkt, header_fields) +
                    self.byte_list_sprint('header',
                                          pkt.pack_header(), wrap))
        else:
            return []

    def trailer_sprint(self, pkt):
        trailer_fields = pkt.get_trailer_field_list()
        if len(trailer_fields):
            return self.field_list_sprint(pkt, trailer_fields)
        else:
            return []

    def payload_sprint(self, pkt):
        _bytes = pkt.pack_payload()
        if not len(_bytes):
            return []
        if self._full_width < 60:
            wrap = 8
        else:
            wrap = 16
        lines = [
            self.horizontal_line(),
            self.full_width_right(
                ' '.join(f'{x:2d}' for x in range(wrap))),
            self.blank_line()]
        lines += self.byte_list_sprint('payload', _bytes, wrap)
        return lines

    def byte_list_sprint(self, list_name, byte_list, wrap=16):
        _bytes = byte_list
        i = 0
        lines = []
        while i < len(_bytes):
            line = f'{list_name}[{i:d}]  {_bytes[i]:#04x} '
            if (i + wrap) < len(_bytes):
                line += ' '.join([f'{x:02x}' for x in _bytes[i+1:i+wrap]])
            elif (i + 1) < len(_bytes):
                line += ' '.join([f'{x:02x}' for x in _bytes[i+1:]])
                line += '   ' * ((i + wrap) - len(_bytes))
            lines.append(self.full_width_right(line))
            i += wrap
        return lines

    def field_list_sprint(self, pkt, field_names):
        field_lines = [
            self.horizontal_line(),
            self.full_width_centered(pkt.__class__.__name__),
            self.blank_line()]
        for field in field_names:
            field_lines.append(
                self.label_value_line(field,
                                      pkt.get_field_value_str(field)))
        field_lines.append(self.blank_line())
        return field_lines
