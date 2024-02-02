import pandas as pd
from plot import makePlot


num = 218
title = 'Bentheimer'
drain = False
imbibe = False
probable = True
hysteresis = True
includeTrapping = True


results = {'drainage':{}, 'imbibition':{}}
cycle=3
label = 'wt' if includeTrapping else 'nt'
for i in range(1,cycle+1):
    cycleLabel = 'cycle'+str(i)
    if includeTrapping:
        results['drainage'][label+'_'+cycleLabel] = pd.read_csv(
            './results_csv/Flowmodel_Bentheimer_Drainage_{}_wt_{}.csv'.format(
                cycleLabel, num), names=[
            'satW', 'qWout', 'krw', 'qNWout', 'krnw', 'capPres', 'invasions'],
            sep=',', skiprows=17, index_col=False)
        
        results['imbibition'][label+'_'+cycleLabel] = pd.read_csv(
            './results_csv/Flowmodel_Bentheimer_Imbibition_{}_wt_{}.csv'.format(
                cycleLabel, num), names=[
            'satW', 'qWout', 'krw', 'qNWout', 'krnw', 'capPres', 'invasions'],
            sep=',', skiprows=17, index_col=False)
    else:
        results['drainage'][label+'_'+cycleLabel] = pd.read_csv(
            './results_csv/Flowmodel_Bentheimer_Drainage_{}_nt_{}.csv'.format(
                cycleLabel, num), names=[
            'satW', 'qWout', 'krw', 'qNWout', 'krnw', 'capPres', 'invasions'],
            sep=',', skiprows=17, index_col=False)
        
        results['imbibition'][label+'_'+cycleLabel] = pd.read_csv(
            './results_csv/Flowmodel_Bentheimer_Imbibition_{}_nt_{}.csv'.format(
                cycleLabel, num), names=[
            'satW', 'qWout', 'krw', 'qNWout', 'krnw', 'capPres', 'invasions'],
            sep=',', skiprows=17, index_col=False)
        

#print(results)
#from IPython import embed; embed()


if drain:
    mkD = makePlot(num, title, drainage_results, True, True, True, False, include=None)
    mkD.pcSw()
    mkD.krSw()
if imbibe:
    mkI = makePlot(num, title, imbibition_results, True, True, False, True, include=None)
    mkI.pcSw()
    mkI.krSw()
if hysteresis:
    compWithLitData = True
    if not compWithLitData:
        mkH = makePlot(num, title, results, includeTrapping=includeTrapping)
        mkH.pcSw()
        mkH.krSw()
    else:
        mkH = makePlot(num, title, results, includeTrapping=includeTrapping, drain=True,
                       imbibe=True, compWithLitData=compWithLitData)
        mkH.pcSw1()
        mkH.krSw1()
    