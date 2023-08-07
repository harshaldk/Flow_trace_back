#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Here tracebacks for the flow are found by implementing a backtracking algorithm. 
# Traceback flow solutions are saved as a csv file.

def Flow_traceback(xls_path, Input_file):
    xls = pd.ExcelFile(xls_path)
    df_Inp_original = pd.read_excel(xls, Input_file)
    df_Inp = df_Inp_original
    df_Delivery = df_Inp[df_Inp['for_process'] == 'Delivery']
    process = ["Sourcing", "Conditioning", "Treatment", "Forwarding", "Delivery"]
    df_traceback = pd.DataFrame(columns=['Process1', 'Cnt1', 'Week1', 'Amount1', 'Process2', 'Cnt2', 'Week2', 'Amount2',\
                                         'Process3', 'Cnt3', 'Week3', 'Amount3', 'Process4', 'Cnt4', 'Week4', 'Amount4',\
                                         'Process5', 'Cnt5', 'Week5', 'Amount5', 'Demand'])
    Demand = 1
    ans_ind = 0
    for ind in df_Delivery.index:
        start_node = df_Delivery.loc[ind, 'send_from_cnt']
        end_node = df_Delivery.loc[ind, 'to_processing_cnt']
        week = df_Delivery.loc[ind, 'Week']
        amount = df_Delivery.loc[ind, 'Amount']
        df_traceback.loc[ans_ind, 'Demand'] = Demand
        df_traceback.loc[ans_ind, 'Amount5'] = amount
        df_traceback.loc[ans_ind, 'Week5'] = week
        df_traceback.loc[ans_ind, 'Cnt5'] = end_node
        df_traceback.loc[ans_ind, 'Process5'] = "Delivery"
        for proc in reversed(process[0:4]):
            Inp_sub = df_Inp.loc[((df_Inp['Week'] <= week) & (df_Inp['for_process'] == proc) & (df_Inp['to_processing_cnt'] == start_node))]
            df_Inp_sub = pd.DataFrame(Inp_sub)
            for i in df_Inp_sub.index:
                if df_Inp_sub.loc[i, 'Amount'] - amount >= -0.9:
                    start_node = df_Inp_sub.loc[i,'send_from_cnt']
                    end_node = df_Inp_sub.loc[i, 'to_processing_cnt']
                    week = df_Inp_sub.loc[i,'Week']
                    df_Inp.loc[i,'Amount'] = df_Inp.loc[i, 'Amount'] - amount
                    if proc == "Forwarding":
                        df_traceback.loc[ans_ind, 'Amount4'] = amount
                        df_traceback.loc[ans_ind, 'Week4'] = week
                        df_traceback.loc[ans_ind, 'Cnt4'] = end_node
                        df_traceback.loc[ans_ind, 'Process4'] = proc
                    elif proc == "Treatment":
                        df_traceback.loc[ans_ind, 'Amount3'] = amount
                        df_traceback.loc[ans_ind, 'Week3'] = week
                        df_traceback.loc[ans_ind, 'Cnt3'] = end_node
                        df_traceback.loc[ans_ind, 'Process3'] = proc
                    elif proc == "Conditioning":
                        df_traceback.loc[ans_ind, 'Amount2'] = amount
                        df_traceback.loc[ans_ind, 'Week2'] = week
                        df_traceback.loc[ans_ind, 'Cnt2'] = end_node
                        df_traceback.loc[ans_ind, 'Process2'] = proc
                    elif proc == "Sourcing":
                        df_traceback.loc[ans_ind, 'Amount1'] = amount
                        df_traceback.loc[ans_ind, 'Week1'] = week
                        df_traceback.loc[ans_ind, 'Cnt1'] = end_node
                        df_traceback.loc[ans_ind, 'Process1'] = proc
                if ((df_Inp_sub.loc[i, 'Amount'] - amount >= -0.9) and (df_Inp_sub.loc[i, 'Amount'] - amount <= 0.9)):
                    df_Inp = df_Inp.drop(i)
                    break
        Demand += 1
        ans_ind += 1
    df_traceback.rename({'Cnt1': 'Cnt', 'Week1': 'Week', 'Amount1': 'Amount',\
                         'Cnt2': 'Cnt', 'Week2': 'Week', 'Amount2': 'Amount',\
                         'Cnt3': 'Cnt', 'Week3': 'Week', 'Amount3': 'Amount',\
                         'Cnt4': 'Cnt', 'Week4': 'Week', 'Amount4': 'Amount',\
                         'Cnt5': 'Cnt', 'Week5': 'Week', 'Amount5': 'Amount',}, axis = 1, inplace = True)
    df_traceback.to_csv('Flow_tracebacks_{}.csv'.format(Input_file), index = False)


# In[2]:


# Here tracebacks for all possible path are generated using the Depth First Search algorithm. 
# Traceback paths are saved as a csv file.
# This approach is incomeplete yet! 

def DFS_path_traceback(xls_path, Input_file):
    xls = pd.ExcelFile(xls_path)
    df_Inp_original = pd.read_excel(xls, Input_file)
    df_Inp = df_Inp_original
    df_Delivery = df_Inp[df_Inp['for_process'] == 'Delivery']
    list_path = []
    counter = 1
    for i in df_Delivery.index:
        start_node = df_Delivery.loc[i, 'send_from_cnt']
        end_node = df_Delivery.loc[i, 'to_processing_cnt']
        week = df_Delivery.loc[i, 'Week']
        amount = df_Delivery.loc[i, 'Amount']
        Inp_Forwarding = df_Inp.loc[((df_Inp['Week'] <= week) & (df_Inp['for_process'] == "Forwarding") & (df_Inp['to_processing_cnt'] == start_node))]
        df_Forwarding = pd.DataFrame(Inp_Forwarding)
        flag_break_Sourcing = 0
        flag_break_Conditioning = 0
        flag_break_Treatment = 0
        flag_break_Forwarding = 0
        for j in df_Forwarding.index:
            start_node = df_Forwarding.loc[j, 'send_from_cnt']
            end_node = df_Forwarding.loc[j, 'to_processing_cnt']
            week = df_Forwarding.loc[j, 'Week']
            Inp_Treatment = df_Inp.loc[((df_Inp['Week'] <= week) & (df_Inp['for_process'] == "Treatment") & (df_Inp['to_processing_cnt'] == start_node))]
            df_Treatment = pd.DataFrame(Inp_Treatment)
            for k in df_Treatment.index:
                start_node = df_Treatment.loc[k, 'send_from_cnt']
                end_node = df_Treatment.loc[k, 'to_processing_cnt']
                week = df_Treatment.loc[k, 'Week']
                Inp_Conditioning = df_Inp.loc[((df_Inp['Week'] <= week) & (df_Inp['for_process'] == "Conditioning") & (df_Inp['to_processing_cnt'] == start_node))]
                df_Conditioning = pd.DataFrame(Inp_Conditioning)
                for l in df_Conditioning.index:
                    start_node = df_Conditioning.loc[l, 'send_from_cnt']
                    end_node = df_Conditioning.loc[l, 'to_processing_cnt']
                    week = df_Conditioning.loc[l, 'Week']
                    Inp_Sourcing = df_Inp.loc[((df_Inp['Week'] <= week) & (df_Inp['for_process'] == "Sourcing") & (df_Inp['to_processing_cnt'] == start_node))]
                    df_Sourcing = pd.DataFrame(Inp_Sourcing)
                    for m in df_Sourcing.index:
                        list_path.append(["Source", df_Inp.loc[m, 'to_processing_cnt'], df_Inp.loc[m, 'Week'], amount,"Conditioning", df_Inp.loc[l, 'to_processing_cnt'], df_Inp.loc[l, 'Week'], amount,"Treatment", df_Inp.loc[k, 'to_processing_cnt'], df_Inp.loc[k, 'Week'], amount,"Forwarding", df_Inp.loc[j, 'to_processing_cnt'], df_Inp.loc[j, 'Week'], amount,"Delivery", df_Inp.loc[i, 'to_processing_cnt'], df_Inp.loc[i, 'Week'], amount])
                        counter += 1
                        if ((df_Inp.loc[j, 'Amount'] - amount <= 0.9) and (df_Inp.loc[k, 'Amount'] - amount <= 0.9) and (df_Inp.loc[l, 'Amount'] - amount <= 0.9) ):
                            df_Inp = df_Inp.drop(i)
                            df_Inp = df_Inp.drop(j)
                            df_Inp = df_Inp.drop(k)
                            df_Inp = df_Inp.drop(l)                        
                            flag_break_Sourcing = 1
                            flag_break_Conditioning = 1
                            flag_break_Treatment = 1
                            flag_break_Forwarding = 1                              
                        if flag_break_Sourcing == 1:
                            break
                    if flag_break_Conditioning == 1:
                        break
                if flag_break_Treatment == 1:
                    break
            if flag_break_Forwarding == 1:
                break
    df_dfs_paths = pd.DataFrame(list_path)
    df_dfs_paths.columns = ['Process1', 'Cnt', 'Week', 'Amount', 'Process2', 'Cnt', 'Week', 'Amount',\
                                'Process3', 'Cnt', 'Week', 'Amount', 'Process4', 'Cnt', 'Week', 'Amount', 'Process5', 'Cnt', 'Week', 'Amount']  
    df_dfs_paths.to_csv('Flow_paths_DFS_{}.csv'.format(Input_file), index = False)


# In[3]:


import pandas as pd
import numpy as np

if __name__ == "__main__":
    xls_path = 'NetworkFlowProblem-Data.xlsx'
    Input_file = 'Input6' 
    
    Flow_traceback(xls_path, Input_file) # main code for traceback using backtracking algorithm.
    DFS_path_traceback(xls_path, Input_file) # code to generate all paths from source to sink using DFS.   

