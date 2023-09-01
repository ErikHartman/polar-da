import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from typing import List


class PolarPlot:
    def __init__(
        self,
        fig: matplotlib.figure.Figure,
        ax: List[matplotlib.axes.Axes],
        values: np.ndarray,
        size: int = 1,
        colors = None,
        cmap: str = "coolwarm",
        alpha : float = 1,
        labels : List = None,
        label_offset : float = 0
    ) -> None:
        self.values = values
        self.size = size
        self.colors = colors
        self.cmap = cmap
        self.fig = fig
        self.axs = ax
        self.alpha = alpha
        self.labels = labels
        self.label_offset = label_offset

        if isinstance(ax, list):
            ax = np.array(ax)
        if not fig:
            self.fig = plt.figure(figsize=(5, 5))
            self.ax = self.fig.add_subplot(projection="polar")
            self.ax.grid(False)

    def plot(self):
        ngroups, npoints = self.values.shape

        if self.colors is None:
            self.colors = [1] * npoints

        thetas = [n * 2 * np.pi / ngroups for n in range(ngroups)]

        magnitudes = []
        angles = []

        for point in range(npoints):
            vals = self.values[:, point]

            complexes = [get_complex(vals[i], thetas[i]) for i in range(ngroups)]
            real = sum([v.real for v in complexes])
            imag = sum([v.imag for v in complexes])

            magnitutde = np.sqrt(real**2 + imag**2)

            angle = get_angle(real, imag)

            magnitudes.append(magnitutde)
            angles.append(angle)

        self.ax.scatter(
            angles, magnitudes, s=self.size, c=self.colors, cmap=self.cmap, alpha=self.alpha
        )
        self.ax.vlines(thetas, 0, [max(magnitudes)] * ngroups, color="gray")

        if self.cmap:
            cax = self.fig.add_axes([1.1, 0.1, 0.05, 0.8])
            plt.colorbar(
                matplotlib.cm.ScalarMappable(
                    norm=matplotlib.colors.Normalize(
                        vmin=min(self.colors), vmax=max(self.colors)
                    ),
                    cmap=self.cmap,
                ),
                cax=cax,
            )

        self.ax.set_xticks([2*i*np.pi/len(self.labels) for i in range(len(self.labels))], self.labels)
        
        self.rotate_labels(y_offset=self.label_offset)
        return self.fig, self.ax

    def rotate_labels(self, y_offset):
        angles = np.linspace(0, 2 * np.pi, len(self.ax.get_xticklabels()) + 1)
        angles[np.cos(angles) < 0] = angles[np.cos(angles) < 0] + np.pi
        angles = np.rad2deg(angles)

        labels = []
        for label, angle in zip(self.ax.get_xticklabels(), angles):
            x, y = label.get_position()
            lab = self.ax.text(
                x,
                y - y_offset,
                label.get_text(),
                transform=label.get_transform(),
                ha=label.get_ha(),
                va=label.get_va(),
            )
            lab.set_rotation(angle)
            labels.append(lab)
        self.ax.set_xticklabels([])


def get_angle(a, b):
    if a <= 0:
        return np.pi + np.arctan(b / a)
    return np.arctan(b / a)


def get_complex(magnitude, angle):
    return magnitude * np.cos(angle) + magnitude * 1j * np.sin(angle)
