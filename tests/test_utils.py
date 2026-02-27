from med_translation.utils import counter_summary_clean, word_count


def test_word_count_edge_cases():
    assert word_count(None) == 0
    assert word_count(["hello", "world"]) == 2
    assert word_count(1234) == 1
    assert word_count("one two three") == 3


def test_counter_summary_clean_merges_parenthetical_suffix():
    data = [{"errors_1": "Negation (subtle)"}, {"errors_1": "Negation"}]
    result = counter_summary_clean(data, ["errors_1"], clean=True)
    assert result[0] == ("Negation", 2)
