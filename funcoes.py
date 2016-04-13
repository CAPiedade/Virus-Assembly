 #-*- coding:latin1 -*-f
from __future__ import print_function
import math
import itertools
import ast
import os
import numpy

atom_masses = {
    "RU" : 102.91,
    "RB" : 85.468,
    "PT" : 195.09,
    "NI" : 58.71,
    "NA" : 22.99,
    "NB" : 92.906,
    "BH" : 272.0,
    "NE" : 20.179,
    "LI" : 6.941,
    "PB" : 207.2,
    "RE" : 128.207,
    "TL" : 204.37,
    "AS" : 74.922,
    "RA" : 226.03,
    "PD" : 106.4,
    "TI" : 47.9,
    "AL" : 26.982,
    "RN" : 222.0,
    "TE" : 127.6,
    "RH" : 102.906,
    "PO" : 209.0,
    "TA" : 180.95,
    "BE" : 9.0122,
    "FR" : 223.0,
    "XE" : 131.3,
    "BA" : 137.33,
    "HS" : 227.0,
    "LA" : 138.90547,
    "DB" : 268.0,
    "BI" : 206.98,
    "TC" : 97.0,
    "FE" : 55.847,
    "BR" : 79.904,
    "H" : 1.0079,
    "CU" : 63.546,
    "HF" : 178.49,
    "HG" : 200.59,
    "HE" : 4.0026,
    "CL" : 35.453,
    "MG" : 24.305,
    "B" : 10.81,
    "SG" : 271.0,
    "F" : 18.998,
    "I" : 126.9,
    "SR" : 87.62,
    "K" : 39.096,
    "MN" : 54.938,
    "ZN" : 65.38,
    "O" : 15.999,
    "N" : 14.007,
    "P" : 30.974,
    "S" : 32.06,
    "SN" : 118.69,
    "W" : 183.84,
    "V" : 50.941,
    "Y" : 88.906,
    "SB" : 121.75,
    "CS" : 132.91,
    "OS" : 190.2,
    "SE" : 78.96,
    "SC" : 44.955912,
    "AC" : 227.0,
    "CO" : 58.933,
    "AG" : 107.87,
    "KR" : 83.8,
    "C" : 12.011,
    "SI" : 28.086,
    "CA" : 40.08,
    "IR" : 192.22,
    "RF" : 265.0,
    "CD" : 112.41,
    "GE" : 72.59,
    "AR" : 39.948,
    "AU" : 196.97,
    "MT" : 276.0,
    "GA" : 69.72,
    "IN" : 114.82,
    "MO" : 95.94,
    "CR" : 51.996,
    "AT" : 210.0,
    "ZR" : 91.224,
    "X" : 0.0

}
# O X no dicion�rio em cima designa um �tomo desconhecido. C'omo tal, para que
# n�o ocorra erro, deu-se-lhe um valor "0.0" ... Ser� que mudo????

def create_Dict_Atom(l):
    d={}
    d["Estrutura"]=l[0:6].strip()
    d["Linha"] = int(l[6:11])
    d["x"] = float(l[29:37])
    d["y"] = float(l[38:45])
    d["z"] = float(l[46:55])
    a = l[-4:].strip()
    d["Atomo"] = a
    d["TipoAtomo"]=l[13:17].strip()
    d["Massa"] = atom_masses[a]
    d["Res"]= l[17:20]
    d["Posicao"]=int(l[22:26].strip())
    d["Cadeia"]= l[21:22]

    return d

#Leitura do ficheiro PDB
def PDB_read(ficheiro):
    F = open(ficheiro)
    ATOM_PDB=[]
    titulo = ""
    for i in F:
        i = i.strip()
        if i.startswith("TITLE"):
            titulo += i[10:]
        elif i.startswith("ATOM"):
            ATOM_PDB.append(create_Dict_Atom(i))
    F.close()
    return ATOM_PDB, titulo

#C�lcula da massa da prote�na
def Mass(lista):
    M=0.0
    for i in lista:
        M+=i["Massa"]
    return M

#C�lculo do centro de massa
def Mass_Center(lista):
    xc=0.0
    yc=0.0
    zc=0.0
    M = Mass(lista)
    for i in lista:
        xc+=i["x"]*i["Massa"]/M
        yc+=i["y"]*i["Massa"]/M
        zc+=i["z"]*i["Massa"]/M
    return xc,yc,zc


def cadeias(lista):
	s = ''
	L_cadeias = []
	cadeia = []
	for i in lista:
		if i['Cadeia']==s:
			cadeia.append(i)
		else:
			if s=='':
				s = i['Cadeia']
				cadeia = []
				cadeia.append(i)
			else:
				s = i['Cadeia']
				L_cadeias.append(cadeia)
				cadeia = []
				cadeia.append(i)
	L_cadeias.append(cadeia)
	return L_cadeias

def residuos(lista_cadeias):
	res=[]
	L_res =[]
	L_cad_res=[]
	n = 0
	for cadeia in lista_cadeias:
		for atom in cadeia:
			if atom['Posicao']==n:
				res.append(atom)
			else:
				if n == 0:
					n = atom['Posicao']
					res.append(atom)
				else:
					n = atom['Posicao']
					L_res.append(res)
					res=[]
					res.append(atom)
		L_res.append(res)
		L_cad_res.append(L_res)
		res=[]
		L_res=[]
	return L_cad_res

def centroid(DicAtom):
	xc=0.0
	yc=0.0
	zc=0.0
	L_cadeias = cadeias(DicAtom)
	L_cad_res = residuos(L_cadeias)
	Dic_Res = []
	Cad = {}
	r=''
	p=''
	N = 1
	for cadeia in L_cad_res:
		for res in cadeia:
			residuo = []
			for atom in res:
				if atom['TipoAtomo'] not in ['N','CA','C','O']:
					residuo.append(atom)
			if residuo!= []:
				for i in residuo:
					if i['TipoAtomo'] == 'CB' :
						xc+=i["x"]/len(residuo)
						yc+=i["y"]/len(residuo)
						zc+=i["z"]
						r = i['Res']
						p = i['Posicao']
						c = i['Cadeia']
				dic={}
				dic['x']=xc
				dic['y']=yc
				dic['z']=zc
				dic['Res']=r
				dic['Posicao']=p
				dic['Cadeia']=c
				Dic_Res.append(dic)
		Cad[N] = Dic_Res
		N+=1
		Dic_Res =[]

	return Cad

hydrophobe = ['ALA','VAL','LEU','ILE','MET','PHE','TYR','TRP']

def numhydrophobe(centroid,ficheiro):
	F = open(ficheiro+'.txt','w')

	for cad1 in centroid:
		for cad2 in centroid:
			if cad1!=cad2 and cad1 > cad2:
				for atomi in centroid[cad1]:
					for atomj in centroid[cad2]:
						if atomi['Res'] in hydrophobe and atomj['Res'] in hydrophobe:
							I = (atomi['x'],atomi['y'],atomi['z'])
							J = (atomj['x'],atomj['y'],atomj['z'])
							dist = vecdist(I,J)
							#~ D = dist - (
							if dist/1000<=7:
								print('Ligacao entre',atomi['Res'],atomi['Posicao'],' Cadeia',atomi['Cadeia'] ,' com ',atomj['Res'],atomj['Posicao'],' Cadeia',atomj['Cadeia'] ,'distancia',dist/1000,file=F)
	return

def model(PDB):
	F = open(PDB)
	ATOM_PDB=[]
	model={}
	m = 0
	for i in F:
		i= i.strip()

		if i.startswith("MODEL"):
			ATOM_PDB=[]
		elif i.startswith("ATOM"):
			ATOM_PDB.append(i)
		elif i.startswith("ENDMDL"):
			m +=1
			model[m]=ATOM_PDB
		elif i.startswith("TER"):
			m +=1
			model[m]=ATOM_PDB
			ATOM_PDB=[]
	F.close()
	return model


def nCr(n,k):
	f = math.factorial
	C = f(n)/(f(k)*f(n-k))
	return C

def vecdist(A,B):
	Dist = math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2 + (A[2]-B[2])**2)
	return round(Dist,3)

def del_and_compare(num,dicmol,ASU):
    L=[]
    DelDic ={}
    NovoDic = {}
    os.mkdir("Del"+str(num))
    for i in range(len(dicmol)):
	       L.append(i+1)
    Dicionario = open("Dicionario.txt",'w')
    for i in dicmol:
        if len(dicmol[i])==0:
            continue
        else:
            print (dicmol[i], file=Dicionario)
    Dicionario.close()
    for cnj in list(itertools.combinations(L,num)):
        if list(cnj)[0]<=ASU:
            Ficheiro = open("Estrutura" + str(cnj)+".pdb",'w')
            Novo = open("Dicionario.txt",'r')
            Novo = Novo.readlines()
            for line in range(len(Novo)):
                x = Novo[line].strip('[]')
                x = x.split(',')
                NovoDic[line+1]=x
            for i in list(cnj):
                NovoDic.pop(i)
            for line in sorted(NovoDic.keys()):
                print("MODEL", str(line),sep="\t", file=Ficheiro)
                for i in NovoDic[line]:
                    i = i.strip("'] ")
                    i = i.strip()
                    j=i
                    if i[-1]==']':
                        print(i[:-2],file=Ficheiro)
                    else:
                        print (i , file = Ficheiro)
                j=j.split()
                print("TER","  ",int(j[1])+1,"    ",j[3]+" "+j[4]+" "+j[5], file = Ficheiro)
                print("ENDMDL", file = Ficheiro)
            Ficheiro.close()
            V = compare("Estrutura"+str(cnj)+".pdb","Del"+str(num))
            if V == 0:
                os.remove("Estrutura" + str(cnj)+".pdb")
            elif V == 1:
                os.rename("Estrutura" + str(cnj)+".pdb","Del"+str(num)+"/Estrutura " + str(cnj)+".pdb")
    os.remove('Dicionario.txt')
    return




from numpy import *
from math import sqrt

def rigid_transform_3D(A, B):
    try:
        assert len(A) == len(B)
    except:
        return

    A = matrix(A)
    B = matrix(B)
    N = A.shape[0]; # total points

    centroid_A = mean(A, axis=0)
    centroid_B = mean(B, axis=0)

    # centre the points
    AA = A - tile(centroid_A, (N, 1))
    BB = B - tile(centroid_B, (N, 1))

    # dot is matrix multiplication for array
    H = transpose(AA) * BB

    U, S, Vt = linalg.svd(H)

    R = Vt.T * U.T

    # special reflection case
    if linalg.det(R) < 0:
       print ("Reflection detected")
       Vt[2,:] *= -1
       R = Vt.T * U.T

    t = -R*centroid_A.T + centroid_B.T

    return R, t

def rotate_and_translate(moving,fixed,it):
    i=0
    rmse1 = 0
    rmse2 = 0
    moving = matrix(moving)
    fixed = matrix(fixed)
    while i<it:
        n = moving.shape[0]

        reflecmatrix,translatematrix = rigid_transform_3D(moving,fixed)

        rotatedpoints = (reflecmatrix*moving.T) + tile(translatematrix, (1, n))
        rotatedpoints = rotatedpoints.T

        # Find the error
        err = rotatedpoints - fixed

        err = multiply(err, err)
        err = sum(err)
        rmse2 = sqrt(err/n);

        if rmse2 - rmse1 < 1e-10:
            break
        rmse1 = rmse2
        i +=1
        moving = rotatedpoints
    return rmse2

from Bio.SVDSuperimposer import SVDSuperimposer
sup = SVDSuperimposer()

def compare(ficheiro,pasta):
    f1 = parse_PDB(ficheiro)
    listatoms1 =[]
    for atom in f1.get_atoms():
        if atom.name=='CA':
            listatoms1.append(atom.coord)
    arrayatoms1 = asarray(listatoms1)
    for F in os.listdir(pasta):
        f2 = parse_PDB(pasta+'/'+F)
        listatoms2 = []
        for atom in f2.get_atoms():
            if atom.name=='CA':
                listatoms2.append(atom.coord)
        arrayatoms2 = asarray(listatoms2)
        try:
            erro = rotate_and_translate(arrayatoms1,arrayatoms2,100)
        except:
            continue
        if erro < 3:
            return 0

    return 1



def calc_residue_dist(residue_one, residue_two) :
    """Returns the C-alpha distance between two residues"""
    diff_vector  = residue_one["CA"].coord - residue_two["CA"].coord
    return numpy.sqrt(numpy.sum(diff_vector * diff_vector))

def calc_dist_matrix(chain_one, chain_two) :
    """Returns a matrix of C-alpha distances between two chains"""
    answer = numpy.zeros((len(chain_one), len(chain_two)), numpy.float)
    for row, residue_one in enumerate(chain_one) :
        for col, residue_two in enumerate(chain_two) :
            answer[row, col] = calc_residue_dist(residue_one, residue_two)
    return answer

from Bio.PDB.PDBParser import PDBParser

def parse_PDB(fich):
    parser = PDBParser()
    structure = parser.get_structure(fich[:-4],fich)
    return structure

hydrophobe = ['ALA','VAL','LEU','ILE','MET','PHE','TYR','TRP']
acidic = ['ASP','GLU']
basic = ['ARG','LYS']
donor = ['ARG','ASN','CYS','GLN','HIS','LYS','SER','THR','TRP','TYR']
donoratom = ['NE','NH1','NH2','ND2','SG','NE2','ND1','NZ','OG','OG1','NE1','OH']
acceptor = ['ASN','ASP','GLN','GLU','HIS','SD','SER','THR','TYR']
acceptoratom = ['OD1','OD2','OE1','OE2','ND1','NE2','SD','OG','OG1','OH']

def calculate_number_bonds(structure):
    saltbridges=0
    hydrop = 0
    hbonds = 0
    dicionario = {}
    listamodelos = itertools.combinations(range(len(structure)),2)
    for (model1,model2) in listamodelos:
        print(model1+1,model2+1)
        for res1 in structure[model1].get_residues():
            for res2 in structure[model2].get_residues():
                if res1.resname in acidic and res2.resname in basic:
                    for atom1 in res1:
                        for atom2 in res2:
                            if atom1.name=='CB' and atom2.name=='CB':
                                dist = vecdist(atom1.coord, atom2.coord)
                                if dist <=14.0:
                                    try:
                                        acid = res1['OE1']
                                    except:
                                        try:
                                            acid = res1['OE2']
                                        except:
                                            try:
                                                acid = res1['OD1']
                                            except:
                                                acid = res1['OD2']
                                    try:
                                        base = res2['NZ']
                                    except:
                                        try:
                                            base = res2['NH1']
                                        except:
                                            base = res2['NH2']
                                    distancia = vecdist(acid.coord,base.coord)
                                    if distancia <=4.0:
                                        saltbridges+=1
                if res1.resname in hydrophobe and res2.resname in hydrophobe:
                    dist = vecdist(res1['CB'].coord, res2['CB'].coord)
                    if dist <=7.0:
                        hydrop += 1
                if res1.resname in donor and res2.resname in acceptor:
                    for atom1 in res1:
                        for atom2 in res2:
                            if atom1.name in donoratom and atom2.name in acceptoratom:
                                distanc= vecdist(atom1.coord, atom2.coord)
                                if distanc <=4.0:
                                    hbonds +=1
        dicionario[(model1+1,model2+1)]=(saltbridges,hydrop,hbonds)
        saltbridges=0
        hydrop = 0
        hbonds = 0
    return dicionario


def SASA(ficheiro):
	output = os.popen("freesasa -m -S -n 10000 -t 8 '"+str(ficheiro)+"'")
	return output
