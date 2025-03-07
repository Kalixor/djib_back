import sqlparse
import urllib.parse

BASE_URL = "http://localhost:5000/api/query?sql="

def format_and_encode_sql(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    formatted_queries = []
    comment = ""
    sql_query_lines = []  # Liste pour stocker les lignes d'une requête SQL
    
    for line in lines:
        line = line.rstrip()  # Supprimer seulement les espaces à droite
        
        if line.startswith("--"):  # Si c'est un commentaire
            if sql_query_lines:  # Si une requête précédente existe, on la traite
                sql_query = "\n".join(sql_query_lines)  # Reconstruire la requête proprement
                formatted_sql = sqlparse.format(sql_query, reindent=True, keyword_case='upper')
                encoded_sql = urllib.parse.quote(formatted_sql)
                full_url = f"{BASE_URL}{encoded_sql}"
                formatted_queries.append(f"{comment}\n{full_url}\n\n")  # Ajout d'une ligne vide entre les URLs
                sql_query_lines = []  # Réinitialiser la requête
            comment = line  # Stocker le nouveau commentaire
        else:
            sql_query_lines.append(line)  # Ajouter la ligne à la requête
    
    # Traiter la dernière requête si elle existe
    if sql_query_lines:
        sql_query = "\n".join(sql_query_lines)
        formatted_sql = sqlparse.format(sql_query, reindent=True, keyword_case='upper')
        encoded_sql = urllib.parse.quote(formatted_sql)
        full_url = f"{BASE_URL}{encoded_sql}"
        formatted_queries.append(f"{comment}\n{full_url}\n\n")  # Ajout d'une ligne vide entre les URLs
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(formatted_queries)
    
    print(f"Fichier encodé généré : {output_file}")

if __name__ == "__main__":
    input_sql_file = "input.sql"  # Nom du fichier contenant les requêtes SQL non formatées
    output_encoded_file = "output_encoded.txt"  # Fichier de sortie encodé
    format_and_encode_sql(input_sql_file, output_encoded_file)
