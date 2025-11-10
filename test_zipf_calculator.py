### some basic tests to the classes created. Need to add true unittests still.

from zipf_calculator import Zipf_calculator

# Instantiating without parameters (only SUBTLEX methods will be used)
z = Zipf_calculator()

print(z.get_zipf_subtlex_word("dog")) 

print(z.get_zipf_subtlex_word("nonsenseword")) 


words = ["dog", "cat", "nonsenseword"]
print(z.get_zipf_subtlex_list(words))


z.zipf_subtlex("dog")
z.zipf_subtlex(["dog", "cat", "nonsenseword"])

# Test with string
text = "The dog barked. The dog ran."
print(z.tokenize(text))  # ['the', 'dog', 'barked', 'the', 'dog', 'ran']
print(z.get_number_of_tokens(text))  # 6
print(z.get_freq("dog", text))  # 2


print(z.get_zipf_babyLM_10M_word("rat"))
print(z.get_zipf_babyLM_100M_word("rat"))