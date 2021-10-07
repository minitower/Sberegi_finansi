import os
import pandas as pd
import json
import dotenv


class File_work:
    def __init__(self):
        self.directhion_path = os.path.dirname(__file__)
        self.path_with_filename = os.path.abspath(__file__)
        self.path_with_real_data = os.path.join(os.path.dirname(__file__),
                                                'Data_storage')
        print(self.directhion_path + r'\Output')
        if not os.path.exists(self.directhion_path + r'\Output'):
            os.mkdir(self.directhion_path + r'\Output')
        if not os.path.exists(self.directhion_path + r'\Output\img'):
            os.mkdir(self.directhion_path + r'\Output\img')
        if not os.path.exists((self.directhion_path + r'\Output\prior_distribution')):
            os.mkdir(self.directhion_path + r'\Output\prior_distribution')
        self.counter = 0
        os.putenv('DIR_PATH', self.directhion_path)
        os.putenv('FILE_PATH', self.path_with_filename)
        os.putenv('SOURCE', self.path_with_real_data)

    @staticmethod
    def write_in_file(path, message, type='a+', q=True):
        """
        Func for write some message to file
        :param q: bool, print err code ot not
        :param path: absolute path to necessary file (str type)
        :param message: data with message in string format (str type)
        :return: None (None type)
        """
        with open(path, type, encoding='UTF-8') as f:
            f.write(message)
            f.close()
            if not q:
                print(message + 'success writen on file!')

    @staticmethod
    def read_from_file(path, **kwargs):

        """
        Func for read some message from file
        :param path: absolute path to necessary file (str type)
        :return: message from data (str type)
        """
        if os.path.split(path)[1].split('.')[1] == 'csv':
            data = pd.read_csv(path, header=0, encoding='UTF-8',
                               delimiter=kwargs['delimiter'],
                               engine=kwargs['engine'])
            return data
        if os.path.split(path)[1].split('.')[1] == 'json':
            with open(path, 'r', encoding='UTF-8') as file:
                data = json.load(file)
        else:
            with open(path) as f:
                data = f.read()
        return data

    def lst_df_save(self, ind, columns=None, save_csv=True, prefix_csv='Prior_distribution',
                    save_plot=True, prefix_plot='Prior_distribution',
                    suffix_csv='', suffix_plot=''):
        """
        Func for create pd.DataFrame from list of pd.DataFrame or df-like sets
        :param columns:
        :param ind: list of pd.DataFrame or df-like sets *.png
        :param save_csv: bool, save result on %PATH%\\Output\\{prefix}_column_{suffix}.csv or not
        :param prefix_csv: str with prefix of each file *.csv
        :param save_plot: bool, save result on %PATH%\\Output\\{prefix}_column_{suffix}.png or not
        :param prefix_plot: str with prefix of each file *.png
        :param suffix_csv: str with suffix of each file *.csv
        :param suffix_plot: str with suffix of each file *.png
        :return: n pd.DataFrame, where n = len (ind)
        """
        n = 0
        for i in ind:
            if type(i) != pd.DataFrame:
                try:
                    i = pd.DataFrame(i)
                except TypeError:
                    raise TypeError('Wrong type! Your type {} but pd.DataFrame \
                    needed'.format(type(i)))
            if len(ind) == len(columns) and columns:
                ind.columns = columns[n]
                n += 1
            else:
                try:
                    ind.columms == columns
                except IndexError:
                    raise ValueError("Length of values didn't compare. Please, check code")
            if save_csv:
                i.to_csv(self.directhion_path + r'\Output\{}_{}.csv'.format(
                    prefix_csv, suffix_csv
                ))
                print('File {}_{}.csv'.format(
                    prefix_csv, suffix_csv + ' saved on path {}', self.directhion_path + r'\Output'))
                pass

    def f_exist(self, file_name, file_loc=None):
        """
        Func for check file for his location File location can be updated
        from one of common values in File_Work path list or create by user
        :param file_name: name of searching file
        :param file_loc: location of needed file. If None function
        will be search in next list:[File_work.direction_path, File_work.direction_with_filename,
        File_work.path_with_real_data].
        :return: If file_loc is None - return dict where keys - file location,
        and values bool True if exist else False;
        if file_loc defined - return bool True if exist else False
        """
        if file_loc:
            exist = os.path.exists(os.path.join(file_loc, file_name))
            return exist
        else:
            find_file = {}
            for i in [self.directhion_path,
                      self.path_with_filename,
                      self.path_with_real_data]:
                find_file.update({i: os.path.exists(os.path.join(i, file_name))})
            return find_file

    def f_copy_to(self, file_name, file_path_from, file_path_to):
        """
        Func for copy file from one direction to another
        :param file_path_from: dir, where file exist
        :param file_path_to: dir, where file will be created
        :return: None
        """
        try:
            data = self.read_from_file(os.path.join(file_path_from, file_name))
        except:
            raise BaseException('Error with reading of file')
        if self.f_exist(file_name, file_path_to):
            raise FileExistsError('File already exist')
        try:
            self.write_in_file(os.path.join(file_path_to, file_name), data)
        except:
            raise BaseException('Error with writing file')

    def read_txt_as_csv(self, path, header=True):
        with open(path, 'r') as f:
            data = f.read()
        tmp = []
        answer = []
        for i in data.split('\t'):
            if "\n" in i:
                answer.append(tmp)
                tmp = []
            else:
                tmp.append(i)
        answer = pd.DataFrame(answer)
        if header:
            answer.columns = answer.iloc[0]
            answer = answer.drop(0)
        return answer

    def env_change(self, key, value):
        tmp = []
        env_arr = []
        for i in self.read_from_file(self.directhion_path + '\\.env').split('\n'):
            if i[0] != '#':
                tmp.append(i.split('='))
        for i in tmp:
            if i[0] == key:
                i[1] = value
                env_arr.append('='.join(i))
            else:
                env_arr.append('='.join(i))
        print('\n'.join(env_arr))
        self.write_in_file(self.directhion_path+'\\.env', '\n'.join(env_arr), type='w')
        dotenv.load_dotenv()

