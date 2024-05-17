import matplotlib.patches as mpatches


class Puck:
    def __init__(self, x, y, category, color, number, scale=1, font=10, zorder=11):
        self.x = x
        self.y = y
        self.category = category
        self.color = color
        self.number = number
        self.scale = scale
        self.font = font
        self.zorder = zorder

    def create_marker(self):
        if self.category == 'Mil-Mil (US)':
            return mpatches.RegularPolygon((self.x, self.y), numVertices=3, radius=0.12 * self.scale,
                                           orientation=-3.14 / 2, color=self.color, ec='black', lw=1,
                                           zorder=self.zorder)
        elif self.category == 'Mil-Mil (ROK)':
            return mpatches.Circle((self.x, self.y), 0.08 * self.scale, color=self.color, ec='black', lw=1,
                                   zorder=self.zorder)
        else:
            return mpatches.Rectangle((self.x - 0.06 * self.scale, self.y - 0.06 * self.scale), 0.12 * self.scale,
                                      0.12 * self.scale, color=self.color, ec='black', lw=1, zorder=self.zorder)

    def add_to_axes(self, ax):
        marker = self.create_marker()
        shadow = self.create_shadow()
        if shadow:
            ax.add_patch(shadow)
        ax.add_patch(marker)
        ax.text(self.x, self.y, str(self.number), fontsize=self.font, ha='center', va='center', color='white',
                fontweight='bold', zorder=self.zorder + 1)

    def create_shadow(self):
        shadow_color = (0, 0, 0, 0.3)  # black with 30% opacity
        if self.category == 'Mil-Mil (US)':
            return mpatches.RegularPolygon((self.x - 0.01 * self.scale, self.y - 0.01 * self.scale), numVertices=3,
                                           radius=0.12 * self.scale, orientation=-3.14 / 2, color=shadow_color,
                                           zorder=self.zorder - 1)
        elif self.category == 'Mil-Mil (ROK)':
            return mpatches.Circle((self.x - 0.01 * self.scale, self.y - 0.01 * self.scale), 0.08 * self.scale,
                                   color=shadow_color, zorder=self.zorder - 1)
        else:
            return mpatches.Rectangle((self.x - 0.07 * self.scale, self.y - 0.07 * self.scale), 0.12 * self.scale,
                                      0.12 * self.scale, color=shadow_color, zorder=self.zorder - 1)
