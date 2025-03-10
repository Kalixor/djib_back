# Documentation de l'API

Cette documentation présente l'ensemble des endpoints disponibles sur l'API, leurs descriptions et les requêtes SQL associées.

---

## Endpoints

### 1. GET `/recettes-par-bureau`

- **Description :**  
  API qui renvoie les recettes par bureau et type de taxes pour l'année 2022.  
  *Commentaire associé :* TABLEAU 1 [2-R-Mens-Bureau]: Affiche les recettes par bureaux par catégories de taxe par mois.

- **Requête SQL :**
  ```sql
  SELECT
      dt.CodeOffice,
      (SELECT TRIM(o.OfficeName)
       FROM douanedb.AccountingDatasOfficesTaxes o
       WHERE o.CodeOffice = dt.CodeOffice
       LIMIT 1) AS OfficeName,
      DATE_FORMAT(dt.Date, '%Y-%m') AS Month,
      dt.CodeTaxe,
      TRIM(dt.TaxeDescription) AS TaxeDescription,
      SUM(dt.AmountPaid) AS TotalAmountPaid
  FROM douanedb.AccountingDatasTaxesList dt
  WHERE YEAR(Date) = 2022
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
  ```

---

### 2. GET `/recettes-par-taxe`

- **Description :**  
  Affiche les recettes par catégories de taxe réparties par mois.  
  *Commentaire associé :* TABLEAU 2 [R-Bud-Mens].

- **Requête SQL :**
  ```sql
  SELECT
      CodeTaxe,
      TaxeDescription,
      DATE_FORMAT(Date, '%Y-%m') AS Month,
      SUM(AmountPaid) AS TotalAmountPaid
  FROM douanedb.AccountingDatasTaxesList
  GROUP BY CodeTaxe, TaxeDescription, Month
  ORDER BY CodeTaxe, Month;
  ```

---

### 3. GET `/recettes-par-mode`

- **Description :**  
  API qui renvoie les recettes par bureau et mode de recouvrement réparties par mois.  
  *Commentaire associé :* TABLEAU 3 [Mod-Recouv]: Affiche les recettes par bureau et mode de recouvrement réparties par mois.

- **Requête SQL :**
  ```sql
  SELECT
      m.CodeOffice,
      (SELECT o.OfficeName
       FROM douanedb.AccountingDatasOfficesTaxes o
       WHERE o.CodeOffice = m.CodeOffice
       LIMIT 1) AS OfficeName,
      DATE_FORMAT(m.Date, '%Y-%m') AS Month,
      m.MopDsc,
      SUM(m.TotalAmountIn) AS TotalAmountPaid
  FROM douanedb.MopDatasOffices m
  GROUP BY m.CodeOffice, OfficeName, m.MopDsc, Month
  ORDER BY m.CodeOffice, Month, m.MopDsc;
  ```

---

### 4. GET `/recettes`

- **Description :**  
  Affiche les recettes par bureau.  
  *Commentaire associé :* TABLEAU 4 [R-Journalières].

- **Requête SQL :**
  ```sql
  SELECT Date, CodeOffice, OfficeName, TotalAmountPaid
  FROM douanedb.AccountingDatasOfficesTaxes
  ```

---

### 5. GET `/recettes_tic_tva`

- **Description :**  
  Affiche les recettes des différents taux de TICs & TVA répartis par mois.  
  *Commentaire associé :* TABLEAU 5 [1-TIC-TX].

- **Requête SQL :**
  ```sql
  SELECT CodeTaxe, DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(AmountPaid) AS TotalAmountPaid
  FROM douanedb.AccountingDatasTaxesList
  WHERE (CodeTaxe like '%TIC%' OR CodeTaxe like '%TVA%')
  GROUP BY CodeTaxe, Month
  ORDER BY CodeTaxe, Month
  ```

---

### 6. GET `/bureaux`

- **Description :**  
  Affiche les bureaux par CodeOffice.

- **Requête SQL :**
  ```sql
  SELECT DISTINCT CodeOffice, TRIM(OfficeName) AS OfficeName
  FROM douanedb.AccountingDatasOfficesTaxes
  ```

---

### 7. GET `/taxes`

- **Description :**  
  Affiche une table de liaison des CodeTaxe par TaxeDescription.

- **Requête SQL :**
  ```sql
  SELECT DISTINCT CodeTaxe, TaxeDescription
  FROM douanedb.AccountingDatasTaxesList
  WHERE TaxeDescription IS NOT NULL
  ```

---

### 8. GET `/recettes_annuel`

- **Description :**  
  Agrégation des recettes par années.

- **Requête SQL :**
  ```sql
  SELECT
      DATE_FORMAT(Date, '%Y') AS Year,
      SUM(TotalAmountPaid) AS TotalAmountPaid,
      SUM(TotalAmountAssessed) AS TotalAmountAssessed
  FROM douanedb.AccountingDatasOfficesTaxes
  GROUP BY Year
  ORDER BY Year;
  ```

---

### 9. GET `/recettes_mensuelle`

- **Description :**  
  Agrégation des recettes par mois.

- **Requête SQL :**
  ```sql
  SELECT
      DATE_FORMAT(Date, '%Y-%m') AS Month,
      SUM(TotalAmountPaid) AS TotalAmountPaid,
      SUM(TotalAmountAssessed) AS TotalAmountAssessed
  FROM douanedb.AccountingDatasOfficesTaxes
  GROUP BY Month
  ORDER BY Month;
  ```

