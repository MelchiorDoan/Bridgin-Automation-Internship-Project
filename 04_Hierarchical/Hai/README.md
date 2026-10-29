# DECISIONS

1. **Features:** I used the average kWh of Air Conditioning, Heater, Fridge and the other seven appliances, because a total mostly counts how many readings a home has; I dropped the overall average because it repeats the other four.
2. **Scaling:** I chose z-score because it keeps equal weight for each feature and min-max is more sensitive to one extreme home; I assume no extreme outliers and roughly bell-shaped columns (not checked).
3. **Method:** I used hierarchical clustering with Ward and Euclidean distance because it is the usual starting point, but Ward likes round, similar-sized groups, so a neat tree proves nothing alone and I tested it against shuffled data.
4. **Evidence:** The tree is a smooth pyramid, cophenetic is 0.375, silhouette is about 0.13 for k = 2 to 6, and at k = 3 the real 0.133 sits inside the shuffled range of 0.113 to 0.146.
5. **Conclusion:** I found no strong clusters in the 500 homes, so I do not claim segments.
6. **Tiers:** I ranked homes by the average of the 4 scaled features and cut them into equal thirds (low, medium, high), labelled "tiers, not clusters", with two caveats: AC, Heater and Fridge each use about 20 readings per home so they are noisy, "Other" is steadier, and scaling gives all four equal weight; and homes near a cut line are almost the same.
7. **Limits:** I tested only 4 features, only Ward, k = 3 for the 20-seed test, and the data looks simulated; AC, Heater and Fridge each use about 20 readings per home (5 to 41), so they are noisy.
