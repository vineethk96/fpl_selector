#!/usr/bin/env python3
"""
FPL Draft - Pre-Draft Analysis Script
=====================================

This script should be run before your draft to:
1. Fetch and analyze current season data
2. Generate position rankings
3. Identify value picks and sleepers
4. Create team-by-team analysis
5. Generate draft cheat sheets

Usage:
    python pre_draft_analysis.py

Make sure to set your FBR API key:
    export FBRAPI_KEY="your_api_key_here"
"""

import pandas as pd
import numpy as np
import requests
import os
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class PreDraftAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('FBRAPI_KEY')
        if not self.api_key:
            print("WARNING: FBRAPI_KEY not found in environment variables")
            print("Set it with: export FBRAPI_KEY='your_api_key_here'")
        
        self.base_url = "https://api.fbrapi.com/v1"
        self.position_weights = self._initialize_position_weights()
        self.premier_league_teams = [
            'Arsenal', 'Aston Villa', 'AFC Bournemouth', 'Brentford', 'Brighton & Hove Albion',
            'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham',
            'Liverpool', 'Luton Town', 'Manchester City', 'Manchester United', 'Newcastle United',
            'Nottingham Forest', 'Sheffield United', 'Tottenham Hotspur', 'West Ham United', 'Wolverhampton Wanderers'
        ]
        
        # Data storage
        self.players_data = None
        self.team_data = None
        
    def _initialize_position_weights(self):
        """Initialize FPL scoring weights by position"""
        return {
            'FW': {
                'goals': 9, 'assists': 6, 'shots_on_target': 2, 'key_passes': 2,
                'successful_dribbles': 1, 'accurate_crosses': 1, 'yellow_cards': -2,
                'red_cards': -7, 'aerials_won': 0.5, 'clean_sheets': 0.25,
                'penalty_goals': 9, 'penalty_missed': -4, 'own_goals': -5
            },
            'MF': {
                'goals': 9, 'assists': 6, 'shots_on_target': 2, 'key_passes': 2,
                'successful_dribbles': 1, 'accurate_crosses': 1, 'tackles_won': 1,
                'interceptions': 1, 'yellow_cards': -2, 'red_cards': -7,
                'clean_sheets': 0.75, 'penalty_goals': 9, 'penalty_missed': -4
            },
            'DF': {
                'goals': 10, 'assists': 7, 'clean_sheets': 4, 'tackles_won': 1,
                'interceptions': 1, 'yellow_cards': -2, 'red_cards': -7,
                'shots_on_target': 2, 'aerials_won': 1, 'penalty_goals': 10,
                'goals_against': -2, 'own_goals': -5
            },
            'GK': {
                'clean_sheets': 5, 'saves': 2, 'penalty_saves': 8,
                'goals_against': -2, 'yellow_cards': -2, 'red_cards': -7,
                'assists': 7, 'goals': 10
            }
        }
    
    def fetch_premier_league_data(self, season='2024-25'):
        """Fetch current Premier League player data from FBR API"""
        print(f"Fetching Premier League data for {season}...")
        
        # Example FBR API endpoints (adjust based on actual API documentation)
        endpoints = {
            'players': f"{self.base_url}/players/premier-league/{season}",
            'teams': f"{self.base_url}/teams/premier-league/{season}",
            'fixtures': f"{self.base_url}/fixtures/premier-league/{season}"
        }
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        all_data = {}
        
        for data_type, url in endpoints.items():
            try:
                print(f"Fetching {data_type}...")
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    all_data[data_type] = data
                    print(f"✓ Successfully fetched {data_type}")
                else:
                    print(f"✗ Error fetching {data_type}: {response.status_code}")
                    # Fallback to sample data for demo
                    all_data[data_type] = self._get_sample_data(data_type)
                    
            except requests.RequestException as e:
                print(f"✗ Network error fetching {data_type}: {e}")
                all_data[data_type] = self._get_sample_data(data_type)
        
        self._process_api_data(all_data)
        return all_data
    
    def _get_sample_data(self, data_type):
        """Return sample data when API is unavailable"""
        if data_type == 'players':
            return {
                'players': [
                    {
                        'name': 'Mohamed Salah', 'team': 'Liverpool', 'position': 'FW',
                        'goals': 24, 'assists': 13, 'apps': 34, 'mins': 3060,
                        'shots_on_target': 89, 'key_passes': 86, 'successful_dribbles': 45,
                        'yellow_cards': 2, 'red_cards': 0, 'clean_sheets': 18
                    },
                    {
                        'name': 'Bruno Fernandes', 'team': 'Manchester United', 'position': 'MF',
                        'goals': 8, 'assists': 15, 'apps': 32, 'mins': 2880,
                        'shots_on_target': 45, 'key_passes': 102, 'tackles_won': 45,
                        'yellow_cards': 5, 'red_cards': 0, 'clean_sheets': 12
                    },
                    {
                        'name': 'Virgil van Dijk', 'team': 'Liverpool', 'position': 'DF',
                        'goals': 2, 'assists': 3, 'apps': 35, 'mins': 3150,
                        'tackles_won': 67, 'interceptions': 89, 'aerials_won': 156,
                        'yellow_cards': 1, 'red_cards': 0, 'clean_sheets': 18
                    },
                    {
                        'name': 'Alisson', 'team': 'Liverpool', 'position': 'GK',
                        'goals': 0, 'assists': 1, 'apps': 36, 'mins': 3240,
                        'saves': 89, 'clean_sheets': 18, 'goals_conceded': 28,
                        'yellow_cards': 0, 'red_cards': 0, 'penalty_saves': 2
                    }
                ]
            }
        elif data_type == 'teams':
            return {
                'teams': [
                    {'name': 'Liverpool', 'goals_for': 86, 'goals_against': 28, 'clean_sheets': 18},
                    {'name': 'Manchester City', 'goals_for': 89, 'goals_against': 31, 'clean_sheets': 17},
                    {'name': 'Arsenal', 'goals_for': 78, 'goals_against': 35, 'clean_sheets': 15}
                ]
            }
        return {}
    
    def _process_api_data(self, api_data):
        """Process and clean the API data"""
        if 'players' in api_data:
            self.players_data = pd.DataFrame(api_data['players'].get('players', []))
            if not self.players_data.empty:
                self.players_data = self._clean_player_data(self.players_data)
        
        if 'teams' in api_data:
            self.team_data = pd.DataFrame(api_data['teams'].get('teams', []))
    
    def _clean_player_data(self, df):
        """Clean and standardize player data"""
        # Ensure numeric columns
        numeric_cols = ['goals', 'assists', 'apps', 'mins', 'shots_on_target', 
                       'key_passes', 'yellow_cards', 'red_cards']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Add derived metrics
        df['goals_per_90'] = (df['goals'] * 90) / df['mins'].replace(0, 1)
        df['assists_per_90'] = (df['assists'] * 90) / df['mins'].replace(0, 1)
        df['goal_contributions'] = df['goals'] + df['assists']
        df['gc_per_90'] = (df['goal_contributions'] * 90) / df['mins'].replace(0, 1)
        
        return df
    
    def calculate_fpl_scores(self):
        """Calculate FPL scores for all players"""
        if self.players_data is None or self.players_data.empty:
            print("No player data available")
            return
        
        print("Calculating FPL scores...")
        
        def calc_score(row):
            pos = row['position']
            if pos not in self.position_weights:
                return 0
            
            weights = self.position_weights[pos]
            score = 0
            
            for stat, weight in weights.items():
                if stat in row and pd.notna(row[stat]):
                    score += row[stat] * weight
            
            # Normalize to per-game basis
            games = max(row.get('apps', 1), 1)
            return score / games * 38  # Project to full season
        
        self.players_data['fpl_score'] = self.players_data.apply(calc_score, axis=1)
        self.players_data['fpl_score_per_game'] = self.players_data['fpl_score'] / 38
    
    def generate_position_rankings(self, top_n=25):
        """Generate top N rankings by position"""
        if self.players_data is None:
            print("No data available for rankings")
            return {}
        
        print(f"Generating top {top_n} rankings by position...")
        
        rankings = {}
        positions = ['FW', 'MF', 'DF', 'GK']
        
        for pos in positions:
            pos_data = self.players_data[self.players_data['position'] == pos].copy()
            if pos_data.empty:
                continue
                
            # Sort by FPL score
            pos_data = pos_data.nlargest(top_n, 'fpl_score')
            
            # Select relevant columns
            display_cols = ['name', 'team', 'goals', 'assists', 'apps', 'fpl_score', 'goals_per_90', 'assists_per_90']
            if pos == 'GK':
                display_cols = ['name', 'team', 'clean_sheets', 'saves', 'apps', 'fpl_score']
            elif pos == 'DF':
                display_cols = ['name', 'team', 'goals', 'assists', 'clean_sheets', 'apps', 'fpl_score']
            
            # Filter to available columns
            available_cols = [col for col in display_cols if col in pos_data.columns]
            rankings[pos] = pos_data[available_cols].round(2)
        
        return rankings
    
    def identify_value_picks(self, min_apps=15):
        """Identify potential value picks and sleepers"""
        if self.players_data is None:
            return {}
        
        print("Identifying value picks and sleepers...")
        
        # Filter players with minimum appearances
        eligible = self.players_data[self.players_data['apps'] >= min_apps].copy()
        
        value_picks = {}
        
        for pos in ['FW', 'MF', 'DF', 'GK']:
            pos_data = eligible[eligible['position'] == pos].copy()
            if pos_data.empty:
                continue
            
            # Find players with good per-game metrics but maybe lower total scores
            if pos in ['FW', 'MF']:
                # Look for high goal contribution per 90
                pos_data['value_metric'] = pos_data['gc_per_90']
                threshold = pos_data['value_metric'].quantile(0.7)  # Top 30%
            elif pos == 'DF':
                # Defenders: combine clean sheets and goal contributions
                pos_data['value_metric'] = (pos_data.get('clean_sheets', 0) * 2 + 
                                          pos_data['goal_contributions'])
                threshold = pos_data['value_metric'].quantile(0.6)
            else:  # GK
                pos_data['value_metric'] = pos_data.get('clean_sheets', 0) + pos_data.get('saves', 0) * 0.1
                threshold = pos_data['value_metric'].quantile(0.6)
            
            # Find value picks: good metrics but not in top FPL scores
            fpl_threshold = pos_data['fpl_score'].quantile(0.8)  # Top 20% by FPL score
            
            value_candidates = pos_data[
                (pos_data['value_metric'] >= threshold) & 
                (pos_data['fpl_score'] < fpl_threshold)
            ].nsmallest(10, 'fpl_score')  # Lowest FPL scores among good metric players
            
            if not value_candidates.empty:
                display_cols = ['name', 'team', 'apps', 'value_metric', 'fpl_score']
                if pos in ['FW', 'MF']:
                    display_cols.extend(['goals', 'assists', 'gc_per_90'])
                elif pos == 'DF':
                    display_cols.extend(['goals', 'assists', 'clean_sheets'])
                else:
                    display_cols.extend(['clean_sheets', 'saves'])
                
                available_cols = [col for col in display_cols if col in value_candidates.columns]
                value_picks[pos] = value_candidates[available_cols].head(5).round(2)
        
        return value_picks
    
    def team_analysis(self):
        """Analyze teams for clean sheet potential and attack strength"""
        if self.players_data is None:
            return {}
        
        print("Analyzing teams...")
        
        team_stats = {}
        
        for team in self.premier_league_teams:
            team_players = self.players_data[self.players_data['team'] == team]
            if team_players.empty:
                continue
            
            # Defensive metrics
            defenders = team_players[team_players['position'] == 'DF']
            goalkeepers = team_players[team_players['position'] == 'GK']
            
            avg_clean_sheets = 0
            if not defenders.empty or not goalkeepers.empty:
                all_defensive = pd.concat([defenders, goalkeepers])
                avg_clean_sheets = all_defensive.get('clean_sheets', pd.Series([0])).mean()
            
            # Attacking metrics
            attackers = team_players[team_players['position'].isin(['FW', 'MF'])]
            total_goals = attackers['goals'].sum() if not attackers.empty else 0
            total_assists = attackers['assists'].sum() if not attackers.empty else 0
            
            team_stats[team] = {
                'avg_clean_sheets': round(avg_clean_sheets, 1),
                'total_goals': int(total_goals),
                'total_assists': int(total_assists),
                'attack_strength': round((total_goals + total_assists) / len(attackers) if len(attackers) > 0 else 0, 1),
                'defensive_rating': 'High' if avg_clean_sheets > 15 else 'Medium' if avg_clean_sheets > 10 else 'Low'
            }
        
        return team_stats
    
    def generate_draft_cheat_sheet(self):
        """Generate a comprehensive draft cheat sheet"""
        print("Generating draft cheat sheet...")
        
        cheat_sheet = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'top_players_by_position': self.generate_position_rankings(25),
            'value_picks': self.identify_value_picks(),
            'team_analysis': self.team_analysis(),
            'draft_strategy': {
                'rounds_1_3': [
                    "Target elite midfielders (Bruno, KDB, Saka)",
                    "Consider premium forwards (Haaland, Salah)",
                    "Avoid goalkeepers - wait until round 6+",
                    "Look for players with penalty duties"
                ],
                'rounds_4_6': [
                    "Fill midfielder positions with consistent scorers",
                    "Target defenders from top defensive teams",
                    "Consider your first goalkeeper here",
                    "Look for players with multiple category contributions"
                ],
                'rounds_7_plus': [
                    "Focus on upside picks and breakout candidates",
                    "Target newly promoted team standouts",
                    "Consider injury-prone players with high ceilings",
                    "Fill bench with players who could surprise"
                ]
            }
        }
        
        return cheat_sheet
    
    def save_analysis(self, cheat_sheet, filename=None):
        """Save analysis to files"""
        if filename is None:
            filename = f"fpl_draft_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}"
        
        # Save as JSON
        json_file = f"{filename}.json"
        with open(json_file, 'w') as f:
            # Convert DataFrames to dict for JSON serialization
            json_data = {}
            for key, value in cheat_sheet.items():
                if isinstance(value, dict):
                    json_data[key] = {}
                    for k, v in value.items():
                        if isinstance(v, pd.DataFrame):
                            json_data[key][k] = v.to_dict('records')
                        else:
                            json_data[key][k] = v
                else:
                    json_data[key] = value
            
            json.dump(json_data, f, indent=2, default=str)
        
        print(f"Analysis saved to: {json_file}")
        
        # Save readable text summary
        txt_file = f"{filename}.txt"
        with open(txt_file, 'w') as f:
            f.write(f"FPL Draft Analysis - {cheat_sheet['timestamp']}\n")
            f.write("=" * 60 + "\n\n")
            
            # Top players by position
            f.write("TOP PLAYERS BY POSITION\n")
            f.write("-" * 30 + "\n")
            for pos, players in cheat_sheet['top_players_by_position'].items():
                f.write(f"\n{pos} - Top 10:\n")
                f.write(players.head(10).to_string(index=False))
                f.write("\n")
            
            # Value picks
            f.write("\nVALUE PICKS & SLEEPERS\n")
            f.write("-" * 30 + "\n")
            for pos, players in cheat_sheet['value_picks'].items():
                f.write(f"\n{pos} Value Picks:\n")
                f.write(players.to_string(index=False))
                f.write("\n")
            
            # Team analysis
            f.write("\nTEAM ANALYSIS\n")
            f.write("-" * 30 + "\n")
            for team, stats in cheat_sheet['team_analysis'].items():
                f.write(f"{team}: Clean Sheets: {stats['avg_clean_sheets']}, "
                       f"Goals+Assists: {stats['total_goals']+stats['total_assists']}, "
                       f"Defense: {stats['defensive_rating']}\n")
        
        print(f"Summary saved to: {txt_file}")

def main():
    """Main execution function"""
    print("FPL Draft - Pre-Draft Analysis")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = PreDraftAnalyzer()
    
    # Fetch current season data
    print("\n1. Fetching Premier League data...")
    api_data = analyzer.fetch_premier_league_data('2024-25')
    
    # Calculate FPL scores
    print("\n2. Calculating FPL scores...")
    analyzer.calculate_fpl_scores()
    
    # Generate comprehensive analysis
    print("\n3. Generating analysis...")
    cheat_sheet = analyzer.generate_draft_cheat_sheet()
    
    # Display quick summary
    print("\n4. QUICK SUMMARY")
    print("-" * 20)
    
    if cheat_sheet['top_players_by_position']:
        for pos in ['FW', 'MF', 'DF', 'GK']:
            if pos in cheat_sheet['top_players_by_position']:
                top_5 = cheat_sheet['top_players_by_position'][pos].head(5)
                print(f"\nTop 5 {pos}:")
                for idx, row in top_5.iterrows():
                    print(f"  {row['name']} ({row['team']}) - {row.get('fpl_score', 'N/A'):.1f}")
    
    # Save analysis
    print("\n5. Saving analysis...")
    analyzer.save_analysis(cheat_sheet)
    
    print("\n" + "=" * 50)
    print("Pre-draft analysis complete!")
    print("Files saved for reference during draft.")
    print("Run live_draft_tool.py during your actual draft.")

if __name__ == "__main__":
    main()