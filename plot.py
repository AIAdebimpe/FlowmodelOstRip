import pandas as pd
import numpy as np
from matplotlib import markers, axes, pyplot as plt
import os
pd.options.mode.chained_assignment = None

class makePlot():
    muw, munw, sigma = 0.821e-3, 0.838e-3, 57e-3
    lnetwork, absK, absK0 = 3.0035e-3, 2.7203e-12, 1.85e-12
    area = lnetwork**2
    lmean, rmean = 0.0001973, 2.2274e-05
    por = 0.2190

    def __init__(self, num, title,  results,
                 compWithLitData=False, compWithPrevData=False, drain=False, imbibe=False, exclude=None, include=None, hysteresis=False, includeTrapping=True):

        self.colorlist = ['g', 'c', 'y', 'm', 'k', 'b', 'lightcoral', 'lime',    
                          'navy', 'tomato', 'khaki', 'olive', 'gold', 'teal', 'darkcyan', 'tan', 'limegreen']
        self.markerlist = ['v', '^', '<', '>', 'p', 'P','d', 'D', 'h', 'H', 's', 'o', 'v', '^', 
                           's', 'v', 'o', '^',  'd', 'D', 'h', 'H']
        self.linelist = ['--', ':', '-.', '--', (0, (1, 1)), (0, (5, 10)), (0, (5, 1)), 
                         (0, (3, 1, 1, 1)), (0, (3, 10, 1, 10, 1, 10)), (0, (3, 1, 1, 1, 1, 1))]
        self.num = num
        self.title = title
        self.compWithLitData = compWithLitData
        self.compWithPrevData = compWithPrevData
        self.drain = drain
        self.imbibe = imbibe
        self.exclude = exclude
        self.include = include
        self.results = results
        self.hysteresis = hysteresis
        self.label = 'wt' if includeTrapping else 'nt'
        self.img_dir = "./result_images/"
        os.makedirs(os.path.dirname(self.img_dir), exist_ok=True)
        
        if self.drain:
            drainageBank(self)
        if self.imbibe:
            imbibitionBank(self)
            
    def pcSw(self):
        filename = self.img_dir+'Pc_vs_Sw_hysteresis_{}_{}_{}.png'.format(
            self.title, self.label, self.num)
        
        leg = []
        ind = 0 

        for val1 in self.results.keys():
            for val2 in self.results[val1].keys():
                res = self.results[val1][val2]
                print(res)
                plt.plot(res['satW'], res['capPres']/1000, '--v',
                         color=self.colorlist[ind], linewidth=1.5)
                #from IPython import embed; embed()
                leg.append(val1+'_'+val2)
                ind += 1
            
        plt.ylabel('Capillary Pressure(kPa)')
        plt.legend(leg)
        plt.ylim(0, 25)
        plt.xlim(0, 1)
        plt.xlabel('Sw')
        plt.savefig(filename, dpi=500)
        plt.close()

    def pcSw1(self):
        filename = self.img_dir+'Pc_vs_Sw_hysteresis_{}_{}_{}_wld.png'.format(
            self.title, self.label, self.num)
        
        leg = []
        ind = 0

        for val1 in self.results.keys():
            if val1 != 'Literature data':
                for val2 in self.results[val1].keys():
                    res = self.results[val1][val2]
                    print(res)
                    plt.plot(res['satW'], res['capPres']/1000, '--v',
                            color=self.colorlist[ind], linewidth=1.5)
                    #from IPython import embed; embed()
                    leg.append(val1+'_'+val2)
                    ind += 1
            else:
                res = self.results[val1]['pcSwDra']
                res1 = res.loc[res['source'] == 'MICP']
                res2 = res.loc[res['source'] != 'MICP']
                if not res1.empty:
                    plt.scatter(res1['satW'], res1['capPres']/1000, s=30, marker='o',
                                facecolors='none', edgecolors='b')
                    leg.append('MICP')
                if not res2.empty:
                    plt.scatter(res2['satW'], res2['capPres']/1000, s=30, marker='s',
                                facecolors='none', edgecolors='k')
                    #from IPython import embed; embed()
                    leg.append('Raeesi et al drainage')

                res = self.results[val1]['pcSwImb']
                res1 = res.loc[res['source'] == 'Raeesi']
                res2 = res.loc[res['source'] == 'Lin']
                if not res1.empty:
                    plt.scatter(res1['satW'], res1['capPres']/1000, s=30, marker='s',
                                facecolors='none', edgecolors='b')
                    leg.append('Raeesi et al imbibition')
                if not res2.empty:
                    plt.scatter(res2['satW'], res2['capPres']/1000, s=30, marker='d',
                                facecolors='none', edgecolors='r')
                    #from IPython import embed; embed()
                    leg.append('Lin et al')
                
            '''else:
                plt.plot(res['satW'], res['capPres']/1000, linestyle=self.linelist[ind], 
                         color=self.colorlist[ind], linewidth=2)
                leg.append(val)
                ind += 1'''
            
        plt.ylabel('Capillary Pressure(kPa)')
        plt.legend(leg)
        plt.ylim(0, 25)
        plt.xlim(0, 1)
        plt.xlabel('Sw')
        plt.savefig(filename, dpi=500)
        plt.close()

    
    def krSw(self):
        filename = self.img_dir+'kr_vs_Sw_hysteresis_{}_{}_{}.png'.format(
            self.title, self.label, self.num)
        
        leg = []
        j = 0

        for val1 in self.results.keys():
            for val2 in self.results[val1].keys():
                res = self.results[val1][val2]
                print(res)
                plt.plot(res['satW'], res['krw'], '--v',
                        color=self.colorlist[j], linewidth=1.5)
                plt.plot(res['satW'], res['krnw'], '--v',
                        color=self.colorlist[j], linewidth=1.5, label = '_nolegend_')
                #leg.append(val)
                #from IPython import embed; embed()
                leg.append(val1+'_'+val2)
                j += 1
            
        plt.ylabel('Relative Permeability')
        plt.legend(labels=leg)
        plt.xlabel('Sw')
        plt.xlim(0, 1.0)
        plt.ylim(0, 1.0)
        plt.savefig(filename, dpi=500)
        plt.close()

    def krSw1(self):
        filename = self.img_dir+'kr_vs_Sw_hysteresis_{}_{}_{}_wld.png'.format(
            self.title, self.label, self.num)
        
        leg = []
        j = 0

        for val1 in self.results.keys():
            if val1 != 'Literature data':
                for val2 in self.results[val1].keys():
                    res = self.results[val1][val2]
                    print(res)
                    plt.plot(res['satW'], res['krw'], '--v',
                            color=self.colorlist[j], linewidth=1.5)
                    plt.plot(res['satW'], res['krnw'], '--v',
                            color=self.colorlist[j], linewidth=1.5, label = '_nolegend_')
                    #leg.append(val)
                    #from IPython import embed; embed()
                    leg.append(val1+'_'+val2)
                    j += 1

            else:
                res = self.results[val1]['krSwDra']        
                plt.scatter(res['satW'], res['krw'], s=30, marker='s',
                    facecolors='none', edgecolors='k')
                leg.append('drainage Lit. data (krw)')
                plt.scatter(res['satW'], res['krnw'], s=30, marker='o',
                            facecolors='none', edgecolors='k')
                leg.append('drainage Lit. data (krnw)')

                res = self.results[val1]['krSwImb']        
                plt.scatter(res['satW'], res['krw'], s=30, marker='s',
                    facecolors='none', edgecolors='r')
                leg.append('imbibition Lit. data (krw)')
                plt.scatter(res['satW'], res['krnw'], s=30, marker='o',
                            facecolors='none', edgecolors='r')
                leg.append('imbibition Lit. data (krnw)')
                
            
        plt.ylabel('Relative Permeability')
        plt.legend(labels=leg)
        plt.xlabel('Sw')
        plt.xlim(0, 1.0)
        plt.ylim(0, 1.0)
        plt.savefig(filename, dpi=500)
        plt.close()


class drainageBank:
    def __init__(self, obj):
        self.obj = obj
        if self.compWithLitData:
            self.__compWithLitData__()
        if self.compWithPrevData:
            self.__compWithPrevData__()

    def __getattr__(self, name):
        return getattr(self.obj, name)

    def __compWithLitData__(self):
        self.results['Literature data'] = self.results.get('Literature data', {})
        
        self.results['Literature data']['pcSwDra'] = pd.read_csv(
            './results_csv/Exp_Results_Bentheimer_Drainage_Pc_Sw.csv',
            names=['source', 'satW', 'Pc', 'capPres'], sep=',',
            skiprows=1, index_col=False)
        
        self.results['Literature data']['krSwDra'] = pd.read_csv(
            './results_csv/Exp_Results_Bentheimer_Drainage_kr_Sw.csv',
            names=['satW', 'krw', 'krnw'], sep=',',
            skiprows=1, index_col=False)
        
        
        '''self.results['Valvatne et al.'] = pd.read_csv(
            './results_csv/pnflow_Bentheimer_Drainage_010725.csv',
            names=['satW', 'capPres', 'krw', 'krnw', 'RI'], sep=',',
            skiprows=1, index_col=False)'''
        
    def __compWithPrevData__(self):
        if self.include:
            todo = list(self.include)
        else:
            todo = np.arange(1, self.num).tolist()
            if self.exclude:
                todo = np.setdiff1d(todo, self.exclude).tolist()

        while True:
            try:
                n = todo.pop(0)
                self.results['model_'+str(n)] = pd.read_csv(
                    "./results_csv/FlowmodelOOP_{}_Drainage_{}.csv".format(self.title, n),
                    names=['satW', 'qWout', 'krw', 'qNWout', 'krnw', 'capPres', 'invasions'],
                    sep=',', skiprows=18, index_col=False)
            except FileNotFoundError:
                pass
            except IndexError:
                break


class imbibitionBank():
    def __init__(self, obj):
        self.obj = obj
        if self.compWithLitData:
            self.__compWithLitData__()
        if self.compWithPrevData:
            self.__compWithPrevData__()

    def __getattr__(self, name):
        return getattr(self.obj, name)
        
    def __compWithLitData__(self):
        self.results['Literature data'] = self.results.get('Literature data', {})
        
        self.results['Literature data']['pcSwImb'] = pd.read_csv(
            './results_csv/Exp_Results_Bentheimer_Imbibition_Pc_Sw.csv',
            names=['source', 'satW', 'Pc', 'capPres'], sep=',',
            skiprows=1, index_col=False)
        self.results['Literature data']['krSwImb'] = pd.read_csv(
            './results_csv/Exp_Results_Bentheimer_Imbibition_kr_Sw.csv',
            names=['satW', 'krw', 'krnw'], sep=',',
            skiprows=1, index_col=False)
        
        '''self.results['Valvatne et al.'] = pd.read_csv(
            './results_csv/pnflow_Bentheimer_Imbibition_010725.csv', names=[
                'satW', 'capPres', 'krw', 'krnw', 'RI'], sep=',', skiprows=1,
            index_col=False)'''
            
    def __compWithPrevData__(self):
        if self.include:
            todo = list(self.include)
        else:
            todo = np.arange(1, self.num).tolist()
            if self.exclude:
                todo = np.setdiff1d(todo, self.exclude).tolist()
        while True:
            try:
                n = todo.pop(0)
                self.results['model_'+str(n)] = pd.read_csv(
                    "./results_csv/FlowmodelOOP_{}_Imbibition_{}.csv".format(self.title, n),
                    names=['satW', 'qWout', 'krw', 'qNWout', 'krnw', 'capPres', 'invasions'],
                    sep=',', skiprows=18, index_col=False)
            except FileNotFoundError:
                pass
            except IndexError:
                break