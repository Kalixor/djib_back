from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pymysql
from typing import List, Dict
import markdown
from fastapi.responses import HTMLResponse


# Connexion aux paramètres de la base de données MySQL sur AWS
DB_CONFIG = {
    "host": "douane-db.cfi0m28swsnu.us-east-1.rds.amazonaws.com",
    "user": "douanedb",
    "password": "sXfJ9KtAF7MJgMQa9*hN",
    "database": "douanedb",
    "cursorclass": pymysql.cursors.DictCursor
}

app = FastAPI()

# app.mount("/doc", StaticFiles(directory="."), name="docs")
#  python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

@app.get("/doc", response_class=HTMLResponse)
def get_documentation():
    with open("doc.md", "r", encoding="utf-8") as file:
        md_content = file.read()
    html_content = markdown.markdown(md_content)
    return HTMLResponse(content=f"<html><body>{html_content}</body></html>") 


# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplacez "*" par un domaine spécifique si besoin (ex: ["https://example.com"])
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)

def execute_query(query: str) -> List[Dict]:
    """Exécute une requête SQL et retourne les résultats."""
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return results
    finally:
        connection.close()

# TABLEAU 1 [2-R-Mens-Bureau]: Affiche les recettes par bureaux par categories de taxe par mois
@app.get("/recettes-par-bureau")
def get_recettes():
    """API qui renvoie les recettes par bureau et type de taxes pour l'année 2022."""
    query = """
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
    """
    return execute_query(query)

# TABLEAU 2 [R-Bud-Mens]: Affiche les recettes par categories de taxe réparties par mois
@app.get("/recettes-par-taxe")
def get_recettes_par_taxe():
    query = """
       SELECT 
            CodeTaxe,
            TaxeDescription,
            DATE_FORMAT(Date, '%Y-%m') AS Month,
        SUM(AmountPaid) AS TotalAmountPaid
        FROM douanedb.AccountingDatasTaxesList
        GROUP BY CodeTaxe, TaxeDescription, Month
        ORDER BY CodeTaxe, Month;
    """
    return execute_query(query)

# TABLEAU 3 [Mod-Recouv]: Affiche les recettes par bureau et mode de recouvrement réparties par mois
@app.get("/recettes-par-mode")
def get_recettes_par_mode():
    """API qui renvoie les recettes par bureau et type de taxes pour l'année 2022."""
    query = """
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
    """
    return execute_query(query)

# TABLEAU 4 [R-Journalières ]: Affiche les recettes par bureau
@app.get("/recettes")
def get_recettes():
    query = """
        SELECT Date, CodeOffice, OfficeName, TotalAmountPaid
        FROM douanedb.AccountingDatasOfficesTaxes
    """
    return execute_query(query)

 # TABLEAU 5 [1-TIC-TX]: Affiche les recettes des différents taux de TICs & TVA répartis par mois

# TABLEAU 5 [1-TIC-TX]: Affiche les recettes des différents taux de TICs & TVA répartis par mois
@app.get("/recettes_tic_tva")
def get_recettes_tic_tva():
    query = """
        SELECT CodeTaxe, DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(AmountPaid) AS TotalAmountPaid
        FROM douanedb.AccountingDatasTaxesList
        WHERE (CodeTaxe like '%TIC%' OR CodeTaxe like '%TVA%')
        GROUP BY CodeTaxe, Month
        ORDER BY CodeTaxe, Month
    """
    return execute_query(query)

# Affiche les bureaux par codeOffice
@app.get("/bureaux")
def get_bureaux():
    query = """
        SELECT DISTINCT CodeOffice, TRIM(OfficeName) As OfficeName FROM douanedb.AccountingDatasOfficesTaxes
    """
    return execute_query(query)

# Affiche une table de liaison des codeTaxe par TaxeDescription
@app.get("/taxes")
def get_taxes():
    query = """
        SELECT DISTINCT CodeTaxe, TaxeDescription FROM douanedb.AccountingDatasTaxesList WHERE TaxeDescription IS NOT NULL
    """
    return execute_query(query)

# Agregation par années
@app.get("/recettes_annuel")
def get_recettes_annuel():
    query = """
        SELECT 
            DATE_FORMAT(Date, '%Y') AS Year,
            SUM(TotalAmountPaid) AS TotalAmountPaid,
            SUM(TotalAmountAssessed) AS TotalAmountAssessed
        FROM douanedb.AccountingDatasOfficesTaxes
        GROUP BY Year
        ORDER BY Year;
    """
    return execute_query(query)

# Agregation par mois
@app.get("/recettes_mensuelle")
def get_recettes_mensuelle():
    query = """
        SELECT 
            DATE_FORMAT(Date, '%Y-%m') AS Month,
            SUM(TotalAmountPaid) AS TotalAmountPaid,
            SUM(TotalAmountAssessed) AS TotalAmountAssessed
        FROM douanedb.AccountingDatasOfficesTaxes
        GROUP BY Month
        ORDER BY Month;
    """
    return execute_query(query)

# Agregation par semaine
@app.get("/recettes_hebdo")
def get_recettes_hebdo():
    query = """
        SELECT 
            DATE_FORMAT(Date, '%Y-%v') AS Week,
            SUM(TotalAmountPaid) AS TotalAmountPaid,
            SUM(TotalAmountAssessed) AS TotalAmountAssessed
        FROM douanedb.AccountingDatasOfficesTaxes
        GROUP BY Week
        ORDER BY Week;
    """
    return execute_query(query)

# Agregation par jour
@app.get("/recettes_jour")
def get_recettes_jour():
    query = """
        SELECT 
            DATE_FORMAT(Date, '%Y-%m-%d') AS Day,
            SUM(TotalAmountPaid) AS TotalAmountPaid,
            SUM(TotalAmountAssessed) AS TotalAmountAssessed
        FROM douanedb.AccountingDatasOfficesTaxes
        GROUP BY Day
        ORDER BY Day;
    """
    return execute_query(query)