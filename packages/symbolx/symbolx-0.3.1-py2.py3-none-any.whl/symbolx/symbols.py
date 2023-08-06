import os
import glob
import uuid
import itertools
import numpy as np
import karray as ka
import json
from json import JSONDecodeError
from typing import Union, List, Dict
from .handler import DataCollection
from .settings import settings, allowed_string, value_type_name_map


class SymbolsHandler:
    def __init__(self, method:str, folder_path:str=None, obj:DataCollection=None):
        ''' 
        method: "folder" or "object"
        kwargs:
            folder_path: path to folder with symbol files
            object: DataCollection object
        '''
        assert isinstance(method, str), "Arg 'method' must be a string."
        assert method in ["folder", "object"], "Arg 'method' must be either 'folder' or 'object'"
        self.method = method
        self.folder_path = None
        self.symbols_book = None
        self.symbol_handler_token = str(uuid.uuid4()) # TODO: this can be changed by hashing the input file
        self.saved_symbols = {}
        self.token_info = None
        self.input_method(method=method, folder_path=folder_path, obj=obj)

    def input_method(self, method:str, **kwargs):
        if method == "object":
            self.from_object(obj=kwargs['obj'])
        elif method == "folder":
            self.from_folder(folder_path=kwargs['folder_path'])
        else:
            raise Exception('A method mus be provided from either "object" or "folder"')

    def from_object(self, obj:DataCollection):
        self.symbols_book = obj.symbols_book
        self.collector = obj.collector
        self.short_names = obj.short_names
        for n_v in self.symbols_book:
            settings.append((*n_v,self.symbol_handler_token))


    def from_folder(self, folder_path:str=None):
        self.token_info = {}
        self.folder_path = folder_path
        files = glob.glob(os.path.join(self.folder_path, "*.feather"))
        self.symbols_book = {}
        for file in files:
            loaded_file_dict = from_feather_info(file)
            self.symbols_book[(loaded_file_dict['name'],loaded_file_dict['value_type'])] = file

            token = loaded_file_dict['symbol_handler_token']
            settings.append((loaded_file_dict['name'],loaded_file_dict['value_type'],loaded_file_dict['symbol_handler_token']))

            if token not in self.token_info:
                self.token_info[token] = {}
            self.token_info[token][(loaded_file_dict['name'],loaded_file_dict['value_type'])] = file
        if len(self.token_info) > 1:
            print(f"There are Symbols' files with different symbol_handler_token in {folder_path}")
            print("       Symbol's scenario short names or id's might be in conflict.")
            print("       Make sure all Symbols are from the same symbol_handler_token")
            print("       Otherwise, it may happen, for example, different scenarios have the same id.")
            print("       See 'token_info' attribute of SymbolsHandler for more information")


    def append(self, **kwargs):
        for name in kwargs:
            symbol = kwargs[name]
            assert len(set(name).difference(set(allowed_string))) == 0, f"Symbol name '{name}' contains special characters. Please, change the name of the symbol. Allowed chars are: {allowed_string}"
            symbol.name = name
            self.saved_symbols[(name, symbol.value_type)] = symbol

    def save(self, folder_path=None, appended_or_all:str='all', gls=None, overwrite:bool=False):
        files = glob.glob(os.path.join(folder_path,'*.feather'))
        existing_pairs = {}
        print("Checking folder for duplicate symbol names...")
        for ff in files:
            file = os.path.basename(ff)
            name_sections = file.split('.')
            name = name_sections[0]
            value_type = name_sections[1]
            token = name_sections[2]
            assert (name,value_type) not in existing_pairs, f"Only one symbol name {name}.{value_type} should be found in '{folder_path}' folder. Two or more found\nTokens: {existing_pairs[(name,value_type)]} and {token}"
            existing_pairs[(name,value_type)] = token
        print("Checking passed")
        if folder_path is None:
            assert self.folder_path is not None, "folder_path must be provided"
            folder_path = self.folder_path
        os.makedirs(folder_path, exist_ok=True)
        if appended_or_all == 'all':
            symbol_map = []
            assert gls is not None, "if 'appended_or_all' is 'all' then provide gls=globals() to able to capture all variables that are Symbol instances"
            for name, symbol in gls.items():
                if isinstance(symbol, Symbol):
                    symbol.name = name
                    symbol_map.append(symbol)
        elif appended_or_all == 'appended':
            symbol_map = list(self.saved_symbols.values())
        else:
            raise Exception(f"Function argument 'appended_or_all' must be 'appended' or 'all'. Given: {appended_or_all}")

        for symbol in symbol_map:
            if not overwrite:
                assert (symbol.name,symbol.value_type) not in existing_pairs, f"Only one symbol name {symbol.name}.{symbol.value_type} should be saved in '{folder_path}' folder. Existing file found:\n{symbol.name}.{symbol.value_type}.{existing_pairs[(symbol.name,symbol.value_type)]}.feather"
            file_name = f"{symbol.name}.{symbol.value_type}.{symbol.symbol_handler_token}.feather"
            file_path = os.path.join(folder_path,file_name)
            symbol.to_feather(file_path)

    def get_info(self, symbol_name, value_type):
        assert (symbol_name, value_type) in self.symbols_book, f"Pairs {(symbol_name, value_type)} not present in the symbols_book attribute of SymbolsHandler"
        if isinstance(self.symbols_book[(symbol_name, value_type)], dict):
            return self.symbols_book[(symbol_name, value_type)]
        elif isinstance(self.symbols_book[(symbol_name, value_type)], str):
            return self.symbols_book[(symbol_name, value_type)]

    def __repr__(self):
        return f'''SymbolsHandler(method='{self.method}')'''

def from_feather_dict(path, use_threads=True, with_="polars"):
    import pyarrow.feather as ft
    arr = ka.from_feather(path, use_threads=use_threads, with_=with_)
    restored_table = ft.read_table(path, use_threads=use_threads)
    custom_meta_key = 'symbolx'
    restored_meta_json = restored_table.schema.metadata[custom_meta_key.encode()]
    restored_meta = recurse(restored_meta_json)
    return dict(array=arr,**restored_meta)

def from_feather_info(path):
    import pyarrow.feather as ft
    restored_table = ft.read_table(path)
    custom_meta_key = 'symbolx'
    restored_meta_json = restored_table.schema.metadata[custom_meta_key.encode()]
    restored_meta = json.loads(restored_meta_json)
    return dict(name=restored_meta['name'], value_type=restored_meta['value_type'], symbol_handler_token=restored_meta['symbol_handler_token'])

def recurse(d):
    if isinstance(d, dict):
        loaded_d = d
    elif isinstance(d, bytes):
        loaded_d = json.loads(d)
    else:
        return d
    new_dc = {}
    for k, v in loaded_d.items():
        if k.isdigit():
            r = int(k)
        else:
            r = k
        new_dc[r] = recurse(v)
    return new_dc

def build_array(symbol_name:str, value_type:str, symbol_handler:SymbolsHandler):
    """
    Create an array of all existing scenarios
    """
    list_of_arrays = []
    for scenario_id in symbol_handler.get_info(symbol_name, value_type)['scenario_data']:
        array_with_id = insert_id_dim(symbol_name, value_type, scenario_id, symbol_handler)
        list_of_arrays.append(array_with_id)
    return ka.concat(list_of_arrays)

def insert_id_dim(symbol_name:str, value_type:str, scenario_id:str, symbol_handler:SymbolsHandler):
    """
    Insert dimension id with the corresponding scenario_id.
    """
    single_symbol = symbol_handler.get_info(symbol_name, value_type)['scenario_data'][scenario_id]
    single_array_dict = symbol_handler.collector[single_symbol['collector']]['loader'](**single_symbol)
    oarray = ka.Array(**single_array_dict)
    narray = oarray.add_dim(id=symbol_handler.short_names[scenario_id])
    return narray


class Symbol:
    def __init__(
        self,
        name: str=                      None,
        value_type: str=                'v',
        metadata: dict=                 None,
        array: ka.Array=                None,
        symbol_handler_token: str=      None,
        symbol_handler: SymbolsHandler= None,
        ):
        '''
        A class for creating symbols.
        '''
        self.__dict__["_repo"] = {}
        if symbol_handler is not None:
            if 'object' == symbol_handler.method:
                self.build(symbol_handler, name, value_type)
            elif 'folder' == symbol_handler.method:
                self.load(symbol_handler, name, value_type)
        else:
            if settings.exists((name,value_type,symbol_handler_token)):
                print("The symbol name has already been taken by another Symbol stored in SymbolsHandler.")
                print("Please choose another name to avoid overwriting the existing symbol when saving the current symbol.")
            self.name=                 name
            self.value_type=           value_type
            self.metadata=             metadata
            self.array=                array
            self.symbol_handler_token= symbol_handler_token
        self.check_input()
        # optional attributes
        self.dataframe = None


    def __setattr__(self, name, value):
        self._repo[name] = value

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name) # ipython requirement for repr_html
        if name == "dataframe":
            if name in self._repo:
                if self._repo[name] is None:
                    self._repo[name] = self.array.to_pandas()
                    return self._repo[name].copy()
                else:
                    #Sanity check
                    df = self._repo[name]
                    dense = df.value.values.reshape(self.array.shape)
                    if np.allclose(dense, self.array.dense):
                        return df.copy()
                    else:
                        print(f"Getting dataframe again...")
                        self._repo[name] = self.array.to_pandas()
                        return self._repo[name].copy()
            else:
                self.definition_msg(name) # dev msg
        else:
            return self._repo[name]

    def build(self, symbol_handler:SymbolsHandler, name: str=None, value_type: str=None):
        assert isinstance(symbol_handler, SymbolsHandler), "'symbol_handler' must be a SymbolsHandler object"
        assert isinstance(name, str), "'name' must be a string"
        assert isinstance(value_type, str), "'value_type' must be a string"
        print(f"{name:<25} value_type: {value_type_name_map[value_type]} ({value_type})")

        key = (name,value_type)
        assert key in symbol_handler.symbols_book, f"'{key}' is not present in 'symbol_handler.symbols_book' dictionary"

        self.name=                 name
        self.value_type=           value_type
        self.metadata=             symbol_handler.get_info(*key)['metadata']
        self.array=                build_array(name, value_type, symbol_handler)
        self.symbol_handler_token= symbol_handler.symbol_handler_token
        
    def load(self, symbol_handler:SymbolsHandler, name: str=None, value_type: str=None):
        assert isinstance(symbol_handler, SymbolsHandler), "'symbol_handler' must be a SymbolsHandler object"
        assert isinstance(name, str), "'name' must be a string"
        assert isinstance(value_type, str), "'value_type' must be a string"
        print(f"{name:<25} value_type: {value_type_name_map[value_type]} ({value_type})")

        key = (name,value_type)
        assert key in symbol_handler.symbols_book, f"'{key}' is not present in 'symbol_handler.symbols_book' dictionary"

        file_path = symbol_handler.get_info(*key)
        symbol_dict = from_feather_dict(file_path, with_=ka.settings.feather_with)
        self.name=                 name
        self.value_type=           value_type
        self.metadata=             symbol_dict['metadata']
        self.array=                symbol_dict['array']
        self.symbol_handler_token= symbol_dict['symbol_handler_token']

    def to_arrow(self):
        table = self.array.to_arrow()
        existing_meta = table.schema.metadata
        custom_meta_key = 'symbolx'
        custom_metadata = {}
        attr = ['name', 'value_type', 'metadata','symbol_handler_token']
        for k,v in self._repo.items():
            if k in attr:
                custom_metadata[k] = v

        custom_meta_json = json.dumps(custom_metadata)
        existing_meta = table.schema.metadata
        combined_meta = {custom_meta_key.encode() : custom_meta_json.encode(),**existing_meta}
        table = table.replace_schema_metadata(combined_meta)
        return table

    def to_feather(self, path:str):
        import pyarrow.feather as ft
        sets = set(allowed_string)
        sets.add(os.path.sep)
        joint = ''.join(sorted(sets))
        assert len(set(path).difference(sets)) == 0, f"There are/is special characters in path '{path}'. Allowed chars are: {joint}"

        table = self.to_arrow()
        ft.write_feather(table, path)
        print(f"{path}")
        return None

    def check_input(self):
        assert self.name is not None and isinstance(self.name, str), "Name of symbol must be provided."
        assert self.value_type is not None and isinstance(self.value_type, str), "Value type of symbol must be provided."
        assert self.metadata is not None and isinstance(self.metadata, dict), "metadata of symbol must be provided."
        assert self.array is not None and isinstance(self.array, ka.Array), "Array must be provided."
        assert self.symbol_handler_token is not None and isinstance(self.symbol_handler_token, str), "Symbol handler token must be provided."

    @property
    def dims(self):
        return self.array.dims

    @property
    def df(self):
        return self.dataframe.set_index(self.array.dims)

    @property
    def dfm(self):
        dfm = self.dataframe
        for k, v in self.metadata.items():
            dfm[k] = dfm["id"].map(v)
        return dfm

    @property
    def dfc(self):
        dfc = self.dataframe
        for k, v in self.metadata.items():
            if 'custom_' in k:
                dfc[k] = dfc["id"].map(v)
        return dfc
    
    def to_polars(self):
        return self.array.to_polars()

    def to_pandas(self):
        return self.array.to_pandas()

    def metadata_union(self, other=None):
        self_metadata = self.metadata
        other_metadata = other.metadata
        new_metadata = {}
        for elem in self_metadata.keys():
            new_metadata[elem] = {**self_metadata[elem],**other_metadata[elem]}
        return new_metadata

    def new_symbol(self, array, new_name, other=None):
        if isinstance(other, Symbol):
            assert self.symbol_handler_token == other.symbol_handler_token, "Symbol handler tokens must be the same"
            new_metadata = self.metadata_union(other)
        elif other is None or isinstance(other,(int,float)):
            new_metadata = self.metadata
        else:
            raise Exception(f'other must be either a Symbol object, int, float or None, but it is: {str(type(other))}')
        new_object = Symbol(name=new_name, value_type='v',
                            metadata=new_metadata, array=array, 
                            symbol_handler_token=self.symbol_handler_token)
        return new_object

    def __add__(self, other):
        flag = False
        if isinstance(other, (int, float)):
            new_array = self.array + other
            new_name =  f"({self.name})+{str(other)}"
            return self.new_symbol(new_array, new_name, other)
        elif isinstance(other, Symbol):
            new_array = self.array + other.array
            new_name = f"({self.name})+({other.name})"
            return self.new_symbol(new_array, new_name, other)
        else:
            raise Exception(f'{type(other)} is not supported')

    def __sub__(self, other):
        flag = False
        if isinstance(other, (int, float)):
            new_array = self.array - other
            new_name =  f"({self.name})-{str(other)}"
            return self.new_symbol(new_array, new_name, other)
        elif isinstance(other, Symbol):
            new_array = self.array - other.array
            new_name = f"({self.name})-({other.name})"
            return self.new_symbol(new_array, new_name, other)
        else:
            raise Exception(f'{type(other)} is not supported')

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            new_array = self.array * other
            new_name = f"({self.name})*{str(other)}"
            return self.new_symbol(new_array, new_name, other)
        elif isinstance(other, Symbol):
            diffdims = list(set(self.dims).symmetric_difference(other.dims))
            lendiff = len(diffdims)
            if set(self.dims) == set(other.dims):
                new_array = self.array * other.array
                new_name = f"({self.name})*({other.name})"
                return self.new_symbol(new_array, new_name, other)
            elif lendiff == 1:
                new_array = self.array * other.array
                new_name = f"({self.name})*({other.name})"
                return self.new_symbol(new_array, new_name, other)
            elif lendiff > 1:
                common_dims = list(set(self.dims).intersection(other.dims))
                if len(common_dims) > 0:
                    new_array = self.array * other.array
                    new_name = f"({self.name})*({other.name})"
                    return self.new_symbol(new_array, new_name, other)
                else:
                    raise Exception(f"The difference in dimensions is greater than one: '{diffdims}' and has no common dimensions")
        else:
            raise Exception(f'{type(other)} is not supported')

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            new_array = self.array / other
            new_name = f"({self.name})/{str(other)}"
            return self.new_symbol(new_array, new_name, other)
        elif isinstance(other, object):
            diffdims = set(self.dims).symmetric_difference(other.dims)
            lendiff = len(diffdims)
            if set(self.dims) == set(other.dims):
                new_array = self.array / other.array
                new_name = f"({self.name})/({other.name})"
                return self.new_symbol(new_array, new_name, other)
            elif lendiff == 1:
                new_array = self.array / other.array
                new_name = f"({self.name})/({other.name})"
                return self.new_symbol(new_array, new_name, other)

            elif lendiff > 1:
                raise Exception(f"The difference in dimensions is greater than one: '{diffdims}'")
        else:
            raise Exception("The second term is not known, must be a int, float or a Symbol object")

    def __radd__(self, other):
        if isinstance(other, (int, float)):
            new_array =  other + self.array
            new_name = f"{str(other)}+({self.name})"
            return self.new_symbol(new_array, new_name, other)

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            new_array = other - self.array
            new_name = f"{str(other)}-({self.name})"
            return self.new_symbol(new_array, new_name, other)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            new_array = other*self.array
            new_name = f"{str(other)}*({self.name})"
            return self.new_symbol(new_array, new_name, other)

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            new_array = other/self.array
            new_name = f"{str(other)}/({self.name})"
            return self.new_symbol(new_array, new_name, other)

    def rename(self, new_name: str):
        return self.new_symbol(self.array, new_name)

    def dimreduc(self, dim:str='h', aggfunc=np.add.reduce):
        '''
        aggfunc in [np.add.reduce,np.multiply.reduce,np.average]. defult np.add.reduce
        '''
        new_array = self.array.reduce(dim, aggfunc)
        new_name = f"({self.name}).dimreduc({dim},{aggfunc})"
        return self.new_symbol(new_array, new_name)

    @property
    def items(self):
        return self.array.coords

    def rename_dim(self, **kwargs):
        """ This function renames a dimension in a symbol.

        Args:
            old_dim (str): dimension to be renamed
            new_dim (str): new dimension name

        Returns:
            symbol: Returns a new symbol with the renamed dimension.
        """
        new_array = self.array.rename(**kwargs)
        new_name = f"({self.name}).rename_dim(**{kwargs})"
        return self.new_symbol(new_array, new_name)
        
    def add_dim(self, dim_name: str, value: Union[str,int,dict]):
        '''
        dim_name: new dimension name
        value:  if value is a string, the dimension column will contain this value only.
                if value is a dict, the dict must look like {column_header:{column_element: new_element_name}}
                where column_header must currently exists and all column_elements must have a new_element_name.
        '''
        if isinstance(value, (str,int)):
            new_array = self.array.add_dim(**{dim_name:value})
            new_name = f"({self.name}).add_dim({dim_name},{value})"
            return self.new_symbol(new_array, new_name)

        elif isinstance(value, dict):
            new_array = self.array.add_dim(**{dim_name:value})
            new_name = f"({self.name}).add_dim({dim_name},{value})"
            return self.new_symbol(new_array, new_name)
        else:
            raise Exception('value is neither str nor dict')

    def dropna(self):
        new_array = self.array.dropna()
        new_name = f"({self.name}).dropna()"
        return self.new_symbol(new_array, new_name)

    def dropinf(self, pos, neg):
        new_array = self.array.dropinf(pos,neg)
        new_name = f"({self.name}).dropna({pos=},{neg=})"
        return self.new_symbol(new_array, new_name)

    def drop(self, dims:Union[str,List[str]]):
        new_array = self.array.drop(dims=dims)
        new_name = f"({self.name}).dropna({dims=})"
        return self.new_symbol(new_array, new_name)

    def round(self, decimals:int):
        new_array = self.array.round(decimals=decimals)
        new_name = f"({self.name}).round({decimals=})"
        return self.new_symbol(new_array, new_name)

    def elems_to_datetime(self, new_dim:str, actual_dim:str, reference_date:str='01-01-2030', freq:str='H', sort_corrds:bool=True):
        new_array = self.array.elems_to_datetime(new_dim=new_dim, actual_dim=actual_dim, reference_date=reference_date, freq=freq, sort_coords=sort_corrds)
        new_name = f"({self.name}).elems_to_datetime({new_dim}{actual_dim},{reference_date},{freq},{sort_corrds})"
        return self.new_symbol(new_array, new_name)

    def elems_to_int(self, new_dim:str, actual_dim:str):
        new_array = self.array.elems_to_int(new_dim, actual_dim)
        new_name = f"({self.name}).elems_to_int({new_dim=},{actual_dim=})"
        return self.new_symbol(new_array, new_name)

    def find_ids(self, **kwargs):
        '''
        find ids whose headings comply the criteria to the value indicated
        dictionary heading as key and value as tuple of (operator, value)
        Example: Z.find_ids(**{'time_series_scen':('==','NaN'),'co2price(n,tech)':('<',80)})
        '''
        dc = self.metadata
        collector = []
        for k,v in dc.items():
            if k in kwargs.keys():
                flag = False
                nan_str = False
                id_list = []
                for k2, v2 in v.items():
                    if isinstance(v2,str):
                        if isinstance(kwargs[k][1],str):
                            if eval(f"'{v2}' {kwargs[k][0]} '{kwargs[k][1]}'"):
                                id_list.append(k2)
                                if not flag:
                                    flag = True
                            if kwargs[k][1] != 'NaN' and v2 == 'NaN':
                                nan_str = True
                        else:
                            continue
                    elif np.isnan(v2):
                        if np.isnan(kwargs[k][1]):
                            if kwargs[k][0] == '==':
                                id_list.append(k2)
                                if not flag:
                                    flag = True
                        else:
                            if kwargs[k][0] == '!=':
                                id_list.append(k2)
                                if not flag:
                                    flag = True
                            elif kwargs[k][0] != '==':
                                print(f"{k} in {k2} has NaN value for condition '{kwargs[k][0]} {str(kwargs[k][1])}'. Not included")
                            
                    elif np.isnan(kwargs[k][1]):
                        if kwargs[k][0] == '!=':
                            id_list.append(k2)
                            if not flag:
                                flag = True
                        else:
                            continue
                    elif eval(f"{v2} {kwargs[k][0]} {kwargs[k][1]}"):
                        id_list.append(k2)
                        if not flag:
                            flag = True
                collector.append(set(id_list))
                if not flag:
                    print(f"Column '{k}' does not contain '{kwargs[k][1]}'")
                if nan_str:
                    print(f"Column '{k}' has 'NaN' as string. You can filter such string too.")
        not_present = []
        for cond in kwargs.keys():
            if cond in dc.keys():
                pass
            else:
                not_present.append(cond)
        if not_present:
            str_cond = ";".join(not_present)
            print(f"{str_cond} not in symbol's data")
        return set.intersection(*collector)

    def id_info(self,ID:Union[str,int]):
        '''Gives informaion about the ID

        Args:
            ID (str): ID of the scenario
        Returns:
              A dictionary with the following Modifiers as keys and the corresponding value.
        Example:
           >>> Z.id_info('S0001')
        '''
        dc = dict()
        for k, v in self.metadata.items():
            if ID in v.keys():
                dc[k] = v[ID]
        return dc
    
    def shrink(self, neg: Union[bool, list]=False, **kwargs):
        ''' 
        Shrinks the symbol to keep only those rows that comply the given criteria.
        karg is a dictionary of symbol sets as key and elements of the set as value.
        sets and elements must be present in the symbol.
        
        eg:
        Z.shrink(**{'tech':['pv','bio'],'h':[1,2,3,4]})
        
        returns a new symbol
        '''
        if len(kwargs) > 1:
            if isinstance(neg,list):
                assert len(neg) == len(kwargs)
            else:
                new_neg = []
                for _ in range(len(kwargs)):
                    new_neg.append(neg)
                neg = new_neg
        else:
            neg = [neg]

        for key, value in kwargs.items():
            if key in self.dims:
                if set(value).issubset(self.items[key]):
                    pass
                else:
                    not_present = set(value) - (set(value) & set(self.items[key]))
                    present = (set(value) & set(self.items[key]))
                    if len(present) == 0:
                        raise Exception(f"{not_present} is/are not in {self.items[key]}")
                    else:
                        # print(f"    Only {present} exist in {self.items[key]} and meet criteria at '{key}', while not {not_present}")
                        kwargs[key] = sorted(present)
            else:
                raise Exception(f"'{key}' is not in {self.dims} for symbol {self.name}")

        right_kwargs = {k:v for k,v in kwargs.items()}
        i = 0
        for key in kwargs:
            if neg[i]:
                all_elems = self.items[key].tolist()
                for skip_elem in kwargs[key]:
                    all_elems.remove(skip_elem)
                right_kwargs[key] = all_elems

        new_array = self.array.shrink(**right_kwargs)
        new_name = f"({self.name}).shrink(neg={neg},{','.join(['='.join([k,str(v)]) for k,v in kwargs.items()])})"
        return self.new_symbol(new_array, new_name)

    def shrink_by_attr(self, neg=False, **kwargs):
        ''' 
        shrink_with_attributes generates new symbol based on other attributes of the dataframe. Attributes can be seen with Symbol.get('modifiers').
        Shrink the symbol to keep only the row that comply the criteria in kargs.
        kargs is a dictionary of symbol attributes as key and elements of the attribute columns as value.
        attributes and attribute's elements must be present in the symbol.

        eg:
        Z.shrink_by_attr(**{'run':[0,1],'country_set':['NA']})

        returns a new symbol
        '''
        for key, value in kwargs.items():
            dc = self.metadata
            if key not in dc.keys():
                raise Exception(f"'{key}' is not in {list(dc.keys())} for symbol {self.name}")
        
        id_list = sorted(set([item for sublist in list(self.create_mix(kwargs).values()) for item in sublist]))
        new_object = self.shrink(id=id_list, neg=neg)
        new_object.name = f"(neg={neg},{self.name}).shrink_by_attr({','.join(['='.join([k,str(v)]) for k,v in kwargs.items()])})"
        return new_object

    def refdiff(self, reference_id:Union[int,str]=0):
        ''' '''
        new_object = self - self.shrink(id=[reference_id]).dimreduc('id')
        new_object.name = f"({self.name}).refdiff({reference_id})"
        return new_object

    def create_mix(self, criteria):
        ''' '''
        combination = self.create_combination(criteria)
        order = criteria.keys()
        return self._find_ids_by_tuple(order,combination)

    def create_combination(self, criteria: dict):
        return list(itertools.product(*criteria.values()))


    def _find_ids_by_tuple(self,key_order,combination):
        groups = {}
        for i, pair in enumerate(combination):
            config = {}
            for k, v in zip(key_order, pair):
                config[k] = ('==',v)
            groups[i] = list(self.find_ids(**config))
        return groups

    def _ref_diff_group(self,refs,groups, verbose=False):
        symbols = []
        for key in groups:
            if len(refs[key]) == 0:
                if verbose:
                    print(f"{refs} for key = {key} no reference id found")
                    print(groups)
                continue
            else:
                refdiff_symbol = self.shrink(id=list(groups[key])).refdiff(refs[key][0])
                symbols.append(refdiff_symbol)
        return sum(symbols)

    def refdiff_by_sections(self, criteria_dict, criteria_ref_dict, verbose=False):
        ''' '''
        groups = self.create_mix(criteria_dict)
        criteria_ref_full = {**criteria_dict,**criteria_ref_dict}
        refs = self.create_mix(criteria_ref_full)
        assert all([len(refs[key]) <= 1 for key in refs]), f"It should be only one reference scenario per group {criteria_ref_full.keys()} but more were found: {refs}"
        return self._ref_diff_group(refs,groups,verbose)

    def definition_msg(self, name):
        print(f"Attribute '{name}' must be defined first in __init__ method")

    def __repr__(self):
        return f'''Symbol(name='{self.name}', \n       value_type='{self.value_type}')'''


def from_feather(path):
    return Symbol(**from_feather_dict(path, with_=ka.settings.feather_with))