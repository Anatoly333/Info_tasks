def norm_card(name):
    num = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
           '9': 9, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    if len(name) == 2:
        return [num[name[0]], name[1]]
    else:
        return [10, name[2]]


def cringe_card(num, m):
    sgn = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
           9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    return sgn[num] + m


def normed(cards):
    return [norm_card(card) for card in cards]


def kick(winners, hands):
    mx = [0, 0]
    hands_ = [sorted([hand[0][0], hand[1][0]], reverse=True) for hand in hands]
    for pl in winners:
        if hands_[pl] > mx:
            mx = hands_[pl]
    alife = []
    for pl in winners:
        if hands_[pl] == mx:
            alife.append(pl)
    return alife


def find_straight_flush(cards):
    found = [0 for i in range(15)]
    cnt = {'S': 0, 'C': 0, 'H': 0, 'D': 0}
    mx = 0
    m = 'S'
    for card in cards:
        cnt[card[1]] += 1
        if mx < cnt[card[1]]:
            mx = cnt[card[1]]
            m = card[1]
    if mx < 5:
        return 0
    for card in cards:
        found[card[0]] = found[card[0]] or (card[1] == m)
    sl = 0
    best_fs = 0
    if found[14] and found[2] and found[3] and found[4] and found[5]:
        best_fs = 5
    for i in range(2, 15):
        if found[i]:
            sl += 1
        else:
            sl = 0
        if sl >= 5:
            best_fs = i
    if best_fs:
        return best_fs
    return 0


def find_four(cards):
    found = [0 for i in range(15)]
    for card in cards:
        found[card[0]] += 1
    f = 0
    b = 0
    for i in range(14, 1, -1):
        if not f and found[i] == 4:
            f = i
        elif found[i] and not b:
            b = i
    if f:
        return [f, b]
    return [0, 0]


def find_three(cards):
    found = [0 for i in range(15)]
    for card in cards:
        found[card[0]] += 1
    f = 0
    b = [0, 0]
    for i in range(14, 1, -1):
        if not f and found[i] >= 3:
            f = i
        elif found[i] and not b[0]:
            b[0] = i
            if found[i] > 1:
                b[1] = i
        elif found[i] and not b[1]:
            b[1] = i
    if f:
        return [f] + b
    return [0, 0, 0]


def find_pair(cards):
    found = [0 for i in range(15)]
    for card in cards:
        found[card[0]] += 1
    f = []
    b = []
    for i in range(14, 1, -1):
        if found[i] >= 2 and len(f) < 2:
            f.append(i)
        elif found[i]:
            b.append(i)
    if len(f) == 1:
        return [sorted(f, reverse=True), b[:3]]
    if len(f) >= 2:
        return [sorted(f, reverse=True), b[:1]]
    return [sorted(f, reverse=True), []]


def find_two_pairs(cards):
    p = find_pair(cards)
    if len(p[0]) > 1:
        return p
    return [[], []]


def find_pairs(cards):
    p = find_pair(cards)
    if len(p[0]):
        return p
    return [[], []]


def find_full_house(cards):
    f3 = find_three(cards)[0]
    f2 = find_pair(cards)[0]
    if not f3:
        return [0, 0]
    if len(f2) == 1:
        return [0, 0]
    for p in f2:
        if p != f3:
            return [f3, p]
    return [0, 0]


def find_flush(cards):
    cnt = {'S': 0, 'C': 0, 'H': 0, 'D': 0}
    mx = 0
    m = 'S'
    for card in cards:
        cnt[card[1]] += 1
        if mx < cnt[card[1]]:
            mx = cnt[card[1]]
            m = card[1]
    if mx < 5:
        return [0, 0, 0, 0, 0]
    ans = []
    for card in cards:
        if card[1] == m:
            ans.append(card[0])
    ans = sorted(ans, reverse=True)
    return ans[:5]


def find_straight(cards):
    found = [0 for i in range(15)]
    for card in cards:
        found[card[0]] += 1
    sl = 0
    best_s = 0
    if found[14] and found[2] and found[3] and found[4] and found[5]:
        best_s = 5
    for i in range(2, 15):
        if found[i]:
            sl += 1
        else:
            sl = 0
        if sl >= 5:
            best_s = i
    if best_s:
        return best_s
    return 0


def find_best_card(cards):
    return sorted([card[0] for card in cards], reverse=True)[:5]


def maybe_this_combination(checker, players_hands, community_cards):
    ans = []
    rate = [checker(hand + community_cards) for hand in players_hands]
    mx = max(rate)
    if (type(mx) == int and mx != 0) or (type(mx) == list
    and len(mx) != 0 and (mx[0] != 0 and mx[0] != [])):
        for i in range(len(players_hands)):
            if mx == rate[i]:
                ans.append(i)
        return ans
    return 0


def who_wins(players_hands, community_cards):
    checkers = [find_straight_flush, find_four, find_full_house, find_flush,
                find_straight, find_three, find_two_pairs, find_pairs, find_best_card]
    for checker in checkers:
        ans = maybe_this_combination(checker, players_hands, community_cards)
        if ans:
            return ans


def count_win_probabilities(
    players_private_cards: list[tuple[str, str]],
    known_community_cards: list[str],
    already_dropped_cards: list[str] = []):
    already_dropped_cards = set(already_dropped_cards)
    players_hands = [list(hand) for hand in players_private_cards]
    for hand in players_hands:
        already_dropped_cards.update(hand)
    for card in known_community_cards:
        already_dropped_cards.add(card)
    players_hands = [normed(hand) for hand in players_hands]
    ans = [0.0 for i in range(len(players_hands))]
    deck = []
    for i in range(2, 15):
        for m in ['S', 'D', 'H', 'C']:
            if not (cringe_card(i, m) in already_dropped_cards):
                deck.append([i, m])
    if len(known_community_cards) == 0:
        for i in range(len(deck)):
            for j in range(i):
                for k in range(j):
                    for t in range(k):
                        for s in range(t):
                            ww = who_wins(players_hands, [deck[i], deck[j], deck[k], deck[t], deck[s]])
                            for pl in ww:
                                ans[pl] += 1.0/len(ww)
    if len(known_community_cards) == 3:
        for i in range(len(deck)):
            for j in range(i):
                ww = who_wins(players_hands, normed(known_community_cards) + [deck[i], deck[j]])
                for pl in ww:
                    ans[pl] += 1.0/len(ww)
    if len(known_community_cards) == 4:
        for i in range(len(deck)):
            ww = who_wins(players_hands, normed(known_community_cards) + [deck[i]])
            for pl in ww:
                ans[pl] += 1.0/len(ww)
    if len(known_community_cards) == 5:
        ww = who_wins(players_hands, normed(known_community_cards))
        for pl in ww:
            ans[pl] += 1.0/len(ww)
    s = sum(ans)
    ans = [x/s for x in ans]
    return ans


print(count_win_probabilities([('KH', '2S'), ('2D', 'AH')], ['QD', '3D', 'KD', '5D'], ['5C', '4S', '7H', 'QH', '6S', 'QS', '3H', '6C', 'QC', '8S', 'AC', '7C', '6H', 'KC', '9S', '10C', '2H', 'KS', '9C', '8C', '10D', '3S', '9D', '4H', '5H']))

