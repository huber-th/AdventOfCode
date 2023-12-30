""" filesystem paths module """
from pathlib import Path


def load_data(file: str):
    """
    Load and sanitize data
    """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        return [tuple(g.split(' ')) for g in f.read().strip().split('\n')]


def hand_value(h: str) -> int:
    """
    Determine the value of the hand played

    A - Rock - 1
    B - Paper - 2
    C - Siccors - 3
    """
    v = 0
    if h == 'A':
        v += 1
    if h == 'B':
        v += 2
    if h == 'C':
        v += 3
    return v


def determine_winner(a: str, b: str) -> int:
    """
    Determine the winner of a hand played
    """
    if a == b:
        return 0
    if a == 'A' and b == 'B':
        return 1
    if a == 'A' and b == 'C':
        return -1
    if a == 'B' and b == 'A':
        return -1
    if a == 'B' and b == 'C':
        return 1
    if a == 'C' and b == 'A':
        return 1
    if a == 'C' and b == 'B':
        return -1
    assert False, f'{a} and {b} as a combo not supported'


def convert_hand(h: str) -> str:
    """
    Convert hand X/Y/Z to A/B/class
    """
    if h == 'X':
        return 'A'
    if h == 'Y':
        return 'B'
    if h == 'Z':
        return 'C'
    assert False, f'Unknown input {h}'


def count_game(a: str, b: str) -> tuple[int,int]:
    """
    Count the game by determining the hand value and outcome
    """
    score_a = 0
    score_b = 0

    score_a += hand_value(a)
    score_b += hand_value(b)

    winner = determine_winner(a,b)

    if winner == -1:
        score_a += 6
    if winner == 1:
        score_b += 6
    if winner == 0:
        score_a += 3
        score_b += 3

    return (score_a,score_b)


def count_games(games: list[tuple[str,...]]) -> tuple[int,int]:
    """
    Count score for all games
    """
    score_a: int = 0
    score_b: int = 0

    for game in games:
        b = convert_hand(game[1])
        game_score = count_game(game[0],b)
        score_a += game_score[0]
        score_b += game_score[1]

    return (score_a,score_b)


def determine_hand(a: str, g: str) -> str:
    """
    Determine the hand to play if X means loose, Y means draw and Z means win
    """
    if g == 'Y':
        return a
    if g == 'X':
        if a == 'A':
            return 'C'
        if a == 'B':
            return 'A'
        if a == 'C':
            return 'B'
    if g == 'Z':
        if a == 'A':
            return 'B'
        if a == 'B':
            return 'C'
        if a == 'C':
            return 'A'
    assert False, f'Unknown combo {a} and {g}'


def determine_hands_to_play(games: list[tuple[str,...]]) -> tuple[int,int]:
    """
    Determine which hand to play according to the guide and calculate the score
    """
    score_a: int = 0
    score_b: int = 0

    for game in games:
        hand = determine_hand(game[0],game[1])
        game_score = count_game(game[0],hand)
        score_a += game_score[0]
        score_b += game_score[1]

    return (score_a,score_b)


if __name__ == '__main__':
    games = load_data('input')

    print('Part one:')
    print(count_games(games)[1])

    print('Part two:')
    print(determine_hands_to_play(games)[1])
