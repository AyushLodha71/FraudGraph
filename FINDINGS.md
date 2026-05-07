# Data Exploration Findings

## Dataset Overview
There are 394 columns and 590540 rows. An average transaction is of $135, but the average is going up because of some really high amount transactions. If arranged in ascending order, even the 75% transaction is $125, $10 less than the average. So, the average is most probably shifted up because of some high value transactions.

## Fraud Distribution
There are about 20,663 fraud transactions, about 3.5% of the total transactions.

## Missing Data
We are missing no card numbers. So, we have all values in card1. Upon observation, whenever V1 is missing, V10 is missing. Only 314 of ~600,000 transactions do not have a value for V100. Also found out the top 20 columns where the data is missing.

## Card Analysis
Found out the number of cards that have less than 10, 20 and 30 transactions respectively.
Here are some findings:
	1. Total unique cards: 13,553
	2. Max transactions: 14,932
	3. Min transactions: 1
	4. Below 10: 9,255 cards, 4.8% transactions, 4.0% fraud
	5. Below 20: 10,918 cards, 8.6% transactions, 6.8% fraud
	6. Below 30: 11,630 cards, 11.5% transactions, 8.5% fraud

## Threshold Decision
I found out all of the cards with less than n transaction. Here n were 10, 20 and 30. Then I found out the total number of transactions that would be excluded and their respective percentages. Finally, I counted the total number of transactions that would be excluded AND were fraud, along with percentages.

## Design Decisions
After looking at the numbers, 10 would have been too low to create graphs that would have given a meaningful decision/prediction. 30 would have been too much as I was loosing more  cases to study. Also, looking at number of transactions between 20 and 30, they were not much. Finally, I thought that 20 would neither be too messy and tough to create graphs nor be too vague prediction.

## Open Questions
Would 30 be a better pivot? The reason for this question is that the % of fraud cases is lesser in 30 that in 20. But, if I use 30, then I will loose more than 80% of the cards. So, I am confused.