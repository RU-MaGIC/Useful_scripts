import os, csv
import plotly.graph_objects as go
import plotly.io
import pandas as pd

def framer(index, path_list):
    ##Need a way to find the sample file names from the name?
    samplep='clust'+str(index)+'_p.txt'
    samplez='clust'+str(index)+'_z.txt'
    dfz=pd.read_csv(samplez, skiprows=2, sep='\t')# IPA adds 2 rows at the top- skip that shit
    dfp=pd.read_csv(samplep, skiprows=2, sep='\t')
    df=pd.merge(dfz, dfp, on='Canonical Pathways',how='outer', indicator=True, 
          suffixes=('_z', '_p')) #does the merge based on the canonical pathways column, adds suffixes to determine which is which
    keep_list = path_list
    df=df[df['Canonical Pathways'].str.contains('|'.join(keep_list))]
    return df

def dict_build(clust_numbers, path_list):
    d={}
    for i in range(0,clust_numbers-1):
        d["clust "+str(i)]=framer(i, path_list)
    return d


def imager(samples, pathways):
    d=dict_build(len(samples), pathways)
    for key in d.keys():
        pathways=d[key]['Canonical Pathways'] #gets the list of names of pathways
        fig=go.Figure() #initialize the figure
        
        for sample in samples:
            text=d[key][sample[0]+' '+str(key)+'_p']
            size=[]
            for i in range(0,len(d[key])):
                size.append(15)
            zscore=d[key][sample[0]+' '+str(key)+'_z']
            
            shape=[]
            for s in d[key][sample[0]+' '+str(key)+'_p']:
                if float(s) > 1.3: #1.3 is -log10(0.05)
                    shape.append('circle')
                else:
                    shape.append('triangle-down')
                
            colors=[]
            for i in range(0, len(d[key])):
                colors.append(str(sample[1]))
            fig.add_trace(go.Scatter(x=pathways,
                                    y=zscore,
                                    text=text,
                                    mode='markers',
                                    name=sample[0]+' '+str(key),
                                    marker=dict(
                                        color=colors,
                                        size= [x for x in size],
                                        symbol=shape,
                                    ),
                                    ))

        fig.update_layout(
            autosize=False,
            width=1000,
            height=750,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            ),
            paper_bgcolor="white",
            title="Pathway Enrichment",
            xaxis_title="IPA Pathway",
            yaxis_title="z-score",
            legend_title_text='Circles=p<0.05, triangles=p>0.05'
        )
        fig.show()   
        name=key
        plotly.offline.plot(fig, filename=name+'.html', auto_open=False)
        plotly.io.write_image(fig, name+'.jpg', format='jpeg')
        plotly.io.write_image(fig, name+'.pdf',format='pdf')
        plotly.io.write_image(fig, name+'.svg',format='svg')

imager([['SA','rgb(255, 65, 54)'],['AF','rgb(44, 160, 101)'],['NB','rgb(255, 144, 14)']],#sample name with colors per sample
       ['Th2','Th1','Cell Cycle','Death',
        'NRF2','Nitric Oxide','Neuroinflammation',
        'Exhaustion','Interferon','Stat3',
        'Coronavirus' #Just some keywords I looked for based on fun guesses and previous discussions
     ])

