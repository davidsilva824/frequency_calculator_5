from zipf_stats import Zipf_stats


stat = Zipf_stats('results_non_heads.csv','stat_non_head_all.csv')

print(stat.all_means_all_groups())

print(stat.all_sd_all_groups())

print(stat.cohens_d_all('irregular_singular','irregular_plural'))



list_a = [10, 20, 30, 40, 50]
list_b = [11, 21, 29, 42, 53]

stats = Zipf_stats()

    # 3. Call the new method
d_value = stats.cohens_d_from_lists(list_a, list_b)

    # 4. Print the results
print(f"List 1: {list_a}")
print(f"List 2: {list_b}")
print(f"Calculated Cohen's d: {d_value}")
print("Expected Cohen's d:  -0.809")