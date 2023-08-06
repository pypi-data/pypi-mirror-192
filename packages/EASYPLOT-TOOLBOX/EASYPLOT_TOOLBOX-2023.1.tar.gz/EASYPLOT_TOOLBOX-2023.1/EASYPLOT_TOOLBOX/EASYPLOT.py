import matplotlib.pyplot as plt
import seaborn as sns

def CONVERT_SI_TO_INCHES(WIDTH, HEIGHT):
    """ 
    This function convert figure dimensions from meters to inches.
    
    Input:
    WIDTH    |  Figure width in SI units       |         |  Float
    HEIGHT   |  Figure height in SI units      |         |  Float
    
    Output:
    WIDTH    |  Figure width in INCHES units   |         |  Float
    HEIGHT   |  Figure height in INCHES units  |         |  Float
    """
    
    # Converting dimensions
    WIDTH /= 0.0254
    HEIGHT /= 0.0254
    
    return WIDTH, HEIGHT

def SAVE_GRAPHIC(NAME, EXT, DPI):
    """ 
    This function saves graphics according to the selected extension.

    Input: 
    NAME  | Path + name figure               |         |  String
          |   NAME = 'svg'                   |         |  
          |   NAME = 'png'                   |         |
          |   NAME = 'eps'                   |         | 
          |   NAME = 'pdf'                   |         |
    EXT   | File extension                   |         |  String
    DPI   | The resolution in dots per inch  |         |  Integer
    
    Output:
    N/A
    """
    
    plt.savefig(NAME + '.' + EXT, dpi = DPI, bbox_inches = 'tight', transparent = True)

def HISTOGRAM_CHART(DATASET, PLOT_SETUP):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOT_TOOLBOX/
    """
    
    # Setup
    NAME = PLOT_SETUP['NAME']
    W = PLOT_SETUP['WIDTH']
    H = PLOT_SETUP['HEIGHT']
    X_AXIS_LABEL = PLOT_SETUP['X AXIS LABEL']
    X_AXIS_SIZE = PLOT_SETUP['X AXIS SIZE']
    Y_AXIS_LABEL = PLOT_SETUP['Y AXIS LABEL']
    Y_AXIS_SIZE = PLOT_SETUP['Y AXIS SIZE']
    AXISES_COLOR = PLOT_SETUP['AXISES COLOR']
    LABELS_SIZE = PLOT_SETUP['LABELS SIZE']     
    LABELS_COLOR = PLOT_SETUP['LABELS COLOR']
    CHART_COLOR = PLOT_SETUP['CHART COLOR']
    BINS = int(PLOT_SETUP['BINS'])
    KDE = PLOT_SETUP['KDE']
    DPI = PLOT_SETUP['DPI']
    EXT = PLOT_SETUP['EXTENSION']
    
    # Dataset and others information
    AUX = DATASET['DATASET']
    COLUMN = DATASET['COLUMN']
    DATA = AUX[COLUMN]
    
    # Plot
    [W, H] = CONVERT_SI_TO_INCHES(W, H)
    sns.set(style = 'ticks')
    FIG, (AX_BOX, AX_HIST) = plt.subplots(2, figsize = (W, H), sharex = True, gridspec_kw = {'height_ratios': (.15, .85)})
    sns.boxplot(x=DATA, ax = AX_BOX, color = CHART_COLOR)
    sns.histplot(DATA, ax = AX_HIST, kde = KDE, color = CHART_COLOR, bins = BINS)
    AX_BOX.set(yticks = [])
    AX_BOX.set(xlabel='')
    font = {'fontname': 'DejaVu Sans',
            'color':  LABELS_COLOR,
            'weight': 'normal',
            'size': LABELS_SIZE}
    AX_HIST.set_xlabel(X_AXIS_LABEL, fontdict = font)
    AX_HIST.set_ylabel(Y_AXIS_LABEL, fontdict = font)
    AX_HIST.tick_params(axis = 'x', labelsize = X_AXIS_SIZE, colors = AXISES_COLOR)
    AX_HIST.tick_params(axis = 'y', labelsize = Y_AXIS_SIZE, colors = AXISES_COLOR)
    plt.grid()
    sns.despine(ax = AX_HIST)
    sns.despine(ax = AX_BOX, left = True)
    
    # Save figure
    SAVE_GRAPHIC(NAME, EXT, DPI)