import matplotlib.patches as mpatches


class Puck:
    def __init__(self, category, color, x, y, x_add, y_add, radius):
        self.category = category
        self.mark = None
        if self.category == 'Mil-Mil (US)':
            self.mark = mpatches.RegularPolygon((x + x_add, y + y_add), numVertices=3, radius=radius,
                                                orientation=-3.14 / 2, color=color,
                                                ec='black', lw=1.5)
        elif self.category == 'Mil-Mil (ROK)':
            self.mark = mpatches.Circle((x + x_add, y + y_add), radius, color=color,
                                        ec='black', lw=1.5)
        else:
            self.mark = mpatches.Rectangle((x + x_add - radius, y + y_add - radius), radius * 2, radius * 2, color=color,
                                             ec='black', lw=1.5)

        self.shadow = mpatches.Shadow(self.mark, -0.1, -0.1, alpha=0.3)
