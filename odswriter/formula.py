# The MIT License (MIT)
#
# Copyright (c) 2014 Michael Mulqueen (http://michael.mulqueen.me.uk/)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re


try:
    unicode
except NameError:
    _convert_unicode = False
else:
    _convert_unicode = True


class Formula(object):
    """
        IMPORTANT NOTE: The formula object currently does no validation on the formula that you supply and it assumes
        you will supply it with a valid formula.

        For this reason, it's important that you: use . (point, full stop, period) as the decimal separator and ; as the
        argument separator.

        It is strongly recommended that you test your generated spreadsheets in LibreOffice because odswriter will not
        warn you of formula related mistakes.
    """
    def __init__(self, s):
        self.formula_string = s

    def __repr__(self):
        return "Formula({!r})".format(self.formula_string)

    def __str__(self):
        result = self.__unicode__()
        if _convert_unicode:
            return result.encode("UTF-8")
        else:
            return result

    def __unicode__(self):
        s = self.formula_string
        # Remove = sign if present
        if s.startswith("="):
            s = s[1:]
        # Wrap cell refs in square brackets.
        s = re.sub(
            r"(\"(?:[^\"]|\"\")*\")|([A-Z]+[0-9]+(?::[A-Z]+[0-9]+)?)",
            lambda m: m.group(1) or "[{}]".format(m.group(2)),
            s
        )
        # Place a . before cell references, so for example . A2 becomes .A2
        s = re.sub(
            r"(\"(?:[^\"]|\"\")*\")|([A-Z]+[0-9]+)(?!\()",
            lambda m: m.group(1) or r".{}".format(m.group(2)),
            s
        )
        return u"of:={}".format(s)
