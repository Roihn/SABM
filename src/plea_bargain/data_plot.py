import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Georgia'
plt.rcParams.update({'font.size': 12})

# TCU Test Plot
def plot_personalize(data, N, output_folder = "Output"):
    linestyle = ['--', '-', '-']
    marker = ['.', 'o', 's']
    color = ['black', 'red', 'blue']
    label = ['Simulation Mean Scores', 'Simulation 25th %tile', 'Simulation 75th %tile', 'Mean Scores', '25th %tile', '75th %tile']
    
    plt.rcParams['figure.figsize'] = (6, 12)
    for i in range(len(data)):
        x = ['Hostility', 'Risk Taking', 'Social Support']
        y = data[i]
        if i < 3: plt.plot(x, y, linestyle = linestyle[i % 3], marker = marker[i % 3], color = color[i % 3], label = label[i])
        else: plt.plot(x, y, linestyle = linestyle[i % 3], marker = marker[i % 3], color = color[i % 3], label = label[i], alpha = 0.35)
    
    plt.title(f'TCU Score Profiles (N = {N})')
    plt.xlabel('Item')
    plt.ylabel('Score')
    plt.legend(loc=0)
    plt.ylim((10, 50))
    plt.grid()
    
    plt.savefig(f"{output_folder}/TCU_Test_Result.png")
    plt.show(block=True)
    plt.close()

# Result Plot
def plot_decision(avg, x_label, y_label, group_num, situation_num, output_folder = "Output"):
    import matplotlib.ticker as mtick
    # 'Not Guilty', 'Guilty', 'Uncertain'
    linestyle = ['-', '-', '--']
    marker = ['D', '^', 's']
    color = ['gray', 'black', 'black']
    label = y_label[:group_num]

    for i in range(len(avg)):
        x = x_label[:situation_num]
        y = avg[i]
        if i < 3: plt.plot(x, y, linestyle = linestyle[i % 3], marker = marker[i % 3], color = color[i % 3], label = label[i])
        else: plt.plot(x, y, linestyle = linestyle[i % 3], marker = marker[i % 3], color = 'red', label = label[i], alpha = 0.35)
    
    fmt = '%.0f%%'
    yticks = mtick.FormatStrFormatter(fmt)
    plt.gca().yaxis.set_major_formatter(yticks)

    plt.title(f'')
    plt.xlabel('Probability of Conviction')
    plt.ylabel('WTAP Percentage')
    plt.ylim(bottom = 0)
    plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))
    plt.subplots_adjust(right=0.5, left=0.1)
    plt.grid(axis = 'y')

    fig = plt.gcf()
    fig.set_size_inches(8, 6)
    fig.set_dpi(300)
    
    plt.savefig(f"{output_folder}/decision_plot.png", dpi = 100)
    plt.show(block=True)
    plt.close()

def plot_decision_specific(avg, x_label, y_label, group_num, situation_num, specific_group_number, output_folder = "Output"):
    import matplotlib.ticker as mtick
    linestyle = ['-', '-', '--']
    marker = ['D', '^', 's']
    color = ['gray', 'black', 'black']
    label = y_label[specific_group_number - 1]

    for i in range(len(avg)):
        x = x_label[:situation_num]
        y = avg[i]
        if i < 3: plt.plot(x, y, linestyle = linestyle[i % 3], marker = marker[i % 3], color = color[i % 3], label = label)
        else: plt.plot(x, y, linestyle = linestyle[i % 3], marker = marker[i % 3], color = 'red', label = label, alpha = 0.35)
    
    fmt = '%.0f%%'
    yticks = mtick.FormatStrFormatter(fmt)
    plt.gca().yaxis.set_major_formatter(yticks)

    plt.title(f'')
    plt.xlabel('Probability of Conviction')
    plt.ylabel('WTAP Percentage')
    plt.ylim(bottom = 0)
    plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))
    plt.subplots_adjust(right=0.5, left=0.1)
    plt.grid(axis = 'y')

    fig = plt.gcf()
    fig.set_size_inches(8, 6)
    fig.set_dpi(300)
    
    plt.savefig(f"{output_folder}/decision_plot.png", dpi = 100)
    plt.show(block=True)
    plt.close()
