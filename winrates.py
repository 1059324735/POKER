# from game import *
from tools import progressBar

def merge(cards1, cards2):
    c = []
    h = j = 0
    while j < len(cards1) and h < len(cards2):
        if Winner(cards1[j],cards2[h]) == 1:
            c.append(cards1[j])
            j += 1
        else:
            c.append(cards2[h])
            h += 1

    if j == len(cards1):
        for i in cards2[h:]:
            c.append(i)
    else:
        for i in cards1[j:]:
            c.append(i)

    return c


def merge_sort(Hands_combination):
    if len(Hands_combination) <= 1:
        return Hands_combination
    middle = len(Hands_combination)//2
    left = merge_sort(Hands_combination[:middle])
    right = merge_sort(Hands_combination[middle:])
    return merge(left, right)


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
data = np.empty((len(public_namelist),len(hands_namelist)))
for j in progressBar(range(n_public)):
    sort_list = []
    for i in range(n_hands):
        if (hands[i][0] in publics[j]) or (hands[i][1] in publics[j]):
            data[j,i] = np.nan #
        else:
            sort_list.append(hands[i]+publics[j])
    sort_result = merge_sort(sort_list)
    indlist = []
    for i in sort_result:
        temp = []
        for x in i:
            if x not in publics[j]:
                temp.append(x)
        indlist.append(temp)

    for i in range(len(sort_result)):
        data[j,hands.index(tuple(indlist[i]))] = i
        
        
    
# for i in range(n_hands):
#     print(f"Hands = {hands_namelist[i]}")
#     for j in progressBar(range(n_public)):
#         if (hands[i][0] in publics[j]) or (hands[i][1] in publics[j]):
#             data[i,j] = np.nan #
#         else:
#             try: 
#                 data[i,j] = Calc_winrate(hands[i],publics[j])
#             except Exception as excpt:
#                 combinations_w_error.append((i,j,excpt))
#                 data[i,j] = np.nan
#                 print(f"Error {type(excpt)} raised when hands = {hands_namelist[i]}, public = {public_namelist[j]}. (i,j = {i},{j})")
            

# pd.DataFrame
TP = pd.DataFrame(data = data,
                  index = hands_namelist,
                  columns = public_namelist
                 )

