import csv
import json
from statistics import mean

def load_input_data(csv_file):
    """Load input player data from CSV file with headers: player_name, team_name, stat_type, image_url, odds_type, line_score."""
    input_data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            input_data.append(row)
    return input_data

def load_previous_match_data(csv_file):
    """Load previous match records from CSV file with headers: Player, Maps, Rounds, K-D Diff, K/D, Rating."""
    previous_data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            previous_data.append(row)
    return previous_data

def collect_player_stats(player_names, previous_data):
    """Collect player stats (K-D Diff, K/D, Rating) based on the player names."""
    stats = {"K-D Diff": [], "K/D": [], "Rating": []}
    found_players = []

    for row in previous_data:
        for name in player_names:
            if row["Player"].lower() == name.lower():
                found_players.append(name)  # Track found players
                stats["K-D Diff"].append(float(row["K-D Diff"]))
                stats["K/D"].append(float(row["K/D"]))
                stats["Rating"].append(float(row["Rating"]))

    return stats, found_players

def predict_performance(player_stats, odds_type, line_score):
    """Predict player performance based on average historical data and odds."""
    avg_kd_diff = mean(player_stats["K-D Diff"]) if player_stats["K-D Diff"] else 0
    avg_kd = mean(player_stats["K/D"]) if player_stats["K/D"] else 0
    avg_rating = mean(player_stats["Rating"]) if player_stats["Rating"] else 0
    
    # Adjust prediction based on odds line (50/50% based)
    prediction_factor = 0.5 * line_score if odds_type == "standard" else 0.5 * (line_score / 2)
    
    # Predicting the line score for the next match
    predicted_line_score = round(avg_kd + prediction_factor, 2)  # Modify this logic as per your requirements

    return {
        "predicted_kd_diff": round(avg_kd_diff + prediction_factor, 2),
        "predicted_kd": round(avg_kd + prediction_factor, 2),
        "predicted_rating": round(avg_rating + prediction_factor, 2),
        "predicted_line_score": predicted_line_score  # Include predicted line score
    }

def calculate_win_probability(predictions):
    """Calculate win probability based on predicted K/D and Rating."""
    kd = predictions["predicted_kd"]
    rating = predictions["predicted_rating"]

    # Example calculation for win probability
    player_score = (kd * 2 + rating)  # You can adjust this formula as needed
    total_score = player_score + 1  # Prevent division by zero

    win_probability = (player_score / total_score) * 100
    return round(win_probability, 2)

def save_predictions_to_json(predictions, output_file):
    """Save the player predictions to a JSON file, clearing previous content."""
    with open(output_file, 'w') as file:  # Opening in 'w' mode clears the file
        json.dump(predictions, file, indent=4)

def main():
    # Load the input player data
    input_file = './extracted_data/cs2_player_info.csv'  # Replace with your actual CSV file path
    input_data = load_input_data(input_file)

    # Load previous match data (historical performance)
    previous_match_file = './cs2_old_data/cs2_player_stats.csv'  # Replace with your actual CSV file path
    previous_data = load_previous_match_data(previous_match_file)

    predictions = []

    # Iterate through each player in the input data
    for player in input_data:
        player_names = player["player_name"].split(" + ")  # Split combined names by " + "
        player_stats, found_players = collect_player_stats(player_names, previous_data)

        if found_players:  # If any player was found
            # Predict performance based on historical stats and odds
            player_prediction = predict_performance(player_stats, player["odds_type"], float(player["line_score"]))

            # Calculate win probability based on predicted performance
            win_probability = calculate_win_probability(player_prediction)

            # Add relevant details from input data (name, team, image URL)
            player_prediction["player_names"] = found_players  # Store all found player names
            player_prediction["team_name"] = player["team_name"]
            player_prediction["image_url"] = player["image_url"]
            player_prediction["stat_type"] = player["stat_type"]  # Set the stat type name here
            player_prediction["win_probability"] = win_probability
            player_prediction["loss_probability"] = round(100 - win_probability, 2)  # Calculate loss probability
            
            # Save the predicted line score for the next match
            player_prediction["predicted_line_score"] = player_prediction["predicted_line_score"]

            # Append prediction data to the list
            predictions.append(player_prediction)

    # Save predictions to a JSON file
    output_file = './predictions/cs2_prediction.json'
    save_predictions_to_json(predictions, output_file)

    print(f"Predicted player data saved to '{output_file}'")

if __name__ == "__main__":
    main()
