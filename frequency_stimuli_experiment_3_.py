# Version 3.0
# It searches for 16 forms of the compound if it is regular, including possessive forms.


import os
import re
from collections import Counter
import inflect  
from zipf_calculator_babyLM import Zipf_calculator_babyLM

# this part is just to download he BabyLM datasets and create the concatenate_train files.
#  in case they are not already in the working folder. 
print("Checking for corpus files...")  
corpus_setup = Zipf_calculator_babyLM()
print("Corpus files are ready.")
#----------------------------------------------

### Insert combinations in compound_groups.


CORPUS_FILENAMES = [
    "concatenated_train_10M.csv",
    "concatenated_train_100M.csv"
]

def make_possessive(word):
    
    if word.endswith('s'):
        return word + "'"
    else:
        return word + "'s"
 
def get_all_phrases():

    
    p = inflect.engine() # to transform plurals into singulars and vice versa

    compound_groups = [
    (
        ['goose', 'geese', 'swan', 'swans'],
        ['protector', 'trader', 'tracker', 'expert']
    ),
    (
        ['ox', 'oxen', 'cow', 'cows'],
        ['register', 'trader', 'tracker', 'finder']
    ),
    (
        ['louse', 'lice', 'flea', 'fleas'],
        ['issue', 'trader', 'tracker', 'expert']
    ),
    (
        ['mouse', 'mice', 'rat', 'rats'],
        ['issue', 'trader', 'tracker', 'inspector']
    ),
    (
        ['foot', 'feet', 'leg', 'legs'],
        ['issue', 'examination', 'expert', 'inspector']
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
        ['protector', 'register', 'hangout', 'brigade']
    ),
    (
        ['man', 'men', 'boy', 'boys'],
        ['committee', 'register', 'finder', 'hangout']
    ),
    (
        ['salesman', 'salesmen', 'retailer', 'retailers'],
        ['committee', 'inspector', 'protector', 'employer']
    ),
    (
        ['nobleman', 'noblemen', 'aristocrat', 'aristocrats'],
        ['patrol', 'hangout', 'committee', 'brigade']
    ),
    (
        ['boatman', 'boatmen', 'shipmate', 'shipmates'],
        ['brigade', 'finder', 'inspector', 'employer']
    ),
    (
        ['craftsman', 'craftsmen', 'labourer', 'labourers'],
        ['employer', 'examination', 'hangout', 'finder']
    ),
    (
        ['fireman', 'firemen', 'lifeguard', 'lifeguards'],
        ['examination', 'employer', 'brigade', 'patrol']
    )
]
    
    singular_phrases = []
    plural_phrases = []
    possessive_phrases = []
    
    # Sorts phrases into the three lists.
    for group, head_list in compound_groups:
        
        for head in head_list:
            
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

                # Add POSSESSIVE variations
                poss_subject = make_possessive(subject)
                
                # e.g., "rat's eater" or "rats' eater"
                possessive_phrases.append(f"{poss_subject} {singular_head}")
                
                # e.g., "rat's eaters" or "rats' eaters"
                if singular_head != plural_head:
                    possessive_phrases.append(f"{poss_subject} {plural_head}")
                # ---------------------------------------
            
    # Return three distinct lists
    return singular_phrases, plural_phrases, possessive_phrases

# Get the list of all phrase variations
singular_phrases, plural_phrases, possessive_phrases = get_all_phrases()

all_phrases = singular_phrases + plural_phrases + possessive_phrases

# Build ONE combined regex pattern

pattern_core = "|".join(re.escape(p) for p in all_phrases)
combined_pattern = re.compile(r'\b(' + pattern_core + r')\b')

print("Combined regex pattern built. Starting file processing...")
print(f"(Searching for {len(all_phrases)} total variations)")


# Loop through each file
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

        # Run the SINGLE regex search
        all_matches = combined_pattern.findall(corpus_text)

        # Count the frequencies of the results
        if not all_matches:
            print("No items were found.")
            print(f"\n--- END OF REPORT FOR: {filename} ---")
            continue

        frequency_counts = Counter(all_matches)

        # Print the results
        # Prints results in THREE separate, grouped sections
        
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
    
        # Print Plurals
        print("\n--- Plural Head Forms ---")
        found_in_plural = False
        for phrase in plural_phrases:
            count = frequency_counts.get(phrase, 0)
            if count > 0:
                print(f"{phrase}: {count}")
                found_in_plural = True

        if not found_in_plural:
            print("No items found for this group.")

        # Print Possessives ---
        print("\n--- Possessive Forms ---")
        found_in_possessive = False
        for phrase in possessive_phrases:
            count = frequency_counts.get(phrase, 0)
            if count > 0:
                print(f"{phrase}: {count}")
                found_in_possessive = True
                
        if not found_in_possessive:
            print("No items found for this group.")


        print(f"\n--- END OF REPORT FOR: {filename} ---")

    except MemoryError:
        print(f"MemoryError: The file '{filename}' is too large to read into memory.")
    except Exception as e:
        print(f"An error occurred while reading '{filename}': {e}")