# coding: utf-8

import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

def print_graphs(year = '2018', month = '05', day = '11', ticks_number = 7, temp_min = 20, temp_max = 28, hum_min = 20, 
        hum_max = 70):
    
    df_table1, df_table2, df_ante = load_data(year, month, day)
    
    df_time = create_datetime(df_ante)
    
    df = create_dataframe(df_table1, df_table2, df_ante, df_time)
    
    #remove redundant dates and times
    df = df.drop(['DATE','TIME'],axis=1)
    
    time_save = time_saver(df_table2)
    
    datetime_ticks = get_ticks(ticks_number, df_ante)
    
    tick_spaces = tick_spacing(df_ante, ticks_number)
    
    plot_temp(temp_min, temp_max, tick_spaces, datetime_ticks, df_table2, df, time_save)
    plot_hum(hum_min, hum_max, tick_spaces, datetime_ticks, df_table2, df, time_save)

def get_numbers(year = '2018', month = '05', day = '11', time_ignore = 10):
    
    df_table1, df_table2, df_ante = load_data(year, month, day)
    
    df_time = create_datetime(df_ante)
    
    df = create_dataframe(df_table1, df_table2, df_ante, df_time)
    
    #remove redundant dates and times
    df = df.drop(['DATE','TIME'],axis=1)
    
    print_max(df, time_ignore)
    print_min(df, time_ignore)
    
    k, j = time_drift(df_table1, df_table2, time_ignore)
    
    print_max_drift(df_table1, df_table2, k, j, time_ignore)
    
    table1_drift = sum(i>0.99 for i in k)
    table2_drift = sum(i>0.99 for i in j)
    
    one_c_drift(table1_drift, table2_drift)
    
    print_temp_minutes(df)
    print_hum_minutes(df)

def load_data(year, month, day): 
    #choose which columns to keep
    cols = [1,2,3,4]

    path_file = 'C:/Users/mattj/Documents/Data logger diamond lab/'
    path_date = '_'+year+'_'+month+'_'+day+'.xlsx'

    #create data frames from excel files for each datalogger
    df_table1 = pd.read_excel(path_file + 'Table 1/table1' + path_date,
                       usecols = cols,
                       header = 7) 
    df_table2 = pd.read_excel(path_file + 'Table 2/table2' + path_date, 
                       usecols = cols,
                       header = 7) 
    df_ante = pd.read_excel(path_file + 'Ante room/ante' + path_date, 
                       usecols = cols,
                       header = 7)

    #relabel columns to something more useful
    df_table1.columns = ['DATE','TIME','Temperature table1','Relative Humidity table1']
    df_table2.columns = ['DATE','TIME','Temperature table2','Relative Humidity table2']
    df_ante.columns = ['DATE','TIME','Temperature ante','Relative Humidity ante']
    return df_table1, df_table2, df_ante

def create_datetime(data_frame):
    #combines date and time into datetime column

    #create list and append it with the combination of date and time
    time_ = []
    for i in range(len(data_frame.index)):
        time_.append(str(data_frame.loc[i,'DATE']) + str(" ")+ str(data_frame.loc[i,'TIME']))

    #turn list into data frame and rename it
    df_time = pd.DataFrame(time_)
    df_time.columns = ['Datetime']
    return df_time

def create_dataframe(df_table1, df_table2, df_ante, df_time):
    #combine all the data frames into a single dataframe
    df = pd.concat([df_table1,df_table2,df_ante,df_time],axis=1)
    return df

def time_saver(df_table2):
    #create a string used for the filename when saving by striping and renaming one of the last entries in the dataframe
    time_save = datetime.datetime.strptime(df_table2.loc[len(df_table2.index)-3,'DATE'],"%d.%m.%Y").strftime("%Y-%m-%d")
    return time_save

def get_ticks(ticks_number, df_ante):
    #create the x gridline labels
    datetime_ticks = []
    for i in range(ticks_number): #cuts up the length of the dataframe into equal segments to use as indices for datetime
        datetime_ticks.append(i * round((len(df_ante.index)-1)/ticks_number))
    datetime_ticks.append(len(df_ante.index)-1)
    return datetime_ticks

def tick_spacing(df_ante, ticks_number):
    #create the gridline spacing
    tick_spaces = np.arange(0,len(df_ante.index)-1,(len(df_ante.index)-2)/ticks_number)
    return tick_spaces

def plot_temp(temp_min, temp_max, tick_spaces, datetime_ticks, df_table2, df, time_save):
    #plot the temperature
    df.plot(x='Datetime',
            y=['Temperature table1','Temperature table2','Temperature ante'],
            figsize=(20,10))
    plt.ylim(temp_min, temp_max)
    plt.xlim(0,len(df_table2.index))
    plt.ylabel('Temperature °C')
    plt.title('Lab Temperature')
    plt.xticks(tick_spaces,(df.loc[datetime_ticks,'Datetime']))
    plt.grid()
    plt.savefig('C:/Users/mattj/Pictures/Datalogger/Temperature/' + 'Temperature ' + time_save)
    plt.show()

def plot_hum(hum_min, hum_max, tick_spaces, datetime_ticks, df_table2, df, time_save):
    #plot the humidity
    df.plot(x='Datetime',
            y=['Relative Humidity table1','Relative Humidity table2','Relative Humidity ante'],
            figsize=(20,10))
    plt.ylim(hum_min, hum_max)
    plt.xlim(0,len(df_table2.index))
    plt.ylabel('Relative Humidity (%)')
    plt.title('Lab Humidity')
    plt.xticks(tick_spaces,(df.loc[datetime_ticks,'Datetime']))
    plt.grid()
    plt.savefig('C:/Users/mattj/Pictures/Datalogger/Humidity/'+ 'Humidity ' + time_save )
    plt.show()

def maximum_values(df, time_ignore):
    #get all the maximum values
    max_values = df.loc[time_ignore-1:,['Temperature table1','Temperature table2','Temperature ante','Relative Humidity table1','Relative Humidity table2'
       ,'Relative Humidity ante']].max(axis=0)
    return max_values

def minimum_values(df, time_ignore):
    #get all the minimum values
    min_values = df.loc[time_ignore-1:,['Temperature table1','Temperature table2','Temperature ante','Relative Humidity table1','Relative Humidity table2'
       ,'Relative Humidity ante']].min(axis=0)
    return min_values

def time_drift(df_table1, df_table2, time_ignore):
    #compare the temperature at each point in time with every point in time within 1 hour and create lists with the 
    #difference of those temperatures for each datalogger
    time_ignore = 10 #the first 10 minutes of data is ignored due to erroneously high starting values
    k = []
    append_k = k.append
    for i in range (len(df_table1)-61-time_ignore):
        intermediate = df_table1.loc[i+time_ignore,['Temperature table1']]
        for l in range(1,61):
            append_k(intermediate-df_table1.loc[i+time_ignore+l,
            ['Temperature table1']])
    k = [abs(x) for x in k]
    k = [float(x) for x in k]
    
    j = []
    append_j = j.append
    for i in range (len(df_table2)-61-time_ignore):
        intermediate = df_table2.loc[i+time_ignore,['Temperature table2']]
        for l in range(1,61):
            append_j(intermediate-df_table2.loc[i+time_ignore+l,
            ['Temperature table2']])
    j = [abs(x) for x in j]
    j = [float(x) for x in j]
    return k, j

#only useful in jupyter notebook
#def table1_maxdrift_pos(df_table1, time_ignore, k):
#    #the location and values of the biggest temperature drift on table 1
#    display(df_table1.loc[[(np.argmax(k)//60) + time_ignore,(np.argmax(k)//60 + np.argmax(k)-(np.argmax(k)//60)*60)+
#                   time_ignore + 1], ['Temperature table1','DATE','TIME']])

#def table2_maxdrift_pos(df_table2, time_ignore, j):
#    #the location and values of the biggest temperature drift on table 2
#    display(df_table2.loc[[(np.argmax(j)//60)+time_ignore,(np.argmax(j)//60+np.argmax(j)-(np.argmax(j)//60)*60)+
#                   + time_ignore + 1],['Temperature table2','DATE','TIME']])

def temp_minutes(df):
    #find the amount of times temp is above 25 and below 20
    #table1
    temp1_1 = df[df["Temperature table1"] > 25].count()[["Temperature table1"]]#above 25
    temp1_2 = df[df["Temperature table1"] < 20].count()[["Temperature table1"]]#below 20

    #table2
    temp2_1 = df[df["Temperature table2"] > 25].count()[["Temperature table2"]]
    temp2_2 = df[df["Temperature table2"] < 20].count()[["Temperature table2"]]

    #ante
    tempa_1 = df[df["Temperature ante"] > 25].count()[["Temperature ante"]]
    tempa_2 = df[df["Temperature ante"] < 20].count()[["Temperature ante"]]

    #total number of minutes outside temperature operating range
    table1_temp_minutes = temp1_1 + temp1_2
    table2_temp_minutes = temp2_1 + temp2_2
    ante_temp_minutes = tempa_1 + tempa_2
    
    return table1_temp_minutes, table2_temp_minutes, ante_temp_minutes

def hum_minutes(df):
    #find the amount of times humidity is above 50% and below 30%
    #table1
    hum1_1 = df[(df["Relative Humidity table1"] > 50)].count()["Relative Humidity table1"]#above 50
    hum1_2 = df[(df["Relative Humidity table1"] < 30)].count()["Relative Humidity table1"]#below 30

    #table2
    hum2_1 = df[(df["Relative Humidity table2"] > 50)].count()["Relative Humidity table2"]
    hum2_2 = df[(df["Relative Humidity table2"] < 30)].count()["Relative Humidity table2"]

    #ante room
    huma_1 = df[(df["Relative Humidity ante"] > 50)].count()["Relative Humidity ante"]
    huma_2 = df[(df["Relative Humidity ante"] < 30)].count()["Relative Humidity ante"]

    #total number of minutes outside humidity operating range 
    table1_humidity_minutes = hum1_1+hum1_2
    table2_humidity_minutes = hum2_1+hum2_2
    ante_humidity_minutes = huma_1+huma_2
    
    return table1_humidity_minutes, table2_humidity_minutes, ante_humidity_minutes

def print_max(df, time_ignore):
    max_values = maximum_values(df, time_ignore)
    print('Maximum Values\n'+
          'Temperature table1', str(max_values[0]) + '°C\n'+
          'Temperature table2', str(max_values[1]) + '°C\n'+ 
          'Temperature ante', str(max_values[2]) + '°C\n' + 
         'Humidity table1', str(max_values[3]) + '%\n' +
         'Humidity table2', str(max_values[4]) + '%\n'+
         'Humidity ante', str(max_values[5]) + '%\n')

def print_min(df, time_ignore):
    min_values = minimum_values(df, time_ignore)
    print('Minimum Values\n'+
          'Temperature table1', str(min_values[0]) + '°C\n'+
          'Temperature table2', str(min_values[1]) + '°C\n'+ 
          'Temperature ante', str(min_values[2]) + '°C\n' + 
         'Humidity table1', str(min_values[3]) + '%\n' +
         'Humidity table2', str(min_values[4]) + '%\n'+
         'Humidity ante', str(min_values[5]) + '%\n')

def print_max_drift(df_table1, df_table2, k, j, time_ignore):
    print('Maximum temperature drift\n'+
          'Table1 ' + str(round(max(k),1)) +'°C between',
          str(df_table1.loc[(np.argmax(k)//60)+time_ignore, ['TIME']][0])+' - '+ str(df_table1.loc[(np.argmax(k)//60
                            + np.argmax(k)-(np.argmax(k)//60)*60)+time_ignore + 1, ['TIME']][0])+' on '+ 
                            str(df_table1.loc[(np.argmax(k)//60)+ time_ignore, ['DATE']][0])+'\n'

          'Table2 ' + str(round(max(j),1)) +'°C between',
          str(df_table2.loc[(np.argmax(j)//60)+time_ignore, ['TIME']][0])+' - '+ str(df_table2.loc[(np.argmax(j)//60
                            +np.argmax(j)- (np.argmax(j)//60)*60)+ time_ignore +1, ['TIME']][0])+' on '+ 
                            str(df_table2.loc[(np.argmax(j)//60)+ time_ignore, ['DATE']][0])+'\n')

def one_c_drift(table1_drift, table2_drift):
    print('Amount of data points with >1°C drift\n'+
          'table1 ' +str(table1_drift) + '\n'
          'table2 ' +str(table2_drift)+ '\n')

def print_temp_minutes(df):
    table1_temp_minutes, table2_temp_minutes, ante_temp_minutes = temp_minutes(df)
    print('Minutes outside of temperature range (20-25°C)\n'
         'table1', str(table1_temp_minutes[0]) + '\n'
         'table2', str(table2_temp_minutes[0]) + '\n'
         'ante', str(ante_temp_minutes[0])+ '\n')

def print_hum_minutes(df):
    table1_humidity_minutes, table2_humidity_minutes, ante_humidity_minutes = hum_minutes(df)
    print('Minutes outside of humidity range (30-50%)\n'
         'table1', str(table1_humidity_minutes) + '\n'
         'table2', str(table2_humidity_minutes) + '\n'
         'ante', str(ante_humidity_minutes) + '\n')

print_graphs()
get_numbers()