from Model_to_fit import *
from plot_creator.create_plot import *
import dotenv
import numpy as np

dotenv.load_dotenv()
calculator = fw.read_from_file(fw.path_with_real_data + r'\calculator.json')
prod_cube = fw.read_txt_as_csv(fw.path_with_real_data + r'\SQLAExport.csv',
                               header=True)
df_basic = prod_cube[['nProductGID', 'sPeriodType', 'nOrgProfitCenterGID', 'nSegmentGID_RB']]

df_basic['Пол клиента'] = np.random.choice(['M', 'F'], size=len(df_basic))
df_basic['Возраст клиента'] = np.random.choice(range(23, 87), size=len(df_basic))
df_basic.columns = ['Product ID', 'Period', 'Value of pay', 'Segment of payment',
                    "Client's gender", "Client's age"]
df_basic.to_csv(fw.directhion_path+r'\Data_storage\table.csv')
print(df_basic)