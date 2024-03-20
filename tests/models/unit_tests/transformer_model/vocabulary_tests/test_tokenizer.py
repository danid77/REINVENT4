import pytest

from reinvent.models.transformer.core.vocabulary import SMILESTokenizer
from tests.test_data import SCAFFOLD_TO_DECORATE, WARHEAD_PAIR


@pytest.mark.parametrize(
    "input, expected",
    [
        ("CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O", [
                "C",
                "C",
                "(",
                "C",
                ")",
                "C",
                "c",
                "1",
                "c",
                "c",
                "c",
                "(",
                "c",
                "c",
                "1",
                ")",
                "[C@@H]",
                "(",
                "C",
                ")",
                "C",
                "(",
                "=",
                "O",
                ")",
                "O"
            ]),
        ("C%12CC(Br)C1CC%121[ClH]", [
                "C",
                "%12",
                "C",
                "C",
                "(",
                "Br",
                ")",
                "C",
                "1",
                "C",
                "C",
                "%12",
                "1",
                "[ClH]",
            ]),
        (SCAFFOLD_TO_DECORATE, ['[*]', 'c', '1', 'c', 'c', 'c', '(', 'c', 'c', '1', ')', 'c', '2', 'c', 'c', '(', 'n', 'n', '2', 'c',
             '3', 'c', 'c', 'c', '(', 'c', 'c', '3', ')', 'S', '(', '=', 'O', ')', '(', '=', 'O', ')', 'N', ')', '[*]',
            ]),
        (WARHEAD_PAIR, ['*', 'C', '1', 'C', 'C', 'C', 'C', 'C', '1', '|',
                        '*', 'C', '1', 'C', 'C', 'C', 'C', '(', 'O', 'N', ')', 'C', '1'])
    ]
)

def test_tokenize(input, expected):
    tokenizer = SMILESTokenizer()
    result = tokenizer.tokenize(input, with_begin_and_end=False)
    assert result == expected

@pytest.mark.parametrize(
    "input, expected",
    [
        ([
                "C",
                "C",
                "(",
                "C",
                ")",
                "C",
                "c",
                "1",
                "c",
                "c",
                "c",
                "(",
                "c",
                "c",
                "1",
                ")",
                "[C@@H]",
                "(",
                "C",
                ")",
                "C",
                "(",
                "=",
                "O",
                ")",
                "O"
            ], "CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O"),
        ([
                "C",
                "%12",
                "C",
                "C",
                "(",
                "Br",
                ")",
                "C",
                "1",
                "C",
                "C",
                "%12",
                "1",
                "[ClH]",
            ], "C%12CC(Br)C1CC%121[ClH]"),
        (['[*]', 'c', '1', 'c', 'c', 'c', '(', 'c', 'c', '1', ')', 'c', '2', 'c', 'c', '(', 'n', 'n', '2', 'c',
             '3', 'c', 'c', 'c', '(', 'c', 'c', '3', ')', 'S', '(', '=', 'O', ')', '(', '=', 'O', ')', 'N', ')', '[*]',
            ], SCAFFOLD_TO_DECORATE),
        (['*', 'C', '1', 'C', 'C', 'C', 'C', 'C', '1', '|',
                        '*', 'C', '1', 'C', 'C', 'C', 'C', '(', 'O', 'N', ')', 'C', '1'], WARHEAD_PAIR)
    ]
)
def test_untokenize(input, expected):
    tokenizer = SMILESTokenizer()
    result = tokenizer.untokenize(expected)
    assert result == expected