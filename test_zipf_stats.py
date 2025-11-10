from zipf_stats import Zipf_stats

list_a = [10, 20, 30, 40, 50]
list_b = [11, 21, 29, 42, 53]

stats = Zipf_stats()

d_value = stats.cohens_d_from_lists(list_a, list_b)

print(f"List 1: {list_a}")
print(f"List 2: {list_b}")
print(f"Calculated Cohen's d: {d_value}")
print("Expected Cohen's d:  -0.809")