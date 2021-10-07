from Model_to_fit import *
from plot_creator.create_plot import *
import dotenv
import numpy as np

dotenv.load_dotenv()
calculator = fw.read_from_file(fw.path_with_real_data + r'\calculator.json')
df_basic = pd.read_csv(fw.directhion_path+r'\Data_storage\table.csv')

bn = BN_creator(df_basic)

prior = bn.prior_distribution(partitioned=False, save=True)

n = 0
for i in prior:
    plt = Plots(i)
    fw.env_change('XLABEL', df_basic.columns[n])
    fw.env_change('YLABEL', 'Frequency')
    fw.env_change('TITLE', '')
    plt.build_one_plot(save=True, show=False)
    n+=1
