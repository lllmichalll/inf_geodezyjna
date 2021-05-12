


import geopandas
import numpy as np
import matplotlib.pyplot as plt

 

gdf = geopandas.read_file('PD_STAT_GRID_CELL_2011.shp') 
gdf = gdf.to_crs('EPSG:4326')
gdf.plot('TOT', legend = True)
gdf['centroid'] = gdf.centroid
 
# %%

 

import shapely
#
xmin, ymin, xmax, ymax = [13, 48, 25, 56]
#
n_cells = 30
cell_size = (xmax - xmin)/n_cells
#
grid_cells = []

 

# %%

 

for x0 in np.arange(xmin, xmax + cell_size, cell_size):
    for y0 in np.arange(ymin, ymax + cell_size, cell_size):
        # bounds
        x1 = x0 - cell_size
        y1 = y0 + cell_size
        grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))
cell = geopandas.GeoDataFrame(grid_cells, columns = ['geometry'])

 

# %%

 

ax = gdf.plot(markersize = .1, figsize = (12, 8), column = 'TOT', cmap = 'jet')

 

plt.autoscale(False)
cell.plot(ax = ax, facecolor = 'none', edgecolor = 'grey')
ax.axis('off')

 

# %%

 

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

