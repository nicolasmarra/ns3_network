import csv
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


# fonction pour parser et extraire les donées utiliser pour le tracer des courbes ici l'énergie et le temp correspondant
def extract_energy_from_file(file_name):
    energies = []
    time = []
    with open(file_name, 'r') as file:
        for line in file:
            if "Total energy consumption" in line:
                energy_index = line.find("is") + 3  
                energy_str = line[energy_index:].split("J")[0]  
                energy = float(energy_str)  
                energies.append(energy) 

                time_str=line.find("+")+1
                time_str_end=line.find("s")
                time_str=line[time_str:time_str_end]
                time.append(float(time_str))
    return time, energies


#fonction pour écrire les données dans un fichier csv 
def write_to_csv(energies, time, csv_name):
    with open(csv_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Energy'])
        for t, e in zip(time, energies):
            writer.writerow([t, e])

#fonction pour lisser les données
def smooth_data(x, y, window_size=5, poly_order=2):
    smoothed_y = savgol_filter(y, window_size, poly_order)
    return x, smoothed_y

def packet_size_test():
    file_name = "periodic_60_fixe_packet_size_10"
    file_name_2 = "periodic_60_fixe_packet_size_30"
    file_name_3 = "periodic_60_fixe_packet_size_120"

    time, energies = extract_energy_from_file(file_name)
    write_to_csv(energies, time, 'data.csv')
    time, energies = extract_energy_from_file(file_name_2)
    write_to_csv(energies, time, 'data2.csv')
    time, energies = extract_energy_from_file(file_name_3)
    write_to_csv(energies, time, 'data3.csv')

    data = pd.read_csv("data.csv")
    data['Time'], data['Energy'] = smooth_data(data['Time'], data['Energy'])
    sns.lineplot(data=data, x='Time', y='Energy', label='period 60 & packet size 10')

    data2 = pd.read_csv("data2.csv")
    data2['Time'], data2['Energy'] = smooth_data(data2['Time'], data2['Energy'])
    sns.lineplot(data=data2, x='Time', y='Energy', label='period 60 & packet size 30')

    data3 = pd.read_csv("data3.csv")
    data3['Time'], data3['Energy'] = smooth_data(data3['Time'], data3['Energy'])
    sns.lineplot(data=data3, x='Time', y='Energy', label='period 60 & packet size 120')

    plt.xlabel('Time in seconds (s)')
    plt.ylabel('Energy in Joules (J)')
    plt.title('Energy consumption in function of time')
    plt.legend()
    plt.show()


def period_test():
    file_name = "periodic_10_packet_size_20_fixe"
    file_name_2 = "periodic_60_packet_size_20_fixe"
    file_name_3 = "periodic_300_packet_size_20_fixe"

    time, energies = extract_energy_from_file(file_name)
    write_to_csv(energies, time, 'data.csv')
    time, energies = extract_energy_from_file(file_name_2)
    write_to_csv(energies, time, 'data2.csv')
    time, energies = extract_energy_from_file(file_name_3)
    write_to_csv(energies, time, 'data3.csv')

    data = pd.read_csv("data.csv")
    data['Time'], data['Energy'] = smooth_data(data['Time'], data['Energy'])
    sns.lineplot(data=data, x='Time', y='Energy', label=' period 10 & packet size 20')

    data2 = pd.read_csv("data2.csv")
    data2['Time'], data2['Energy'] = smooth_data(data2['Time'], data2['Energy'])
    sns.lineplot(data=data2, x='Time', y='Energy', label='period 60 & packet size 20')

    data3 = pd.read_csv("data3.csv")
    data3['Time'], data3['Energy'] = smooth_data(data3['Time'], data3['Energy'])
    sns.lineplot(data=data3, x='Time', y='Energy', label='period 300 & packet size 20')

    plt.xlabel('Time in seconds (s)')
    plt.ylabel('Energy in Joules (J)')
    plt.title('Energy consumption in function of time')
    plt.legend()
    plt.show()



def coding_rate():
    filename = "coding_rate_1"
    filename2 = "coding_rate_2"
    filename3 = "coding_rate_3"
    filename4 = "coding_rate_4"

    time, energies = extract_energy_from_file(filename)
    write_to_csv(energies, time, 'data.csv')
    time, energies = extract_energy_from_file(filename2)
    write_to_csv(energies, time, 'data2.csv')
    time, energies = extract_energy_from_file(filename3)
    write_to_csv(energies, time, 'data3.csv')
    time, energies = extract_energy_from_file(filename4)
    write_to_csv(energies, time, 'data4.csv')

    data = pd.read_csv("data.csv")
    data['Time'], data['Energy'] = smooth_data(data['Time'], data['Energy'])
    sns.lineplot(data=data, x='Time', y='Energy', label=' coding rate 1')

    data2 = pd.read_csv("data2.csv")
    data2['Time'], data2['Energy'] = smooth_data(data2['Time'], data2['Energy'])
    sns.lineplot(data=data2, x='Time', y='Energy', label='coding rate 2')

    data3 = pd.read_csv("data3.csv")
    data3['Time'], data3['Energy'] = smooth_data(data3['Time'], data3['Energy'])
    sns.lineplot(data=data3, x='Time', y='Energy', label='coding rate 3')

    data4 = pd.read_csv("data4.csv")
    data4['Time'], data4['Energy'] = smooth_data(data4['Time'], data4['Energy'])
    sns.lineplot(data=data4, x='Time', y='Energy', label='coding rate 4')

    plt.xlabel('Time in seconds (s)')
    plt.ylabel('Energy in Joules (J)')
    plt.title('Energy consumption in function of time')
    plt.legend()
    plt.show()


def crc1():

    file_name = "coding_rate_1"
    file_name_2 = "cdr1_nocrc"

    time, energies = extract_energy_from_file(file_name)
    write_to_csv(energies, time, 'data.csv')
    time, energies = extract_energy_from_file(file_name_2)
    write_to_csv(energies, time, 'data2.csv')

    data = pd.read_csv("data.csv")
    data['Time'], data['Energy'] = smooth_data(data['Time'], data['Energy'])
    sns.lineplot(data=data, x='Time', y='Energy', label='coding rate 1 with CRC')

    data2 = pd.read_csv("data2.csv")
    data2['Time'], data2['Energy'] = smooth_data(data2['Time'], data2['Energy'])
    sns.lineplot(data=data2, x='Time', y='Energy', label='coding rate 1 without CRC')

    plt.xlabel('Time in seconds (s)')
    plt.ylabel('Energy in Joules (J)')
    plt.title('Energy consumption in function of time')
    plt.legend()
    plt.show()

def crc3():

    file_name = "coding_rate_3"
    file_name_2 = "cdr3_nocrc"

    time, energies = extract_energy_from_file(file_name)
    write_to_csv(energies, time, 'data.csv')
    time, energies = extract_energy_from_file(file_name_2)
    write_to_csv(energies, time, 'data2.csv')

    data = pd.read_csv("data.csv")
    data['Time'], data['Energy'] = smooth_data(data['Time'], data['Energy'])
    sns.lineplot(data=data, x='Time', y='Energy', label='coding rate 3 with CRC')

    data2 = pd.read_csv("data2.csv")
    data2['Time'], data2['Energy'] = smooth_data(data2['Time'], data2['Energy'])
    sns.lineplot(data=data2, x='Time', y='Energy', label='coding rate 3 without CRC')

    plt.xlabel('Time in seconds (s)')
    plt.ylabel('Energy in Joules (J)')
    plt.title('Energy consumption in function of time')
    plt.legend()
    plt.show()

def traffic_test_2():
    
    file_name = "coding_rate_2"
    file_name_2 = "cdr2_up"

    time, energies = extract_energy_from_file(file_name)
    write_to_csv(energies, time, 'data.csv')
    time, energies = extract_energy_from_file(file_name_2)
    write_to_csv(energies, time, 'data2.csv')

    data = pd.read_csv("data.csv")
    data['Time'], data['Energy'] = smooth_data(data['Time'], data['Energy'])
    sns.lineplot(data=data, x='Time', y='Energy', label='coding rate 2 without CONFIRMED')

    data2 = pd.read_csv("data2.csv")
    data2['Time'], data2['Energy'] = smooth_data(data2['Time'], data2['Energy'])
    sns.lineplot(data=data2, x='Time', y='Energy', label='coding rate 2 with CONFIRMED')

    plt.xlabel('Time in seconds (s)')
    plt.ylabel('Energy in Joules (J)')
    plt.title('Energy consumption in function of time')
    plt.legend()
    plt.show()

def traffic_test_3():

    file_name = "coding_rate_3"
    file_name_2 = "cdr3_up"

    time, energies = extract_energy_from_file(file_name)
    write_to_csv(energies, time, 'data.csv')
    time, energies = extract_energy_from_file(file_name_2)
    write_to_csv(energies, time, 'data2.csv')

    data = pd.read_csv("data.csv")
    data['Time'], data['Energy'] = smooth_data(data['Time'], data['Energy'])
    sns.lineplot(data=data, x='Time', y='Energy', label='coding rate 3 without CONFIRMED')

    data2 = pd.read_csv("data2.csv")
    data2['Time'], data2['Energy'] = smooth_data(data2['Time'], data2['Energy'])
    sns.lineplot(data=data2, x='Time', y='Energy', label='coding rate 3 with CONFIRMED')

    plt.xlabel('Time in seconds (s)')
    plt.ylabel('Energy in Joules (J)')
    plt.title('Energy consumption in function of time')
    plt.legend()
    plt.show()



if __name__ == '__main__':
    packet_size_test()
    period_test()
    coding_rate()
    crc1()
    crc3()
    traffic_test_2()
    traffic_test_3()