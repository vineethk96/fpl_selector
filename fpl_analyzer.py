import pandas as pd
import numpy as np
import requests
from typing import List, Dict, Optional, Union
import warnings
warnings.filterwarnings('ignore')

class FPLPlayerAnalyzer:
    """
    Fantasy Premier League Draft Player Analyzer
    
    This class helps analyze players based on FPL point system and suggests
    suitable replacements when players are taken in the draft.
    """
    
    def __init__(self):
        self.position_weights = self._initialize_position_weights()
        self.premier_league_teams = [
            'Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton',
            'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham',
            'Liverpool', 'Luton', 'Manchester City', 'Manchester Utd', 'Newcastle Utd',
            'Nottingham Forest', 'Sheffield Utd', 'Tottenham', 'West Ham', 'Wolves'
        ]
        self.taken_players = []
        
    def _initialize_position_weights(self) -> Dict:
        """Initialize position-specific scoring weights from FPL system"""
        return {
            'FW': {  # Forward
                'goals': 9,
                'assists': 6,
                'shots_on_target': 2,
                'key_passes': 2,
                'successful_dribbles': 1,
                'accurate_crosses': 1,
                'yellow_cards': -2,
                'red_cards': -7,
                'aerials_won': 0.5,
                'effective_clearances': 0.15,
                'saves': 2,
                'smothers': 1,
                'clean_sheets': 0.25,
                'tackles_won': 1,
                'penalty_kicks_drawn': 2,
                'penalty_kicks_missed': -4,
                'own_goals': -5,
                'dispossessed': -0.5,
                'blocked_shots': 1,
                'goals_against': -0.15,
                'interceptions': 1,
                'penalty_saves': 8,
                'high_claims': 1
            },
            'MF': {  # Midfielder
                'goals': 9,
                'assists': 6,
                'shots_on_target': 2,
                'key_passes': 2,
                'successful_dribbles': 1,
                'accurate_crosses': 1,
                'tackles_won': 1,
                'interceptions': 1,
                'yellow_cards': -2,
                'red_cards': -7,
                'clean_sheets': 0.75,
                'saves': 2,
                'smothers': 1,
                'effective_clearances': 0.25,
                'aerials_won': 0.5,
                'penalty_kicks_drawn': 2,
                'own_goals': -5,
                'dispossessed': -0.5,
                'blocked_shots': 1,
                'goals_against': -1,
                'penalty_kicks_missed': -4,
                'penalty_saves': 8,
                'high_claims': 1
            },
            'DF': {  # Defender
                'goals': 10,
                'assists': 7,
                'goals_against': -2,
                'tackles_won': 1,
                'interceptions': 1,
                'yellow_cards': -2,
                'red_cards': -7,
                'clean_sheets': 4,
                'shots_on_target': 2,
                'saves': 2,
                'penalty_kicks_drawn': 2,
                'smothers': 1,
                'key_passes': 2,
                'successful_dribbles': 1,
                'aerials_won': 1,
                'blocked_shots': 1,
                'effective_clearances': 0.25,
                'own_goals': -5,
                'dispossessed': -0.5,
                'penalty_saves': 8,
                'penalty_kicks_missed': -4,
                'accurate_crosses': 1,
                'high_claims': 1
            },
            'GK': {  # Goalkeeper
                'goals_against': -2,
                'clean_sheets': 3,
                'saves': 2,
                'high_claims': 1,
                'smothers': 1,
                'yellow_cards': -2,
                'red_cards': -7,
                'shots_on_target': 2,
                'tackles_won': 1,
                'key_passes': 2,
                'clean_sheets_full_game': 5,
                'penalty_kicks_missed': -4,
                'assists': 7,
                'penalty_kicks_drawn': 2,
                'dispossessed': -0.5,
                'aerials_won': 1,
                'blocked_shots': 1,
                'effective_clearances': 0.25,
                'successful_dribbles': 1,
                'goals': 10,
                'penalty_saves': 8,
                'own_goals': -5,
                'interceptions': 1,
                'accurate_crosses': 1
            }
        }
    
    def fetch_fbref_data(self, league_id: str = 'eng-premier-league', season: str = '2024-2025') -> Optional[pd.DataFrame]:
        """
        Fetch player data from FBRef using worldfootballR-style endpoints
        
        Args:
            league_id: League identifier (default: eng-premier-league)
            season: Season year (default: 2024-2025)
        """
        try:
            # This would typically use the worldfootballR API or similar
            # For demonstration, using placeholder URL structure
            base_url = "https://fbrapi.com/api/players"
            params = {
                'league': league_id,
                'season': season,
                'format': 'json'
            }
            
            # Note: You'll need to replace this with actual API calls
            # response = requests.get(base_url, params=params)
            # data = response.json()
            
            # For now, return sample structure
            print("Note: Replace this with actual FBRef API call")
            print("You can use the worldfootballR library or fbrapi.com")
            
            return None
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def load_sample_data(self) -> pd.DataFrame:
        """
        Load sample player data for demonstration
        In practice, this would be replaced with real FBRef data
        """
        sample_data = {
            'player': ['Mohamed Salah', 'Bruno Fernandes', 'Virgil van Dijk', 'Alisson', 
                      'Harry Kane', 'Kevin De Bruyne', 'Ruben Dias', 'Jordan Pickford',
                      'Bukayo Saka', 'Gabriel Jesus', 'William Saliba', 'Aaron Ramsdale'],
            'team': ['Liverpool', 'Manchester Utd', 'Liverpool', 'Liverpool',
                    'Bayern Munich', 'Manchester City', 'Manchester City', 'Everton',
                    'Arsenal', 'Arsenal', 'Arsenal', 'Arsenal'],
            'position': ['FW', 'MF', 'DF', 'GK', 'FW', 'MF', 'DF', 'GK', 'MF', 'FW', 'DF', 'GK'],
            'goals': [24, 8, 2, 0, 36, 7, 1, 0, 11, 11, 1, 0],
            'assists': [13, 15, 3, 1, 8, 18, 2, 1, 13, 5, 1, 0],
            'shots_on_target': [89, 45, 12, 2, 156, 31, 8, 3, 67, 43, 6, 1],
            'key_passes': [86, 102, 23, 12, 78, 124, 18, 15, 89, 34, 12, 8],
            'successful_dribbles': [45, 23, 8, 1, 34, 12, 4, 2, 78, 23, 3, 1],
            'tackles_won': [23, 45, 67, 12, 12, 34, 78, 8, 34, 18, 89, 6],
            'interceptions': [12, 34, 89, 23, 8, 23, 67, 15, 23, 12, 78, 9],
            'clean_sheets': [18, 12, 18, 18, 0, 15, 15, 8, 12, 12, 18, 8],
            'yellow_cards': [2, 5, 1, 0, 4, 3, 2, 1, 1, 2, 3, 0],
            'red_cards': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'games_played': [34, 32, 35, 36, 35, 28, 33, 36, 35, 29, 34, 32],
            'minutes_played': [3060, 2880, 3150, 3240, 3150, 2340, 2970, 3240, 3150, 2320, 3060, 2880]
        }
        
        return pd.DataFrame(sample_data)
    
    def calculate_fpl_score(self, player_data: pd.Series, position: str) -> float:
        """
        Calculate FPL score based on position-specific weights
        
        Args:
            player_data: Player statistics series
            position: Player position (FW, MF, DF, GK)
        """
        weights = self.position_weights[position]
        score = 0
        
        for stat, weight in weights.items():
            if stat in player_data:
                score += player_data[stat] * weight
        
        # Normalize by games played if available
        if 'games_played' in player_data and player_data['games_played'] > 0:
            score = score * (38 / max(player_data['games_played'], 1))  # Normalize to full season
            
        return score
    
    def add_taken_players(self, players: List[str]):
        """Add players that have been taken in the draft"""
        self.taken_players.extend(players)
        print(f"Added {len(players)} players to taken list. Total taken: {len(self.taken_players)}")
    
    def suggest_players(self, position: str, num_suggestions: int = 5, 
                       exclude_teams: List[str] = None) -> pd.DataFrame:
        """
        Suggest best available players for a position
        
        Args:
            position: Position to search (FW, MF, DF, GK)
            num_suggestions: Number of suggestions to return
            exclude_teams: Teams to exclude from suggestions
        """
        # Load data (in practice, this would be real FBRef data)
        df = self.load_sample_data()
        
        if exclude_teams is None:
            exclude_teams = []
        
        # Filter by position and availability
        available_players = df[
            (df['position'] == position) & 
            (~df['player'].isin(self.taken_players)) &
            (~df['team'].isin(exclude_teams))
        ].copy()
        
        if available_players.empty:
            print(f"No available players found for position {position}")
            return pd.DataFrame()
        
        # Calculate FPL scores
        available_players['fpl_score'] = available_players.apply(
            lambda row: self.calculate_fpl_score(row, position), axis=1
        )
        
        # Add per-game averages
        available_players['goals_per_game'] = available_players['goals'] / available_players['games_played']
        available_players['assists_per_game'] = available_players['assists'] / available_players['games_played']
        
        # Sort by FPL score and return top suggestions
        suggestions = available_players.nlargest(num_suggestions, 'fpl_score')
        
        return suggestions[['player', 'team', 'position', 'fpl_score', 'goals', 'assists', 
                          'goals_per_game', 'assists_per_game', 'games_played']]
    
    def compare_players(self, player_names: List[str]) -> pd.DataFrame:
        """
        Compare multiple players across key FPL metrics
        
        Args:
            player_names: List of player names to compare
        """
        df = self.load_sample_data()
        
        comparison_players = df[df['player'].isin(player_names)].copy()
        
        if comparison_players.empty:
            print("No players found for comparison")
            return pd.DataFrame()
        
        # Calculate FPL scores for each
        for idx, row in comparison_players.iterrows():
            comparison_players.at[idx, 'fpl_score'] = self.calculate_fpl_score(row, row['position'])
        
        # Add relevant per-game stats
        comparison_players['goals_per_game'] = comparison_players['goals'] / comparison_players['games_played']
        comparison_players['assists_per_game'] = comparison_players['assists'] / comparison_players['games_played']
        comparison_players['key_passes_per_game'] = comparison_players['key_passes'] / comparison_players['games_played']
        
        return comparison_players[['player', 'team', 'position', 'fpl_score', 'goals_per_game', 
                                 'assists_per_game', 'key_passes_per_game', 'tackles_won', 'clean_sheets']]
    
    def team_analysis(self, team_name: str) -> Dict:
        """
        Analyze team's fantasy prospects
        
        Args:
            team_name: Name of the team to analyze
        """
        df = self.load_sample_data()
        team_players = df[df['team'] == team_name]
        
        if team_players.empty:
            return {"error": f"No data found for team {team_name}"}
        
        analysis = {
            'team': team_name,
            'total_players': len(team_players),
            'avg_clean_sheets': team_players['clean_sheets'].mean(),
            'total_goals': team_players['goals'].sum(),
            'total_assists': team_players['assists'].sum(),
            'best_fpl_player': None,
            'positions_covered': team_players['position'].unique().tolist()
        }
        
        # Find best FPL player
        team_players_copy = team_players.copy()
        for idx, row in team_players_copy.iterrows():
            team_players_copy.at[idx, 'fpl_score'] = self.calculate_fpl_score(row, row['position'])
        
        best_player = team_players_copy.loc[team_players_copy['fpl_score'].idxmax()]
        analysis['best_fpl_player'] = {
            'name': best_player['player'],
            'position': best_player['position'],
            'fpl_score': best_player['fpl_score']
        }
        
        return analysis
    
    def get_draft_strategy(self, current_round: int, your_pick_position: int, 
                          total_teams: int = 12) -> Dict:
        """
        Get draft strategy recommendations based on current situation
        
        Args:
            current_round: Current draft round
            your_pick_position: Your position in the draft (1-12)
            total_teams: Total number of teams in league
        """
        strategy = {
            'round': current_round,
            'pick_position': your_pick_position,
            'recommendations': []
        }
        
        # Early rounds (1-3): Target elite players
        if current_round <= 3:
            strategy['recommendations'] = [
                "Target elite midfielders or forwards",
                "Consider premium defenders from top teams",
                "Avoid goalkeepers in early rounds",
                "Look for players with multiple category contributions"
            ]
        
        # Middle rounds (4-8): Fill core positions  
        elif current_round <= 8:
            strategy['recommendations'] = [
                "Secure reliable midfielders",
                "Target defenders with clean sheet potential",
                "Consider your first goalkeeper",
                "Look for consistent performers over boom/bust players"
            ]
        
        # Late rounds (9+): Depth and upside
        else:
            strategy['recommendations'] = [
                "Target high-upside young players",
                "Consider players returning from injury",
                "Look at newly promoted team standouts",
                "Fill bench with players who could break out"
            ]
        
        return strategy

def main():
    """Example usage of the FPL Player Analyzer"""
    
    # Initialize the analyzer
    analyzer = FPLPlayerAnalyzer()
    
    print("FPL Draft Player Analyzer")
    print("=" * 50)
    
    # Example 1: Add some taken players
    print("\n1. Adding taken players...")
    analyzer.add_taken_players(['Mohamed Salah', 'Bruno Fernandes'])
    
    # Example 2: Get suggestions for forwards
    print("\n2. Best available forwards:")
    fw_suggestions = analyzer.suggest_players('FW', 5)
    if not fw_suggestions.empty:
        print(fw_suggestions.to_string(index=False))
    
    # Example 3: Compare players
    print("\n3. Comparing midfielders:")
    mf_comparison = analyzer.compare_players(['Kevin De Bruyne', 'Bukayo Saka'])
    if not mf_comparison.empty:
        print(mf_comparison.to_string(index=False))
    
    # Example 4: Team analysis
    print("\n4. Arsenal team analysis:")
    arsenal_analysis = analyzer.team_analysis('Arsenal')
    for key, value in arsenal_analysis.items():
        print(f"{key}: {value}")
    
    # Example 5: Draft strategy
    print("\n5. Draft strategy for round 7, pick 7:")
    strategy = analyzer.get_draft_strategy(7, 7)
    for rec in strategy['recommendations']:
        print(f"- {rec}")
    
    print("\n" + "=" * 50)
    print("To use with real data:")
    print("1. Install worldfootballR or use fbrapi.com")
    print("2. Replace load_sample_data() with actual FBRef data")
    print("3. Update team names to match current season")
    print("4. Add more sophisticated analysis functions")

if __name__ == "__main__":
    main()