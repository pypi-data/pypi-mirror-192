import os
import zipfile
import urllib.request
import pickle
import numpy as np

from pyairtable import Table

PICKLE_PATH = '.pickle'


class CourseInfo():
    def __init__(self, title, uid, version=1):
        self.info = {
            'title': title, 
            'uid': uid,
            'version': version,
        }
    
    def __call__(self, *args, **kwds):
        return self.info


class FileManager():
    def __init__(self, course_info: CourseInfo, debug=False, pickle_path='.pickle'):
        self.api_token = 'patON4DhGmQLQjdEr.37865a577686d067523f2c914cdfab5e45a9f8f81b32cf8b62fcf7cb163a9dc0'
        self.base_id = 'appLgpuFIEfGhsjhw'
        self.table_name = 'tblUsF3BQhKCpZ6K7'
        
        self.course_info = course_info
        self.debug = debug
        self.pickle_path = pickle_path
        # 폴더 생성
        if not os.path.isdir(pickle_path):
            os.mkdir(pickle_path)
        
    def save_pickle(self, data, filename, pickle_path='.pickle'):
        # pickle 파일로 저장
        pkl_filename = os.path.join(pickle_path, f"{filename}.pkl")
        with open(pkl_filename,'wb') as f:
            pickle.dump(data, f)
        if self.debug:
            print(pkl_filename, 'Saved.')            
        return pkl_filename

    def load_pickle(self, filename, pickle_path='.pickle'):
        with open(os.path.join(pickle_path, f'{filename}.pkl'),'rb') as f:
             data = pickle.load(f)
        return data
    
    def create_filename(self, question_no: int):
        info = self.course_info()
        return f"{info['title'].lower()}-{info['uid'].lower()}-ver-{info['version']:02d}-question-{question_no:02d}"
    
    def save_answer(self, answer, question_no, type='value'):
        filename = self.create_filename(question_no=question_no)
        self.save_pickle(answer, filename=filename)
        print(f'[SAVED] {filename}')
    
    def load_answer(self, question_no, type='value'):
        filename = self.create_filename(question_no=question_no)
        return self.load_pickle(filename=filename)
    
    def get_download_url(self):
        table = Table(self.api_token, self.base_id, self.table_name)
        rows = table.all(sort=['id'])
        download_url = None
        info = self.course_info()
        for r in rows:
            fields = r['fields']
            if 'uid' in fields:
                if fields['uid'].lower() == info['uid'].lower():
                    download_url = fields['download_url']
                    break
        return download_url
    
    def download_answers(self):
        url = self.get_download_url()
        if url:
            info = self.course_info()
            filename = f"{info['title'].lower()}-{info['uid'].lower()}-ver-{info['version']:02d}.zip"
            urllib.request.urlretrieve(url, filename)
            zip_ref = zipfile.ZipFile(filename, 'r')
            zip_ref.extractall(self.pickle_path)
            zip_ref.close()

            os.remove(filename)
            return True
        else:
            return False
    
class Grade():
    def __init__(self):
        pass
    
    # def check_type(self, value):
    #     if type(value) == 
    #     return 'TYPE_VALUE'
    
    def compare_value(self, val1, val2):
        if type(val1) != type(val2):
            return False
        return val1 == val2

    def compare_dataframe(self, df1, df2, sample_case_count=10):
        if df1.shape != df2.shape:
            return False
        else:
            for s in range(sample_case_count):
                row = np.random.randint(df1.shape[0])
                col = np.random.randint(df1.shape[1])
                if df1.iloc[row, col] != df2.iloc[row, col]:
                    return False
                
        return True


grade = None
file = None
info = None


def init(title, uid, version=1, mode='quiz'):
    global grade, file, info
    if not info:
        info = CourseInfo(title, uid, version)
    
    if info:
        file = FileManager(course_info=info, debug=False)
        if mode == 'quiz':
            if file.download_answers():
                print('[완료]')
            else:
                print('[에러]')
            
        
    grade = Grade()
    

def check_answer(user_ans, question_no, type='value'):
    global grade, file
    if grade and file:
        ans = file.load_answer(question_no, type='value')
        if grade.compare_value(user_ans, ans):
            print('Result: [PASS]')
        else:
            print('Result: [FAIL]')