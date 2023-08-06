
import os
import symbolx as syx
from symbolx import DataCollection, SymbolsHandler, Symbol

print("Test 1")
folder = "csv_0"
syx.compress_subdirs(folder=folder, zip_extension='7z', delete=False)
# syx.unzip_all(folder=folder, zip_extension='7z', delete=False)
DC = DataCollection()
DC.add_collector(collector_name='csv_collector', parser=syx.symbol_parser_csv, loader=syx.load_csv)
DC.add_folder('csv_collector', folder)
DC.add_custom_attr(collector_name='csv_collector', keep_zeros=False)
DC.adquire(id_integer=False, zip_extension='7z')
# DC.adquire(id_integer=False, zip_extension=None)
SH = SymbolsHandler(method='object', obj=DC)

var1 = Symbol(name='VAR1', symbol_handler=SH)
var2 = Symbol(name='VAR2', symbol_handler=SH)
var3 = Symbol(name='VAR3', symbol_handler=SH)

print(var1.dfc)
print(var2.dfc)
print(var3.dfc)

var1*var3
var2*var3

print("Test 2")
folder = "csv_1"
syx.compress_subdirs(folder=folder, zip_extension='7z', delete=False)
# syx.unzip_all(folder=folder, zip_extension='7z', delete=False)
DC = DataCollection()
DC.add_collector(collector_name='csv_collector', parser=syx.symbol_parser_csv, loader=syx.load_csv)
DC.add_folder('csv_collector', folder)
DC.add_custom_attr(collector_name='csv_collector', keep_zeros=False)
# DC.adquire(id_integer=False, zip_extension='7z')
DC.adquire(id_integer=False, zip_extension=None)
SH = SymbolsHandler(method='object', obj=DC)

var1 = Symbol(name='VAR1', symbol_handler=SH)
var2 = Symbol(name='VAR2', symbol_handler=SH)
var3 = Symbol(name='VAR3', symbol_handler=SH)

var1*var3
var2*var3

print("Test 3")
folder = "feather_0"
syx.compress_subdirs(folder=folder, zip_extension='7z', delete=False)
# syx.unzip_all(folder=folder, zip_extension='7z', delete=False)
DC = DataCollection()
DC.add_collector(collector_name='feather_collector', parser=syx.symbol_parser_feather, loader=syx.load_feather)
DC.add_folder('feather_collector', folder)
DC.add_custom_attr(collector_name='feather_collector', keep_zeros=False)
# DC.adquire(id_integer=False, zip_extension='7z')
DC.adquire(id_integer=False, zip_extension=None)
SH = SymbolsHandler(method='object', obj=DC)

EnergyBalance = Symbol(name='EnergyBalance', value_type='m', symbol_handler=SH)

# print(EnergyBalance.array.long.index)
# print(EnergyBalance.array.long.value)
# print(EnergyBalance.array.coords)
# print(EnergyBalance.metadata)


print("Test 4")
folder = "gdx_0"
syx.compress_subdirs(folder=folder, zip_extension='7z', delete=False)
# syx.unzip_all(folder=folder, zip_extension='7z', delete=False)
DC = DataCollection()
DC.add_collector(collector_name='gdx_collector', parser=syx.symbol_parser_gdx, loader=syx.load_gdx)
DC.add_folder('gdx_collector', folder)
DC.add_custom_attr(collector_name='gdx_collector', 
                    inf_to_zero=True, 
                    verbose=False, 
                    keep_zeros=False)
# DC.adquire(id_integer=True, gams_dir=os.getenv("GAMS_DIR"), zip_extension='7z')
DC.adquire(id_integer=False, gams_dir=os.getenv("GAMS_DIR"), zip_extension=None)
SH = SymbolsHandler(method='object', obj=DC)


G_L = Symbol(name='G_L', symbol_handler=SH)

# print(G_L.metadata)
print(G_L.dfm)