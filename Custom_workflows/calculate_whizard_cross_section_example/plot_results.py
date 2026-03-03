import pandas as pd
import matplotlib.pyplot as plt

# # Create DataFrame
# df = pd.read_csv("results.csv")

# print(df)

data = {
    "MC Type": [
        r"$e^+e^- \rightarrow \nu\bar{\nu}H[H \rightarrow b\bar{b}]$",
        r"$e^+e^- \rightarrow \mu^+\mu^-H[H \rightarrow b\bar{b}]$",
        r"$e^+e^- \rightarrow b\bar{b}H[H \rightarrow W^+W^-]$",
        r"$e^+e^- \rightarrow b\bar{b}H[H \rightarrow b\bar{b}]$"
    ],
    "Calc σ (pb)": [0.02686, 0.00394, 0.00636, 0.01729],
    "Err (pb)": [0.00035, 0.00005, 0.00010, 0.00022],
    "Central σ (pb)": [0.0269, 0.00394, 0.00645, 0.01745]
}

# Create DataFrame
df = pd.DataFrame(data)
# Set up plot
fig, ax = plt.subplots(figsize=(6, 6))

# Create x positions for each category
x_pos = range(len(df))

# Plot Calc σ with error bars
ax.errorbar(
    x_pos,
    df["Calc σ (pb)"],
    yerr=df["Err (pb)"],
    fmt='o',
    color='black',
    label="FLARE ± Err"
)

ax.set_xticks(x_pos)
ax.set_xticklabels(df["MC Type"], rotation=90, ha='center')

# Plot Central σ as red X's
ax.scatter(
    x_pos,
    df["Central σ (pb)"],
    color='red',
    marker='x',
    zorder=3,
    label="winter2023 (FCC)"
)
# ax.set_yscale("log")
# Labels and legend
ax.set_ylabel("Cross Section σ (pb)")
ax.set_title("Cross Sections for MC Types")
ax.legend()

fig.tight_layout()
fig.savefig("categorical_scatter_cross_sections.pdf")

# import pandas as pd
# import matplotlib.pyplot as plt

# # Use mathtext for LaTeX-style rendering
# plt.rcParams['mathtext.fontset'] = 'dejavusans'
# plt.rcParams['font.size'] = 12

# # Data with LaTeX-style MC Types
# data = {
#     "MC Type": [
#         r"$e^+e^- \rightarrow \nu\bar{\nu}H[H \rightarrow b\bar{b}]$",
#         r"$e^+e^- \rightarrow \mu^+\mu^-H[H \rightarrow b\bar{b}]$",
#         r"$e^+e^- \rightarrow b\bar{b}H[H \rightarrow W^+W^-]$",
#         r"$e^+e^- \rightarrow b\bar{b}H[H \rightarrow b\bar{b}]$"
#     ],
#     "Calc σ (pb)": [0.02686, 0.00394, 0.00636, 0.01729],
#     "Err (pb)": [0.00035, 0.00005, 0.00010, 0.00022],
#     "Central σ (pb)": [0.0269, 0.00394, 0.00645, 0.01745]
# }

# # Create DataFrame
# df = pd.DataFrame(data)

# # Set up horizontal plot
# fig, ax = plt.subplots(figsize=(8, 6))

# # Y positions for each category
# y_pos = range(len(df))

# # Horizontal error bars for Calc σ
# ax.errorbar(
#     x=df["Calc σ (pb)"],
#     y=y_pos,
#     xerr=df["Err (pb)"],
#     fmt='o',
#     color='black',
#     label="Calc σ ± Err"
# )

# # Plot Central σ as red dots
# ax.scatter(
#     df["Central σ (pb)"],
#     y_pos,
#     marker='x',
#     s=100, 
#     color='red',
#     zorder=3,
#     label="Central σ"
# )

# # Set y-ticks with LaTeX-formatted MC Type labels
# ax.set_yticks(y_pos)
# ax.set_yticklabels(df["MC Type"])

# # Labels and legend
# ax.set_xlabel(r"Cross Section $\sigma$ (pb)")
# ax.set_title("Cross Sections for MC Types")
# ax.legend()

# fig.tight_layout()
# fig.savefig('results.png')
