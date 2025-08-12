# FPL Draft Day Cheat Sheet 🏈

## Quick Setup (Before Draft Starts)

```bash
# Activate virtual environment
source fpl_draft_env/bin/activate

# Set API key (if you have one)
export FBRAPI_KEY="your_api_key_here"

# Run pre-draft analysis (30 minutes before draft)
python pre_draft_analysis.py

# Start live draft tool when draft begins
python live_draft_tool.py
```

## Live Draft Tool Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add <player>` | Mark player as taken | `add Mohamed Salah` |
| `suggest <pos>` | Get position suggestions | `suggest FW` |
| `compare <p1,p2>` | Compare players | `compare Haaland,Kane` |
| `strategy` | Get round strategy | `strategy` |
| `status` | Show draft status | `status` |
| `search <name>` | Find player info | `search Saka` |
| `myroster <player> <pos>` | Add to your roster | `myroster Salah FW` |
| `help` | Show all commands | `help` |
| `quit` | Exit tool | `quit` |

## Position Codes
- `FW` = Forwards (need 2)
- `MF` = Midfielders (need 5) 
- `DF` = Defenders (need 3)
- `GK` = Goalkeepers (need 1)
- `BENCH` = Bench players (need 6)

## Draft Strategy by Round (7th Pick)

### Rounds 1-3: Elite Talent
- **Target**: Bruno Fernandes, Kevin De Bruyne, Bukayo Saka
- **Avoid**: Goalkeepers, risky injury-prone players
- **Focus**: Players with multiple category contributions

### Rounds 4-6: Core Building  
- **Target**: Reliable midfielders, top-6 defenders
- **Consider**: First goalkeeper if elite option available
- **Focus**: Consistent performers, clean sheet potential

### Rounds 7-10: Value & Needs
- **Target**: Fill required positions, upside picks
- **Consider**: Defenders from solid defensive teams
- **Focus**: Players with breakout potential

### Rounds 11+: Depth & Sleepers
- **Target**: Young players with opportunity
- **Consider**: Newly promoted team standouts
- **Focus**: High-ceiling bench players

## Key FPL Scoring Reminders

### High-Value Stats:
- **Goals**: 9-10 points (position dependent)
- **Assists**: 6-7 points  
- **Clean Sheets**: 3-5 points (position dependent)
- **Penalty Saves**: 8 points
- **Tackles/Interceptions**: 1 point each

### Avoid These:
- **Yellow Cards**: -2 points
- **Red Cards**: -7 points  
- **Own Goals**: -5 points
- **Goals Conceded**: -1 to -2 points

## Team Clean Sheet Rankings

### Tier 1 (18+ clean sheets projected):
- Liverpool, Manchester City, Arsenal

### Tier 2 (12-17 clean sheets):
- Newcastle, Tottenham, Brighton

### Tier 3 (8-12 clean sheets):  
- Chelsea, Aston Villa, West Ham

### Avoid for Clean Sheets:
- Newly promoted teams, bottom-half teams

## Penalty Takers to Target

**Confirmed/Likely**:
- Bruno Fernandes (Man United)
- Mohamed Salah (Liverpool) 
- Harry Kane (if in PL)
- Ivan Toney (Brentford)
- James Maddison (Tottenham)

**Worth Monitoring**:
- Cole Palmer (Chelsea)
- Alexander Isak (Newcastle)
- Ollie Watkins (Aston Villa)

## Snake Draft Pick Calculator

### Your Position: 7th
- **Round 1**: Pick 7
- **Round 2**: Pick 18 (12+6)  
- **Round 3**: Pick 19 (7)
- **Round 4**: Pick 30 (12+6)
- **Round 5**: Pick 31 (7)

### Picks Until Yours Formula:
- **Odd rounds**: Target pick - current pick
- **Even rounds**: (Total teams - target pick + 1) - current pick + remaining in round

## Emergency Contacts

### If Tool Crashes:
1. Restart: `python live_draft_tool.py`
2. Re-add taken players with `add <player>` 
3. Check status with `status`

### If API Fails:
- Tool falls back to sample data automatically
- Pre-generated rankings still available in analysis files

### Key Files Generated:
- `fpl_draft_analysis_YYYYMMDD_HHMM.json` (data file)
- `fpl_draft_analysis_YYYYMMDD_HHMM.txt` (readable summary)

## Quick Tips

### Before Your Pick:
1. `suggest <position>` for your target position
2. `compare <player1,player2>` for tough decisions  
3. `strategy` for round-specific advice

### After Each Pick (Others):
1. `add <player name>` to mark as taken
2. Check `status` to see picks until yours

### Draft Day Psychology:
- **Stay flexible** - don't reach for players
- **Value over need** early - fill needs later
- **Trust your prep** - use the analysis data
- **Track trends** - are people going heavy on certain positions?

## Common Mistakes to Avoid

❌ **Taking GK too early** (wait until round 6+)  
❌ **Reaching for your favorite players** (value matters)  
❌ **Ignoring bye weeks/rotation** (less relevant but still factor)  
❌ **Forgetting to mark players taken** (tool needs updates)  
❌ **Not having backup plans** (always have 2-3 targets per round)

## Last-Minute Prep Checklist

- [ ] Virtual environment activated
- [ ] API key set (or sample data ready)
- [ ] Pre-draft analysis completed  
- [ ] Draft position and league size confirmed
- [ ] Live tool tested with a few commands
- [ ] Top targets for first 5 rounds identified
- [ ] Backup options noted for each round

**Good luck! May your picks be wise and your players stay healthy! 🍀⚽**