## Finegold Chess: Never Play f6!

Grandmaster Ben Finegold has [some thoughts](https://www.reddit.com/r/chess/comments/e4m2ae/does_someone_know_all_or_some_of_ben_finegolds/) on how you ought to play chess.

In his videos and lectures Ben sets out a number of general pieces of advice which he sarcastically refers to as *rules*, including:

* Never play f6 (or f3)
* Always play Kb1 (or Kb8)
* Always play Bf8 (or Bf1)
* Always sac the exchange

These rules are generally helpful - playing f6 or f3 weakens your king, Kb1 after castling long helps get it out of the center, and a bishop on f8 is a good defensive resource. Of course these moves aren't always the best idea and are sometimes downright silly. They are overly-broad tongue-in-cheek suggestions, not rules. But what if they were?

How would chess look if we were *forced* to follow Ben's rules? How much of a performance penalty would each rule exact? Are there particular common positions or openings where a rule is particularly punitive? How much would it matter if our opponent *knew* we were playing by these rules?

We can try to answer these questions with the help of an engine. [Stockfish](https://stockfishchess.org/) is an open source engine, so I'm free to fiddle with the generation of legal moves that's performed by the `movegen.cpp` file. By doing so, we transform Stockfish into FinegoldFish, the world's strongest chess engine at this variant where certain moves are compelled or forbidden according to Ben's grandmasterly demands.

In this article we're only going to look at Rule 1: Never play f6.

I've put the most interesting results below, but if you're curious about my methods you can keep reading the following sections. If you've got positions or ideas you're curious about, drop a comment and I'll see if I can make it happen.

## Results: Never Play f6

### Opening DB Analysis

### Sample Game: Caro-Kann Advance

### Sample Game: French Advance

https://lichess.org/study/9HUPUTCa/dAggmhu8#0

## Methods: Modifying Stockfish

This is my first foray into c++. Be gentle :)

### Rule 1: Never Play f6

Pawn moves are handled in Stockfish's `ExtMove* generate_pawn_moves()` ([link to source](https://github.com/official-stockfish/Stockfish/blob/master/src/movegen.cpp)). A block of that function begins with the `if (Type != CAPTURES)` condition, covering forward pawn pushes. That's where we'd find f2f3 and f7f6.

Single pawn moves are collected in the array `b1` then pumped into `moveList`. Forbidding the push f3 or f6 is just a matter of adding in a conditional when emptying b1.

```

        while (b1) 
        { 
            Square to = pop_lsb(&b1); 
            Square from = to-Up; 
            if (from == SQ_F7 && to == SQ_F6) // Finegold rule: never play f6 
                continue; 
            if (from ==SQ_F2 && to == SQ_F3) // Finegold rule: never play f3 
                continue; 
            *moveList++ = make_move(to - Up, to); 
        }
```

The astute reader will realize this might not be the best implementation, since there are positions in chess in which f6 is the **only** legal move. FinegoldFish will think those positions are stalemate, while the rest of the world would disagree. A better implementation might be just ensuring the evaluation of the move f6 is always -infinity, or checking to see if f6 is present once the entire set of legal moves is generated any only removing it if other legal moves are available.