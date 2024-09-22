import numpy as np

# *************************************#
# Spelling Correction - NLP
# Leonard Eshun
# *************************************#

alphabets = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]


corpus_dtype = [("word", "U50"), ("count", "i8")]

corpus = np.loadtxt("corpus.tsv", delimiter="\t", dtype=corpus_dtype)

bigrams = np.genfromtxt(
    "bigrams.csv", delimiter=",", names=True, dtype=None, encoding="utf-8"
)
additions = np.genfromtxt(
    "additions.csv", delimiter=",", names=True, dtype=None, encoding="utf-8"
)
# prefix with value # doesn't get loaded
deletions = np.genfromtxt(
    "deletions.csv", delimiter=",", names=True, dtype=None, encoding="utf-8"
)
substitutions = np.genfromtxt(
    "substitutions.csv", delimiter=",", names=True, dtype=None, encoding="utf-8"
)
unigrams = np.genfromtxt(
    "unigrams.csv", delimiter=",", names=True, dtype=None, encoding="utf-8"
)

# sum of all the counts in the corpus
sum_of_corpus = np.sum(corpus["count"])


def find_deletion_probability(word: str) -> int:
    alteration = word.split("~")[0]
    if alteration[0] == "#":
        return 0

    expected_word = word.split("~")[1]
    # find P(x|w)P(w)
    # Find the word in the corpus and retrieve its count
    count_in_corpus = corpus[corpus["word"] == expected_word]["count"][0]
    # P(w) = count found in corpus / total counts
    # P(x|w) = value in deletion csv / value in bigram
    # Finding value in deletion
    # filter by the prefix column
    count_in_deletion = deletions[deletions["prefix"] == alteration[0]]
    # filter result above by the deleted column
    count_in_deletion = count_in_deletion[count_in_deletion["deleted"] == alteration[1]]

    if len(count_in_deletion) > 0:
        count_in_deletion = count_in_deletion[0][2]
    else:
        count_in_deletion = 0

    # Finding value in bigram
    count_in_bigram = bigrams[bigrams["bigram"] == alteration]["count"][0]

    return (count_in_corpus / sum_of_corpus) * (count_in_deletion / count_in_bigram)


def find_substitution_probability(word: str) -> int:
    alteration = word.split("~")[0]
    if alteration[0] == "#":
        return 0

    expected_word = word.split("~")[1]
    # find P(x|w)P(w)
    # Find the word in the corpus and retrieve its count
    count_in_corpus = corpus[corpus["word"] == expected_word]["count"][0]
    # P(w) = count found in corpus / total counts
    # P(x|w) = value in substitutions csv / value in unigram
    # Finding value in substitutions
    # filter by the original column
    count_in_substitutions = substitutions[substitutions["original"] == alteration[0]]
    # filter result above by the substituted column
    count_in_substitutions = count_in_substitutions[
        count_in_substitutions["substituted"] == alteration[1]
    ]
    if len(count_in_substitutions) > 0:
        count_in_substitutions = count_in_substitutions[0][2]
    else:
        count_in_substitutions = 0
    # Finding value in unigram
    count_in_unigram = unigrams[unigrams["unigram"] == alteration[0]]["count"][0]

    return (count_in_corpus / sum_of_corpus) * (
        count_in_substitutions / count_in_unigram
    )


def find_addition_probability(word: str) -> int:
    alteration = word.split("~")[0]
    if alteration[0] == "#":
        return 0

    expected_word = word.split("~")[1]
    # find P(x|w)P(w)
    # Find the word in the corpus and retrieve its count
    count_in_corpus = corpus[corpus["word"] == expected_word]["count"][0]
    # P(w) = count found in corpus / total counts
    # P(x|w) = value in additions csv / value in unigram
    # Finding value in additions
    # filter by the original column
    count_in_additions = additions[additions["prefix"] == alteration[0]]
    # filter result above by the substituted column
    count_in_additions = count_in_additions[
        count_in_additions["added"] == alteration[1]
    ]
    if len(count_in_additions) > 0:
        count_in_additions = count_in_additions[0][2]
    else:
        count_in_additions = 0
    # Finding value in unigram
    count_in_unigram = unigrams[unigrams["unigram"] == alteration[0]]["count"][0]

    return (count_in_corpus / sum_of_corpus) * (count_in_additions / count_in_unigram)


def correct(original: str) -> str:
    possible_words_dictionary = dict()
    # get all possible word alterations
    possible_word_alterations = get_edits(original, alphabets)
    # remove the words not in dictionary
    for alteration in possible_word_alterations:
        # pick the word from edit's output
        # this function is slow
        # if np.isin(alteration[1], corpus["word"]):
        if alteration[1] in corpus["word"]:
            # only add the words in the corpus
            possible_words_dictionary[alteration] = 0

    # at this point we have the list of valid words and what happened to them
    # now calculate the probabilities
    for dictionary in possible_words_dictionary:
        # tuple
        operation_n_altered = dictionary[0]
        operation = operation_n_altered.split(":")[0]
        altered = operation_n_altered.split(":")[1]

        word = dictionary[1]
        if operation == "d":
            possible_words_dictionary[dictionary] = find_deletion_probability(
                # join the alteration to the expected word
                altered
                + "~"
                + word
            )
        elif operation == "s":
            possible_words_dictionary[dictionary] = find_substitution_probability(
                # join the alteration to the expected word
                altered
                + "~"
                + word
            )
        elif operation == "a":
            possible_words_dictionary[dictionary] = find_addition_probability(
                # join the alteration to the expected word
                altered
                + "~"
                + word
            )

    # get the largest probability
    correct_word = ""
    largest_number = 0
    for key, value in possible_words_dictionary.items():
        if value >= largest_number:
            largest_number = value
            correct_word = key

    return correct_word[1]


def get_edits(original: str, characters: list[str]) -> list[tuple[str, str]]:
    edits = []

    # generate deletions
    for idx, char in enumerate(original):
        previous_char = original[idx - 1] if idx > 0 else "#"
        edits.append((f"d:{previous_char}{char}", original[:idx] + original[idx + 1 :]))

    # generate substitutions
    for idx, old_char in enumerate(original):
        for new_char in characters:
            edits.append(
                (
                    f"s:{old_char}{new_char}",
                    original[:idx] + new_char + original[idx + 1 :],
                )
            )

    # generate additions
    for idx, char in enumerate("#" + original):
        for new_char in characters:
            edits.append(
                (
                    f"a:{char}{new_char}",
                    original[:idx] + new_char + original[idx:],
                )
            )

    return edits
