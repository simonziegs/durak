# Durak Bot Simulator

A Python-based simulator for the card game Durak, featuring AI bots with distinct strategies. This project allows you to evaluate bot performance in head-to-head matchups, tracking wins, losses, average turns, transfers, and cards left in losses. Currently, it supports four bot strategies: `random`, `aggressive`, `defensive`, and `trump_lover`.

## Overview

Durak is a traditional Russian card game where players aim to shed all their cards. The game uses a 36-card deck (6 to Ace, four suits), with one suit designated as trump. The simulator implements a two-player version, pitting bots against each other to analyze their effectiveness.

### Features
- **Game Logic**: Full implementation of Durak rules, including attacking, defending, transferring, and taking cards.
- **Bot Strategies**:
  - `random`: Plays a random legal action.
  - `aggressive`: Prioritizes attacking with high-ranking cards.
  - `defensive`: Focuses on beating with low non-trumps and transferring when possible.
  - `trump_lover`: Prefers using trump cards to beat or attack.
- **Evaluation**: Runs matchups between all bot pairs, producing win rates and statistics.

## Requirements
- Python 3.6+
- No external libraries required (uses only `random` from the standard library).

## Setup
1. **Clone or Download**: Get the project files into a local directory.
2. **Verify Files**: Ensure `game.py`, `bots.py`, and `evaluate.py` are present.

## Usage
Run the evaluation script to see how bots perform against each other:

```
python evaluate.py
```
- **Default Settings**: Evaluates 4 bots (random, aggressive, defensive, trump_lover) with 100 games per matchup pair.

- **Output**: Displays:
    - Per-bot stats: wins, losses, win rate, average turns, transfers, and cards left in losses.
    - Win rate matchup matrix showing head-to-head performance.
 
## Modification
- **Change Bots**: Edit strategies list in evaluate.py to include/exclude bots.

- **Adjust Games**: Modify num_games in evaluate_bots() call (e.g., evaluate_bots(strategies, num_games=50)).

- **Add Bots**: Implement new strategies in bots.py under get_bot_action().

## Game Rules
- **Deck**: 36 cards (6-A, Spades, Hearts, Diamonds, Clubs).

- **Trump**: Last card’s suit is trump; trumps beat non-trumps, higher ranks beat lower ranks.

- **Play**:
    - Attacker plays cards (same rank if table non-empty).
    - Defender beats (higher same suit or trump) or takes.
    - Defender can transfer a card of the same rank as table cards, swapping roles.
    - Attacker can stop if all attacks are beaten.

- **End**: First player to empty their hand wins; opponent with cards loses.

## Next Steps
- Add CFR Bot




