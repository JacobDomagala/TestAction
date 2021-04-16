import matplotlib.pyplot as plt
import argparse
import os
import requests
from datetime import date
import pandas as pd
import numpy as np
import textwrap

def prepare_data():
    templates_total_times = []
    templates = []

    with open('build_result.txt') as f:
        lines = f.read().splitlines()

        for idx, line in enumerate(lines):
            if line.startswith("**** Templates that took longest to instantiate:"):
                for template in lines[idx+1:idx+10]:
                    delimeter = template.index("ms")
                    templates_total_times.append(int(template[:delimeter]))
                    templates.append(template[delimeter+3:])
                break

    return templates, templates_total_times

def generate_graph(templates, templates_total_times):

    barWidth = 0.50
    fig, ax = plt.subplots(figsize=(19, 10))
    plt.subplots_adjust(left=0.05, bottom=0.6, right=0.95, top=0.95)
    plt.rc('font', size=9, family='serif')

    templates_total_times = [t//1000 for t in templates_total_times]
    TTT = templates_total_times

    # Add x, y gridlines
    ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)

    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)

    ax.invert_yaxis()

    yAxies = range(len(TTT))

    ax.barh(yAxies, TTT, height=barWidth, label ='total time (sec)')

    for idx, i in enumerate(ax.patches):
        plt.text(i.get_width()+0.2, i.get_y()+0.5, str(round((i.get_width()), 2)), fontsize = 10, fontweight ='bold', color ='gray')


    yTicks = range(len(TTT))
    plt.yticks([r for r in yTicks], yTicks)

    plt.legend()


    templates = [f"{idx}: {line}\n\n\n" for idx, line in enumerate(templates)]
    test = "".join(item for item in templates)

    fig.text(0.05, 0.01, f"{test}", wrap=True)


    plt.show()


def create_md_page():
    with open("test.md", "w") as f:
        f.write(f"### build history </br>\n"
        "[![](https://github.com/JacobDomagala/TestAction/wiki/build_status_badge.svg)](https://github.com/JacobDomagala/TestAction/wiki/build_times.png)\n"
        "</br>\n"
        "### Another section\n"
        "## Subsection\n"
        " Some interesting data </br>\n"
        "## Second Subsection\n"
        )

if __name__ == "__main__":
    templates, templates_total_times = prepare_data()
    generate_graph(templates, templates_total_times)
    create_md_page()
