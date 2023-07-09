from gflex_load_2_133 import gflex,FAULTS
import os
import numpy as np
import pandas as pd


#FILE = 'erofinal_3km_smooth2km'
#FILE = 'test_3km'
#FILE = 'rand_erofinal_3km'
FILE = 'holocene_ifremer_3km'
#FILE = 'input_elev_3km'

#NAME_ini = FILE
NAME_ini = 'gps-sedim_3km'
#NAME_ini = 'erofinal_3km_smooth2km_p40'
#NAME_ini = 'sedim_3km'

PATH = '/Users/juliettegrosset/work/ERO/' 


# Fichier de charge en entrée
PATHFILE = 'data/Final/sedim/'
#PATHFILE = 'data/Final/data_processing/output/ascii/'
#PATHFILE = 'data/Final/map/'

nb = 1
nb_exist = 0

RUN_GFLEX = True

gps_point = True
GPS = PATH + 'data/gps/Blewitt_final.txt'

NAME_fault = 'NONE' #NONE Si pas utile
dip_left = [False,True]
dip = [45,25,65]
friction = [0.1,0.6]

ADDLOAD = True

#grid_coord = ['NONE','NONE','NONE','NONE']
grid_coord = [38,52,-6,20]  # NONE ou coordonnées de la grille en WGS84 (latmin, latmax, lonmin,lonmax)
#Si ValueError: could not broadcast input array from shape = augmenter la grille (grid_coord)
systeme_coord  = 'UTM31'
#systeme_coord  = 'UTM19'
uniform_grid=True # True si la grille du fichier input a une taille de cellule uniforme (dx = dy)


## gflex input 

tfin = 0   # (yr)           
tau =  [1]

method = 'SAS'
g = 9.81        #gravité
E = 1E11        #Module d'Young
nu = 0.25       #coef de poisson
rho_m = 3300    #densité du manteau
rho_q = 1500 #1500 #2700 #densité de la charge        WARNING : dans l'eau, prendre en compte le contraste de densité entre l'eau et les sédiments 
rho_f = 2500 #2500 #0 #densité du matériel de remplissage
Te = [10,20,30,40] #[10,20,30,40]       #épaisseur élastique
coef = 1	 #1	#-1E-2 #-0.28E-2	#Si besoin, coefficient de conversion pour le fichier d'entrée

psave = 40 # pas d'enregistrement dans le fichier de sortie (si psave = 40, un point enregistré tous les 40 points)

###################################################################################################
###    Loop over tau and Te   -  No need to modify anything below                               ###
###################################################################################################


for f in np.arange(nb_exist,nb,1) :
	if nb == 1 :
		DATA = PATH + PATHFILE + FILE + '.asc'
		NAME = NAME_ini
	else : 
		DATA = PATH + PATHFILE + 'random/' + FILE + '_' + str(f) + '.asc'
		NAME = NAME_ini + '_' + str(f)
		print('tirage = ' + str(f))
	
	
	if RUN_GFLEX :		
		for i in tau :
			for j in Te :
				print('TE =' + str(j))
				NAME_model = NAME + '_Te' + str(j) + 'km_tau' + str(i) +'yr'
			
				if nb == 1 :
					os.makedirs(PATH+'output/'+NAME+'/'+NAME_model,exist_ok=True)
					INPUT = open(PATH+'output/'+NAME+'/'+NAME_model+'/input_'+NAME_model,'w+')
				
				else :
					os.makedirs(PATH+'output/RANDOM/'+NAME+'/'+NAME_model,exist_ok=True)
					INPUT = open(PATH+'output/RANDOM/'+NAME+'/'+NAME_model+'/input_'+NAME_model,'w+')
			
				INPUT.write('Model name = {} \nFault name = {} \nDip = {}     Dip north = {} \nFriction = {} \n'.format(NAME_model,NAME_fault,dip,dip_left,friction))
				INPUT.write('Tau = {} \nTfin = {} \ng = {} \nE = {} \nnu = {} \nrho_m = {} \nrho_fill = {} \nTe = {}'.format(tau,tfin,g,E,nu,rho_m,rho_f,Te))

				gFlex_param = [method,g,E,nu,rho_m,rho_f,j*1000,coef]
		
			
				#RUN#
				gflex(PATH,NAME,DATA,tfin,i,gFlex_param,systeme_coord,gps_point,GPS,grid_coord,ADDLOAD,uniform_grid,psave,rho_q,nb)


if NAME_fault != 'NONE' : 
	for i in tau :
		for j in Te :
		
			print('\n \n \n \n \n \n \n \n \n TE =' + str(j) + '\n ')
			
			NAME_model = NAME + '_Te' + str(j) + 'km_tau' + str(i) +'yr'
			os.makedirs(PATH+'output/'+NAME+'/'+NAME_model+'/'+NAME_fault,exist_ok=True)
			
			for d in dip :
				for dn in dip_left :
					for f in friction :
	
						fault = [NAME_fault,d,dn,f] #latitude, longitude, azimuth, pendage, friction
						FAULTS(PATH,NAME,i,j,systeme_coord,fault,tfin)
							
