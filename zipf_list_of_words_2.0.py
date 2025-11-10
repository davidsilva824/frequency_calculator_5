from zipf_calculator import Zipf_calculator
import pandas as pd  

print()

input_string = input("Insert the words separated by a comma (e.g. man, dog,...): ")
words = [word.strip().lower() for word in input_string.split(",")]

print()

a = Zipf_calculator()


subtlex_results = a.zipf_subtlex(words)

print(subtlex_results)

baby10m_results = a.zipf_babyLM_10M(words)

print(baby10m_results)

baby100m_results = a.zipf_babyLM_100M(words)

print(baby100m_results)


data = {
    "Zipfsubtlex": [subtlex_results.get(word, 0) for word in words],
    "Zipf 10M": [baby10m_results.get(word, 0) for word in words],
    "Zipf 100M": [baby100m_results.get(word, 0) for word in words]
}

df = pd.DataFrame(data, index=words)

print("\n\n--- Zipf Values ---")
print()
print(df)
print()

output_filename = "zipf_results.csv"
try:
    df.to_csv(output_filename)
    print(f"\nSuccessfully saved results to {output_filename}")
except Exception as e:
    print(f"\nError: Could not save file. {e}")
# ----------------------