-- ============================================================
--  Monthly SKU Sales Pivot with Shares and Ranking
--  Technique: conditional aggregation (CASE WHEN) + window functions
--  Two dialects provided: SQLite (tested) and SQL Server (T-SQL).
-- ============================================================

-- ---------- SQLite ----------
WITH monthly AS (
    SELECT
        SKU,
        SUM(CASE WHEN strftime('%m', OrderDate) = '01' THEN UnitsSold ELSE 0 END) AS Jan,
        SUM(CASE WHEN strftime('%m', OrderDate) = '02' THEN UnitsSold ELSE 0 END) AS Feb,
        SUM(CASE WHEN strftime('%m', OrderDate) = '03' THEN UnitsSold ELSE 0 END) AS Mar,
        SUM(UnitsSold) AS Q1
    FROM sales
    GROUP BY SKU
)
SELECT
    SKU, Jan, Feb, Mar, Q1,
    ROUND(1.0 * Jan / SUM(Jan) OVER (), 2) AS JanShare,
    ROUND(1.0 * Feb / SUM(Feb) OVER (), 2) AS FebShare,
    ROUND(1.0 * Mar / SUM(Mar) OVER (), 2) AS MarShare,
    ROUND(1.0 * Q1  / SUM(Q1)  OVER (), 2) AS Q1Share,
    ROW_NUMBER() OVER (ORDER BY Q1 DESC) AS Rank
FROM monthly
ORDER BY Q1 DESC;


-- ---------- SQL Server (T-SQL) ----------
/*
WITH monthly AS (
    SELECT
        SKU,
        SUM(CASE WHEN MONTH(OrderDate) = 1 THEN UnitsSold ELSE 0 END) AS Jan,
        SUM(CASE WHEN MONTH(OrderDate) = 2 THEN UnitsSold ELSE 0 END) AS Feb,
        SUM(CASE WHEN MONTH(OrderDate) = 3 THEN UnitsSold ELSE 0 END) AS Mar,
        SUM(UnitsSold) AS Q1
    FROM sales
    GROUP BY SKU
)
SELECT
    SKU, Jan, Feb, Mar, Q1,
    CAST(Jan AS FLOAT) / SUM(Jan) OVER () AS JanShare,
    CAST(Feb AS FLOAT) / SUM(Feb) OVER () AS FebShare,
    CAST(Mar AS FLOAT) / SUM(Mar) OVER () AS MarShare,
    CAST(Q1  AS FLOAT) / SUM(Q1)  OVER () AS Q1Share,
    ROW_NUMBER() OVER (ORDER BY Q1 DESC) AS Rank
FROM monthly
ORDER BY Q1 DESC;
*/
