import requests

# Configuration
API_URL = "http://127.0.0.1:5002/api/chat"
HEADERS = {"Content-Type": "application/json"}

def test_api():
    print("=== Testeur d'API Wikipedia/OpenAI ===")
    print(f"Endpoint: {API_URL}\n")
    
    while True:
        # Demande la question à l'utilisateur
        question = input("Posez votre question (ou 'quit' pour quitter): ").strip()
        
        if question.lower() in ('quit', 'exit', 'q'):
            break
            
        if not question:
            print("Veuillez entrer une question valide.\n")
            continue
            
        try:
            # Envoi de la requête
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json={"query": question},
                timeout=10  # 10 secondes timeout
            )
            
            # Affichage des résultats
            print("\n=== Réponse ===")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Article suggéré: {data.get('suggested_article')}")
                print(f"Succès: {data.get('success')}")
                print("\nExtrait du contenu:")
                print(data.get('content')[:500] + "...")  # Affiche les 500 premiers caractères
            else:
                print(f"Erreur: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"\nErreur de connexion: {str(e)}")
            print("Vérifiez que le serveur Flask est bien en cours d'exécution.\n")
        except Exception as e:
            print(f"\nErreur inattendue: {str(e)}")
            
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_api()