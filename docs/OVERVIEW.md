# N-SQL Overview

**N-SQL** is the query language for **Law-N**, designed to operate on **live network state** rather than static rows in a traditional database.

Where classic SQL queries tables like:

```sql
SELECT * FROM users WHERE id = 1;
SELECT channel, frequency, tower_id, latency_ms
FROM network.routes
WHERE device = '0xA4C1'
  AND g_layer IN ('4G', '5G')
  AND signal_quality >= 0.85;
