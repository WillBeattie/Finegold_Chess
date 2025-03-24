
## Methods: Modifying Stockfish
This is my first foray into c++.  Be gentle :) 

### Rule 1: Never Play f6
Pawn moves are handled in `ExtMove* generate_pawn_moves()`.  A block of that function begins with the `if (Type != CAPTURES)` condition, covering forward pawn pushes.  That's where we'd find f2f3 and f7f6.

Single pawn moves are collected in the array `b1` then pumped into `moveList`.  Forbidding the push f3 or f6 is just a matter of adding in a conditional when emptying b1.
```
        while (b1)
        {
            Square to = pop_lsb(&b1);
            Square from = to-Up;
            if (from == SQ_F7 && to == SQ_F6) // Finegold rule: never play f6
                continue;
            if (from ==SQ_F2 && to == SQ_F3)  // Finegold rule: never play f3
                continue;
            *moveList++ = make_move(to - Up, to);
        }
```

The astute reader will realize this might not be the best implementation, since there are positions in chess in which f6 is the **only** legal move.  FinegoldFish will think those positions are stalemate, while the rest of the world would disagree.  A better implementation might be just ensuring the evaluation of the move f6 is always -infinity, or checking to see if f6 is present once the entire set of legal moves is generated any only removing it if other legal moves are available.
### Rule 2: Always play Kb1
Unlike **never play f6**, this is a prescriptive rule.  In the strictest interpretation, **always play Kb1** means 'if Kb1 is legal, it is forced'.  A more generous interpretation would be 'if you just played 0-0-0, and Kb1 is legal on your next move you must play it,' but that's way more difficult to implement.

Since it's prescriptive this is going to be *way* more harmful to the quality of play than Rule 1.  If your king ever makes it near b1, that square is a black hole, preventing you from ever activating in the endgame.  The only way to escape the b1 pit is if you get checked out of there.

### Rule 3: Always play Bf8 (or Bf1)
Similar to Rule 2, this is a prescriptive rule with a black hole effect.  One can imagine developing the King's bishop, being forced to undevelop, then repeating in a vicious cycle.  Castling kingside seems near impossible without some help from the opponent (e.g. capturing the bishop or playing an interference move once it's off its starting square).  The more I consider this the more harmful it seems - I wonder if *I* could beat Stockfish if it's kneecapped with this rule.

### Rule 4: Always sac the exchange
A trickier one to implement.  #TODO

## Test Framework

I wrote a program to take a position (given by a FEN) and compare the evaluation of normal Stockfish 11 vs. the modified engines.  

While I have some specific positions I was curious about, I also took the Lichess Master's DB and extracted every position reached over 1000 times, checking for positions where a Finegold rule carries a penalty of > 0.5 pawns.  

[^1]: I chose to modify Stockfish 11, as it was the last version of Stockfish with a purely hand-crafted evaluation function instead of one partially or fully trained by neural nets (NNUE).  Since those neural nets are trained on games with normal, non-Finegold, rules I thought it best to avoid them.  Maybe it doesn't make a difference, since surely the hand-crafted evaluations contain weights and values that have been tuned in normal chess games, but OK who knows.
