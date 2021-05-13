


import geopandas
import numpy as np
import matplotlib.pyplot as plt

gdf = geopandas.read_file('PD_STAT_GRID_CELL_2011.shp') 
gdf = gdf.to_crs('EPSG:4326')
gdf.plot('TOT', legend = True)
gdf['centroid'] = gdf.centroid

import shapely
#
xmin, ymin, xmax, ymax = [13, 48, 25, 56]
#
n_cells = 30
cell_size = (xmax - xmin)/n_cells
#
grid_cells = []

for x0 in np.arange(xmin, xmax + cell_size, cell_size):
    for y0 in np.arange(ymin, ymax + cell_size, cell_size):
        # bounds
        x1 = x0 - cell_size
        y1 = y0 + cell_size
        grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))
cell = geopandas.GeoDataFrame(grid_cells, columns = ['geometry'])
 
ax = gdf.plot(markersize = .1, figsize = (12, 8), column = 'TOT', cmap = 'jet')

 

plt.autoscale(False)
cell.plot(ax = ax, facecolor = 'none', edgecolor = 'grey')
ax.axis('off')

merged = geopandas.sjoin(gdf, cell, how = 'left', op = 'within')
dissolve = merged.dissolve(by = 'index_right', aggfunc = 'sum')
cell.loc[dissolve.index, 'TOT'] = dissolve.TOT.values

ax = cell.plot(column = 'TOT', figsize = (12, 8), cmap = 'viridis', vmax = 700000, edgecolor = 'grey', legend = True)
plt.autoscale(False)
ax.set_axis_off()
plt.axis('equal')
plt.title('liczba ludnosci w siatce')
w_0_14 = sum(gdf.MALE_0_14) + sum(gdf.FEM_0_14)
w_15_64 = sum(gdf.MALE_15_64) + sum(gdf.FEM_15_64)
w_65__ = sum(gdf.MALE_65__) + sum(gdf.FEM_65__)
print('Przedział wiekowy 0-14', w_0_14)
print('Przedział wiekowy 15-64', w_15_64)
print('Przedział wiekowy >65', w_65__)
suma_men = sum(gdf.MALE_0_14) + sum(gdf.MALE_15_64) + sum(gdf.MALE_65__)
print('Ludność męska w przedziałach wiekowych z podpunktów a-c',  suma_men)
suma_fem = sum(gdf.FEM_0_14) + sum(gdf.FEM_15_64) + sum(gdf.FEM_65__)
print('Ludność żeńska w przedziałach wiekowych z podpunktów a-c',  suma_fem)
ludn = w_0_14 + w_15_64 + w_65__
print('Liczba ludnosci Polski:', ludn)

gdf2 = geopandas.read_file('woj')

slaskie = (gdf2.area[0]) / 1000000
opolskie = (gdf2.area[1])/1000000
swietokrzyskie = (gdf2.area[2])/1000000
pomorskie = (gdf2.area[3])/1000000
podlaskie = (gdf2.area[4])/1000000
zachodniopomorskie = (gdf2.area[5])/1000000
dolnoslaskie = (gdf2.area[6])/1000000
wielkopolskie = (gdf2.area[7])/1000000
podkarpackie = (gdf2.area[8])/1000000
malopolskie = (gdf2.area[9])/1000000
warminsko_mazurskie = (gdf2.area[10])/1000000
lodzkie = (gdf2.area[11])/1000000
mazowieckie = (gdf2.area[12])/1000000
kujawsko_pomorskie = (gdf2.area[13])/1000000
lubelskie = (gdf2.area[14])/1000000
lubuskie = (gdf2.area[15])/1000000

f = [ludn/slaskie,
     ludn/opolskie,
     ludn/swietokrzyskie,
     ludn/pomorskie,
     ludn/podlaskie,
     ludn/zachodniopomorskie,
     ludn/dolnoslaskie,
     ludn/wielkopolskie,
     ludn/podkarpackie,
     ludn/malopolskie,
     ludn/warminsko_mazurskie,
     ludn/lodzkie,
     ludn/mazowieckie,
     ludn/kujawsko_pomorskie,
     ludn/lubelskie,
     ludn/lubuskie]

print('Ratio liczby ludności do powierzchni dla województwa:')
print('śląskiego:', int(f[0]))
print('opolskiego:', int(f[1]))
print('świętokrzyskiego:', int(f[2]))
print('pomorskiego:', int(f[3]))
print('podlaskiego:', int(f[4]))
print('zachodniopomorsiego:', int(f[5]))
print('dolnośląskiego:', int(f[6]))
print('wielkopolskiego:', int(f[7]))
print('podkarpackiego:', int(f[8]))
print('małopolskiego:', int(f[9]))
print('warmińsko-mazurskiego:', int(f[10]))
print('Łódzkiego:', int(f[11]))
print('mazowieckiego:', int(f[12]))
print('kujawsko pomorskiego:', int(f[13]))
print('lubelskiego:', int(f[14]))
print('lubuskiego:', int(f[15]))
