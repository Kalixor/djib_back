-- TABLE OFFICE TAXES : Recettes totales (payés et prévus) ANNUELLE
SELECT 
    STRFTIME('%Y', CAST(Date AS DATE)) AS Year,
    SUM(TotalPaidValue) AS TotalPaidValue,
    SUM(TotalAssessedValue) AS TotalAssessedValue,
FROM df_offices_taxes
GROUP BY Year
ORDER BY Year

-- TABLE OFFICE TAXES : Recettes totales (payés et prévus) ANNUELLE avec variations et ecarts
SELECT 
    yd1.Year,
    yd1.TotalPaidValue,
    yd1.TotalAssessedValue,
    
    -- Valeur de l'année précédente (Previous)
    yd2.TotalPaidValue AS Previous,

    -- Variation en pourcentage
    CASE 
        WHEN yd2.TotalPaidValue IS NOT NULL AND yd2.TotalPaidValue <> 0 
        THEN ((yd1.TotalPaidValue - yd2.TotalPaidValue) / yd2.TotalPaidValue) * 100
        ELSE NULL 
    END AS Variation,

    -- Écart entre TotalAssessedValue et TotalPaidValue
    (yd1.TotalPaidValue - yd1.TotalAssessedValue) AS Ecart

FROM (
    SELECT 
        STRFTIME('%Y', CAST(Date AS DATE)) AS Year,
        SUM(TotalPaidValue) AS TotalPaidValue,
        SUM(TotalAssessedValue) AS TotalAssessedValue
    FROM df_offices_taxes
    GROUP BY Year
) AS yd1
LEFT JOIN (
    SELECT 
        STRFTIME('%Y', CAST(Date AS DATE)) AS Year,
        SUM(TotalPaidValue) AS TotalPaidValue
    FROM df_offices_taxes
    GROUP BY Year
) AS yd2 
ON CAST(yd1.Year AS INTEGER) = CAST(yd2.Year AS INTEGER) + 1  -- Jointure sur l'année précédente

ORDER BY yd1.Year;


-- TABLE OFFICE TAXES : Recettes totales (payés et prévus) MENSUELLE
SELECT 
    STRFTIME('%Y-%m', CAST(Date AS DATE)) AS Month,
    SUM(TotalPaidValue) AS TotalPaidValue,
    SUM(TotalAssessedValue) AS TotalAssessedValue,
FROM df_offices_taxes
GROUP BY Month
ORDER BY Month

-- TABLE OFFICE TAXES : Recettes totales (payés et prévus) JOURNALIERE
SELECT 
    STRFTIME('%Y-%m-%d', CAST(Date AS DATE)) AS Day,
    SUM(TotalPaidValue) AS TotalPaidValue,
    SUM(TotalAssessedValue) AS TotalAssessedValue,
FROM df_offices_taxes
GROUP BY Day
ORDER BY Day

-- TABLE OFFICE TAXES : Recettes totales (payés et prévus) JOURNALIERE POUR UNE DATE
SELECT 
    STRFTIME('%Y-%m-%d', CAST(Date AS DATE)) AS Day,
    SUM(TotalPaidValue) AS TotalPaidValue,
    SUM(TotalAssessedValue) AS TotalAssessedValue,
FROM df_offices_taxes
WHERE CAST(Date AS DATE) = '2024-05-15'
GROUP BY Day
ORDER BY Day

-- TABLE OFFICE TAXES : Recettes totales (payés et prévus) JOURNALIERE POUR INTERVAL 
SELECT 
    STRFTIME('%Y-%m-%d', CAST(Date AS DATE)) AS Day,
    SUM(TotalPaidValue) AS TotalPaidValue,
    SUM(TotalAssessedValue) AS TotalAssessedValue,
FROM df_offices_taxes
WHERE CAST(Date AS DATE) BETWEEN '2024-05-15' AND '2024-06-20'
GROUP BY Day
ORDER BY Day




-- TABLE TAXES LIST :Paiements reçus et prévus par Bureau par Taxes JOURNALIER
SELECT 
    CodeOffice,
    CodeTaxe,
    STRFTIME('%Y-%m-%d', CAST(Date AS DATE)) AS Day,
    SUM(AmountPaid) AS AmountPaid,
    SUM(AmountAssessed) AS AmountAssessed,
FROM df_taxes
GROUP BY CodeOffice, CodeTaxe, Day

-- TABLE TAXES LIST :Paiements reçus et prévus par Bureau et par Taxes HEBDOMADAIRE
SELECT 
    CodeOffice,
    CodeTaxe,
    STRFTIME('%Y-%W', CAST(Date AS DATE)) AS Week,
    SUM(AmountPaid) AS AmountPaid,
    SUM(AmountAssessed) AS AmountAssessed,
FROM df_taxes
GROUP BY CodeOffice, CodeTaxe, Week
ORDER BY Week

-- TABLE TAXES LIST :Paiements reçus et prévus par Bureau et par Taxes MENSUELLE
SELECT 
    CodeOffice,
    CodeTaxe,
    STRFTIME('%Y-%m', CAST(Date AS DATE)) AS Month,
    SUM(AmountPaid) AS AmountPaid,
    SUM(AmountAssessed) AS AmountAssessed,
FROM df_taxes
GROUP BY CodeOffice, CodeTaxe, Month
ORDER BY Month

-- TABLE TAXES LIST :Paiements reçus et prévus par Bureau et par Taxes ANNUELLE
SELECT 
    CodeOffice,
    CodeTaxe,
    STRFTIME('%Y', CAST(Date AS DATE)) AS Year,
    SUM(AmountPaid) AS AmountPaid,
    SUM(AmountAssessed) AS AmountAssessed,
FROM df_taxes
GROUP BY CodeOffice, CodeTaxe, Year
ORDER BY Year



-- TABLE DATA OFFICE : Entrées journalières par Bureau par mode de paiement JOURNALIERE
SELECT 
    CodeOffice,
    MopCod,
    STRFTIME('%Y-%m-%d', CAST(Date AS DATE)) AS Day,
    SUM(TotalAmountIn) AS TotalAmountIn,
FROM df_offices
GROUP BY CodeOffice, MopCod, Day
ORDER BY Day

-- TABLE DATA OFFICE : Entrées journalières par Bureau par mode de paiement JOURNALIERE
SELECT 
    CodeOffice,
    MopCod,
    STRFTIME('%Y-%m-%d', CAST(Date AS DATE)) AS Day,
    SUM(TotalAmountIn) AS TotalAmountIn,
FROM df_offices
GROUP BY CodeOffice, MopCod, Day
ORDER BY Day


-- TABLE DATA OFFICE : Entrées journalières par Bureau par mode de paiement HEBDO
SELECT 
    CodeOffice,
    MopCod,
    STRFTIME('%Y-%W', CAST(Date AS DATE)) AS Week,
    SUM(TotalAmountIn) AS TotalAmountIn,
FROM df_offices
GROUP BY CodeOffice, MopCod, Week
ORDER BY Week


-- TABLE DATA OFFICE : Entrées journalières par Bureau par mode de paiement MENSUELLE
SELECT 
    CodeOffice,
    MopCod,
    STRFTIME('%Y-%m', CAST(Date AS DATE)) AS Month,
    SUM(TotalAmountIn) AS TotalAmountIn,
FROM df_offices
GROUP BY CodeOffice, MopCod, Month
ORDER BY Month

-- TABLE DATA OFFICE : Entrées journalières par Bureau par mode de paiement ANNUELLE
SELECT 
    CodeOffice,
    MopCod,
    STRFTIME('%Y', CAST(Date AS DATE)) AS Year,
    SUM(TotalAmountIn) AS TotalAmountIn,
FROM df_offices
GROUP BY CodeOffice, MopCod, Year
ORDER BY Year


-- TABLE DATA OFFICE :  CodeOffice par OfficeName
SELECT 
    DISTINCT CodeOffice,
    OfficeName,
FROM df_offices_taxes


-- TABLE DATA OFFICE :  CodeOffice par OfficeName
SELECT 
    DISTINCT CodeOffice,
    OfficeName,
FROM df_offices_taxes
WHERE OfficeName IS NOT NULL


-- TABLE DATA OFFICE :  CodeTax  par TaxDescription
SELECT 
    DISTINCT CodeTaxe,
    TaxeDescription,
FROM df_taxes
WHERE TaxeDescription IS NOT NULL

-- Bureaux par Taxe, par Mois
SELECT 
    CodeOffice,
    CodeTaxe,
    STRFTIME('%Y-%m', CAST(Date AS DATE)) AS Month,
    SUM(AmountPaid) AS TotalAmountPaid
FROM df_taxes
GROUP BY CodeOffice, CodeTaxe, Month
ORDER BY CodeOffice, Month, CodeTaxe


-- Recette par Bureaux et par Taxe, reparti par Mois
SELECT 
	dt.CodeOffice,
	(SELECT o.OfficeName 
	 FROM df_offices_taxes o 
	 WHERE o.CodeOffice = dt.CodeOffice
	 LIMIT 1) AS OfficeName,
	STRFTIME('%Y-%m', CAST(dt.Date AS DATE)) AS Month,
	dt.CodeTaxe,
	dt.TaxeDescription,
	SUM(dt.AmountPaid) AS TotalAmountPaid
FROM df_taxes dt
WHERE STRFTIME('%Y', CAST(dt.Date AS DATE)) = 2022
GROUP BY 
	dt.CodeOffice, 
	OfficeName, 
	STRFTIME('%Y-%m', CAST(dt.Date AS DATE)),
	dt.CodeTaxe,
	dt.TaxeDescription
ORDER BY 
	dt.CodeOffice, 
	Month, 
	dt.CodeTaxe

    DB_CONFIG = {
    "host": "douane-db.cfi0m28swsnu.us-east-1.rds.amazonaws.com",
    "user": "douanedb",
    "password": "sXfJ9KtAF7MJgMQa9*hN",
    "database": "douanedb",
    "cursorclass": pymysql.cursors.DictCursor
}