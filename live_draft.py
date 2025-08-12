#!/usr/bin/env python3
"""
FPL Draft - Live Draft Tool
===========================

Interactive tool to use during your actual draft.
Features:
- Track taken players in real-time
- Get position-specific suggestions
- Compare players quickly
- Strategic recommendations by round
- Draft position calculator (snake draft)

Usage:
    python live_draft_tool.py

Commands during draft:
    add <player_name>       - Mark player as taken
    suggest <position>      - Get suggestions for position (FW/MF/DF/GK)
    compare <name1,name2>   - Compare two players
    strategy               - Get current round strategy
    status                 - Show draft status
    help                   - Show all commands
    quit                   - Exit tool
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import math

class LiveDraftTool:
    def __init__(self):
        self.taken_players = []
        self.draft_order = []
        self.current_round = 1
        self.your_position = 7  # Default to 7th pick as mentioned
        self.total_teams = 12   # Standard league size
        self.players_data = None
        self.analysis_data = None
        
        # Load pre-draft analysis if available
        self.load_analysis_data()
        
        # Draft requirements
        self.roster_requirements = {
            'FW': 2,
            'MF': 5, 
            'DF': 3,
            'GK': 1,
            'BENCH': 6
        }
        
        # Your current roster
        self.your_roster = {
            'FW': [],
            'MF': [],
            'DF': [],
            'GK': [],
            'BENCH': []
        }
        
    def load_analysis_data(self):
        """Load the pre-draft analysis data"""
        # Look for the most recent analysis file
        analysis_files = [f for f in os.listdir('.') if f.startswith('fpl_draft_analysis_') and f.endswith('.json')]
        
        if analysis_files:
            latest_file = sorted(analysis_files)[-1]
            print(f"Loading analysis data from: {latest_file}")
            try:
                with open(latest_file, 'r') as f:
                    self.analysis_data = json.load(f)
                    
                # Convert back to DataFrame format for easier handling
                if 'top_players_by_position' in self.analysis_data:
                    self.players_data = {}
                    for pos, players in self.analysis_data['top_players_by_position'].items():
                        self.players_data[pos] = pd.DataFrame(players)
                        
                print("✓ Analysis data loaded successfully")
            except Exception as e:
                print(f"✗ Error loading analysis data: {e}")
        else:
            print("No pre-draft analysis found. Run pre_draft_analysis.py first for best results.")
            self._create_sample_data()
    
    def _create_sample_data(self):
        """Create minimal sample data if no analysis available"""
        sample_players = {
            'FW': pd.DataFrame([
                {'name': 'Erling Haaland', 'team': 'Manchester City', 'fpl_score': 285, 'goals': 27, 'assists': 5},
                {'name': 'Mohamed Salah', 'team': 'Liverpool', 'fpl_score': 275, 'goals': 24, 'assists': 13},
                {'name': 'Harry Kane', 'team': 'Tottenham', 'fpl_score': 265, 'goals': 30, 'assists': 8},
                {'name': 'Darwin Núñez', 'team': 'Liverpool', 'fpl_score': 220, 'goals': 15, 'assists': 9},
                {'name': 'Alexander Isak', 'team': 'Newcastle', 'fpl_score': 210, 'goals': 12, 'assists': 4}
            ]),
            'MF': pd.DataFrame([
                {'name': 'Bruno Fernandes', 'team': 'Manchester United', 'fpl_score': 255, 'goals': 8, 'assists': 15},
                {'name': 'Kevin De Bruyne', 'team': 'Manchester City', 'fpl_score': 250, 'goals': 7, 'assists': 18},
                {'name': 'Bukayo Saka', 'team': 'Arsenal', 'fpl_score': 240, 'goals': 11, 'assists': 13},
                {'name': 'Cole Palmer', 'team': 'Chelsea', 'fpl_score': 220, 'goals': 13, 'assists': 11},
                {'name': 'Phil Foden', 'team': 'Manchester City', 'fpl_score': 215, 'goals': 11, 'assists': 9}
            ]),
            'DF': pd.DataFrame([
                {'name': 'Virgil van Dijk', 'team': 'Liverpool', 'fpl_score': 180, 'goals': 2, 'assists': 3, 'clean_sheets': 18},
                {'name': 'William Saliba', 'team': 'Arsenal', 'fpl_score': 175, 'goals': 1, 'assists': 1, 'clean_sheets': 15},
                {'name': 'Ruben Dias', 'team': 'Manchester City', 'fpl_score': 170, 'goals': 1, 'assists': 2, 'clean_sheets': 17},
                {'name': 'Gabriel', 'team': 'Arsenal', 'fpl_score': 165, 'goals': 4, 'assists': 1, 'clean_sheets': 15},
                {'name': 'Trent Alexander-Arnold', 'team': 'Liverpool', 'fpl_score': 160, 'goals': 1, 'assists': 12, 'clean_sheets': 18}
            ]),
            'GK': pd.DataFrame([
                {'name': 'Alisson', 'team': 'Liverpool', 'fpl_score': 140, 'clean_sheets': 18, 'saves': 89},
                {'name': 'Ederson', 'team': 'Manchester City', 'fpl_score': 135, 'clean_sheets': 17, 'saves': 62},
                {'name': 'Aaron Ramsdale', 'team': 'Arsenal', 'fpl_score': 125, 'clean_sheets': 15, 'saves': 98},
                {'name': 'Jordan Pickford', 'team': 'Everton', 'fpl_score': 120, 'clean_sheets': 8, 'saves': 134},
                {'name': 'Nick Pope', 'team': 'Newcastle', 'fpl_score': 115, 'clean_sheets': 10, 'saves': 112}
            ])
        }
        self.players_data = sample_players
    
    def calculate_current_pick(self):
        """Calculate whose pick it is in a snake draft"""
        total_picks_made = len(self.taken_players)
        current_round = (total_picks_made // self.total_teams) + 1
        pick_in_round = (total_picks_made % self.total_teams) + 1
        
        # Snake draft logic
        if current_round % 2 == 1:  # Odd rounds (1, 3, 5, ...)
            current_picker = pick_in_round
        else:  # Even rounds (2, 4, 6, ...)
            current_picker = self.total_teams - pick_in_round + 1
        
        # Calculate when your next pick is
        picks_until_yours = 0
        if current_picker <= self.your_position and current_round % 2 == 1:
            picks_until_yours = self.your_position - current_picker
        elif current_picker >= self.your_position and current_round % 2 == 0:
            picks_until_yours = current_picker - self.your_position
        else:
            # Need to wait until next round
            remaining_picks_this_round = self.total_teams - pick_in_round + 1
            if current_round % 2 == 1:  # Currently odd, next will be even
                next_round_position = self.total_teams - self.your_position + 1
            else:  # Currently even, next will be odd
                next_round_position = self.your_position
            picks_until_yours = remaining_picks_this_round + next_round_position - 1
        
        return {
            'current_round': current_round,
            'current_picker': current_picker,
            'picks_until_yours': picks_until_yours,
            'total_picks_made': total_picks_made
        }
    
    def add_taken_player(self, player_name):
        """Add a player to the taken list"""
        if player_name not in self.taken_players:
            self.taken_players.append(player_name)
            print(f"✓ Added {player_name} to taken players list")
            
            # Update draft status
            draft_status = self.calculate_current_pick()
            print(f"Draft Status: Round {draft_status['current_round']}, "
                  f"Pick {draft_status['current_picker']}, "
                  f"{draft_status['picks_until_yours']} picks until yours")
        else:
            print(f"⚠ {player_name} already marked as taken")
    
    def get_available_players(self, position, num_suggestions=10):
        """Get available players for a position"""
        if not self.players_data or position not in self.players_data:
            print(f"No data available for position {position}")
            return pd.DataFrame()
        
        pos_data = self.players_data[position].copy()
        
        # Filter out taken players
        available = pos_data[~pos_data['name'].isin(self.taken_players)]
        
        if available.empty:
            print(f"No available players found for {position}")
            return pd.DataFrame()
        
        # Sort by FPL score and return top suggestions
        top_available = available.head(num_suggestions)
        return top_available
    
    def suggest_players(self, position, num_suggestions=8):
        """Get player suggestions for a position"""
        print(f"\n🎯 TOP {num_suggestions} AVAILABLE {position}:")
        print("-" * 50)
        
        available = self.get_available_players(position, num_suggestions)
        
        if available.empty:
            return
        
        for idx, (_, player) in enumerate(available.iterrows(), 1):
            name = player['name']
            team = player['team']
            fpl_score = player.get('fpl_score', 0)
            
            # Position-specific stats
            if position == 'GK':
                stats = f"CS: {player.get('clean_sheets', 0)}, Saves: {player.get('saves', 0)}"
            elif position == 'DF':
                stats = f"G: {player.get('goals', 0)}, A: {player.get('assists', 0)}, CS: {player.get('clean_sheets', 0)}"
            else:  # FW, MF
                stats = f"G: {player.get('goals', 0)}, A: {player.get('assists', 0)}"
            
            print(f"{idx:2d}. {name:25s} ({team:15s}) [{stats}] - {fpl_score:.1f}")
    
    def compare_players(self, player_names):
        """Compare multiple players"""
        print(f"\n⚖️  PLAYER COMPARISON:")
        print("-" * 60)
        
        comparison_data = []
        
        for player_name in player_names:
            player_info = None
            
            # Search through all positions
            for pos in ['FW', 'MF', 'DF', 'GK']:
                if pos in self.players_data:
                    pos_data = self.players_data[pos]
                    matches = pos_data[pos_data['name'].str.contains(player_name, case=False, na=False)]
                    if not matches.empty:
                        player_info = matches.iloc[0].to_dict()
                        player_info['position'] = pos
                        break
            
            if player_info:
                comparison_data.append(player_info)
            else:
                print(f"⚠ Player '{player_name}' not found")
        
        if len(comparison_data) < 2:
            print("Need at least 2 valid players to compare")
            return
        
        # Display comparison
        for player in comparison_data:
            name = player['name']
            team = player['team']
            pos = player['position']
            fpl_score = player.get('fpl_score', 0)
            
            print(f"\n{name} ({team}) - {pos}")
            print(f"  FPL Score: {fpl_score:.1f}")
            
            if pos == 'GK':
                print(f"  Clean Sheets: {player.get('clean_sheets', 0)}")
                print(f"  Saves: {player.get('saves', 0)}")
            else:
                print(f"  Goals: {player.get('goals', 0)}")
                print(f"  Assists: {player.get('assists', 0)}")
                if pos == 'DF':
                    print(f"  Clean Sheets: {player.get('clean_sheets', 0)}")
            
            taken_status = "❌ TAKEN" if player['name'] in self.taken_players else "✅ Available"
            print(f"  Status: {taken_status}")
    
    def get_draft_strategy(self):
        """Get strategic recommendations for current situation"""
        draft_status = self.calculate_current_pick()
        current_round = draft_status['current_round']
        picks_until_yours = draft_status['picks_until_yours']
        
        print(f"\n📋 DRAFT STRATEGY - Round {current_round}")
        print("-" * 40)
        
        # Analyze your current roster needs
        roster_needs = []
        for pos, required in self.roster_requirements.items():
            if pos != 'BENCH':
                current_count = len(self.your_roster[pos])
                if current_count < required:
                    roster_needs.append(f"{pos}: {required - current_count} needed")
        
        if roster_needs:
            print("🎯 Immediate Needs:")
            for need in roster_needs:
                print(f"   - {need}")
        
        # Round-specific strategy
        print(f"\n🧠 Round {current_round} Strategy:")
        
        if current_round <= 3:
            strategies = [
                "Target elite midfielders or top forwards",
                "Avoid goalkeepers (wait until round 6+)",
                "Look for penalty takers and set-piece specialists",
                "Consider players from attacking teams"
            ]
        elif current_round <= 6:
            strategies = [
                "Fill core midfielder positions",
                "Target defenders from top-6 teams for clean sheets",
                "Consider your first goalkeeper if good value",
                "Look for consistent, high-floor players"
            ]
        elif current_round <= 10:
            strategies = [
                "Focus on filling required positions",
                "Target players with high upside potential",
                "Consider differential picks from mid-table teams",
                "Look for players returning from injury"
            ]
        else:
            strategies = [
                "Fill bench with breakout candidates",
                "Target young players with opportunity",
                "Consider players from newly promoted teams",
                "Look for injury replacements who could start"
            ]
        
        for strategy in strategies:
            print(f"   - {strategy}")
        
        print(f"\n⏰ You pick in {picks_until_yours} selections")
    
    def show_draft_status(self):
        """Show current draft status"""
        draft_info = self.calculate_current_pick()
        
        print(f"\n📊 DRAFT STATUS")
        print("-" * 30)
        print(f"Round: {draft_info['current_round']}")
        print(f"Current Picker: Position {draft_info['current_picker']}")
        print(f"Your Position: {self.your_position}")
        print(f"Picks Until Yours: {draft_info['picks_until_yours']}")
        print(f"Total Picks Made: {draft_info['total_picks_made']}")
        print(f"Players Taken: {len(self.taken_players)}")
        
        # Show your roster
        print(f"\n👤 YOUR ROSTER:")
        total_picked = 0
        for pos, players in self.your_roster.items():
            required = self.roster_requirements.get(pos, 0)
            current = len(players)
            total_picked += current
            
            if pos == 'BENCH':
                print(f"  {pos}: {current}/{required} - {players if players else 'Empty'}")
            else:
                status = "✅" if current >= required else "❌"
                print(f"  {pos}: {current}/{required} {status} - {players if players else 'Empty'}")
        
        print(f"\nTotal Roster: {total_picked}/17")
    
    def add_to_your_roster(self, player_name, position):
        """Add a player to your roster"""
        if position in self.your_roster:
            required = self.roster_requirements.get(position, 0)
            current = len(self.your_roster[position])
            
            if current < required or position == 'BENCH':
                self.your_roster[position].append(player_name)
                print(f"✓ Added {player_name} to your {position}")
                
                # Also mark as taken
                self.add_taken_player(player_name)
            else:
                print(f"⚠ {position} is full ({current}/{required})")
        else:
            print(f"⚠ Invalid position: {position}")
    
    def quick_help(self):
        """Show available commands"""
        print(f"\n🛠️  AVAILABLE COMMANDS:")
        print("-" * 30)
        commands = [
            ("add <player>", "Mark player as taken"),
            ("suggest <pos>", "Get suggestions (FW/MF/DF/GK)"),
            ("compare <p1,p2>", "Compare players"),
            ("strategy", "Get draft strategy"),
            ("status", "Show draft status"),
            ("myroster <player> <pos>", "Add to your roster"),
            ("search <name>", "Find player info"),
            ("help", "Show this help"),
            ("quit", "Exit tool")
        ]
        
        for cmd, desc in commands:
            print(f"  {cmd:20s} - {desc}")
    
    def search_player(self, search_term):
        """Search for a player across all positions"""
        print(f"\n🔍 SEARCH RESULTS for '{search_term}':")
        print("-" * 40)
        
        found_players = []
        
        for pos in ['FW', 'MF', 'DF', 'GK']:
            if pos in self.players_data:
                pos_data = self.players_data[pos]
                matches = pos_data[pos_data['name'].str.contains(search_term, case=False, na=False)]
                
                for _, player in matches.iterrows():
                    taken_status = "❌ TAKEN" if player['name'] in self.taken_players else "✅ Available"
                    fpl_score = player.get('fpl_score', 0)
                    
                    print(f"  {player['name']} ({player['team']}) - {pos}")
                    print(f"    FPL Score: {fpl_score:.1f} | Status: {taken_status}")
                    
                    found_players.append(player['name'])
        
        if not found_players:
            print("  No players found matching that search term")
    
    def run_interactive_mode(self):
        """Run the interactive draft tool"""
        print("🏈 FPL LIVE DRAFT TOOL")
        print("=" * 50)
        print("Type 'help' for commands or 'quit' to exit")
        
        # Initial setup
        try:
            your_pos = input(f"Your draft position (1-{self.total_teams}) [default: {self.your_position}]: ").strip()
            if your_pos:
                self.your_position = int(your_pos)
                
            total_teams = input(f"Total teams in league [default: {self.total_teams}]: ").strip()
            if total_teams:
                self.total_teams = int(total_teams)
        except ValueError:
            print("Using default values")
        
        print(f"\n✓ Setup complete! You're picking {self.your_position} out of {self.total_teams}")
        
        while True:
            try:
                # Show current draft status
                draft_info = self.calculate_current_pick()
                prompt = f"[R{draft_info['current_round']}|{draft_info['picks_until_yours']} until you] > "
                
                command = input(prompt).strip().lower()
                
                if command == 'quit' or command == 'exit':
                    print("Good luck with your draft! 🍀")
                    break
                elif command == 'help':
                    self.quick_help()
                elif command == 'status':
                    self.show_draft_status()
                elif command == 'strategy':
                    self.get_draft_strategy()
                elif command.startswith('add '):
                    player_name = command[4:].strip()
                    self.add_taken_player(player_name)
                elif command.startswith('suggest '):
                    position = command[8:].strip().upper()
                    if position in ['FW', 'MF', 'DF', 'GK']:
                        self.suggest_players(position)
                    else:
                        print("Use: suggest FW|MF|DF|GK")
                elif command.startswith('compare '):
                    players = command[8:].strip().split(',')
                    players = [p.strip() for p in players]
                    self.compare_players(players)
                elif command.startswith('search '):
                    search_term = command[7:].strip()
                    self.search_player(search_term)
                elif command.startswith('myroster '):
                    parts = command[9:].strip().split()
                    if len(parts) >= 2:
                        player_name = ' '.join(parts[:-1])
                        position = parts[-1].upper()
                        self.add_to_your_roster(player_name, position)
                    else:
                        print("Use: myroster <player name> <position>")
                elif command == '':
                    continue
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n\nGood luck with your draft! 🍀")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    """Main function to run the live draft tool"""
    tool = LiveDraftTool()
    tool.run_interactive_mode()

if __name__ == "__main__":
    main()