import os
import tomllib
import tomli_w
import pandas as pd
import tempfile
import openpyxl
import string as _string
from Bio import SeqIO
import lib_dzne_basetables


class FileExtensionError(ValueError):
    pass


def walk(resources):
    for resource in resources:
        if resource in ("", '-'):
            yield resource
        elif os.path.isfile(resource):
            yield resource
        elif os.path.isdir(resource):
            for root, dirnames, filenames in os.walk(resource):
                for filename in filenames:
                    yield os.path.join(root, filename)
        else:
            raise ValueError()




class StreamType:
    class _Stream:
        @property
        def streamType(self):
            return self._streamType
        @property
        def ext(self):
            return os.path.splitext(self._string)
        def __str__(self):
            return self._string
        def read(self):
            if self._string == "":
                return self._streamType.get_default_data()
            if self._string == "-":
                return self._streamType.read_stdin()
            #if not os.path.isfile(self._string):
            #    raise FileNotFoundError()
            return self._streamType.read(self._string)
        def write(self, data, overwrite=False):
            if self._string == "":
                # quiet
                return
            if self._string == "-":
                print(self._streamType.data_to_str(data))
                return
            if os.path.isdir(self._string):
                raise NotImplementedError()
            #self._streamType._fits(string)
            if os.path.exists(self._string) and not overwrite:
                raise IOError()
            self._streamType.write(self._string, data)
    def __call__(self, string):
        if type(string) is not str:
            raise TypeError(f"Streams can only be created from strings! The type {type(string)} is not supported! ")
        if string not in ("", '-') and self._extensions is not None:
            y, x = os.path.splitext(string)
            if x not in self._extensions.keys():
                raise FileExtensionError(f"{ascii(string)}: {ascii(x)} not among {tuple(self._extensions.keys())}! ")
        #stream = type(self)._Stream()
        stream = StreamType._Stream()
        stream._streamType = self
        stream._string = string
        return stream
    def __init__(self, *, extensions=None):
        self._extensions = dict(extensions) if (extensions is not None) else None
    def get_default_data(self):
        raise NotImplementedError()
    def read_stdin(self):
        raise NotImplementedError()
    def read(self, string):
        raise NotImplementedError()
    def data_to_str(self, data):
        return data.__repr__()
    def write(self, string, data):
        raise NotImplementedError()
        

class ResourceStreamType(StreamType):
    def __init__(self, streamType):
        super().__init__()
        self._streamType = streamType
    @property
    def streamType(self):
        return self._streamType
    def read(self, string):
        files = list()
        if string in ("", '-'):
            files.append(string)
        elif os.path.isfile(string):
            files.append(string)
        elif os.path.isdir(string):
            for root, dirnames, filenames in os.walk(string):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
        else:
            raise ValueError()    
        return [self._streamType(file) for file in files]    


class CharsStreamType(StreamType):
    def data_to_str(self, data):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = os.path.join(tmpdir, 'a')
            self.write(tmpfile, data)
            with open(tmpfile, 'r') as s:
                return s.read()


class _SeqreadStreamType(StreamType):
    def __init__(self):
        super().__init__(extensions=dict(type(self)._datatypes))
        self._require_qv = True
class SeqreadInStreamType(_SeqreadStreamType):
    _datatypes = {
        '.phd': 'phd',
        '.ab1': 'abi',
    }
    def get_default_data(self):
        return {
            'qv': 0,
            'seq': "",
        }
    def read(self, string):
        y, x = os.path.splitext(string)
        record = SeqIO.read(string, SeqreadInStreamType._datatypes[x])
        ans = dict()
        ans['seq'] = str(record.seq).upper()
        error = None
        try:
            ll = record.letter_annotations['phred_quality']
        except KeyError as exc:
            error = exc
            ans['qv'] = None
        else:
            if len(ll) == 0:
                ans['qv'] = 0
            else:
                ans['qv'] = int(round(sum(ll) / len(ll)))
        if self._require_qv:
            if error is not None:
                raise error
        return ans
class SeqreadOutStreamType(_SeqreadStreamType):
    _datatypes = {
        '.phd': 'phd',
    }
    def write(self, string, data):
        data = dict(data)
        y, x = os.path.splitext(string)
        record = SeqRecord(data.pop('seq'))
        record.letter_annotations['phred_quality'] = [data.pop('qv')] * len(record.seq)
        if len(data):
            raise ValueError()
        SeqIO.write(string, SeqreadInStreamType._datatypes[x], record)
    def data_to_str(self, data):
        return data.__repr__


class TOMLStreamType(CharsStreamType):
    def __init__(self):
        super().__init__(extensions={'.toml': "TOML"})
    def get_default_data(self):
        return dict()
    def read(self, string):
        with open(string, 'rb') as s:
            return tomllib.load(s)
    def write(self, string, data):
        with open(string, 'wb') as s:
            tomli_w.dump(data, s)

class TextStreamType(CharsStreamType):
    def __init__(self):
        super().__init__(extensions={'.log': 'Log', '.txt': 'Text'})
    def get_default_data(self):
        return list()
    def read(self, string):
        lines = list()
        with open(string, 'r') as s:
            for line in s:
                assert line.endswith('\n')
                lines.append(line[:-1])
        return lines
    def write(self, string, data):
        with open(string, 'w') as s:
            for line in data:
                print(line, file=s)

class BASEStreamType(CharsStreamType):
    def __init__(self, basetype=None):
        self._basetype = basetype
        if basetype is None:
            x = None
        elif basetype in {'a', 'd', 'm', 'y', 'c'}:
            x = {f".{basetype}base": f"{basetype}base"}
        else:
            raise ValueError()
        super().__init__(extensions=x)
    def get_default_data(self):
        return lib_dzne_basetables.table.make(basetype=self._basetype)
    def read(self, string):
        data = pd.read_csv(
            string,
            sep='\t',
            encoding='latin-1',
            index_col=False,
            dtype='str',
            keep_default_na=False,
            na_values=[],
        )
        try:
            data = lib_dzne_basetables.table.make(data, basetype=self._basetype)
        except BaseException as exc:
            raise ValueError(f"The BASE-table {ascii(string)} violates the standards! ") from exc
        return data
    def write(self, string, data):
        lib_dzne_basetables.table.check(data, basetype=self._basetype)
        data.to_csv(
            string, 
            sep='\t',
            index=False,
        )
        #return
        #messages = list()
        #text = TextStreamType()(string).read()
        #columns = text[0].split('\n')
        #_columns = list()
        #for c in columns:
        #    if c == "":
        #        messages.append("Column names are not allowed to me empty! ")
        #        continue
        #    if c[0] in _string.digits:
        #        messages.append("Column names are not allowed to start with a digit! ")
        #        continue
        #    forbiddenchars = set(c) - set(columnchars)
        #    if len(forbiddenchars):
        #        messages.append(f"Column names are not allowed to contain the chars {forbiddenchars}! ")
        #        continue
        #    if c in _columns:
        #        messages.append(f"Column name {c} is a duplicate! ")
        #        continue
        #    _columns.append(c)
        #rows = list()
        #for line in text[1:]:
        #    rows.append(dict(zip(columns, line)))
        #body = text[1:]
        #title_chars = _string.ascii_uppercase + _string.digits + '_'
        #element_chars = _string.ascii_letters + _string.digits + _string.punctuation.replace("\"", "").replace("'", "")
        #with open(string, 'r') as s:
        #    heading = 
    #class ColumnTitleError(KeyError):
    #    pass
    #class ElementError(ValueError):
    #    pass

        #text = ""
        #columns = list(data.columns)
        #_columns = list()
        #errors = list()
        #for column in columns:
        #    if column in _columns:
        #        errors.append(KeyError(f"The column-title {column} occures more than once. "))
        #        continue
        #    _columns.append(column)
        #    if (
        #        (type(column) is not str) 
        #        or (column == "") 
        #        or (column[0] in string.digits) 
        #        or (0 == len(set(column) - set(string.digits + string.ascii_uppercase + '_')))
        #    ):
        #        errors.append(KeyError(f"The column {column} has an improper title. "))
        #lines = ['\t'.join(columns)]
        #for i, row in data.iterrows():
        #    for col in columns:
        #        value = row[col]
        #
        #if len(errors):
        #    raise ExceptionGroup(errors)
        


class WorkbookStreamType(StreamType):
    def __init__(self):
        super().__init__(extensions={'.xlsx':'excel'})
    def get_default_data(self):
        return openpyxl.Workbook()
    def read(self, string):
        return openpyxl.load_workbook(filename=string)
    def write(self, string, data):
        #if type(data) is not openpyxl.Workbook:
        #    raise TypeError()
        data.save(filename=string)















        






        