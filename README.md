# PI2C : Quoridor Game

Ce projet a pour but de créer une petite intelligence artificielle capable de jouer de façon autonome à un jeu de plateau qui dans notre cas est le jeu du quoridor. 

## Fonctionnalités de l'IA

- Connexion TCP à un serveur 
- Communication serveur/client
- Déplacement automatique du joueur 
- Placement automatique de murs en fonction de la position de l'adversaire
- Algorithme de recherche type BFS

## Stratégie utilisée 

## Utilisation 

Afin de pouvoir utiliser cette IA, il faut commencer par démarrer correctement le serveur se trouvant dans le dossier PI2CChampionshipRunner en spécifiant convenablement le nom du jeu. Mais avant ça, il faut s'assurer que tous les modules sont correctement installés dans la version python utilisée. Les modules nécessaires au lancement de serveur sont dans le fichier requierements.txt du dossier PI2C. 

Les modules peuvent directement être installés depuis le terminal via la commande 'pip -r install requirements.txt'

Ensuite, il ne reste qu'à lancer les codes de deux joueurs. Une fois la requête de connexion acceptée et la réponse au ping convenablement envoyée, la partie peut commencer. 

Afin de pouvoir jouer, il est essentiel de pouvoir recevoir des requêtes de jeu, et de répondre à ces requêtes avec un format correct. Autrement, les mouvements de type pawn ou blocker ne seront pas reconnus. 

Pour information, chacun des échanges entre le serveur et le client se font via des fichiers json. 

## Auteur 

Ce projet a été développé par Onya Pierrot et Mournin Ibtihal.
