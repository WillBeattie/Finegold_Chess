import matplotlib
from matplotlib.ticker import ScalarFormatter

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd

plt.ion()


def plot_eval_against_frequency(df, detail=False):
    from matplotlib.ticker import ScalarFormatter

    fig, ax = plt.subplots(figsize=(8, 5))
    cmap = {'Double King Pawn': 'C0',
            'Double Queen Pawn': 'C1',
            'Sicilian': 'C2',
            'French': 'C3',
            'Caro-Kann': 'C4',
            'Gruenfeld': 'C5',
            'Indian Defences': 'C6',
            'Other 1. e4': 'C7',
            'Other 1. d4': 'C8',
            'Other': 'C9'}

    for eco_family, group in df.groupby('ECO Family'):
        group.plot.scatter(x='Number of Master Games', y='No f6 Delta', label=eco_family, ax=ax, c=cmap[eco_family],
                           alpha=0.5)

    ax.set_xscale('log')
    ax.set_ylim(-10, 250)
    ax.grid(':', alpha=0.5)
    ax.set_title('How much does the no-f6 rule hurt each opening?')
    ax.set_ylabel('Change in Evaluation if f6 is illegal (centipawns)')
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.ticklabel_format(style='plain', axis='x')
    plt.legend(title='Opening Family')

    if detail:
        from adjustText import adjust_text

        labeled_positions = [
            {'x': 46, 'y': 179 + 42, 'label': 'Vukovic Gambit'},
            {'x': 659, 'y': 111, 'label': "Exchange Ruy, King's Bishop"},
            {'x': 1240, 'y': 56, 'label': "Caro-Kann Panov"},
            {'x': 268, 'y': 83, 'label': "Petrov, Chigorin"},
            {'x': 8559, 'y': 84, 'label': "French, Closed Tarrasch"},
            {'x': 2922, 'y': 91, 'label': "KID Saemisch Gambit"},
            {'x': 219, 'y': 64, 'label': "KID Averbakh, 7. dxc5"},
            {'x': 391, 'y': 129, 'label': "Ruy Lopez, Dilworth"},
            {'x': 566, 'y': 83, 'label': "Exchange Gruenfeld, Spassky"},
            {'x': 1338, 'y': 71, 'label': "Budapest, Rubinstein"}
        ]
        ax.set_xlim(30, 30000)
        ax.set_ylim(50, 250)
        texts = [ax.text(pos['x'], pos['y'], pos['label'], fontsize=10) for pos in labeled_positions]

        adjust_text(texts, ax=ax, expand_text=(1.0, 1.3), arrowprops=dict(arrowstyle='-', color='black', lw=0.5, relpos=(0,0.5)))
    return ax


def opening_by_eco_code(code):
    family = code[0]
    num = int(code[1:])

    match family:
        case 'A':
            if num < 45 or num > 79:
                return 'Other'
            elif num < 50:
                return 'Other 1. d4'
            else:
                return 'Indian Defences'

        case 'B':
            if num < 10:
                return 'Other 1. e4'
            elif num < 20:
                return 'Caro-Kann'
            else:
                return 'Sicilian'

        case 'C':
            if num < 20:
                return 'French'
            else:
                return 'Double King Pawn'
        case 'D':
            if num < 70:
                return 'Double Queen Pawn'
            else:
                return 'Gruenfeld'
        case 'E':
            return 'Indian Defences'
        case _:
            raise ValueError(f'Invalid code: {code}')


def plot_eval_against_f6(df):
    fig, ax = plt.subplots(figsize=(8, 6))

    cmap = {'Double King Pawn': 'C0',
            'Double Queen Pawn': 'C1',
            'Sicilian': 'C2',
            'French': 'C3',
            'Caro-Kann': 'C4',
            'Gruenfeld': 'C5',
            'Indian Defences': 'C6',
            'Other 1. e4': 'C7',
            'Other 1. d4': 'C8',
            'Other': 'C9'}
    df['f6 frequency'] = 100 * df['Number of f6 moves'] / df['Number of Master Games']
    df = df[df['f6 frequency'] > 5]

    # for eco_family, group in df.groupby('ECO Family'):
    #    group.plot.scatter(x='f6 frequency', y='No f6 Delta', label=eco_family, ax=ax, c=cmap[eco_family], alpha=0.8)

    for i, row in df.iterrows():
        ax.scatter([row['f6 frequency']], [row['No f6 Delta']], label=row['ECO Name'])
    ax.set_xlabel('Frequency of ..f6 in master play (%)')
    ax.set_ylim(0, 120)
    ax.set_xlim(0, 100)
    ax.set_ylabel('Change in Evaluation if f6 is illegal (centipawns)')
    ax.grid(':', alpha=0.5)
    ax.set_title('When Masters Play f6, is it because they need to?')
    plt.legend(fontsize=9)
    plt.tight_layout()
    return ax


def load_df():
    df = pd.read_json('../results/ECO_w_Master_Games_Evaluated.json')
    df = df.T
    df = df[df['SF Eval'].notna()]  # Remove unevaluated positions
    df = df[df['No f6 Eval'].notna()]  # Remove unevaluated positions
    df['No f6 Delta'] = df['No f6 Eval'] - df['SF Eval']  # Add column for plotting
    df.sort_values('No f6 Delta', inplace=True, ascending=False)
    # df['ECO Family'] = df['ECO Code'].str[0]
    df['ECO Family'] = df['ECO Code'].apply(opening_by_eco_code)
    return df


if __name__ == "__main__":
    df = load_df()
    ax = plot_eval_against_frequency(df, detail=False)
    plt.tight_layout()
    plt.show()
