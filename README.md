# Code_thesis_jgrosset

Code gFlex_alpes.py, créée avec S. MAZZOTTI dans le cadre du stage de M. GAMELIN, Mai-juin 2020.

!!! Les numero à la fin de noms des codes renvois au cahier de labo (ex : les informations pour le fichier input_1-124.py sont
visibles à la page 124 du cahier de labo numero 1) !!!



Ce code utilise le code gFlex (Wickert, 2016) qui résout les équations de flexure en 3D, ici à partir de solution analytique. L'épaisseur élastique est donc constante.
A été implémenté : 

	- La lecture d'une grille representant une charge variable spatialement 
	- La relaxation lithosphérique visqueuse (cf Turcotte et Schubert)
	- Les calculs de tenseurs de déformation et de contrainte en tout point 
	

Dans launcher-gflex.py, rentrer les paramètres de modélisation. Sauf cas particulier, il n'est pas nécessaire de changer 
des paramètres dans gflex_alpes.py. Les variables sont :
	- Le nom du modèle 
	- Le chemin du repertoire ainsi que le fichier d'entrée (.asc)
	- Les paramètres de faille (NB : Si on ne cherche pas la projection sur une faille, rentrer NAME_FAULT = 'NONE')
			Nom, pendage, pendage vers le nord, friction (NB : les coordonnés doivent être présenté dans un fichier de la forme : failles/coord_NAME_fault)
	- Les paramètre de modélisation gFlex 
			g, Module d'Young (E), poisson (nu), densités, épaisseur élastique
	- Les paramètres de temps : 
			tfin(yr), le nombre d'année après l'ajustement (= le moment qui nous interesse) 
			tau(yr), le temps caractéristiques (dans la formule de la relaxation ; doit être différent de 0, parce que division par tau)
			NB : Pour un modèle purement élastique, entrer tfin = 0 
			
	- Le fichier de référence de position GPS (NB : Si pas interessé, point_gps = Fault) 




Les fichiers de sorties sont : 
	- input_{Name_model} :  Sauvegarde des inputs du modèle 
	- gflex_U_{tfin}kyr : Longitude, Latitude, Flexure (deplacement verticale(m)), Deplacement selon x(m), Deplacement selon y(m), Vitesse verticale(mm/a), vx(mm/a), vy(mm/a) 
	- gflex_E_{tfin}kyr : Longitude, Latitude, tenseur de déformation (Exx, Exy, Eyy), tenseur de contrainte (Sxx, Sxy, Syy, MPa)
	- gflex_S-vpropre_{tfin}kyr : Longitude, Latitude, Composante principale du vecteur propre de contrainte (MPa,plan horizontal), Azimut de ce vecteur(degree), Composante secondaire du vecteur propre de contrainte(MPa), Azimut de ce vecteur(degree) 
	- gflex_Epoint_{tfin}kyr : Longitude, Latitude, tenseur de tau de déformation (exx, exy, eyy (yr-1)), vecteurs propres de tau de déformation (h1(yr-1), h2(yr-1), Az1(degree), Az2(degree)), Emax(yr-1)
	- Si GPS_point = True : gflex_v_pointgps_{tfin}kyr.txt : Latitude, Longitude (point gps), Vnord(mm/a), Vest(mm/a), Vup(mm/a), 0, 0, 0
	- Si Fault : /{NAME_FAULT}/{NAME_MODEL}_{NAME_FAULT} : Longitude, Latitude, flexure(m), vitesse(mm/a),azimut(degree), perturbation de contrainte(MPa), rake(degree)  
