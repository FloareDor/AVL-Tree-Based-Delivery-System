# Author: Sai Ravi Teja G

class AVL_BALANCED_BST:
    def __init__(self):
        self.root = None
        
    def insert_node(self, current_node, new_node):
        if not self.root:
            self.root = new_node
            current_node = self.root
        elif new_node.priority > current_node.priority:
            if current_node.right:
                self.insert_node(current_node.right, new_node)
            else:
                current_node.right = new_node
                new_node.parent = current_node
        else:
            if current_node.left:
                self.insert_node(current_node.left, new_node)
            else:
                current_node.left = new_node
                new_node.parent = current_node
        
        current_node.update_height()
        self.rebalance(current_node)

    def remove_node(self, current_node, priority, id):
        if not current_node:
            return
        
        elif current_node.id == id:
            parent = current_node.parent
            if not current_node.left:
                if not parent:
                    if not current_node.right:
                        self.root = None
                    else:
                        self.root = current_node.right
                        current_node.parent = None
                else:
                    if not current_node.right:
                        if parent.left == current_node:
                            parent.left = None
                        else:
                            parent.right = None
                    else:
                        if parent.left == current_node:
                            parent.left = current_node.right
                            current_node.right.parent = parent
                            tree_bro = 3
                        else:
                            parent.right = current_node.right
                            current_node.right.parent = parent
                            tree_bro = 10
                current_node = current_node.right

            elif not current_node.right:
                parent = current_node.parent
                if not parent:
                    self.root = current_node.left
                    current_node.left.parent = None
                else:
                    if parent.left == current_node:
                        parent.left = current_node.left
                        current_node.left.parent = parent
                    else:
                        parent.right = current_node.left
                        current_node.left.parent = parent
                current_node = current_node.left

            else:
                min_node = self.find_min(current_node.right)
                self.swap_nodes(current_node, min_node)
                self.remove_node(current_node, priority, id)
        
        elif priority > current_node.priority:
            self.remove_node(current_node.right, priority, id)
        else:
            self.remove_node(current_node.left, priority, id)
        
        if current_node:
            current_node.update_height()
            self.rebalance(current_node)

    # def get_eta(self, order):
    #     if not self.eta_tree.root:
    #         return order.current_system_time + order.delivery_time
    #     else:
    #         prev_order = self.order_tree.get_next(order.priority)

    #         if prev_order:
    #             prev_eta = self.eta_tree.find_by_order_id(prev_order.value.order_id)
    #             if prev_eta:
    #                 return prev_eta.value.eta + prev_order.value.delivery_time + order.delivery_time
    #             else:
    #                 return order.current_system_time + order.delivery_time
    #         else:
    #             print(111111111111111111)
    #             return order.current_system_time + order.delivery_time

    def rotate_right(self, node_a, node_b):
        parent = node_a.parent

        left_child_b = node_b.left
        node_b.left = node_a
        node_a.parent = node_b
        node_a.right = left_child_b
        if left_child_b:
            left_child_b.parent = node_a
        node_b.parent = parent

        node_a.update_height()
        node_b.update_height()

        if not parent:
            self.root = node_b
        elif parent.left == node_a:
            parent.left = node_b
            parent.update_height()
        elif parent.right == node_a:
            parent.right = node_b
            parent.update_height()

    def rotate_left(self, node_a, node_b):
        parent = node_a.parent

        right_child_b = node_b.right
        node_b.right = node_a
        node_a.parent = node_b
        node_a.left = right_child_b
        if right_child_b:
            right_child_b.parent = node_a
        node_b.parent = parent

        node_a.update_height()
        node_b.update_height()

        if not parent:
            self.root = node_b
        elif parent.left == node_a:
            parent.left = node_b
            parent.update_height()
        elif parent.right == node_a:
            parent.right = node_b
            parent.update_height()

    def rotate_right_left(self, node_a, node_b, node_c):
        self.rotate_left(node_b, node_c)
        self.rotate_right(node_a, node_c)

    def rotate_left_right(self, node_a, node_b, node_c):
        self.rotate_right(node_b, node_c)
        self.rotate_left(node_a, node_c)
    
    def rebalance(self, current_node):
        if not current_node:
            return
        if self.get_balance_factor(current_node) < -1:
            if self.get_balance_factor(current_node.right) == 1:
                self.rotate_right_left(current_node, current_node.right, current_node.right.left)
            else:
                self.rotate_right(current_node, current_node.right)

        elif self.get_balance_factor(current_node) > 1:
            if self.get_balance_factor(current_node.left) == -1:
                self.rotate_left_right(current_node, current_node.left, current_node.left.right)
            else:
                self.rotate_left(current_node, current_node.left)

    @staticmethod
    def get_balance_factor(node):
        if not node.left and not node.right:
            return 0
        elif not node.left:
            return -node.right.height
        elif not node.right:
            return node.left.height
        else:
            return node.left.height - node.right.height
        
    @staticmethod
    def find_min(node):
        while node.left:
            node = node.left
        return node
    
    @staticmethod
    def swap_nodes(node_a, node_b):
        node_a.id, node_b.id = node_b.id, node_a.id
        node_a.created_at, node_b.created_at = node_b.created_at, node_a.created_at 
        node_a.order_value, node_b.order_value = node_b.order_value, node_a.order_value
        node_a.deliveryTime, node_b.deliveryTime = node_b.deliveryTime, node_a.deliveryTime
        node_a.eta, node_b.eta = node_b.eta, node_a.eta
        node_a.priority, node_b.priority = node_b.priority, node_a.priority