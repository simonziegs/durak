# evaluate.py
from game import DurakGame
from bots import get_bot_action
from collections import defaultdict

def simulate_game(bot0_strategy, bot1_strategy, max_turns=100):
    game = DurakGame()
    stats = {
        "turns": 0,
        "transfers": [0, 0],
        "cards_left": [0, 0]
    }
    
    while not game.is_terminal() and game.turns < max_turns:
        current_player = game.attacker if game.unbeaten_attack is None else game.defender
        strategy = bot0_strategy if current_player == 0 else bot1_strategy
        actions = game.get_legal_actions()
        action = get_bot_action(game, actions, strategy)
        
        if action[0] == "transfer":
            stats["transfers"][current_player] += 1
        game.apply_action(action)
        stats["turns"] = game.turns
    
    winner = game.check_winner()
    stats["cards_left"] = [len(game.hands[0]), len(game.hands[1])]
    return winner, stats

def print_matchup_matrix(strategies, matchup_wins, num_games):
    print("\nWin Rate Matchup Matrix:")
    print("------------------------")
    matrix = {s1: {s2: 0 for s2 in strategies} for s1 in strategies}
    for s1 in strategies:
        for s2 in strategies:
            if s1 != s2:
                wins = matchup_wins.get((s1, s2), 0)  # Wins of s1 vs s2
                matrix[s1][s2] = wins / num_games * 100
    print(" " * 10 + " ".join(f"{s:10}" for s in strategies))
    for s1 in strategies:
        print(f"{s1:10}", end=" ")
        for s2 in strategies:
            if s1 == s2:
                print(" " * 10, end=" ")
            else:
                print(f"{matrix[s1][s2]:9.2f}%", end=" ")
        print()

def evaluate_bots(strategies, num_games=1000):
    results = defaultdict(lambda: {"wins": 0, "turns": 0, "transfers": 0, "cards_left": 0})
    matchup_wins = defaultdict(int)  # (bot0, bot1) -> bot0 wins
    
    # Only forward matchups to avoid double-counting
    matchups = [(s1, s2) for i, s1 in enumerate(strategies) for s2 in strategies[i+1:]]
    
    for bot0_strat, bot1_strat in matchups:
        matchup_key = f"{bot0_strat} vs {bot1_strat}"
        for _ in range(num_games):
            winner, stats = simulate_game(bot0_strat, bot1_strat)
            if winner == 0:
                results[bot0_strat]["wins"] += 1
                matchup_wins[(bot0_strat, bot1_strat)] += 1
            elif winner == 1:
                results[bot1_strat]["wins"] += 1
                matchup_wins[(bot1_strat, bot0_strat)] += 1
            results[bot0_strat]["turns"] += stats["turns"]
            results[bot1_strat]["turns"] += stats["turns"]
            results[bot0_strat]["transfers"] += stats["transfers"][0]
            results[bot1_strat]["transfers"] += stats["transfers"][1]
            if winner != 0:
                results[bot0_strat]["cards_left"] += stats["cards_left"][0]
            if winner != 1:
                results[bot1_strat]["cards_left"] += stats["cards_left"][1]
        
        games_per_matchup = num_games
        for bot in [bot0_strat, bot1_strat]:
            results[bot]["turns"] /= games_per_matchup
            results[bot]["transfers"] /= games_per_matchup
            losses = games_per_matchup * len([m for m in matchups if bot in m]) - results[bot]["wins"]
            results[bot]["cards_left"] /= losses if losses > 0 else 1

    print("\nBot Evaluation Results:")
    print("-----------------------")
    for bot, stats in results.items():
        total_games = len([m for m in matchups if bot in m]) * num_games
        win_rate = stats["wins"] / total_games * 100
        print(f"{bot}:")
        print(f"  Wins: {stats['wins']:.2f}")
        print(f"  Losses: {total_games - stats['wins']:.2f}")
        print(f"  Win Rate: {win_rate:.2f}%")
        print(f"  Avg Turns: {stats['turns']:.2f}")
        print(f"  Avg Transfers: {stats['transfers']:.2f}")
        print(f"  Avg Cards Left (Losses): {stats['cards_left']:.2f}")
        print()

    print_matchup_matrix(strategies, matchup_wins, num_games)

    return results

if __name__ == "__main__":
    strategies = ["random", "aggressive", "defensive", "trump_lover"]
    evaluate_bots(strategies, num_games=100)