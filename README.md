## Things that needs to be implemented
1. Reading of game state (done)
2. Knowing what is the next block
3. Knowing where is my current block
4. Reading of the score (done)
5. Keyboard input into browser (done)
6. Create function step() way so that I would screnshot -> reward -> observation (WIP)
7. done = True when game time passes 60s or die (how to check for death)
8. Use screenshot using selenium (go look at test.ipynb)

def step() -> return new_state, reward, done:
    screenshot()
    reward = current_score - prev_score
    done ?

