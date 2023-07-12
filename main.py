import requests
import json
import urllib3
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings()

# Fonction pour effectuer une requête HTTP
def make_request(email):
    # URL de l'API PingUtil
    pingutil_url = "https://api.eva.pingutil.com/email"

    # Construit l'URL de l'API avec l'adresse e-mail à tester
    api_url = f"{pingutil_url}?email={email}"

    # Appelle l'API PingUtil avec l'adresse e-mail
    response = requests.get(api_url, verify=False)

    # Analyse la réponse JSON de l'API
    result = json.loads(response.text)
    result = result["data"]

    # Retourne l'adresse e-mail si elle est valide, sinon retourne None
    if result['deliverable']:
        return email

# Demande à l'utilisateur le nombre de threads à utiliser
num_threads = int(input("Entrez le nombre de threads: "))

# Chemin vers le fichier texte contenant la liste des adresses e-mail
input_file = "emails.txt"

# Chemin vers le fichier texte de sortie
output_file = "resultats.txt"

# Ouvre le fichier texte en mode lecture
with open(input_file, "r") as f:
    # Crée un ThreadPoolExecutor avec le nombre de threads sélectionné par l'utilisateur
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Soumet toutes les requêtes HTTP à ThreadPoolExecutor pour traitement en parallèle
        results = list(executor.map(make_request, [line.strip() for line in f]))

# Filtre les résultats pour ne garder que les adresses e-mail valides
valid_results = [result for result in results if result is not None]

# Écrit les adresses e-mail valides dans le fichier texte de sortie
with open(output_file, "w") as f:
    f.write("\n".join(valid_results))
