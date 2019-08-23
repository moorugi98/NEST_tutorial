# -*- coding: utf-8 -*-
import nest
import nest.raster_plot
import numpy as np
import pylab as plt

def load_spikedata_from_file(spikefile):
    """
    Loads spike data from spikefile and returns it as a numpy array

    Directly borrowed and trimmed from existing method in nest.raster_plot
    
    Returns:
        data    data is a matrix such that
                    data[:,0] is a vector of all gids and
                    data[:,1] a vector with the corresponding time stamps.
    """
    #try:
    if True:
        if nest.is_sequencetype(spikefile):
            data = None
            for f in fname:
                if data == None:
                    print ("Using loadtxt")
                    data = np.loadtxt(f)
                else:
                    print ("Using concatenate")
                    data = np.concatenate((data, np.loadtxt(f)))
        else:
            print ("Loading spike data for file: %s"%spikefile)
            data = np.loadtxt(spikefile)
        return data
    #except:
        print ("Error with loading spike data for file: %s"%spikefile)
        return None


def get_latencies(data,gids,times):
    """
    Params:
        data        data is a matrix such that
                    data[:,0] is a vector of all gids and
                    data[:,1] a vector with the corresponding time stamps.
        gids        list of global ids that we will extract events for
        times       time is a list with at most two entries such that
                    time=[t_max] extracts all events with t< t_max
                    time=[t_min, t_max] extracts all events with t_min <= t < t_max

    
    Returns:
        gids        a list gids of all neurons that spiked during this time 
        latencies   a list containing the corresponding latencies 
    """
    
    try:
        subset_events = nest.raster_plot.extract_events(data,time=times,sel=gids)
        firsts = {}
        for i in range(len(subset_events)):
            if firsts.has_key(subset_events[i][0]):
                continue
            firsts[subset_events[i][0]] = subset_events[i][1]
    except:
        print ("Error with extracting latencies")
        return None,None

    latency_gids = firsts.keys() # node ids that have appeared
    latencies = [firsts[d] for d in latency_gids]
    latency_gids = [int(g) for g in latency_gids]
    
    return latency_gids,latencies


def plot_degree_histogram(out_deg=None,in_deg=None,Norm=True):
    """
    Plot the histogram of in-degree and out-degree values
    
    Parameters
    ----------
    
    out_deg     - list - out degrees.
    in_deg      - list - in degrees.
    Norm        - boolean - if the histogram has to be normalized.
    """
    if out_deg!=None and in_deg!=None:
        ho,bo = np.histogram(out_deg,80)
        hi,bi = np.histogram(in_deg,80)
        if Norm:
            ho = ho*1./np.sum(ho)
            hi = hi*1./np.sum(hi)
        plt.figure(0)
        plt.clf()
        plt.plot(bo[:-1],ho,drawstyle='steps-mid',linewidth=3,color='r')
        plt.plot(bi[:-1],hi,drawstyle='steps-mid',linewidth=3,color='b')
        plt.legend(['out_deg','in_deg'],frameon=False,loc='best')
        plt.xlabel('Counts',fontsize=20)
        plt.ylabel('Frequency',fontsize=20)
    else:
        print ('\nPlot degree histogram:\tNothing to plot!')


def plot_Vm_traces(senders=None,times=None,potentials=None):
    """
    Plot the membrane potential traces
    
    Parameters
    ----------
    
    senders    - array - sender ids from multimeter.
    times      - array - sampling times from multimeter.
    potentials - array - membrane potential values from multimeter.
    """
    if senders is None and times is None and potentials is None:
        plt.figure(1)
        plt.clf()
        n = len(np.unique(senders))
        times = times[::n]
        vms = np.reshape(potentials,[len(potentials)/n,n])
        plt.plot(times,vms, color='gray')
        plt.plot(times,np.mean(vms,1), color='r',linewidth=3)
        plt.xlim(2000,2500)
        plt.xlabel('Time [ms]',fontsize=20)
        plt.ylabel('Potential [mV]',fontsize=20)
    else:
        print ('\nPlot Vm traces:\tNothing to plot!')


def plot_rate_sorted(senders=None,times=None):
    """
    Plot a spike raster with neurons sorted by rate.
    
    Parameters
    ----------
    
    senders    - array - sender ids from spike detector. 
    times      - array - spike times from spike detector.
    """
    if senders!=None and times!=None:
        plt.figure(2)
        plt.clf()
        alltimes = []       ## list of spike trains
        allcounts = []      ## spike count for each neuron
        for neuron in np.unique(senders):
            ntimes = times[senders == neuron]
            alltimes.append(ntimes)
            allcounts.append(len(ntimes))
        ind_allcounts_sorted=np.argsort(allcounts)
        for i,j in enumerate(ind_allcounts_sorted):
            plt.plot(alltimes[j], np.ones(allcounts[j])*i,'|',color='blue',markersize=3)
        #plt.xlim(2000,2500)
        plt.xlabel('Time [ms]',fontsize=20)
        plt.ylabel('Neuron #',fontsize=20)
        return allcounts
    else:
        print ('\nPlot rate sorted:\tNothing to plot!')
        return None


def plot_rate_histogram(count_vector=None,simtime=1e3,Norm=True):
    """
    Plot the histogram of the individual rates
    
    Parameters
    ----------
    
    count_vector - list - number of spikes per neuron. 
    simtime      - float - simulation time.
    Norm         - boolean -if the histogram has to be normalized.
    """
    if count_vector!=None:
        plt.figure(3)
        plt.clf()
        h,b = np.histogram(np.array(count_vector)*1e3/simtime,100)
        if Norm:
            plt.plot(b[:-1],h*1./np.sum(h),drawstyle='steps-mid',linewidth=3,color='b')
        else:
            plt.plot(b[:-1],h,drawstyle='steps-mid',linewidth=3,color='b')
        plt.xlabel('Rate [Hz]',fontsize=20)
        plt.ylabel('Counts',fontsize=20)
    else:
        print ('\nPlot rate vector:\tNothing to plot!')


def animate_raster_plot(pop, pos, events, ts_binwidth=50., simtime=2000., wuptime=1000.):
    """
    Show the animated raster plot.

    Parameters
    ----------

    pop    - list - neuron ids.
    pos    - array - positions of the neurons.
    events - dictionary - senders and times from spike detector.
    """
    gids, ts = events['senders'], events['times']
    ts_bins = np.arange(0., simtime+ts_binwidth, ts_binwidth) + wuptime
    plt.figure()
    for ts_idx in range(len(ts_bins)-1):
        plt.clf()
        gids_tmp = gids[(ts>ts_bins[ts_idx]) * (ts<=ts_bins[ts_idx+1])]
        pos_tmp = pos[np.searchsorted(pop, gids_tmp)]
        plt.plot(pos_tmp[:,0], pos_tmp[:,1], '.')
        plt.xlim(-.5, .5)
        plt.ylim(-.5, .5)
        plt.title("%s - %s" %(ts_bins[ts_idx], ts_bins[ts_idx+1]))
        plt.draw()



