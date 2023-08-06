""" ae.valid unit tests """
from typing import cast

from ae.valid import correct_email, correct_phone


class TestOfflineContactValidation:
    def test_correct_email(self):
        # edge cases: empty string or None as email
        assert correct_email('') == ('', False)
        assert correct_email(cast(str, None)) == ('', False)
        assert correct_email('test') == ('test', False)
        assert correct_email('TesT') == ('TesT', False)
        assert correct_email('TEST') == ('test', False)
        r = []
        assert correct_email('', removed=r) == ('', False)
        assert r == []
        r = []
        assert correct_email(cast(str, None), removed=r) == ('', False)
        assert r == []

        # special characters !#$%&'*+-/=?^_`{|}~; are allowed in local part
        r = []
        assert correct_email('john_smith@example.com', removed=r) == ('john_smith@example.com', False)
        assert r == []
        r = []
        assert correct_email('john?smith@example.com', removed=r) == ('john?smith@example.com', False)
        assert r == []

        # dot is not the first or last character unless quoted, and does not appear consecutively unless quoted
        r = []
        assert correct_email(".john.smith@example.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["0:."]
        r = []
        assert correct_email("john.smith.@example.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["10:."]
        r = []
        assert correct_email("john..smith@example.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["5:."]
        r = []
        assert correct_email('"john..smith"@example.com', removed=r) == ('"john..smith"@example.com', False)
        assert r == []
        r = []
        assert correct_email("john.smith@example..com", removed=r) == ("john.smith@example.com", True)
        assert r == ["19:."]

        # space and "(),:;<>@[\] characters are allowed with restrictions (they are only allowed inside a quoted string,
        # as described in the paragraph below, and in addition, a backslash or double-quote must be preceded
        # by a backslash);
        r = []
        assert correct_email(" john.smith@example.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["0: "]
        r = []
        assert correct_email("john .smith@example.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["4: "]
        r = []
        assert correct_email("john.smith @example.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["10: "]
        r = []
        assert correct_email("john.smith@ example.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["11: "]
        r = []
        assert correct_email("john.smith@ex ample.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["13: "]
        r = []
        assert correct_email("john.smith@example .com", removed=r) == ("john.smith@example.com", True)
        assert r == ["18: "]
        r = []
        assert correct_email("john.smith@example. com", removed=r) == ("john.smith@example.com", True)
        assert r == ["19: "]
        r = []
        assert correct_email("john.smith@example.com  ", removed=r) == ("john.smith@example.com", True)
        assert r == ["22: ", "23: "]
        r = []
        assert correct_email('john(smith@example.com', removed=r) == ('johnsmith@example.com', True)
        assert r == ["4:("]
        r = []
        assert correct_email('"john(smith"@example.com', removed=r) == ('"john(smith"@example.com', False)
        assert r == []

        # comments at begin or end of local and domain part
        r = []
        assert correct_email("john.smith(comment)@example.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["10:(comment)"]
        r = []
        assert correct_email("(comment)john.smith@example.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["0:(comment)"]
        r = []
        assert correct_email("john.smith@example.com(comment)", removed=r) == ("john.smith@example.com", True)
        assert r == ["22:(comment)"]
        r = []
        assert correct_email("john.smith@(comment)example.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["11:(comment)"]
        r = []
        assert correct_email(".john.smith@example.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["0:."]
        r = []
        assert correct_email("john.smith.@example.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["10:."]
        r = []
        assert correct_email("john.smith@.example.com", removed=r) == ("john.smith@example.com", True)
        assert r == ["11:."]
        r = []
        assert correct_email("john.smith@example.com.", removed=r) == ("john.smith@example.com", True)
        assert r == ["22:."]

        # international characters above U+007F
        r = []
        assert correct_email('Heinz.Hübner@example.com', removed=r) == ('Heinz.Hübner@example.com', False)
        assert r == []

        # quoted may exist as a dot separated entity within the local-part, or it may exist when the outermost
        # .. quotes are the outermost characters of the local-part
        r = []
        assert correct_email('abc."def".xyz@example.com', removed=r) == ('abc."def".xyz@example.com', False)
        assert r == []
        assert correct_email('"abc"@example.com', removed=r) == ('"abc"@example.com', False)
        assert r == []
        assert correct_email('abc"def"xyz@example.com', removed=r) == ('abcdefxyz@example.com', True)
        assert r == ['3:"', '7:"']

        # tests from https://en.wikipedia.org/wiki/Email_address
        r = []
        assert correct_email('ex-indeed@strange-example.com', removed=r) == ('ex-indeed@strange-example.com', False)
        assert r == []
        r = []
        assert correct_email("#!$%&'*+-/=?^_`{}|~@example.org", removed=r) == ("#!$%&'*+-/=?^_`{}|~@example.org", False)
        assert r == []
        r = []
        assert correct_email('"()<>[]:,;@\\\\"!#$%&\'-/=?^_`{}| ~.a"@e.org', removed=r) \
            == ('"()<>[]:,;@\\\\"!#$%&\'-/=?^_`{}| ~.a"@e.org', False)
        assert r == []

        r = []
        assert correct_email("A@e@x@ample.com", removed=r) == ("A@example.com", True)
        assert r == ["3:@", "5:@"]
        r = []
        assert correct_email('this is "not" \\allowed@example.com', removed=r) == ('thisisnotallowed@example.com', True)
        assert r == ['4: ', '7: ', '8:"', '12:"', '13: ', '14:\\']

    def test_correct_phone(self):
        assert correct_phone(cast(str, None)) == ('', False)
        assert correct_phone('') == ('', False)

        r = []
        assert correct_phone('+4455667788', removed=r) == ('004455667788', True)
        assert r == ["0:+"]

        r = []
        assert correct_phone(' +4455667788', removed=r) == ('004455667788', True)
        assert r == ["0: ", "1:+"]

        r = []
        assert correct_phone('+004455667788', removed=r) == ('004455667788', True)
        assert r == ["0:+"]

        r = []
        assert correct_phone(' 44 5566/7788', removed=r) == ('4455667788', True)
        assert r == ["0: ", "3: ", "8:/"]

        r = []
        assert correct_phone(' 44 5566/7788-123', removed=r) == ('4455667788123', True)
        assert r == ["0: ", "3: ", "8:/", "13:-"]

        r = []
        assert correct_phone(' 44 5566/7788-123', removed=r, keep_1st_hyphen=True) == ('4455667788-123', True)
        assert r == ["0: ", "3: ", "8:/"]
