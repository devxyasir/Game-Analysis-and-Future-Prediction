import json
import csv

def load_json_data(json_file):
    """Load player and match data from a JSON file."""
    with open(json_file, 'r') as file:
        return json.load(file)

def extract_player_info(matches, players_info):
    """Extract player data by matching projection and player details."""
    player_data_list = []

    for match in matches:
        match_id = match["id"]

        # Extract player ID from relationships
        player_a_id = match["relationships"]["new_player"]["data"]["id"]

        # Find Player A's information
        player_a_info = next((player for player in players_info if player["id"] == player_a_id), None)

        if player_a_info:
            player_a_name = player_a_info["attributes"]["display_name"]
            player_a_team = player_a_info["attributes"]["team"]
            player_a_position = player_a_info["attributes"]["position"]
            player_image_url = player_a_info["attributes"]["image_url"]  # Extract image URL
            
            # Extract stat_type from match
            stat_type = match["attributes"]["stat_type"]  # Assuming this is the correct path
            
            # Access odds_type and line_score from the match attributes
            odds_type = match["attributes"].get("odds_type", None)  # Extract odds type
            line_score = match["attributes"].get("line_score", None)  # Extract line score
            
            # Prepare data for saving to CSV, based on requested headers
            player_data = {
                "gameid": match_id,
                "side": "Blue",  # Placeholder for side (can be Blue/Red)
                "position": player_a_position,
                "playername": player_a_name,
                "playerid": player_a_id,
                "teamname": player_a_team,
                "teamid": player_a_info["relationships"]["team_data"]["data"]["id"],
                "image_url": player_image_url,  # Add image URL
                "stat_type": stat_type,  # Add stat type
                "odds_type": odds_type,  # Add odds type
                "line_score": line_score   # Add line score
            }
            player_data_list.append(player_data)

    return player_data_list

def save_to_csv(player_data, output_file):
    """Save extracted player data to a CSV file, clearing previous content."""
    with open(output_file, mode='w', newline='') as file:  # Opens the file in write mode
        writer = csv.DictWriter(file, fieldnames=[
            "gameid", "side", "position", "playername", "playerid", "teamname", "teamid", "image_url", "stat_type", "odds_type", "line_score"
        ])
        writer.writeheader()  # Write the header
        writer.writerows(player_data)  # Write the player data

def main():
    # Load the League of Legends match data
    json_file = './json/lol_data.json'  # Replace with the actual path of your JSON file
    lol_data = load_json_data(json_file)

    # Extract players from the "included" section of the JSON
    players_info = [player for player in lol_data["included"] if player["type"] == "new_player"]

    # Extract player information based on projections
    player_data = extract_player_info(lol_data["data"], players_info)

    # Save the player information to a CSV file
    output_file = './extracted_data/lol_player_data.csv'
    save_to_csv(player_data, output_file)

    print(f"Player information saved to {output_file}")

if __name__ == "__main__":
    main()
