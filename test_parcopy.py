import unittest
import parcopy1
import parcopy2


def CASE(inp, exp):
    return (inp, exp)


test_cases = [
    # Trivial case
    CASE(
        [("a", "b"), ("b", "c")],
        [("a", "b"), ("b", "c")]
    ),
    # Reversed trivial case
    CASE(
        [("b", "c"), ("a", "b")],
        [("a", "b"), ("b", "c")]
    ),
    # Reorder trivial 3-var case
    CASE(
        [("c", "d"), ("b", "c"), ("a", "b")],
        [("a", "b"), ("b", "c"), ("c", "d")]
    ),
    # Self-loop is optimized away
    CASE(
        [("a", "a")],
        []
    ),
    # 2 self-loops
    CASE(
        [("a", "a"), ("b", "b")],
        []
    ),
    # Loop of 2 vars
    CASE(
        [("a", "b"), ("b", "a")],
        [("tmp", "b"), ("b", "a"), ("a", "tmp")]
    ),
    # Reversed loop of 2 vars
    CASE(
        [("b", "a"), ("a", "b")],
        [("tmp", "a"), ("a", "b"), ("b", "tmp")]
    ),
    # Loop of 3 vars
    CASE(
        [("a", "b"), ("b", "c"), ("c", "a")],
        [("tmp", "c"), ("c", "a"), ("a", "b"), ("b", "tmp")]
    ),
    # 2 loops each of 2 vars
    CASE(
        [("a", "b"), ("b", "a"), ("c", "d"), ("d", "c")],
        [("tmp", "d"), ("d", "c"), ("c", "tmp"), ("tmp", "b"), ("b", "a"), ("a", "tmp")]
    ),
]


class ParCopyTests(unittest.TestCase):
    def test_sequentialize(self) -> None:
        for inp, exp in test_cases:
            for seq_func in (parcopy1.sequentialize, parcopy2.sequentialize):
                with self.subTest(seq_func=seq_func, inp=inp, exp=exp):
                    self.assertEqual(seq_func(inp), exp)

    def test_dup_dest_raises(self) -> None:
        for seq_func in (parcopy1.sequentialize, parcopy2.sequentialize):
            with self.subTest(seq_func=seq_func):
                with self.assertRaises(ValueError):
                    seq_func([("a", "b"), ("b", "c"), ("b", "a")])

    def test_dup_dest(self) -> None:
        for seq_func in (parcopy1.sequentialize, parcopy2.sequentialize):
            with self.subTest(seq_func=seq_func):
                result = seq_func([("a", "b"), ("b", "c"), ("b", "a")], filter_dup_dests=True)
                self.assertEqual(result, [("tmp", "b"), ("b", "a"), ("a", "tmp")])

    def test_fan_out(self) -> None:
        fan_out_cases = [
            CASE(
                [("b", "a"), ("c", "a")],
                [("c", "a"), ("b", "c")]
            ),
            CASE(
                [("a", "d"), ("b", "a"), ("c", "a"), ("d", "c")],
                [("b", "a"), ("a", "d"), ("d", "c"), ("c", "b")]
            ),
            CASE(
                [("b", "a"), ("c", "b"), ("a", "c"), ("d", "c")],
                [("d", "c"), ("c", "b"), ("b", "a"), ("a", "d")]
            ),
        ]
        for inp, exp in fan_out_cases:
            for seq_func in (parcopy1.sequentialize, parcopy2.sequentialize):
                with self.subTest(seq_func=seq_func, inp=inp, exp=exp):
                    self.assertEqual(seq_func(inp), exp)


if __name__ == "__main__":
    unittest.main()
