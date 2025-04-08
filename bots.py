# bots.py
import random
from game import RANKS

def get_bot_action(game, actions, strategy):
    current_player = game.defender if game.unbeaten_attack else game.attacker
    is_defender = game.unbeaten_attack is not None
    if strategy == "random":
        beat_actions = [a for a in actions if a != ["take"] and a[0] != "transfer"]
        transfer_actions = [a for a in actions if a[0] == "transfer"]
        return random.choice(beat_actions if beat_actions else (transfer_actions if transfer_actions else [["take"]]))
    elif strategy == "aggressive":
        beat_actions = [a for a in actions if a != ["take"] and a != ["stop"] and a[0] != "transfer"]
        # if beat_actions:
        #     def card_value(action):
        #         card = action[0]
        #         rank_idx = RANKS.index(card[:-1])
        #         is_trump = card[-1] == game.trump_suit
        #         return (is_trump, rank_idx)
        #     return max(beat_actions, key=card_value)
        # transfer_actions = [a for a in actions if a[0] == "transfer"]
        # return random.choice(transfer_actions if transfer_actions else [["take"]])
        if beat_actions:
            def card_value(action):
                card = action[0]
                rank_idx = RANKS.index(card[:-1])
                is_trump = card[-1] == game.trump_suit
                return (is_trump, rank_idx)
            valid_beat = [a for a in beat_actions if a[0] in game.hands[current_player]]
            if valid_beat:
                return max(valid_beat, key=card_value)
        # Fallback based on role
        if is_defender:
            return ["take"]
        else:
            return ["stop"] if ["stop"] in actions else random.choice(actions)  # Shouldn't reach here with proper legal actions
    elif strategy == "defensive":
        transfer_actions = [a for a in actions if a[0] == "transfer"]
        if transfer_actions:
            return random.choice(transfer_actions)
        beat_actions = [a for a in actions if a != ["take"] and a != ["stop"] and a[0] != "transfer"]
        if beat_actions:
            def card_value(action):
                card = action[0]
                rank_idx = RANKS.index(card[:-1])
                is_trump = card[-1] == game.trump_suit
                return (is_trump, rank_idx)
            valid_beat = [a for a in beat_actions if a[0] in game.hands[current_player]]
            if valid_beat:
                return min(valid_beat, key=card_value)
        # Fallback based on role
        if is_defender:
            return ["take"]
        else:
            return ["stop"] if ["stop"] in actions else random.choice(actions)  # Shouldn't reach here with proper legal actions
    elif strategy == "trump_lover":
        transfer_actions = [a for a in actions if a[0] == "transfer"]
        if transfer_actions:
            return random.choice(transfer_actions)
        beat_actions = [a for a in actions if a != ["take"] and a != ["stop"] and a[0] != "transfer"]
        if beat_actions:
            def card_value(action):
                card = action[0]
                rank_idx = RANKS.index(card[:-1])
                is_trump = card[-1] == game.trump_suit
                # Prioritize trumps, then lowest rank
                return (not is_trump, rank_idx)  # False < True, so trumps come first
            valid_beat = [a for a in beat_actions if a[0] in game.hands[current_player]]
            if valid_beat:
                return min(valid_beat, key=card_value)
        return ["stop"] if not is_defender and ["stop"] in actions else ["take"]
    else:
        raise ValueError(f"Unknown strategy: {strategy}")