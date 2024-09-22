[![CI](https://github.com/siliconshells/NLP_Assignment_3/actions/workflows/workflow.yml/badge.svg)](https://github.com/siliconshells/NLP_Assignment_3/actions/workflows/workflow.yml)

Assignment 3 for the Natural Language Programming course

> Assignment: Noisy Channel Model Spelling Corrector    
> Name: Leonard Eshun

## The following assumptions were made
1. There are no capital letters in the words being corrected
1. The error where the first letter is left out doesn't exist in this model
1. It's assumed that the word being corrected has a single letter edited
1. It's assumed that all wrong words submitted don't have _transposition between adjacent letters_. It could contain addition, substitution or deletion edits.
1. It is assumed that phonetic errors will not be supplied for correction
1. It is assumed that no wrongly applied/used word will be supplied for correction because the algorithm doesn't have context of the sentence in which the word is used.
1. It is assumed that the 'wrong' words are indeed spelt wrongly.

## The following words were tested
    (base) ➜  Assignment 3 /opt/miniconda3/bin/python "/Users/leonard/Library/CloudStorage/Dropbox/Duke/Academics/Year 1 Semester 1/NLP/Assignment 3/noisy_channel_word_corrector.py"
    The wrong word provided was 'camoflage', and the correct word found was 'camouflage'
    The wrong word provided was 'concensus', and the correct word found was 'consensus'
    The wrong word provided was 'contraversy', and the correct word found was 'controversy'
    The wrong word provided was 'definate', and the correct word found was 'definite'
    The wrong word provided was 'conceed', and the correct word found was 'conceded'
    The wrong word provided was 'heirarchy', and the correct word found was 'heirarchy'
    The wrong word provided was 'judgement', and the correct word found was 'judgment'
    The wrong word provided was 'lisence', and the correct word found was 'licence'
    The wrong word provided was 'sargent', and the correct word found was 'sagent'
    The wrong word provided was 'religous', and the correct word found was 'religious'
    The wrong word provided was 'tommorow', and the correct word found was 'tomorow'
    The wrong word provided was 'wierd', and the correct word found was 'wird'
    (base) ➜  Assignment 3 


## Observation
Because this is a Levenshtein edit distance, it performed well for the three(3) edits that were handled by the Levenshtein model, namely additions, substitutions and deletions. Though it tried to correct the fourth type of edit, _transposition between two adjacent letters_, it failed in all scenarios above (wierd, heirarchy and conceed). To make the model successful at these words, we have to handle the fourth edit, transposition between adjacent letters. This could be done by using other Levenshtein models that handle it.