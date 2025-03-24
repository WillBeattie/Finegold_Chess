import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd

plt.ion()


def load_df():
    df = pd.read_json('../results/ECO_w_Master_Games_Evaluated.json')
    df = df.T
    df = df[df['SF Eval'].notna()]  # Remove unevaluated positions
    df = df[df['No f6 Eval'].notna()]  # Remove unevaluated positions
    df['No f6 Delta'] = df['No f6 Eval'] - df['SF Eval']  # Add column for plotting
    df.sort_values('No f6 Delta', inplace=True, ascending=False)
    df['ECO Family'] = df['ECO Code'].str[0]
    return df


def plot_eval_against_frequency(df):
    fig, ax = plt.subplots()
    cmap = {'A': 'C0',
            'B': 'C1',
            'C': 'C2',
            'D': 'C3',
            'E': 'C4'}
    for eco_family, group in df.groupby('ECO Family'):
        group.plot.scatter(x='Number of Master Games', y='No f6 Delta', label=eco_family, ax=ax, c=cmap[eco_family],
                           alpha=0.5)

    ax.set_xscale('log')
    ax.set_ylim(-10, 250)
    ax.grid(':', alpha=0.5)
    ax.set_title('How much does the no-f6 rule hurt each opening?')
    ax.set_ylabel('Change in Evaluation if f6 is illegal (centipawns)')
    plt.legend(title='ECO Family')
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
    cmap = {'A': 'C0',
            'B': 'C1',
            'C': 'C2',
            'D': 'C3',
            'E': 'C4'}

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


if __name__ == "__main__":
    df = load_df()
    ax = plot_eval_against_frequency(df)
    plt.tight_layout()
    plt.show()
