# Hybrid search in Postgres with pgvector and full-text ranks

_Learned: 2025_

**The problem:** vector search alone misses exact keywords (names, ids, quoted phrases). Keyword search alone misses paraphrases. I needed both in the same database I already used for app data.

**What worked:** I stored an embedding with pgvector and a `tsvector` for full-text search on the same row, then combined the two ranked lists with Reciprocal Rank Fusion. Each list contributes `1 / (k + rank)`. I used `k = 60`, the usual default in the published RRF formula and in the pgvector examples.

```sql
WITH semantic AS (
  SELECT id, RANK() OVER (ORDER BY embedding <=> $2) AS rank
  FROM documents
  ORDER BY embedding <=> $2
  LIMIT 20
),
keyword AS (
  SELECT id, RANK() OVER (
    ORDER BY ts_rank_cd(to_tsvector('english', content), query) DESC
  ) AS rank
  FROM documents, plainto_tsquery('english', $1) query
  WHERE to_tsvector('english', content) @@ query
  LIMIT 20
)
SELECT COALESCE(semantic.id, keyword.id) AS id,
       COALESCE(1.0 / (60 + semantic.rank), 0)
     + COALESCE(1.0 / (60 + keyword.rank), 0) AS score
FROM semantic
FULL OUTER JOIN keyword ON semantic.id = keyword.id
ORDER BY score DESC
LIMIT 5;
```

`$1` is the query text and `$2` is the query embedding. Use the pgvector operator that matches your index (`<=>` with `vector_cosine_ops`).

**Why it matters:** hybrid search is just two Postgres indexes and a rank merge. You don't need a separate search product to get keyword-and-meaning results.

Links: [pgvector hybrid search](https://github.com/pgvector/pgvector#hybrid-search)
