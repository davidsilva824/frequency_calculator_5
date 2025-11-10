### This module searches for the best compound combinations of acceptable Non-Heads.
# Conditions imposed in the choice: 
# 1 - goose, ox, louse, mouse, foot, tooth, child, woman and man, have to be used. 
# 2 - Primary criteria of choice: minimizing the highest gap in the mean between singular and plural of each pair, for the 3 datasets. 
# 3 - Secondary criteria of choice: minimazing the maximum gap in the mean between the 4 gropus of noouns.
# 4 - Tertiary criteria of choice: Minimizing the total of the gaps in the 4 groups.       

import itertools
import pandas as pd 
from zipf_stats import Zipf_stats




num_answers = 10 # number of acombinations it should provide.
num_stimuli = 14 # number of stimuli Non_Heads we want to select. 

stats_calculator = Zipf_stats() # calling the class that handles statistics with zipf.

GROUP_KEYS = ("irr_sg", "irr_pl", "reg_sg", "reg_pl")  # names of the groups

def pack(irr_sg, irr_pl, reg_sg, reg_pl): #function that creates a dictionary with the classification 
    return {"irr_sg": irr_sg, "irr_pl": irr_pl, "reg_sg": reg_sg, "reg_pl": reg_pl} 

packs = [
     pack(("goose",4.02777,4.04625,4.22590), ("geese",3.65190,3.54185,3.81799),
         ("swan",3.98376,3.86061,3.83010), ("swans",3.70688,3.50407,3.42038)),

     pack(("goose",4.02777,4.04625,4.22590), ("geese",3.65190,3.54185,3.81799),
         ("duck",4.52952,5.13569,4.95029), ("ducks",3.92771,4.35662,4.38682)),

     pack(("louse",2.66886,2.46267,2.68082), ("lice",3.28680,3.13168,3.04753),
         ("mite",3.08313,3.32797,3.32908), ("mites",3.27780,2.46267,2.89911)),

     pack(("louse",2.66886,2.46267,2.68082), ("lice",3.28680,3.13168,3.04753),
         ("flea",3.49988,3.16164,3.38156), ("fleas",3.45389,2.46267,3.21851)),

     pack(("ox",3.39209,3.52962,3.88383), ("oxen",2.90525,3.82440,3.73648),
         ("ram",3.65334,3.89404,3.98757), ("rams",3.29013,3.32797,3.17247)),

     pack(("ox",3.39209,3.52962,3.88383), ("oxen",2.90525,3.82440,3.73648),
         ("cow",4.44011,4.84529,4.99550), ("cows",4.25276,4.30152,4.41124)),

     pack(("mouse",4.41482,4.63586,4.80005), ("mice",3.91164,4.08936,4.19474),
         ("rat",4.22555,4.12857,4.20520), ("rats",4.02838,3.94934,4.00640)),

     pack(("child", 5.14472, 5.68400, 5.50831), ("children", 5.52835, 5.52085, 5.50545),
         ("adult", 4.40331, 4.29942, 4.71605), ("adults", 4.27277, 4.08936, 4.16001)),

     pack(("woman",5.22085,5.36322,5.36451), ("women",5.28064,5.17616,5.24917),
         ("girl",5.29345,5.71423,5.70143), ("girls",5.22702,5.31617,5.34394)),

     pack(("man",5.85755,5.98106,5.99202), ("men",5.36528,5.57315,5.59830),
         ("boy",5.27610,5.77351,5.75638), ("boys",5.19912,5.40203,5.43891)),

     pack(("salesman",3.69005,3.56534,3.45749), ("salesmen",2.95341,2.93979,2.71490),
         ("vendor",3.12062,2.98555,2.94001), ("vendors",2.97220,2.58761,2.89911)),

     pack(("salesman",3.69005,3.56534,3.45749), ("salesmen",2.95341,2.93979,2.71490),
         ("retailer",3.63074,2.68452,2.90444), ("retailers",3.91663,2.76370,2.81670)),

     pack(("salesman",3.69005,3.56534,3.45749), ("salesmen",2.95341,2.93979,2.71490),
         ("merchant",3.78245,4.02298,4.15379), ("merchants",3.44081,3.54185,3.82695)),

     pack(("tooth",4.08773,3.96328,4.11284), ("teeth",4.70053,4.82878,4.90913),
         ("bone",4.51390,4.41043,4.45257), ("bones",4.42982,4.50930,4.46426)),

     pack(("foot",4.91934,5.09072,5.10584), ("feet",5.07716,5.31637,5.35163),
         ("leg",4.87632,4.76298,4.81129), ("legs",4.85298,4.93494,4.96283)),

     pack(("foot", 4.91934, 5.09072, 5.10584), ("feet", 5.07716, 5.31637, 5.35163),
         ("hand", 5.43662, 5.6605, 5.66254), ("hands", 5.24962, 5.45962, 5.48105)),

     pack(("nobleman",2.82284,3.26431,3.33305), ("noblemen",2.53458,2.46267,3.02001),
         ("aristocrat",3.08843,2.28658,2.89371), ("aristocrats",3.08313,2.88864,2.90970)),

     pack(("nobleman",2.82284,3.26431,3.33305), ("noblemen",2.53458,2.46267,3.02001),
         ("courtier",2.65952,2.88864,2.77595), ("courtiers",2.92618,2.76370,3.13984)),

     pack(("boatman",2.62515,2.83065,3.31284), ("boatmen",2.64022,2.83065,2.84796),
         ("shipmate",2.34895,2.76370,2.77595), ("shipmates",2.60955,3.06473,3.18375)),

     pack(("craftsman",3.25684,3.02694,2.79680), ("craftsmen",3.44081,2.83065,2.94001),
         ("labourer",3.10398,3.13168,2.90970), ("labourers",3.11071,3.21600,3.13675)),

     pack(("fisherman",3.75073,3.49070,3.73959), ("fishermen",3.99284,3.63876,3.64480),
         ("gardener",3.87872,3.61902,3.94050), ("gardeners",3.74262,3.02694,3.18375)),

     pack(("policeman",4.06178,4.44795,4.40577), ("policemen",3.62053,3.84288,3.69219),
         ("detective",4.25540,4.46122,4.43279), ("detectives",3.85830,3.65765,3.59701)),

     pack(("fireman",3.48107,4.10282,4.43763), ("firemen",3.29996,3.66679,3.77738),
         ("lifeguard",2.96525,2.28658,2.69819), ("lifeguards",2.74106,2.46267,2.37084)),

     pack(("fireman", 3.48107, 4.10282, 4.43763), ("firemen", 3.29996, 3.66679, 3.77738),
         ("gardener", 3.87872, 3.61902, 3.94050), ("gardeners", 3.74262, 3.02694, 3.18375)),
]

def gap(vals): # function used in the criteria for the 
    return max(vals) - min(vals)

def score_combo(packs_subset): # receives a subpack of the 24 packs and returns their statistics for comparison.
    group_size = len(packs_subset)
    
    group_values = [[[] for _ in range(3)] for _ in range(4)] # creates a "table" where the values for each group will be stored 
    
    for P in packs_subset: # go through each pack and retrieve the numerical values (3 zipfs) for each condition. 
        for gi, key in enumerate(GROUP_KEYS):
            _, subtlex, baby10, baby100 = P[key]
            group_values[gi][0].append(subtlex)
            group_values[gi][1].append(baby10)
            group_values[gi][2].append(baby100)
            
    means = [[sum(group_values[g][c])/group_size for c in range(3)] for g in range(4)]

    # --- THIS SCORING LOGIC IS UNCHANGED ---
    # secondary: overall group gaps per column (as before)
    gaps = [gap([means[g][c] for g in range(4)]) for c in range(3)]

    # primary: minimize SG↔PL differences within irregular and within regular
    d_irr = [abs(means[1][c] - means[0][c]) for c in range(3)]  # irr_pl - irr_sg
    d_reg = [abs(means[3][c] - means[2][c]) for c in range(3)]  # reg_pl - reg_sg
    
    primary = max(d_irr + d_reg)        # worst within-pair difference across columns
    secondary_main = max(gaps)          # then minimize worst overall gap
    secondary_sum = sum(gaps)           # then minimize total gaps
    # --- END OF UNCHANGED SCORING LOGIC ---

    # --- (NEW) 4. Calculate requested Cohen's d *using your module* ---
    # Compare singulars: irr_sg (group 0) vs reg_sg (group 2)
    cohen_d_sg = [
        stats_calculator.cohens_d_from_lists(group_values[0][c], group_values[2][c]) 
        for c in range(3)
    ]
    # Compare plurals: irr_pl (group 1) vs reg_pl (group 3)
    cohen_d_pl = [
        stats_calculator.cohens_d_from_lists(group_values[1][c], group_values[3][c])
        for c in range(3)
    ]
    cohen_d_vals = (cohen_d_sg, cohen_d_pl) # Package them
    
    # (MODIFIED) Return the new d_vals
    return primary, secondary_main, secondary_sum, gaps, means, cohen_d_vals


def show(ids, packs, gaps, means, cohen_d_vals):
    
    print("Combo IDs:", ids)
    for idx in ids:
        P = packs[idx]
        a, b, c, d = P["irr_sg"], P["irr_pl"], P["reg_sg"], P["reg_pl"]
        print(f"  {a[0]}/{b[0]} — {c[0]}/{d[0]}")
    labels = ["SUBTLEX", "BabyLM-10M", "BabyLM-100M"]
    print("Group means (Irr-SG / Irr-PL / Reg-SG / Reg-PL):")
    for ci, lab in enumerate(labels):
        col = [means[g][ci] for g in range(4)]
        print(f"  {lab:11s}: " + "  ".join(f"{x:.3f}" for x in col) +
              f"   | gap={max(col)-min(col):.3f}")
    print("Gaps per column:", " / ".join(f"{g:.3f}" for g in gaps))

    print()
    
    # Print the new Cohen's d values ---
    cohen_d_sg, cohen_d_pl = cohen_d_vals # Unpack
    print("Cohen's d (Irr-SG↔Reg-SG / Irr-PL↔Reg-PL):")
    for ci, lab in enumerate(labels):
        print(f"  {lab:11s}:      {cohen_d_sg[ci]:.3f}   /   {cohen_d_pl[ci]:.3f}")
    # ---------------------------------------------

    print("-" * 60)


# precompute word sets (for no repeats)
pack_words = [{P[k][0] for k in GROUP_KEYS} for P in packs]

# ---- Define pack groups based on new requirements ----

# 1. Packs containing the 9 required "pure" irregular pairs
# We must pick ONE pack from each of these 9 groups.
IRR_PACK_GROUPS = [
    ("goose", {0, 1}),
    ("louse", {2, 3}),
    ("child", {4}),
    ("mouse", {5}),
    ("woman", {6}),
    ("man", {7}),
    ("tooth", {11}),
    ("foot", {12, 13}),
    ("ox", {19, 20}),
]

# Get all indices that belong to one of these 9 groups
required_irr_indices = set.union(*[g[1] for g in IRR_PACK_GROUPS])

# 2. "Other" packs (e.g., salesman, nobleman, fireman, etc.)
all_indices = set(range(len(packs)))
# These are the packs NOT in the 9 required groups
other_indices = list(all_indices - required_irr_indices) 

# 3. Define how many "other" packs we need to choose
num_required_irr = len(IRR_PACK_GROUPS)  # This is 9
num_other_to_choose = num_stimuli - num_required_irr  # 14 - 9 = 5

print(f"Goal: {num_stimuli} packs.")
print(f"Scoring objective: Minimize 'within-pair' (SG vs PL) mean \gaps.")
print("-" * 60)

best = []  # (primary, secondary_main, secondary_sum, gaps, means, d_vals, ids)

# 1. Iterate through all (16) possible "base sets" of 9 irregular packs
# 	e.g., (0, 2, 4, 5, 6, 7, 11, 12, 19), (1, 2, 4, 5, 6, 7, 11, 12, 19), etc.
base_set_iter = itertools.product(*[g[1] for g in IRR_PACK_GROUPS])

# 2. Iterate through all combinations of 5 packs from the "other" list
other_set_iter = itertools.combinations(other_indices, num_other_to_choose)

# 3. Combine them: test every base set against every "other" set
for base_ids, other_ids in itertools.product(base_set_iter, other_set_iter):
    
    # Combine the 9 base packs and 5 other packs
    ids = base_ids + other_ids
    
    # Check for word repeats across the full 14-pack set
    used = set()
    ok = True
    for i in ids:
        if used & pack_words[i]:
            ok = False
            break
        used |= pack_words[i]
    if not ok:
        continue
    
    # If no repeats, score this combination
    # (MODIFIED) Store the new d_vals
    primary, secondary_main, secondary_sum, gaps, means, d_vals = score_combo([packs[i] for i in ids])
    rec = (primary, secondary_main, secondary_sum, gaps, means, d_vals, ids)
    
    best.append(rec)
    
    # (UNCHANGED) Sorting key is identical
    best.sort(key=lambda x: (x[0], x[1], x[2]))
    if len(best) > num_answers:
        best.pop()

# ---- report ----
print(f"Found {len(best)} best combinations.")
print("-" * 60)
# (MODIFIED) Unpack the new d_vals
for rank, (obj_main, obj_mid, obj_sum, gaps, means, d_vals, ids) in enumerate(best, 1):
    print(f"Rank {rank}: primary_gap={obj_main:.6f}  worst_overall_gap={obj_mid:.6f}")
    # (MODIFIED) Pass d_vals to the show function
    show(ids, packs, gaps, means, d_vals)