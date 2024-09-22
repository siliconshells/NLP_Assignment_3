from noisy_channel_model_spelling_corrector import correct


def test_corrector():
    # test
    assert correct("camoflage") == "camouflage"
    assert correct("concensus") == "consensus"
    assert correct("tommorow") == "tomorow"
    assert correct("religous") == "religious"
    assert correct("sargent") == "sagent"
    assert correct("lisence") == "licence"
    assert correct("judgement") == "judgment"
    assert correct("definate") == "definite"
    assert correct("contraversy") == "controversy"


if __name__ == "__main__":
    test_corrector()
    print("Test completed successfully")
