import json
import csv

def load_json_data(json_file):
    """Load data from the given JSON file."""
    with open(json_file, 'r') as file:
        return json.load(file)

def extract_player_info(data):
    """Extract player information from the JSON data."""
    player_info_list = []

    for match in data['data']:
        # Extract player ID from the match projection
        player_id = match["relationships"]["new_player"]["data"]["id"]

        # Find the player details in the included section
        player_detail = next((player for player in data["included"] if player["id"] == player_id), None)

        if player_detail:
            # Extract relevant attributes
            player_name = player_detail["attributes"]["display_name"]
            team_name = player_detail["attributes"]["team"]
            image_url = player_detail["attributes"]["image_url"]
            stat_type = match["attributes"]["stat_type"]  # Assuming we want the stat type ID
            
            # Access the projection information for odds type and line score
            odds_type = match["attributes"].get("odds_type", None)  # Get odds_type from attributes
            line_score = match["attributes"].get("line_score", None)  # Get line_score from attributes

            # Prepare data for saving to CSV
            player_data = {
                "player_name": player_name,
                "team_name": team_name,
                "stat_type": stat_type,
                "image_url": image_url,
                "odds_type": odds_type,  # Add odds_type
                "line_score": line_score   # Add line_score
            }
            player_info_list.append(player_data)

    return player_info_list

def save_to_csv(player_info, output_file):
    """Clear content and save extracted player information to a CSV file."""
    with open(output_file, mode='w', newline='') as file:
        # Clear the content of the file before saving new data
        file.truncate(0)
        print("Data Cleared Before Saving Newone")
        
        writer = csv.DictWriter(file, fieldnames=["player_name", "team_name", "stat_type", "image_url", "odds_type", "line_score"])
        writer.writeheader()
        writer.writerows(player_info)

def main():
    json_file = './json/cs2_data.json'  # Replace with the path to your JSON file
    output_file = './extracted_data/cs2_player_info.csv'  # Output CSV file name

    # Load the data from JSON file
    data = load_json_data(json_file)

    # Extract player information
    player_info = extract_player_info(data)

    # Save the player information to a CSV file
    save_to_csv(player_info, output_file)

    print(f"Player information saved to '{output_file}'.")

if __name__ == "__main__":
    main()
