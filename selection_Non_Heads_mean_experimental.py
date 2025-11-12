### This module searches for the best compound combinations of acceptable Non-Heads.
# Several conditions can be imposed on the choice. See below.

import itertools
import pandas as pd 
from zipf_stats import Zipf_stats


num_answers = 10 # number of acombinations it should provide.

num_stimuli = 14 # number of stimuli Non_Heads we want to select. 

decision_method = 'sum_cohens_d'

# other options
# 'difference_mean_singular_plural'
# 'max_mean_dif_all_groups'
# 'sum_mean_dif_all_groups'
# 'max_cohens_d' 
# 'sum_cohens_d'

mandatory_irregular_pairs = [
    "goose", "louse", "child", "mouse", "woman", "man", "tooth", "foot", "ox"
]

stats_calculator = Zipf_stats() # calling the class that handles statistics with zipf.

group_keys = ("irr_sg", "irr_pl", "reg_sg", "reg_pl")  # names of the groups and the order in shich they appear.
                                                       # you can change such order by changing things here. 

def pack(irr_sg, irr_pl, reg_sg, reg_pl): # function that creates a dictionary with the classification 
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

    pack(("tooth",4.08773,3.96328,4.11284), ("teeth",4.70053,4.82878,4.90913),
         ("bone",4.51390,4.41043,4.45257), ("bones",4.42982,4.50930,4.46426)),

    pack(("foot",4.91934,5.09072,5.10584), ("feet",5.07716,5.31637,5.35163),
         ("leg",4.87632,4.76298,4.81129), ("legs",4.85298,4.93494,4.96283)),
    
    pack(("foot", 4.91934, 5.09072, 5.10584), ("feet", 5.07716, 5.31637, 5.35163),
         ("hand", 5.43662, 5.6605, 5.66254), ("hands", 5.24962, 5.45962, 5.48105)),

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

def max_difference(vals): # function used in the criteria for choosing the best combinations.
    return max(vals) - min(vals)


def build_combo_df(packs):
    """
    Build a DataFrame with one row per (pack, group), containing the three datasets.
    Requires global `group_keys = ("irr_sg", "irr_pl", "reg_sg", "reg_pl")`.
    """
    rows = []
    for P in packs:
        for key in group_keys:
            word, subtlex, baby10m, baby100m = P[key]
            rows.append({
                "group": key,
                "subtlex": subtlex,
                "baby10m": baby10m,
                "baby100m": baby100m,
            })
    return pd.DataFrame(rows, columns=["group", "subtlex", "baby10m", "baby100m"])

def calculate_mean_difs(means_df): # calculates differences between the means 
    
    difference_all_groups = [
        max_difference(means_df['subtlex']),
        max_difference(means_df['baby10m']),
        max_difference(means_df['baby100m'])
    ]

    d_irr = [
        abs(means_df.loc['irr_pl']['subtlex'] - means_df.loc['irr_sg']['subtlex']),
        abs(means_df.loc['irr_pl']['baby10m'] - means_df.loc['irr_sg']['baby10m']),
        abs(means_df.loc['irr_pl']['baby100m'] - means_df.loc['irr_sg']['baby100m'])
    ]
    d_reg = [
        abs(means_df.loc['reg_pl']['subtlex'] - means_df.loc['reg_sg']['subtlex']),
        abs(means_df.loc['reg_pl']['baby10m'] - means_df.loc['reg_sg']['baby10m']),
        abs(means_df.loc['reg_pl']['baby100m'] - means_df.loc['reg_sg']['baby100m'])
    ]
    
    max_dif_singular_plural = max(d_irr + d_reg) # here is the maximum mean difference between singular and plural pairs, for a pack, in the three datasets. 
   
    max_group_dif = max(difference_all_groups) # the maximum difference between the 4 conditions in the three datasets, for a combination.

    sum_dif_all_groups = sum(difference_all_groups ) # here is the sum of the differences between the 4 groups. 
    
    return max_dif_singular_plural, max_group_dif, sum_dif_all_groups, difference_all_groups


def calculate_cohens_d(df):
    
    # Compare: irregular singular vs. irregular plural for each dataset.
    cohens_d_irregular = [
        stats_calculator.cohens_d_from_lists(
            df[df['group'] == 'irr_sg']['subtlex'].tolist(), 
            df[df['group'] == 'irr_pl']['subtlex'].tolist()
        ),
        stats_calculator.cohens_d_from_lists(
            df[df['group'] == 'irr_sg']['baby10m'].tolist(), 
            df[df['group'] == 'irr_pl']['baby10m'].tolist()
        ),
        stats_calculator.cohens_d_from_lists(
            df[df['group'] == 'irr_sg']['baby100m'].tolist(), 
            df[df['group'] == 'irr_pl']['baby100m'].tolist()
        )
    ]
    
    # Compare: regular singular vs. regular plural for each dataset. 
    cohens_d_regular = [
        stats_calculator.cohens_d_from_lists(
            df[df['group'] == 'reg_sg']['subtlex'].tolist(), 
            df[df['group'] == 'reg_pl']['subtlex'].tolist()
        ),
        stats_calculator.cohens_d_from_lists(
            df[df['group'] == 'reg_sg']['baby10m'].tolist(), 
            df[df['group'] == 'reg_pl']['baby10m'].tolist()
        ),
        stats_calculator.cohens_d_from_lists(
            df[df['group'] == 'reg_sg']['baby100m'].tolist(), 
            df[df['group'] == 'reg_pl']['baby100m'].tolist()
        )
    ]
    
    max_cohens_d = max(cohens_d_irregular + cohens_d_regular)
    sum_cohens_d = sum(cohens_d_irregular + cohens_d_regular) 

    return (cohens_d_irregular, cohens_d_regular, max_cohens_d, sum_cohens_d)


def show_combo_stimuli(ids, packs): # prints the regular and irregular pairs of 1 combination. 

    print("Combo IDs:", ids)    


    for idx in ids:
        pack = packs[idx]
        # Unpack the word strings
        irr_sg = pack["irr_sg"][0]
        irr_pl = pack["irr_pl"][0]
        reg_sg = pack["reg_sg"][0]
        reg_pl = pack["reg_pl"][0]
        print(f"  {irr_sg}/{irr_pl} — {reg_sg}/{reg_pl}")




def show_combo_stats(gaps, means, cohen_d_vals):
    """Builds and prints a DataFrame of the combo's statistics."""
    
    # Unpack all the data
    cohens_d_irregular, cohens_d_regular = cohen_d_vals
    
    # Create the data for the DataFrame
    data = {
        "SUBTLEX": [
            means[0][0],  # Mean Irr-SG
            means[1][0],  # Mean Irr-PL
            means[2][0],  # Mean Reg-SG
            means[3][0],  # Mean Reg-PL
            gaps[0],
            cohens_d_irregular[0],
            cohens_d_regular[0]
        ],
        "baby10m": [
            means[0][1],
            means[1][1],
            means[2][1],
            means[3][1],
            gaps[1],
            cohens_d_irregular[1],
            cohens_d_regular[1]
        ],
        "baby100m": [
            means[0][2],
            means[1][2],
            means[2][2],
            means[3][2],
            gaps[2],
            cohens_d_irregular[2],
            cohens_d_regular[2]
        ]
    }
    
    # Create the row labels (index)
    index_labels = [
        "Mean Irr-SG",
        "Mean Irr-PL",
        "Mean Reg-SG",
        "Mean Reg-PL",
        "Overall Gap",
        "Cohen's d (Irr)",
        "Cohen's d (Reg)"
    ]
    
    # Create and print the DataFrame
    df_stats = pd.DataFrame(data, index=index_labels)
    
    # Format the DataFrame for printing
    print(df_stats.to_string(float_format="%.3f"))  # float_format="%.3f" says the values of the df should be printed with 3 decimals
    
    print("-" * 60) # printing a separator 


def score_combo(packs_subset): # this function return the values used to rank the combinations, allowing us to choose later wich method to use. 
  
    df = build_combo_df(packs_subset) # bulding a combination of packs.
    
    means_df = df.groupby('group').mean().reindex(group_keys) # creating a dataframe just with the means.
    
    max_dif_singular_plural, max_mean_dif_all_groups, sum_mean_dif_all_groups, _ = calculate_mean_difs(means_df) # change the order here, in order to prioritize diff
    
    # 4. Calculate the Cohen's d values for reporting
    _, _, max_cohens_d, sum_cohens_d = calculate_cohens_d(df)

    return max_dif_singular_plural, max_mean_dif_all_groups, sum_mean_dif_all_groups, max_cohens_d, sum_cohens_d



### finds the indices of the packs of the mandatory irregulars.
irr_packs_indexation = []
for sing_noun in mandatory_irregular_pairs: 
    matching_indices = set()
    for i, pack in enumerate(packs):
        if pack["irr_sg"][0] == sing_noun:
            matching_indices.add(i)
    
    if not matching_indices:
        print(f"Warning: No pack found for '{sing_noun}'")
    else:
        irr_packs_indexation.append((sing_noun, matching_indices))



### finds all the possible combinations.
required_pack_indices = set.union(*[g[1] for g in irr_packs_indexation]) # creates one single set of all mandatory pack indices.

all_indices = set(range(len(packs))) # creates a set of every possible index in your packs list

other_indices = list(all_indices - required_pack_indices) # calculates the other packs that are not mandatory.

num_other_to_choose = num_stimuli - len(irr_packs_indexation) # This line calculates how many "other" packs to pick. 
                                                              # It takes num_stimuli and subtracts the number of mandatory groups.

base_set_iter = itertools.product(*[g[1] for g in irr_packs_indexation]) # creates an iterator that will generate every possible  combination of the mandatory packs.
# itertools.product does the cartesian product (all combinations with one element of ach of 2 groups). Chck google for more details. 

other_set_iter = list(itertools.combinations(other_indices, num_other_to_choose)) # creates another iterator that will generate every possible combination of the non mandatory packs.

pack_words = [{pack[k][0] for k in group_keys} for pack in packs] 
result_list = []

for base_ids, other_ids in itertools.product(base_set_iter, other_set_iter): # main loop. It takes the two previous iterators and pairs every combination of one with every combination of the other. 
    ids = base_ids + other_ids # creates the final, complete combination of 14 pack indices.
# the use of iterators instead of lists here, makes it more memory efficient. 

    used = set()
    ok = True
    for i in ids:
        if used & pack_words[i]:
            ok = False
            break
        used |= pack_words[i]
    if not ok: # checks if ok is false and jumps to the next sequence
        continue
    
    # If no repeats, score this combination
    scores = score_combo([packs[i] for i in ids])
    
    # Append all 5 scores + the pack IDs
    result_list.append(scores + (ids,))

 # let's get the words inside each 

sort_key_map = { ###a dictionary that connects the name of a sorting method to its index in the tuple returned by the score_combo function.
    'max_dif_singular_plural': 0,
    'max_group_dif': 1,
    'sum_dif_all_groups': 2,
    'max_cohens_d': 3,
    'sum_cohens_d': 4
}

primary_key_index = sort_key_map.get(decision_method, 0) # gets the method chosen at the beggining of the code. 

all_score_indices = list(range(5)) # organizes the methods. leaving the excluded ones for the 
all_score_indices.pop(primary_key_index)
sort_key = lambda x: (x[primary_key_index],) + tuple(x[i] for i in all_score_indices)

result_list.sort(key=sort_key) # selects the best combinations

for rec in result_list[:num_answers]:
    
    # Unpack the 5 scores and the ids
    ids = rec[5] # The 'ids' tuple is the 6th item (index 5)
    
    # --- Re-calculate stats for printing ---
    packs_subset = [packs[i] for i in ids]
    df = build_combo_df(packs_subset)
    means_df = df.groupby('group').mean().reindex(group_keys)
    
    _, _, _, gaps = calculate_mean_difs(means_df)
    cohens_d_irregular, cohens_d_regular, _, _ = calculate_cohens_d(df)
    means_list = means_df.values.tolist()
    cohen_d_vals = (cohens_d_irregular, cohens_d_regular)

    show_combo_stimuli(ids, packs)

    print()
    
    show_combo_stats(gaps, means_list, cohen_d_vals)

