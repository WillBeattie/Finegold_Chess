# Never Play f6?!
## What Finegold Chess Teaches us About Middlegame Plans

Grandmaster Ben Finegold has [some thoughts](https://www.reddit.com/r/chess/comments/e4m2ae/does_someone_know_all_or_some_of_ben_finegolds/) on how you ought to play chess.

In his videos and lectures Ben sets out a number of general pieces of advice which he sarcastically refers to as *rules*, including the rule **never play f6**.  His rules are generally helpful (f6 weakens your king, after all) but of course these moves aren't always the best idea and are sometimes downright silly. **Never play f6** is an overly-broad tongue-in-cheek suggestion, not a rule. 

But what if it was?

It turns out we can build a world without f6, and it teaches a great deal about openings and middlegame structures where f6 is a critical resource for black.

## The Approach
Here's the plan:
1. Modify the [Stockfish](https://stockfishchess.org/) engine to make a version that  thinks the move pawn to f6 is illegal.  We'll call it **FinegoldFish**
2. Evaluate every named opening in the Encyclopedia of Chess Openings (ECO) using FinegoldFish, then Stockfish 
3. Compare those evaluations to measure how much of a penalty the 'no f6' rule gives
4. Find some openings that are both a) popular, and b) heavily penalized by the 'no f6' rule
5. Play through some games to try to figure out, in words and variations, why f6 is such an important resource in those lines

## Opening DB Analysis
The figure below shows ~2000 named positions from the ECO (minimum 10 games in the lichess master's DB) on a graph.  The horizontal axis shows popularity, and the vertical axis shows `FinegoldFish_Evaluation - Stockfish_Evaluation`[^1], which gives you a sense of how much black is hurt by the inability to play f6 in that line.  

![Most openings are unaffected by Ben's rule, but not all](../results/all_openings.png)

The vast majority of openings have little to no difference, and that makes sense.  For example, in the Dutch after `1. d4 f5`, f6 is never a legal move for black so the Finegold rule is totally irrelevant.  Even lines where f6 is *one of* black's main plans won't be affected - black just needs some decent alternate plan that don't involve f6.  Despite this, the graph shows some openings become completely unplayable if f6 is ruled out

Let's zoom in on some of the more heavily punished openings and see what they are.

## Reasons You Might Need to Play f6 
I selected ten openings that are both popular and punished by the no-f6 rule and created a study to explore why.  In each line the move f6 is a key resource for black, but for different reasons.  I've grouped them accordingly, and we'll look at an example of each below.

### Tactical Necessity - Vukovic Gambit
Probably the most convincing and least interesting examples of the lot, sometimes f6 is simply the only move to prevent immediate material loss.  Being able to repel a white bishop after it moves to g5 seems to be particularly thematic.

https://lichess.org/study/9HUPUTCa/0vmC6G3v#13
### Contest The White Pawn Center - French Tarrasch
A more familiar reason for f6 comes from closed French structures, which I get a lot as a lover of the Caro-Kann and French.  Typically in these positions Black can't hope to play around white's center and instead must attack it.  It's most common to attack the base of the pawn chain with c5, but attacking the head with f6 is often an important option as well. 

https://lichess.org/study/9HUPUTCa/kfDQhlkN#15
### Open the f-file to Attack! - Ruy Lopez, Dilworth
The Dilworth Ruy Lopez is the only variation I found with f6 as an offensive weapon.  In it, black gets a big initiative but has poor long-term chances, and needs to open lines.  The move f6 is played to open the f-file for black's rook and queen before the white king finds safety. 


https://lichess.org/study/9HUPUTCa/BjTIOAq0#23

### Dark Square King Safety - Gruenfeld, Main Line
Of the many variations of the Gruenfeld this is perhaps the most popular, and it downright stinks without f6.  White sacrifices the exchange to get Black's Gruenfeld fianchettoed bishop, leaving the dark squares around black's king vulnerable.  The move f6 is badly needed to block the long diagonal
https://lichess.org/study/9HUPUTCa/tpf4kQ8k#26



[^1] Evaluations done at depth 30