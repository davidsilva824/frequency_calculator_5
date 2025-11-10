from zipf_calculator_babyLM import Zipf_calculator_babyLM
babylm = Zipf_calculator_babyLM()

print(babylm.get_zipf_babyLM_10M_word("rat"))
print(babylm.get_zipf_babyLM_100M_word("rat"))

print(babylm.get_zipf_babyLM_10M_list(["the", "dog", "apple", "nonsenseword"]))
print(babylm.get_zipf_babyLM_100M_list(["the", "dog", "apple","nonsenseword"]))

print(babylm.zipf_babyLM_10M("apple"))
print(babylm.zipf_babyLM_100M("apple"))

print(babylm.zipf_babyLM_10M(["the", "dog"]))
print(babylm.zipf_babyLM_100M(["the", "dog"]))

