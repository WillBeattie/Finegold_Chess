## Never Play f6?!
### What Finegold Chess Teaches us About Middlegame Plans

Grandmaster Ben Finegold has [some thoughts](https://www.reddit.com/r/chess/comments/e4m2ae/does_someone_know_all_or_some_of_ben_finegolds/) on how you ought to play chess.

In his videos and lectures Ben sets out a number of general pieces of advice which he sarcastically refers to as *rules*, including the rule **never play f6**.  His rules are generally helpful (f6 weakens your king, after all) but of course these moves aren't always the best idea and are sometimes downright silly. **Never play f6** is an overly-broad tongue-in-cheek suggestion, not a rule. 

But what if it was?

It turns out we can build a world without f6, and it teaches a great deal about openings and middlegame structures where f6 is a critical resource for black.

### The Approach
Here's the plan:
1. Modify the [Stockfish](https://stockfishchess.org/) engine to make a version that  thinks the move pawn to f6 is illegal.  We'll call it **FinegoldFish**
2. Evaluate every named opening in the Encyclopedia of Chess Openings (ECO) using FinegoldFish, then Stockfish 
3. Compare those evaluations to measure how much of a penalty the 'no f6' rule gives
4. Find some openings that are both a) popular, and b) heavily penalized by the 'no f6' rule
5. Play through some games to try to figure out, in words and variations, why f6 is such an important resource in those lines

## Results: Never Play f6

### Opening DB Analysis
The figure below shows ~2000 named positions from the ECO (minimum 10 games in the lichess master's DB) on a graph.  The horizontal axis shows popularity, and the vertical axis shows `FinegoldFish_Evaluation - Stockfish_Evaluation`*, which gives you a sense of how much black is hurt by the inability to play f6 in that line.  

![Most openings are unaffected by Ben's rule, but not all](../results/all_openings.png)

The vast majority of openings have little to no difference, and that makes sense.  For example, in the Dutch after `1. d4 f5`, f6 is never a legal move for black so the Finegold rule is totally irrelevant.  
### Sample Game: Caro-Kann Advance

### Sample Game: French Advance

https://lichess.org/study/9HUPUTCa/dAggmhu8#0

* Evaluations done at depth 30