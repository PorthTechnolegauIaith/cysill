#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# VIRTUALENV: cysill-demo
import unittest


class CysillTestCase(unittest.TestCase):
    
    def test_matches(self):
        from demo3 import get_match
        re_tests = (("yn Bangor", "Dwi'n byw yn '''Bangor'''", "yn '''Bangor"),
                    ("Wirfoddolwyr Wlster", "ddynion i [[Gwirfoddolwyr Wlster|Wirfoddolwyr Wlster]]", "Wirfoddolwyr Wlster"),
                    ("seneddol", "rôl sylweddol yn natblygiad [[democratiaeth]] [[senedd]]ol, ynghyd â chyfraniadau pwysig ym myd [[gwyddoniaeth]].", "senedd]]ol"),
                    ("yn Bangor", "yn [[Bangor]]", "yn [[Bangor"))
        for needle, haystack, match in re_tests:
            m = get_match(needle, haystack, int(len(needle)/2))
            self.assertEqual(m, match)
    
    def test_markup_correction(self):
        from demo3 import gwirio_yn_markup
        markup_tests = (("yn Bangor", "ym Mangor", (("yn Bangor", "ym Mangor"),), ["yn [[Bangor]]"], "ym [[Bangor|Mangor]]"),
                        ("yn Bangor", "ym Mangor", (("yn Bangor", "ym Mangor"),), ["yn '''Bangor'''"], "ym '''Mangor'''"),
                        ("yn Bangor", "ym Mangor", (("yn Bangor", "ym Mangor"),), ["yn [http://techiaith.org Bangor]"], "ym [http://techiaith.org Mangor]"))
        for l, l_wedi_gwirio, gwiriadau, markup_lines, cywir in markup_tests:
            gwirio_yn_markup(l, l_wedi_gwirio, gwiriadau, markup_lines)
            self.assertEqual(markup_lines[0], cywir)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CysillTestCase)
    unittest.TextTestRunner().run(suite)