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


# --- (NEW) Helper function to create possessives ---
def make_possessive(word):
    """
    Smartly creates a possessive form of a word.
    rat -> rat's
    rats -> rats'
    mice -> mice's
    """
    if word.endswith('s'):
        return word + "'"
    else:
        return word + "'s"
# --------------------------------------------------


def get_all_phrases():
    """
    MODIFIED:
    Returns THREE separate lists:
    1. All variations for SINGULAR heads.
    2. All variations for PLURAL heads.
    3. All variations for POSSESSIVE subjects.
    """
    
    # 1. Initialize the inflect engine
    p = inflect.engine()

    # 2. Your list of groups and heads
    compound_definitions = [
        (['woman'], ['reproductive']),
        # Add your other groups here, e.g.:
        # (['mouse', 'mice', 'rat', 'rats'], ['eater', 'trader']),
    ]
    
    # We now create THREE separate lists
    singular_phrases = []
    plural_phrases = []
    possessive_phrases = []  # <-- (NEW) List
    
    # 3. Modified loop to sort phrases into the three lists
    for group, head_list in compound_definitions:
        
        for head in head_list:
            
            singular_head = p.singular_noun(head) or head
            plural_head = p.plural(singular_head)
            
            for subject in group:
                
                # --- This logic is UNCHANGED ---
                # Add all SINGULAR head variations
                singular_phrases.append(f"{subject} {singular_head}")
                singular_phrases.append(f"{subject}-{singular_head}")
                singular_phrases.append(f"{subject}{singular_head}")
                
                # Add PLURAL head variations (if plural is different)
                if singular_head != plural_head:
                    plural_phrases.append(f"{subject} {plural_head}")
                    plural_phrases.append(f"{subject}-{plural_head}")
                    plural_phrases.append(f"{subject}{plural_head}")
                # ---------------------------------

                # --- (NEW) Add POSSESSIVE variations ---
                poss_subject = make_possessive(subject)
                
                # e.g., "rat's eater" or "rats' eater"
                possessive_phrases.append(f"{poss_subject} {singular_head}")
                
                # e.g., "rat's eaters" or "rats' eaters"
                if singular_head != plural_head:
                    possessive_phrases.append(f"{poss_subject} {plural_head}")
                # ---------------------------------------
            
    # (MODIFIED) Return three distinct lists
    return singular_phrases, plural_phrases, possessive_phrases

def main():
    """Main function to run the count for all specified files."""
    
    # 1. Get the list of all phrase variations
    # (MODIFIED) Now gets THREE separate lists
    singular_phrases, plural_phrases, possessive_phrases = get_all_phrases()
    
    # (MODIFIED) We combine all three here ONLY for building the regex
    all_phrases = singular_phrases + plural_phrases + possessive_phrases
    
    # 2. Build ONE combined regex pattern
    # This logic remains IDENTICAL.
    # re.escape() will correctly handle the new apostrophe.
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
            # (MODIFIED) Prints results in THREE separate, grouped sections
            
            print("Found items:")
            
            # --- Print Singulars (Unchanged) ---
            print("\n--- Singular Head Forms ---")
            found_in_singular = False
            for phrase in singular_phrases:
                count = frequency_counts.get(phrase, 0)
                if count > 0:
                    print(f"{phrase}: {count}")
                    found_in_singular = True
            if not found_in_singular:
                print("No items found for this group.")
        
            # --- Print Plurals (Unchanged) ---
            print("\n--- Plural Head Forms ---")
            found_in_plural = False
            for phrase in plural_phrases:
                count = frequency_counts.get(phrase, 0)
                if count > 0:
                    print(f"{phrase}: {count}")
                    found_in_plural = True
            if not found_in_plural:
                print("No items found for this group.")

            # --- (NEW) Print Possessives ---
            print("\n--- Possessive Forms ---")
            found_in_possessive = False
            for phrase in possessive_phrases:
                count = frequency_counts.get(phrase, 0)
                if count > 0:
                    print(f"{phrase}: {count}")
                    found_in_possessive = True
            if not found_in_possessive:
                print("No items found for this group.")
            # ---------------------------------


            print(f"\n--- END OF REPORT FOR: {filename} ---")

        except MemoryError:
            print(f"MemoryError: The file '{filename}' is too large to read into memory.")
        except Exception as e:
            print(f"An error occurred while reading '{filename}': {e}")

# Run the script
if __name__ == "__main__":
    main()