import matplotlib.pyplot as plt
import argparse
import os
import requests
from datetime import date
import pandas as pd
import numpy as np

OUTPUT_DIR = os.getenv('INPUT_BUILD_STATS_OUTPUT')
EXP_TEMPLATE_DIR = f"{OUTPUT_DIR}/most_expensive_templates.png"
GRAPH_FILENAME = f"{OUTPUT_DIR}/{os.getenv('INPUT_GRAPH_FILENAME')}"
BADGE_FILENAME = f"{OUTPUT_DIR}/{os.getenv('INPUT_BADGE_FILENAME')}"

NUM_TOP_TEMPLATES = 15

def prepare_data():
    templates_total_times = []
    templates = dict()

    with open(f"{OUTPUT_DIR}/{os.getenv('INPUT_BUILD_RESULT_FILENAME')}") as f:
        lines = f.read().splitlines()

        for idx, line in enumerate(lines):
            if line.startswith("**** Templates that took longest to instantiate:"):
                for index, template in enumerate(lines[idx + 1 : idx + NUM_TOP_TEMPLATES]):
                    delimiter = template.index("ms")
                    templates_total_times.append(int(template[ : delimiter]))

                    tmp_text = template[delimiter + 3 : ]
                    end_of_template_name = tmp_text.index("(")
                    template_name = tmp_text[:end_of_template_name - 1]

                    times_and_avg = tmp_text[end_of_template_name + 1 : ]
                    times_used = int(times_and_avg[:times_and_avg.index(" ")])
                    avg_time = int(times_and_avg[times_and_avg.index("avg") + 3 : times_and_avg.index("ms")])

                    templates[index] = (template_name, times_used, avg_time)

                break

    print(templates)
    return templates, templates_total_times

def generate_graph(templates_total_times):

    SMALL_SIZE = 15
    MEDIUM_SIZE = 25
    BIGGER_SIZE = 35

    plt.rc('font', size=MEDIUM_SIZE, family='serif')
    plt.rc('axes', titlesize=MEDIUM_SIZE, labelsize=MEDIUM_SIZE)
    plt.rc('xtick', labelsize=MEDIUM_SIZE)
    plt.rc('ytick', labelsize=BIGGER_SIZE)
    plt.rc('legend', fontsize=BIGGER_SIZE)
    plt.rc('figure', titlesize=BIGGER_SIZE)

    barWidth = 0.50
    fig, ax = plt.subplots(figsize=(19, 14))

    templates_total_times = [t//1000 for t in templates_total_times]
    TTT = templates_total_times

    # Add x, y gridlines
    ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.8)

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
        plt.text(i.get_width()+0.2, i.get_y()+0.5, str(round((i.get_width()), 2)), fontsize = BIGGER_SIZE, color ='black')


    yTicks = range(len(TTT))
    plt.yticks([r for r in yTicks], yTicks)

    plt.legend()
    plt.tight_layout()

    plt.savefig(EXP_TEMPLATE_DIR)

def create_md_page(templates_text):
    html_table = "<details> <summary> See more </summary>"\
        "<table style=\"width:100%\">"\
        "<tr>"\
        "<th>Label </th>"\
        "<th>Name </th>"\
        "<th>Times </th>"\
        "<th>Avg (ms)</th>"\
        "</tr>"

    templates_string = "| Label | Name | Times | Avg (ms) |\n"\
        "|---|:---:|---|---|\n"
    for idx, (name, times, avg)  in templates_text.items():
        templates_string += f"| **{idx}** | `{name}` | **{times}** | **{avg}** |\n"

        # Change brackets to HTML friendly type
        name = name.replace("<", "&lt;").replace(">", "&gt;")
        html_table += f"<tr><td><b>{idx}</b></td>"\
            f"<td>{name}</td>"\
            f"<td><b>{times}</b></td>"\
            f"<td>{avg}</td></tr>"\

    html_table += "</table></details>"

    with open("Build_Stats.md", "w") as f:
        f.write(f"# Build History\n"
        f"[![](https://github.com/JacobDomagala/TestAction/wiki/{BADGE_FILENAME})](https://github.com/JacobDomagala/TestAction/wiki/{BADGE_FILENAME})\n"
        f"[![](https://github.com/JacobDomagala/TestAction/wiki/{GRAPH_FILENAME})](https://github.com/JacobDomagala/TestAction/wiki/{GRAPH_FILENAME})\n"
        "*** \n"
        "# Build stats\n"
        "## Templates that took longest to instantiate \n"
        f"[![](https://github.com/JacobDomagala/TestAction/wiki/{EXP_TEMPLATE_DIR})](https://github.com/JacobDomagala/TestAction/wiki/{EXP_TEMPLATE_DIR})\n"
        f"{templates_string}"
        "*** \n"
        f"{html_table}"
        )

if __name__ == "__main__":
    templates, templates_total_times = prepare_data()
    generate_graph(templates_total_times)
    create_md_page(templates)
