SELECT 
    CodeOffice,
    CodeTaxe,
    DATE_FORMAT(Date, '%Y-%m') AS Month,
    SUM(AmountPaid) AS TotalAmountPaid
FROM douanedb.AccountingDatasTaxesList
WHERE YEAR(Date) = 2022
GROUP BY CodeOffice, CodeTaxe, Month
ORDER BY CodeOffice, Month, CodeTaxe;

-- # TABLEAU 1 [2-R-Mens-Bureau]: Affiche les recettes par bureaux par categories de taxe par mois
-- # WHERE YEAR(dt.Date) = 2022
 SELECT 
    dt.CodeOffice,
    (SELECT o.OfficeName 
        FROM douanedb.AccountingDatasOfficesTaxes o 
        WHERE o.CodeOffice = dt.CodeOffice
        LIMIT 1) AS OfficeName,
    DATE_FORMAT(dt.Date, '%Y-%m') AS Month,
    dt.CodeTaxe,
    dt.TaxeDescription,
    SUM(dt.AmountPaid) AS TotalAmountPaid
FROM douanedb.AccountingDatasTaxesList dt
GROUP BY 
    dt.CodeOffice, 
    OfficeName, 
    DATE_FORMAT(dt.Date, '%Y-%m'),
    dt.CodeTaxe,
    dt.TaxeDescription
ORDER BY 
    dt.CodeOffice, 
    Month, 
    dt.CodeTaxe;



-- # TABLEAU 2 [R-Bud-Mens]: Affiche les recettes par categories de taxe réparties par mois
SELECT 
    CodeTaxe,
    DATE_FORMAT(Date, '%Y-%m') AS Month,
    SUM(AmountPaid) AS TotalAmountPaid
FROM douanedb.AccountingDatasTaxesList
GROUP BY CodeTaxe, Month
ORDER BY CodeTaxe, Month;

-- # TABLEAU 3 [Mod-Recouv]: Affiche les recettes par bureau et mode de recouvrement réparties par mois
SELECT 
    m.CodeOffice,
    (SELECT o.OfficeName 
     FROM douanedb.AccountingDatasOfficesTaxes o 
     WHERE o.CodeOffice = m.CodeOffice
     LIMIT 1) AS OfficeName,  -- Subquery to fetch OfficeName
    DATE_FORMAT(m.Date, '%Y-%m') AS Month,
    m.MopDsc,
    SUM(m.TotalAmountIn) AS TotalAmountPaid
FROM douanedb.MopDatasOffices m
GROUP BY m.CodeOffice, OfficeName, m.MopDsc, Month
ORDER BY m.CodeOffice, Month, m.MopDsc;

-- # TABLEAU 4 [R-Journalières ]: Affiche les recettes par bureau et mode de recouvrement réparties par mois
SELECT Date, CodeOffice, OfficeName, TotalAmountPaid
FROM douanedb.AccountingDatasOfficesTaxes

-- # TABLEAU 5 [1-TIC-TX]: Affiche les recettes des différents taux de TICs & TVA répartis par mois
SELECT CodeTaxe, DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(AmountPaid) AS TotalAmountPaid
FROM douanedb.AccountingDatasTaxesList
WHERE (CodeTaxe like '%TIC%' OR CodeTaxe like '%TVA%')
GROUP BY CodeTaxe, Month
ORDER BY CodeTaxe, Month