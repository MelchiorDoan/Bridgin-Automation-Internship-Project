# LEARNING LOG

1. **Learned (scaling, silhouette):** Scaling gives every feature an equal say, and silhouette judges a finished clustering (below 0.25 means no real structure, rough rule of thumb; mine was about 0.13).
2. **Learned (why shuffle):** A score alone means little, so I shuffled each column and found my real score (0.133) fell inside the shuffled range (0.113 to 0.146).
3. **Mistakes and fixes:** I overwrote `scaled` (fix: give each result its own name), I used `t=` wrongly in `fcluster` (fix: `t=k, criterion='maxclust'`), I left the shuffle line as a comment (fix: remove the `#` and rerun), and I copied an example, renamed its variables to my real names and overwrote `home_score`, `home_tier` and `home_tiers.csv` with fake data (fix: delete the lines that create example data first, then re-run the real cells).
4. **Habit:** If min, mean and max are the same, something is wrong, so I print a quick check before I trust a result.
5. **Still hard:** [WRITE YOUR OWN SENTENCE HERE]
