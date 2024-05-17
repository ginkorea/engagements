import matplotlib.patches as mpatches


class Puck:
    def __init__(self, x, y, category, color, number, scale=1):
        self.x = x
        self.y = y
        self.category = category
        self.color = color
        self.number = number
        self.scale = scale

    def create_marker(self):
        if self.category == 'Mil-Mil (US)':
            return mpatches.RegularPolygon((self.x, self.y), numVertices=3, radius=0.12 * self.scale,
                                           orientation=-3.14 / 2, color=self.color, ec='black', lw=1, zorder=11)
        elif self.category == 'Mil-Mil (ROK)':
            return mpatches.Circle((self.x, self.y), 0.08 * self.scale, color=self.color, ec='black', lw=1, zorder=11)
        else:
            return mpatches.Rectangle((self.x - 0.06 * self.scale, self.y - 0.06 * self.scale), 0.12 * self.scale,
                                      0.12 * self.scale, color=self.color, ec='black', lw=1, zorder=11)

    def add_to_axes(self, ax):
        marker = self.create_marker()
        shadow = self.create_shadow()
        if shadow:
            ax.add_patch(shadow)
        ax.add_patch(marker)
        ax.text(self.x, self.y, str(self.number), fontsize=10, ha='center', va='center', color='white',
                fontweight='bold', zorder=12)

    def create_shadow(self):
        shadow_color = (0, 0, 0, 0.3)  # black with 30% opacity
        if self.category == 'Mil-Mil (US)':
            return mpatches.RegularPolygon((self.x - 0.01 * self.scale, self.y - 0.01 * self.scale), numVertices=3,
                                           radius=0.12 * self.scale, orientation=-3.14 / 2, color=shadow_color,
                                           zorder=10)
        elif self.category == 'Mil-Mil (ROK)':
            return mpatches.Circle((self.x - 0.01 * self.scale, self.y - 0.01 * self.scale), 0.08 * self.scale,
                                   color=shadow_color, zorder=10)
        else:
            return mpatches.Rectangle((self.x - 0.07 * self.scale, self.y - 0.07 * self.scale), 0.12 * self.scale,
                                      0.12 * self.scale, color=shadow_color, zorder=10)
