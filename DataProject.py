import csv
import os
import pandas 
import matplotlib
import matplotlib.pyplot as plot
import seaborn as sb
import sys

# Get data from csv file & find last columns name
def get_data(csv_file):
    data_list = []
    data = pandas.read_csv(csv_file)
    
    # Iterate through the columns and check for numerical values in each column
    for column in data.columns:
        if pandas.to_numeric(data[column], errors='coerce').notnull().all():
            global data_column
            data_column = column
            break
    
    data_list.append(data)
    data_list.append(data_column)
    
    return data_list


# Sort the DataFrame based on the last column in ascending order    
def sort_data(data, data_column):
    sorted_data = data.sort_values(by=data_column, ascending=True)
    return sorted_data


def plot_data(sorted_data, graph_title, x_axis_data_column, x_axis_label, y_axis_label):
    x = sorted_data[x_axis_data_column]  
    y = sorted_data[data_column]
    num_rows = sorted_data.shape[0]
    num_columns = sorted_data.shape[1]
    figure_width = max(num_rows * 0.03, 14)  # Automates graph size based on rows/columns in csv file
    figure_height = max(num_columns * 0.5, 17)
    
    user_input = 'Bar' #change later
    
    if user_input == "Bar":
        plot.figure(figsize=(figure_width, figure_height))  # Graph Size
        plot.title(graph_title, fontsize=20, fontweight="bold")          
        plot.xlabel(x_axis_label, fontsize=18, fontweight="bold", labelpad=25)           
        plot.ylabel(y_axis_label, fontsize=18, fontweight="bold", labelpad=30)
        
        #plot.tight_layout()
        plot.subplots_adjust(top=0.93, bottom=0.28, left=0.15, right=0.85)
        plot.xticks(rotation=90, fontsize=16)
        plot.yticks(fontsize=14)
        
        plot.bar(x, y, width=0.85)
        
        
        
        
        #plot.grid(True)
        # values = sorted_data[data_column].tolist()
        # for i, value in enumerate(values):
        #     plot.text(value, i, str(value), ha='center', va='top')
            
        fig_name = "BarGraph.png"
        file_path = "/home/asyed_13/AaribProjects/DataProject/static/images/"
        
        plot.savefig(file_path + fig_name)
        
    elif user_input == "Pie":
        plot.pie(y, labels=x, radius=1.2, autopct="%0.01f%%", shadow=True)
        
        plot.savefig("Pie Graph")
        
    elif user_input == "Line":
        plot.xlabel("Industry Types/Households", fontsize=18)
        plot.ylabel(data_column, fontsize=16)
        plot.scatter(x, y)
        plot.plot(x, y)
        
        plot.savefig("Line Graph")
    
def main():
    
    if len(sys.argv) > 1:
        file_uploaded = sys.argv[1]   
        graph_title = sys.argv[2]
        x_axis_data_column = sys.argv[3]
        x_axis_label = sys.argv[4]
        y_axis_label = sys.argv[5]

    
    data = get_data(file_uploaded)
    sorted_data = sort_data(data[0], data[1])
    plot_data(sorted_data, graph_title, x_axis_data_column, x_axis_label, y_axis_label)

main()



