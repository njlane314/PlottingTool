import numpy as np
import matplotlib.pyplot as plt
import uproot
import awkward as ak
import seaborn as sns

class PlottingTools:
    
    def __init__(self):
        # Set font and style
        mpl.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
        mpl.rc('text', usetex=True)

        # Define colors as an instance variable
        self.colors = [
            '#E41A1C', '#377EB8', '#4DAF4A', '#FF7F00', '#984EA3', 
            '#A65628', '#F781BF', '#999999', '#8DD3C7', '#FFFFB3', 
            '#BEBADA', '#FB8072', '#80B1D3', '#FDB462', '#B3DE69', 
            '#FCCDE5', '#D9D9D9', '#BC80BD', '#CCEBC5', '#FFED6F'
        ]
    
    def stacked_histogram1D(self, data_list, case_names, rates_list, plotname, title, xlabel, ylabel, 
                            bins, total_events=1.0, loc='../', logx=False, logy=False):
       """
        Plots a stacked 1D histogram for a dataset.
    
        Parameters:
        - data_list (list of arrays): List of datasets.
        - case_names (list of str): Names for each dataset.
        - rates_list (list of float): List of rates to normalize each dataset.
        - plotname (str): Name of the file to save the plot.
        - title (str): Plot title.
        - xlabel, ylabel (str): Axis labels.
        - bins (array-like): Bin edges for histogram.
        - total_events (float): Total number of events, default to 1.0.
        - loc (str): Path location to save the plot, default to '../'.
        - logx (bool): Use logarithmic scale for x-axis, default to False.
        - logy (bool): Use logarithmic scale for y-axis, default to False.
        """
        fig, ax = plt.subplots(figsize=(9, 3.5))
        htotal = np.zeros(len(bins) - 1)
        
        for i, data in enumerate(data_list):
            h, _ = np.histogram(data, bins=bins)
            h = np.array(h) * rates_list[i] / total_events  
            ax.bar(bins[:-1], h, bottom=htotal, width=np.diff(bins), label=case_names[i],
                   color=self.colors[i % len(self.colors)], alpha=0.8, align='edge')    
            htotal += h
            ax.step(bins, np.append(htotal, htotal[-1]), where='post', color='black', lw=0.5)
    
        if logx:
            ax.set_xscale('log')
        if logy:
            ax.set_yscale('log')
        ax.legend(frameon=False, loc='best')
        ax.set_xlabel(xlabel)
        ax.set_xlim(bins[0], bins[-1])
        ax.set_ylabel(ylabel)
    
        ax.tick_params(which='both', direction='in', top=True, right=True, length=4)
        ax.tick_params(which='minor', length=2)
        ax.minorticks_on()
    
        ax.grid(which='both', linestyle=':', linewidth=0.5, color='gray', alpha=0.5)
    
        plt.tight_layout()
        plt.savefig(f"{loc}{plotname}", dpi=400)
        plt.show()

