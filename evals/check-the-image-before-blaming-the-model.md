# Most "model mistakes" were label mistakes

_Learned: 2026-11-25_

**The problem:** my receipt reader got the store, date and total all right on only 59% of a public test set. I assumed the model was weak at reading.

**What worked:** I opened the image for 24 of the key-field mistakes and judged each one by hand. Only **10 were real model errors**. The other 14 were label problems:

- **Both fair:** brand vs legal company name, short vs long store name.
- **Label style:** the training labels copied the travel date into the invoice date about half the time (taxi receipts: 359 copied it, 252 left it empty), so the model couldn't learn one rule.
- **Label wrong:** day and month swapped, and one receipt in the test set twice with different labels.

The real model errors were useful too: guessing a year when only "29DEC" was printed, reading month-first on receipts from day-first countries, and picking a bus station instead of the bus company.

I kept the official score strict, so it stays comparable with other models. Then I fixed the labels instead of the model.

**Why it matters:** before changing the model, look at 20–30 of its mistakes next to the input. Half the time the fix is in the data.
