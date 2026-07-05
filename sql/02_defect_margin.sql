-- ============================================================
--  Defect Rate vs Profit Margin — correlation-ready extract
--  Reveals the inverse relationship between quality and profitability.
-- ============================================================

-- ---------- SQLite ----------
SELECT
    Date, Orders, Defects, Revenue, Profit,
    ROUND(1.0 * Defects / Orders, 4)  AS DefectRate,
    ROUND(1.0 * Profit  / Revenue, 4) AS ProfitMargin
FROM quality
ORDER BY DefectRate;

-- ---------- SQL Server (T-SQL) ----------
/*
SELECT
    Date, Orders, Defects, Revenue, Profit,
    CAST(Defects AS FLOAT)/Orders  AS DefectRate,
    CAST(Profit  AS FLOAT)/Revenue AS ProfitMargin
FROM quality
ORDER BY DefectRate;
*/
