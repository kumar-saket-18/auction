import pandas as pd
import random
if __name__ == "__main__":
# Load the uploaded Excel file
    file_path = "/Users/kumar/Downloads/The_Curse_Club_Auction_Tagged.xlsx"
    df = pd.read_excel(file_path)

    # Ensure we only modify the Tag column, keep Category same, and try to balance distribution
    players = df.copy()

    # Count total players and target per set
    total_players = len(players)
    sets = ["A", "B", "C"]
    target_per_set = total_players // len(sets)

    # Shuffle players to randomize
    players = players.sample(frac=1, random_state=42).reset_index(drop=True)

    # Assign tags in round-robin to balance distribution
    tags = (sets * (total_players // len(sets) + 1))[:total_players]
    random.shuffle(tags)
    players["Tag"] = tags

    # Save the balanced version
    output_path = "/Users/kumar/Downloads/The_Curse_Club_Auction_Tagged1.xlsx"
    players.to_excel(output_path, index=False)