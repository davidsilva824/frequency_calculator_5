### this module obtains the frequency of compounds (Non-Head + Head) in the datasets of babyLM (10M and 100M).

# It searches for several forms of the compound:
# e.g. 'rat eater'; 'rats eater"; 

import os
import re
from collections import Counter
import inflect 


CORPUS_FILENAMES = [
    "concatenated_train_10M.csv",
    "concatenated_train_100M.csv"
]

def get_all_phrases():
    
    p = inflect.engine() # to transform plurals into singulars and vice versa

    compound_groups = [
        (
            ['goose', 'geese', 'swan', 'swans'],
            ['area', 'trader', 'tracker', 'expert']
        ),
        (
            ['ox', 'oxen', 'cow', 'cows'],
            ['register', 'trader', 'tracker', 'area']
        ),
        (
            ['louse', 'lice', 'flea', 'fleas'],
            ['issue', 'trader', 'tracker', 'expert']
        ),
        (
            ['mouse', 'mice', 'rat', 'rats'],
            ['issue', 'trader', 'tracker', 'protector']
        ),
        (
            ['foot', 'feet', 'leg', 'legs'],
            ['issue', 'examination', 'expert', 'protector']
        ),
        (
            ['tooth', 'teeth', 'bone', 'bones'],
            ['issue', 'examination', 'expert', 'protector']
        ),
        (
            ['child', 'children', 'adult', 'adults'],
            ['patrol', 'register', 'committee', 'brigade']
        ),
        (
            ['woman', 'women', 'girl', 'girls'],
            ['area', 'register', 'committee', 'brigade']
        ),
        (
            ['man', 'men', 'boy', 'boys'],
            ['committee', 'examination', 'area', 'patrol']
        ),
        (
            ['salesman', 'salesmen', 'vendor', 'vendors'],
            ['association', 'inspector', 'protector', 'employer']
        ),
        (
            ['nobleman', 'noblemen', 'aristocrat', 'aristocrats'],
            ['patrol', 'association', 'committee', 'brigade']
        ),
        (
            ['boatman', 'boatmen', 'shipmate', 'shipmates'],
            ['association', 'patrol', 'inspector', 'employer']
        ),
        (
            ['craftsman', 'craftsmen', 'labourer', 'labourers'],
            ['employer', 'inspector', 'examination', 'association']
        ),
        (
            ['fireman', 'firemen', 'lifeguard', 'lifeguards'],
            ['register', 'employer', 'brigade', 'inspector']
        )
    ]
    
    singular_phrases = []
    plural_phrases = []
    
    for non_head_group, head_group in compound_groups:
        for head in head_group:
            
            singular_head = p.singular_noun(head) or head
            plural_head = p.plural(singular_head)
            
            for subject in non_head_group:
               
                singular_phrases.append(f"{subject} {singular_head}")
                singular_phrases.append(f"{subject}-{singular_head}")
                singular_phrases.append(f"{subject}{singular_head}")
                
                if singular_head != plural_head:
                    plural_phrases.append(f"{subject} {plural_head}")
                    plural_phrases.append(f"{subject}-{plural_head}")
                    plural_phrases.append(f"{subject}{plural_head}")
            
    # Return two distinct lists
    return singular_phrases, plural_phrases

def main():
    """Main function to run the count for all specified files."""
    
    # 1. Get the list of all phrase variations
    singular_phrases, plural_phrases = get_all_phrases()
    
    all_phrases = singular_phrases + plural_phrases
    
    # Build ONE combined regex pattern
 
    pattern_core = "|".join(re.escape(p) for p in all_phrases)
    combined_pattern = re.compile(r'\b(' + pattern_core + r')\b')
    
    print("Combined regex pattern built. Starting file processing...")
    print(f"(Searching for {len(all_phrases)} total variations)")


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

          
            all_matches = combined_pattern.findall(corpus_text)

            # Count the frequencies of the results
            if not all_matches:
                print("No items were found.")
                print(f"\n--- END OF REPORT FOR: {filename} ---")
                continue

            frequency_counts = Counter(all_matches)

            # Print the results            
            print("Found items:")
            
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