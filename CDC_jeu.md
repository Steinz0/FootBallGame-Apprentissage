# Cahier des charges<br/>Physique, caractéristiques, règles de jeu et interface

## Moteur de jeu
- Le ballon traverse les joueurs lorsqu'il se déplace très vite
- Le ballon dispose d'une vitesse et d'une acceleration

## Caractéristiques des joueurs
- Chaque joueur possède un nom crée aléatoirement parmi une base de noms
- Chaque joueur est membre d'une équipe
- Chaque joueur a connaissance de :
    - sa distance aux cages adverses
    - sa distance à ses propres cages
    - la position des autres joueurs
    - sa vitesse (manipulée par l'acceleration)
    - son orientation
- Chaque joueur possède des attributs précis (vitesse, puissance, ...)
- Chaque joueur fait parti d'une classe précise
    - Rapide : Se déplace plus rapidement mais frappe moins fort
    - Puissant : Se déplace lentement mais frappe plus fort
    - Equilibré : Se déplace et frappe de manière normale

## Règles de jeu
- Chaque équipe possède 4 joueurs
- Le ballon ne peut pas sortir du terrain (pas de touches, de corners ou de sorties de but)
- Les matchs doivent durer une durée de temps précise continue (pas de mi-temps)
- Il n'y a pas de fautes
- Après un but, on réinitialise la position des joueurs et du ballon
    - L'équipe ayant concédé le but est en position offensive
    - L'équipe ayant marqué le but en positon défensive

## Interface
- Au avant le match, on doit pouvoir :
    - choisir les actions des joueurs
    - choisir les profils des différents joueurs
    - 
- Pendant le match, on doit pouvoir :
    - mettre en pause
    - augmenter la vitesse de jeu
    - diminuer la vitesse de jeu
    - arrêter le match et revenir à l'interface initiale
- Après le match, on doit pouvoir :
    - revoir le match
    - disposer d'une timeline du match
    - jouer un autre match

## Notes supplémentaires
- Chaque match doit être sauvegardé sous forme de fichier .csv
- Libraire mlpsoccer en Python permet la création de terrains de football (peut être utile)
- Il existe des libraires réalisant la conversion Python-JavaScript (Brython et autres, à étudier)
- https://codepen.io/Eika/pen/abdYXY (code pour jeu de football basique en JS)
