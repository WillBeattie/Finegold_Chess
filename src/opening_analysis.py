import matplotlib.pyplot as plt
import pandas as pd

plt.ion()


def load_df():
    df = pd.read_json('../results/test.json')
    df = df.T
    df = df[df['SF Eval'].notna()]  # Remove unevaluated positions
    df = df[df['No f6 Eval'].notna()]  # Remove unevaluated positions
    df['No f6 Delta'] = df['No f6 Eval'] - df['SF Eval']  # Add column for plotting

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
        group.plot.scatter(x='Number of Master Games', y='No f6 Delta', label=eco_family, ax=ax, c=cmap[eco_family], alpha=0.5)

    ax.set_xscale('log')
    ax.set_ylim(-10, 150)
    ax.grid(':', alpha=0.5)
    plt.legend(title='ECO Family')
    return ax


def plot_eval_against_f6(df):
    return


if __name__ == "__main__":
    df = load_df()
    ax = plot_eval_against_frequency(df)
    plt.savefig('../results/test2.png')
