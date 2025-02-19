import sys
import math
from typing import List, Tuple, Optional, Set, Deque


from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
    QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem,
    QVBoxLayout, QWidget, QPushButton, QInputDialog, QMessageBox, QHBoxLayout,
    QComboBox
)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QPainter, QBrush


from AStar import AStar
from Dijkstra import Dijkstra
from GrassFire import GrassFire
from Node import Node


# --------------------------------------------------
# PYQT5 APPLICATION
# --------------------------------------------------

class NetworkApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Builder - A*, Dijkstra, GrassFire")
        self.setGeometry(100, 100, 900, 600)

        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Buttons
        self.circle_button = QPushButton("Add Circle")
        self.line_button = QPushButton("Connect Circles")
        self.find_path_button = QPushButton("Find Path")

        button_layout.addWidget(self.circle_button)
        button_layout.addWidget(self.line_button)

        # Combo box to choose algorithm
        self.algorithm_box = QComboBox()
        self.algorithm_box.addItems(["AStar", "Dijkstra", "GrassFire"])
        button_layout.addWidget(self.algorithm_box)

        button_layout.addWidget(self.find_path_button)
        main_layout.addLayout(button_layout)

        # Graphics Scene/View
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.white)

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        main_layout.addWidget(self.view)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Data structures
        # circles: list of (circleItem, centerQPointF, circle_id, heuristic)
        self.circles: List[Tuple[QGraphicsEllipseItem, QPointF, int, float]] = []
        # lines: list of ( (startCircleData), (endCircleData), weight, lineItem, weightLabel )
        self.lines: List[
            Tuple[
                Tuple[QGraphicsEllipseItem, QPointF, int, float],
                Tuple[QGraphicsEllipseItem, QPointF, int, float],
                float,
                QGraphicsLineItem,
                QGraphicsTextItem
            ]
        ] = []

        self.circle_count: int = 0
        self.start_circle: Optional[Tuple[QGraphicsEllipseItem, QPointF, int, float]] = None
        self.current_mode: str = "circle"

        # Default pens
        self.circle_pen: QPen = QPen(Qt.black)
        self.line_pen: QPen = QPen(Qt.blue)

        # Connect signals
        self.circle_button.clicked.connect(self.set_circle_mode)
        self.line_button.clicked.connect(self.set_line_mode)
        self.find_path_button.clicked.connect(self.find_path)

    def set_circle_mode(self) -> None:
        self.current_mode = "circle"
        # QMessageBox.information(self, "Mode Changed", "You are now in 'Add Circle' mode.")

    def set_line_mode(self) -> None:
        self.current_mode = "line"
        # QMessageBox.information(self, "Mode Changed", "You are now in 'Connect Circles' mode.")

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            position = self.view.mapToScene(event.pos())
            if self.current_mode == "circle":
                self.create_circle(position)
            elif self.current_mode == "line":
                self.connect_circle(position)

    def create_circle(self, position: QPointF) -> None:
        self.circle_count += 1
        circle_id = self.circle_count

        # Ask for heuristic value (even if not used by BFS or Dijkstra,
        # we store it anyway)
        heuristic_value, ok = QInputDialog.getDouble(
            self,
            "Heuristic Value",
            f"Enter the heuristic value for circle #{circle_id}:",
            decimals=2
        )
        if not ok:
            self.circle_count -= 1
            return

        radius = 20
        x = position.x() - radius
        y = position.y() - radius

        circle_item = QGraphicsEllipseItem(x, y, 2 * radius, 2 * radius)
        circle_item.setPen(self.circle_pen)
        circle_item.setBrush(QBrush(Qt.white))
        self.scene.addItem(circle_item)

        # Label
        id_label = QGraphicsTextItem(str(circle_id))
        id_label.setDefaultTextColor(Qt.black)
        id_label.setPos(
            position.x() - id_label.boundingRect().width() / 2,
            position.y() - id_label.boundingRect().height() / 2
        )
        self.scene.addItem(id_label)

        center = QPointF(position.x(), position.y())
        self.circles.append((circle_item, center, circle_id, heuristic_value))

    def connect_circle(self, position: QPointF) -> None:
        # Find a circle near the position
        for circle_item, circle_center, circle_id, heuristic in self.circles:
            if self.distance(position, circle_center) <= 75:
                if not self.start_circle:
                    self.start_circle = (circle_item, circle_center, circle_id, heuristic)
                    QMessageBox.information(self, "Connect Circles", 
                                            "Select another circle to connect.")
                else:
                    end_circle = (circle_item, circle_center, circle_id, heuristic)
                    weight, ok = QInputDialog.getDouble(
                        self,
                        "Edge Weight",
                        f"Enter weight between circle #{self.start_circle[2]} and #{end_circle[2]}:",
                        decimals=2
                    )
                    if ok:
                        line = QGraphicsLineItem(
                            self.start_circle[1].x(), self.start_circle[1].y(),
                            end_circle[1].x(), end_circle[1].y()
                        )
                        line.setPen(self.line_pen)
                        self.scene.addItem(line)

                        # Weight label
                        line_center = QPointF(
                            (self.start_circle[1].x() + end_circle[1].x()) / 2,
                            (self.start_circle[1].y() + end_circle[1].y()) / 2
                        )
                        weight_label = QGraphicsTextItem(f"{weight:.2f}")
                        weight_label.setDefaultTextColor(Qt.red)
                        weight_label.setPos(
                            line_center.x() - weight_label.boundingRect().width() / 2,
                            line_center.y() - weight_label.boundingRect().height() / 2
                        )
                        self.scene.addItem(weight_label)

                        self.lines.append((self.start_circle, end_circle, weight, line, weight_label))

                        self.start_circle = None
                    return
        if not self.start_circle:
            QMessageBox.warning(self, "Invalid Selection", "Click near a circle to start.")

    @staticmethod
    def distance(p1: QPointF, p2: QPointF) -> float:
        return math.hypot(p1.x() - p2.x(), p1.y() - p2.y())

    def build_node_map(self) -> dict:
        """
        Build a dictionary {circle_id: Node} from the current circles and lines.
        Each circle becomes a Node; lines become neighbors.
        """
        node_map = {}
        # Create Node objects
        for circle_item, center, circle_id, heuristic in self.circles:
            node = Node(node_id=circle_id, h=heuristic)
            node_map[circle_id] = node

        # Add neighbors
        for (start_circ, end_circ, weight, line_item, label_item) in self.lines:
            s_id = start_circ[2]
            e_id = end_circ[2]
            node_s = node_map[s_id]
            node_e = node_map[e_id]
            node_s.neighbors.add((node_e, weight))
            node_e.neighbors.add((node_s, weight))  # undirected
        return node_map

    def reset_nodes_for_algorithm(self, node_map: dict, algorithm_name: str):
        """
        Reset each node's fields according to the chosen algorithm.
        """
        if algorithm_name == "AStar":
            for nd in node_map.values():
                nd.reset_for_astar()
        elif algorithm_name == "Dijkstra":
            for nd in node_map.values():
                nd.reset_for_dijkstra()
        elif algorithm_name == "GrassFire":
            for nd in node_map.values():
                nd.reset_for_grassfire()

    def find_path(self):
        if not self.circles:
            QMessageBox.warning(self, "No Circles", "No circles to build a path.")
            return
        if len(self.circles) < 2:
            QMessageBox.warning(self, "Not Enough Circles", "Need at least two circles.")
            return

        # Ask for start and goal
        start_id, ok1 = QInputDialog.getInt(self, "Start Node", "Enter the ID of the start node:")
        if not ok1:
            return
        end_id, ok2 = QInputDialog.getInt(self, "Goal Node", "Enter the ID of the goal node:")
        if not ok2:
            return

        # Build node map
        node_map = self.build_node_map()

        if start_id not in node_map or end_id not in node_map:
            QMessageBox.warning(self, "Invalid ID", "Start or goal ID doesn't exist.")
            return

        start_node = node_map[start_id]
        goal_node  = node_map[end_id]

        # Select algorithm
        algorithm_name = self.algorithm_box.currentText()
        self.reset_nodes_for_algorithm(node_map, algorithm_name)

        # Run chosen pathfinding
        if algorithm_name == "AStar":
            astar = AStar(start_node, goal_node)
            astar.run()
            path = astar.reconstruct_path()

        elif algorithm_name == "Dijkstra":
            dijk = Dijkstra(start_node, goal_node)
            dijk.run()
            path = dijk.reconstruct_path()

        elif algorithm_name == "GrassFire":
            bfs = GrassFire(start_node, goal_node)
            bfs.run()
            path = bfs.reconstruct_path()

        if not path or path[-1] != goal_node:
            QMessageBox.information(self, "No Path Found", "Could not reach the goal.")
            return

        # Highlight path
        self.highlight_path(path)

    def highlight_path(self, path_nodes: List[Node]):
        """
        Recolor the circles and edges on the path.
        path_nodes is a list of Node in order from start to goal.
        """
        # 1. Build a dict from node_id -> (circle_item, center, circle_id, heuristic)
        circle_dict = {
            cid: (circ, center, cid, h)
            for (circ, center, cid, h) in self.circles
        }

        # 2. Reset line colors
        for (start_circ, end_circ, weight, line_item, label_item) in self.lines:
            line_item.setPen(self.line_pen)

        # 3. Highlight edges in the path
        for i in range(len(path_nodes) - 1):
            n1 = path_nodes[i]
            n2 = path_nodes[i + 1]
            # Find line
            for (start_circ, end_circ, weight, line_item, label_item) in self.lines:
                s_id = start_circ[2]
                e_id = end_circ[2]
                if (s_id == n1.id and e_id == n2.id) or (s_id == n2.id and e_id == n1.id):
                    highlight_pen = QPen(Qt.red, 3)
                    line_item.setPen(highlight_pen)
                    break

        # 4. Highlight circles (start in green, end in yellow, mid in cyan)
        if path_nodes:
            start_node = path_nodes[0]
            end_node = path_nodes[-1]
            for node in path_nodes:
                if node.id in circle_dict:
                    (circle_item, _, _, _) = circle_dict[node.id]
                    if node == start_node:
                        circle_item.setBrush(QBrush(Qt.green))
                    elif node == end_node:
                        circle_item.setBrush(QBrush(Qt.yellow))
                    else:
                        circle_item.setBrush(QBrush(Qt.cyan))

    def closeEvent(self, event) -> None:
        # Optional: print graph info on close
        print("\nCircle Details:")
        for _, center, circle_id, heuristic in self.circles:
            print(f"ID: {circle_id}, Heuristic: {heuristic}, "
                  f"Pos=({center.x():.2f},{center.y():.2f})")

        print("\nLine Details:")
        for (start_circle, end_circle, weight, line_item, label_item) in self.lines:
            print(f"From Circle #{start_circle[2]} to #{end_circle[2]} "
                  f"Weight={weight:.2f}")
        super().closeEvent(event)


# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkApp()
    window.show()
    sys.exit(app.exec_())
