import csv
import json
import glob

def load_player_data(csv_file):
    """Load player data from the CSV file."""
    players = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            players.append({
                "playerid": row["playerid"],
                "playername": row["playername"],
                "teamname": row["teamname"],
                "teamid": row["teamid"],
                "image_url": row["image_url"],
                "stat_type": row["stat_type"]
            })
    return players

def collect_player_stats(player_name, csv_pattern):
    """Search for a player's performance data in the 2024 CSV files using their name."""
    stats = {"kills": [], "deaths": [], "assists": []}
    found = False  # Track if player data is found in any file

    for csv_file in glob.glob(csv_pattern):
        print(f"Checking file: {csv_file}")  # Log the current file being checked
        with open(csv_file, 'r', encoding='utf-8') as file:  # Specify encoding here
            reader = csv.DictReader(file)
            for row in reader:
                if row["playername"].lower() == player_name.lower():  # Match player name case-insensitively
                    found = True  # Player found in this file
                    stats["kills"].append(int(row["kills"]))
                    stats["deaths"].append(int(row["deaths"]))
                    stats["assists"].append(int(row["assists"]))
        
        if found:  # If found in this file, exit the loop
            print(f"Player '{player_name}' found in {csv_file}.")
            break

    return stats, found

def calculate_win_probability(kills, assists, deaths):
    """Calculate winning probability based on predicted performance."""
    player_score = (kills + assists) - deaths
    
    # Ensure we do not divide by zero
    if player_score <= 0:
        return 0.0  # Assign 0% win probability if player_score is 0 or negative

    total_score = player_score + 1  # Adding 1 to prevent division by zero
    win_probability = (player_score / total_score) * 100
    return round(win_probability, 2)

# The rest of your code remains unchanged.


def save_predictions_to_json(players_data, output_file):
    """Save all player predictions to a JSON file, clearing previous content."""
    with open(output_file, 'w') as file:  # Opens the file in write mode to clear previous content
        json.dump(players_data, file, indent=4)

def main():
    # Load player data from the specified CSV file
    player_data_file = './extracted_data/lol_player_data.csv'  # Replace with your player data file path
    players = load_player_data(player_data_file)
    
    # Load esports player performance data from 2024 CSV files only
    csv_pattern = './lol_old_data/2024_LoL_esports_match_data_from_OraclesElixir.csv'  # Adjust the pattern for 2024 files
    
    all_predictions = []

    # Iterate through each player and collect performance stats
    for player in players:
        player_name = player["playername"]
        player_names = player_name.split(" + ")  # Split combined names by " + "
        
        combined_stats = {"kills": [], "deaths": [], "assists": []}
        
        for name in player_names:
            # Collect historical performance data for the player by name
            player_stats, found = collect_player_stats(name.strip(), csv_pattern)

            if not found:  # Skip if player data is not found in any file
                print(f"Player '{name.strip()}' not found in any historical data files.")
                continue
            
            # Combine statistics for all players in the team
            combined_stats["kills"].extend(player_stats["kills"])
            combined_stats["deaths"].extend(player_stats["deaths"])
            combined_stats["assists"].extend(player_stats["assists"])

        # Use the last player's stats for predictions, or if none, default to zero
        predicted_kills = combined_stats["kills"][-1] if combined_stats["kills"] else 0
        predicted_deaths = combined_stats["deaths"][-1] if combined_stats["deaths"] else 0
        predicted_assists = combined_stats["assists"][-1] if combined_stats["assists"] else 0

        # Calculate winning probability
        win_probability = calculate_win_probability(predicted_kills, predicted_assists, predicted_deaths)

        # Compile the player data into a dictionary
        player_predictions = {
            "playernames": [name.strip() for name in player_names],
            "teamname": player["teamname"],
            "teamid": player["teamid"],
            "image_url": player["image_url"],
            "stat_type": player["stat_type"],
            "predicted_kills": predicted_kills,
            "predicted_deaths": predicted_deaths,
            "predicted_assists": predicted_assists,
            "win_probability": win_probability,
            "loss_probability": round(100 - win_probability, 2)  # Calculate loss probability
        }
        
        all_predictions.append(player_predictions)
    
    # Save all predictions to a JSON file
    output_file = './predictions/lol_prediction.json'
    save_predictions_to_json(all_predictions, output_file)

    print(f"Predicted player data saved to '{output_file}'")

if __name__ == "__main__":
    main()
