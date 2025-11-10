### this module obtains the frequency of compounds (Non-Head + Head) in the datasets of babyLM (10M and 100M).
# specifically for the items of experiment 2 in Berent & Pinker (2007).


import os
import re
from collections import Counter
import inflect  # <-- Make sure to 'pip install inflect'

# --- Configuration ---

# List of all corpus files you want to check
CORPUS_FILENAMES = [
    "concatenated_train_10M.csv",
    "concatenated_train_100M.csv"
]

# --- End Configuration ---

def get_all_phrases():
    """
    MODIFIED:
    Returns TWO separate lists:
    1. All variations for SINGULAR heads.
    2. All variations for PLURAL heads.
    """
    
    # 1. Initialize the inflect engine
    p = inflect.engine()

    # 2. Your list of groups and heads
    compound_definitions = [
        (['blaze', 'blazes', 'spark', 'sparks'], 'protector'),
        (['breeze', 'breezes', 'storm', 'storms'], 'protector'),
        (['tax', 'taxes', 'toll', 'tolls'], 'collectors'),
        (['sex', 'sexes', 'gender', 'genders'], 'differences'),
        (['vase', 'vaso', 'pot', 'pots'], 'maker'),
        (['hoax', 'hoaxes', 'joke', 'jokes'], 'victims'),
        (['phase', 'phases', 'step', 'steps'], 'classifier'),
        (['hose', 'hoses', 'pipe', 'pipes'], 'installer'),
        (['fox', 'foxes', 'wolf', 'wolves'], 'chaser'),
        (['mix', 'mixes', 'blend', 'blends'], 'winner'),
        (['nose', 'noses', 'thigh', 'thighs'], 'rashes'),
        (['clause', 'clauses', 'article', 'articles'], 'finder'),
        (['maze', 'mazes', 'web', 'webs'], 'decoder'),
        (['quiz', 'quizzes', 'puzzle', 'puzzles'], 'master'),
        (['fax', 'faxes', 'copy', 'copies'], 'man'),
        (['size', 'sizes', 'shape', 'shapes'], 'machine'),
        (['praise', 'praises', 'compliment', 'compliments'], 'getter'),
        (['prize', 'prizes', 'award', 'awards'], 'winner'),
        (['box', 'boxes', 'pack', 'packs'], 'lifters'),
        (['rose', 'roses', 'flower', 'flowers'], 'growers'),
        (['bruise', 'bruises', 'sore', 'sores'], 'healer'),
        (['rise', 'rises', 'drop', 'drops'], 'addict')
    ]
    
    # We now create two separate lists
    singular_phrases = []
    plural_phrases = []
    
    # 3. Modified loop to sort phrases into the two lists
    for group, head in compound_definitions:
        
        singular_head = p.singular_noun(head) or head
        plural_head = p.plural(singular_head)
        
        for subject in group:
            # Add all SINGULAR head variations
            singular_phrases.append(f"{subject} {singular_head}")
            singular_phrases.append(f"{subject}-{singular_head}")
            singular_phrases.append(f"{subject}{singular_head}")
            
            # Add PLURAL head variations (if plural is different)
            if singular_head != plural_head:
                plural_phrases.append(f"{subject} {plural_head}")
                plural_phrases.append(f"{subject}-{plural_head}")
                plural_phrases.append(f"{subject}{plural_head}")
            
    # Return two distinct lists
    return singular_phrases, plural_phrases

def main():
    """Main function to run the count for all specified files."""
    
    # 1. Get the list of all phrase variations
    # MODIFIED: Now gets two separate lists
    singular_phrases, plural_phrases = get_all_phrases()
    # We combine them here ONLY for building the regex
    all_phrases = singular_phrases + plural_phrases
    
    # 2. Build ONE combined regex pattern
    # This logic remains IDENTICAL.
    pattern_core = "|".join(re.escape(p) for p in all_phrases)
    combined_pattern = re.compile(r'\b(' + pattern_core + r')\b')
    
    print("Combined regex pattern built. Starting file processing...")
    print(f"(Searching for {len(all_phrases)} total variations)")


    # 3. Loop through each file
    for filename in CORPUS_FILENAMES:
        
        print("\n" + "="*60)
        print(f"--- FREQUENCY REPORT FOR: {filename} ---")
        print("="*60 + "\n")
        
        if not os.path.exists(filename):
            print(f"Error: File not found at '{filename}'")
            continue 

        print(f"Loading and processing '{filename}'... (This may take a moment)")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                corpus_text = f.read().lower()
                
            print(f"Corpus loaded. Searching...")

            # 4. Run the SINGLE regex search
            # This logic remains IDENTICAL.
            all_matches = combined_pattern.findall(corpus_text)

            # 5. Count the frequencies of the results
            if not all_matches:
                print("No items were found.")
                print(f"\n--- END OF REPORT FOR: {filename} ---")
                continue

            # This logic remains IDENTICAL.
            frequency_counts = Counter(all_matches)

            # 6. Print the results
            # MODIFIED: Prints results in two separate, grouped sections
            
            print("Found items:")
            
            # --- Print Singulars ---
            print("\n--- Singular Head Forms ---")
            found_in_singular = False
            for phrase in singular_phrases:
                count = frequency_counts.get(phrase, 0)
                if count > 0:
                    print(f"{phrase}: {count}")
                    found_in_singular = True
            if not found_in_singular:
                print("No items found for this group.")
        
            # --- Print Plurals ---
            print("\n--- Plural Head Forms ---")
            found_in_plural = False
            for phrase in plural_phrases:
                count = frequency_counts.get(phrase, 0)
                if count > 0:
                    print(f"{phrase}: {count}")
                    found_in_plural = True
            if not found_in_plural:
                print("No items found for this group.")


            print(f"\n--- END OF REPORT FOR: {filename} ---")

        except MemoryError:
            print(f"MemoryError: The file '{filename}' is too large to read into memory.")
        except Exception as e:
            print(f"An error occurred while reading '{filename}': {e}")

# Run the script
if __name__ == "__main__":
    main()