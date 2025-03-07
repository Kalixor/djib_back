from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import duckdb

app = Flask(__name__)

CORS(app, origins=["http://localhost:3476"])


# Charger les fichiers CSV
df_offices = pd.read_csv("./data/MopDatasOffices_202502281210.csv")
df_taxes = pd.read_csv('./data/AccountingDatasTaxesList_202502281210.csv')
df_offices_taxes = pd.read_csv('./data/AccountingDatasOfficesTaxes_202502281210.csv')



# Assurez-vous que les colonnes utilisées pour la jointure existent
# df_offices.rename(columns={'CodeOffice': 'codeOffice'}, inplace=True)
# df_taxes.rename(columns={'CodeOffice': 'codeOffice'}, inplace=True)
# df_taxes.rename(columns={'CodeTaxe': 'taxCode'}, inplace=True)
# df_offices_taxes.rename(columns={'CodeOffice': 'codeOffice'}, inplace=True)


# print(df_offices.columns)
# print(df_taxes.columns)
# print(df_offices_taxes.columns)

# df = df_offices_taxes


# Jointure des données
# print("Avant la jointure avec df_offices_taxes:", df_offices_taxes.columns)
# print(df_offices_taxes.head())  # Vérifie si taxCode est bien présent


# print("avant la jointure df_taxes:", df_taxes.columns)
# print("\n")

# df = df_offices.merge(df_taxes, on='codeOffice', how='left')

# print("aprés jointure df_offices - df_taxes sur codeOffice:", df.columns)
# print("\n")

# df = df_offices.merge(df_offices_taxes, on='codeOffice', how='left')

# print("Après la jointure df_offices avec df_offices_taxes, df:", df.columns)

# print("\n")
# print("\n")


#GET http://127.0.0.1:5000/api/data?page=1&per_page=20
# ****************************************************
@app.route('/api/data', methods=['GET'])
def get_data():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    filters = request.args.to_dict()
    
    # Supprimer les paramètres de pagination des filtres
    filters.pop('page', None)
    filters.pop('per_page', None)
    
    # Appliquer les filtres
    filtered_df = df
    for key, value in filters.items():
        filtered_df = filtered_df[filtered_df[key].astype(str) == value]
    
    # Pagination
    total = len(filtered_df)
    paginated_df = filtered_df.iloc[(page - 1) * per_page: page * per_page]
    
    return jsonify({
        "total": total,
        "page": page,
        "per_page": per_page,
        "data": paginated_df.to_dict(orient='records')
    })

@app.route('/api/count', methods=['GET'])
def get_count():
    filters = request.args.to_dict()
    
    # Appliquer les filtres
    filtered_df = df
    for key, value in filters.items():
        filtered_df = filtered_df[filtered_df[key].astype(str) == value]
    
    return jsonify({"count": len(filtered_df)})

@app.route('/api/recettes', methods=['GET'])
def get_recettes():
    df['Date'] = pd.to_datetime(df['Date'])
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date:
        start_date = pd.to_datetime(start_date)
        df_filtered = df[df['Date'] >= start_date]
    else:
        df_filtered = df.copy()
    
    if end_date:
        end_date = pd.to_datetime(end_date)
        df_filtered = df_filtered[df_filtered['Date'] <= end_date]
    
    recettes = df_filtered.groupby(df_filtered['Date'].dt.date)['TotalAmountIn'].sum().to_dict()
    
    return jsonify({"recettes": recettes})

#http://127.0.0.1:5000/api/query?sql=SELECT%20o.codeOffice,%20t.taxeDescription,%20SUM(t.AmountPaid)%20As%20AmountPaid%20FROM%20df_offices%20o%20JOIN%20df_taxes%20t%20ON%20o.codeOffice%20=%20t.codeOffice%20GROUP%20BY%20o.codeOffice,%20t.taxeDescription

@app.route('/api/query', methods=['GET'])
def run_duckdb_query():
    sql_query = request.args.get('sql')  # Ex: ?sql=SELECT * FROM df WHERE codeOffice='123'
    
    if not sql_query:
        return jsonify({"error": "No SQL query provided"}), 400

    try:
        result_df = duckdb.query(sql_query).to_df()
        return jsonify(result_df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 400



if __name__ == '__main__':
     app.run(debug=True, port=5000, threaded=True)
