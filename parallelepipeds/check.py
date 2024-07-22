import json
from math import *
from time import sleep


#Чтение исходного файла parallelepipeds.json
with open("parallelepipeds.json",'r') as f:
	data = json.load(f)

def diag_f(a,b,c):
	return sqrt(a**2+b**2+c**2)
def volume_f(a,b,c):
	return a*b*c
def surface_area_f(a,b,c):
	return 2*(a*b+a*c+b*c)
def alpha_f(a,d):
	return degrees(acos(a/d))

def beta_f(b,d):
	return degrees(acos(b/d))

def gamma_f(c,d):
	return degrees(acos(c/d))

def radius_described_sphere_f(d):
	return d/2

def volume_described_sphere_f(r):
	return 4/3*pi*pow(r,3)


characteristics={}
for figure,sides in data.items():
	a=float(sides["a"])
	b=float(sides["b"])
	c=float(sides["c"])
	diag=diag_f(a,b,c)
	volume=volume_f(a,b,c)
	surface_area=surface_area_f(a,b,c)
	alpha=alpha_f(a,diag)
	beta=beta_f(b,diag)
	gamma_=gamma_f(c,diag) 
	radius_described_sphere=radius_described_sphere_f(diag)
	volume_described_sphere=volume_described_sphere_f(radius_described_sphere)
	characteristics[figure]={
	"diag":str(diag),
	"volume":str(volume),
	"surface_area":str(surface_area),
	"alpha":str(alpha),
	"beta":str(beta),
	"gamma":str(gamma_),
	"radius_described_sphere":str(radius_described_sphere),
	"volume_described_sphere":str(volume_described_sphere)}

statistics={
	"avg_diag":str(sum([float(i['diag']) for i in characteristics.values()])/len(characteristics)),
    "avg_volume":str(sum([float(i['volume']) for i in characteristics.values()])/len(characteristics)),
    "avg_surface_area":str(sum([float(i['surface_area']) for i in characteristics.values()])/len(characteristics)),
	"avg_alpha":str(sum([float(i['alpha']) for i in characteristics.values()])/len(characteristics)),
	"avg_beta":str(sum([float(i['beta']) for i in characteristics.values()])/len(characteristics)),
	"avg_gamma":str(sum([float(i['gamma']) for i in characteristics.values()])/len(characteristics)),
	"avg_radius_described_sphere":str(sum([float(i['radius_described_sphere']) for i in characteristics.values()])/len(characteristics)),
	"avg_volume_described_sphere":str(sum([float(i['volume_described_sphere']) for i in characteristics.values()])/len(characteristics))}


with open("characteristics.json", 'r') as file:
    characteristics_example=json.load(file)
with open("statistics.json", 'r') as file:
    statistics_example=json.load(file)	

if(characteristics_example==characteristics ):
	print("Файл characteristics.json записан правильно")
if(statistics_example==statistics ):
	print("Файл statistics.json записан правильно")
try:
    with open("characteristics.json", 'r') as file:
        characteristics_example = json.load(file)
    with open("statistics.json", 'r') as file:
        statistics_example = json.load(file)
except json.JSONDecodeError as e:
    print(f"Error loading JSON file: {e}")
