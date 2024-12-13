# Sports Future Prediction

## Description

Welcome to the **Sports Future Prediction** project! This tool leverages historical player data, alongside current player odds from **Prize Picks**, to predict the future performance of players in games like **League of Legends**. By analyzing past player statistics and gameplay patterns, the model predicts the likelihood of a player's success in upcoming matches.

The algorithm takes into account various factors such as previous match outcomes, performance statistics, player attributes, and current betting odds. It uses machine learning techniques to provide predictions, which are visualized through a web application.

## Algorithm Explanation

The core prediction model uses **supervised machine learning** techniques, where the algorithm is trained on historical data and continuously improves its ability to predict outcomes. Here's a breakdown of the process:

1. **Data Collection**: 
   - Historical data about player performance is gathered and stored in the `./data/league_of_legends/` folder.
   - Additional data such as match statistics and betting odds are also fetched from **Prize Picks**.

2. **Data Preprocessing**:
   - The data is cleaned and transformed into a format suitable for machine learning. Missing values are handled, and data is normalized.
   - The dataset is then split into training and testing sets for model evaluation.

3. **Feature Engineering**:
   - Features like past performance (e.g., KDA, win rates, damage dealt) and player attributes are extracted for the prediction model.
   
4. **Model Training**:
   - A machine learning model (such as **Random Forest** or **Gradient Boosting**) is trained using the prepared data.
   - The model learns the relationships between the features and the outcomes (i.e., a player's future performance).

5. **Prediction**:
   - The trained model makes predictions based on new data, including live odds from **Prize Picks** and current player performance stats.
   
6. **Prediction Evaluation**:
   - The model's predictions are evaluated using accuracy metrics, and adjustments are made for improved prediction outcomes.



### Demo Images

Here you can add demo images of your project. For example, screenshots of the web interface, graphs, or prediction results. 

![League of Legend Demo](/assets/lol.png)  
![CS2 Demo](/assets/cs2.png)

---


## Steps to Start the Project

### 1. Clone the Project

To get started, clone the repository using the following command:

```bash
git clone https://github.com/your-username/sports-future-prediction.git
```

### 2. Add Player Data

- Add the **League of Legends players' old data** in the `./data/league_of_legends/` folder.
- Ensure the data is in **CSV** or **JSON** format for easy integration into the model.

### 3. Fetch Player Odds from Prize Picks

To fetch the latest player odds, run the `run_predict.py` script:

```bash
python run_predict.py
```

This script will collect the required data from **Prize Picks** and store it in the relevant format.

### 4. Make Predictions

Once the data is fetched, run the prediction model:

```bash
python make_predictions.py
```

This will process the data and display the predicted outcomes for each player.

### 5. Start the Web Application

To visualize the results, run the `app.py` script:

```bash
python app.py
```

Once the server is running, open your browser and go to the following URL to see the web interface:

```
http://127.0.0.1:5000
```

This will display the prediction results and the corresponding player data.

## Connect with Me!

Feel free to connect with me or follow my work on the following platforms:

[![GitHub](https://img.shields.io/badge/GitHub-Profile-blue)](https://github.com/jaamyasir)  
[![Facebook](https://img.shields.io/badge/Facebook-Profile-blue)](https://www.facebook.com/jamyasir0010)  
[![Medium](https://img.shields.io/badge/Medium-Profile-green)](https://jamyasir.medium.com/)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
