from game import *
from tools import progressBar

deck = Deck()

# Handle exceptions
combinations_w_error = []

# Combinations
hands = list(combinations(deck, 2))
publics = list(combinations(deck, 5))

# Handle name lists
hands_namelist = [i[0].suit+i[0].rank+i[1].suit+i[1].rank 
               for i in hands]
public_namelist = [i[0].suit+i[0].rank+i[1].suit+i[1].rank+
                i[2].suit+i[2].rank+i[3].suit+i[3].rank+i[4].suit+i[4].rank
               for i in publics]
n_hands = len(hands_namelist)
n_public = len(public_namelist)

# Handle data
data = np.empty((len(hands_namelist),len(public_namelist)))
for i in range(n_hands):
    print(f"Hands = {hands_namelist[i]}")
    for j in progressBar(range(n_public)):
        if (hands[i][0] in publics[j]) or (hands[i][1] in publics[j]):
            data[i,j] = np.nan #
        else:
            try: 
                data[i,j] = Calc_winrate(hands[i],publics[j])
            except Exception as excpt:
                combinations_w_error.append((i,j,excpt))
                data[i,j] = np.nan
                print(f"Error {type(excpt)} raised when hands = {hands_namelist[i]}, public = {public_namelist[j]}. (i,j = {i},{j})")
            

# pd.DataFrame
TP = pd.DataFrame(data = data,
                  index = hands_namelist,
                  columns = public_namelist
                 )
