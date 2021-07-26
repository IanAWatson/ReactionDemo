# ReactionDemo
Toy examples of reaction enumeration.

Mostly this is about timing.

On my system, the enumerate script generates products at about 4500 products
per second. If canonicalisation is omitted, that rises to about 5000 per
second.

The reaction file for trxn generates structures about about 58,000 products
per second. Canonicalization substantially slows this however.
