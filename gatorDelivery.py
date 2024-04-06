# Author: Sai Ravi Teja G

from avlTree import AVL_BALANCED_BST
lastReturnTimestamp = 0
numOrders = 0

class OrderNode:
    """
    Represents a node in the AVL tree, storing the details of an order.
    """
    def __init__(self, id, created_at, order_value, deliveryTime, eta, priority):
        self.id = id
        self.created_at = created_at
        self.order_value = order_value
        self.deliveryTime = deliveryTime
        self.eta = eta
        self.priority = priority
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1
        self.test = 0
    
    def update_height(self):
        """
        Update the height of the node based on the heights of its left and right children.
        """
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = max(left_height, right_height) + 1
    
def main():
    tree = AVL_BALANCED_BST()
    nodes = {}  
    orders = {
        "eta": [],             
        "priority": [],         
        "ID": [],              
        "deliveryTime": [],    
        "status": [],
    }
    lastReturnTimestamp = 0
    numOrders = 0

    def calculatePriority(value, time, valueWeight=0.3, timeWeight=0.7):
        """
        Calculate the priority of an order based on its value and arrival time.
        """
        return valueWeight * value / 50 - timeWeight * time

    def printOrder(id):
        """
        Print the details of a specific order.
        """
        order = f"{id}, {nodes[id].created_at}, {nodes[id].order_value}, {nodes[id].deliveryTime}, {nodes[id].eta}"
        return f"[{order}]\n"

    def printOrdersInRange1(start, end):
        """
        Print all orders within a given time range.
        """
        result = ""
        print("numOrders", numOrders)
        for i in range(numOrders):
            print("i", i)
            if orders["eta"][i] > end:
                break
            elif orders["eta"][i] >= start:
                result += f"{orders['ID'][i]}, "
        
        if result:
            return f"[{result[:-2]}]\n" 
        else:
            return "No orders found in that time range\n"
    
    def printOrdersInRange(time1, time2):
        orderString = ""
        print(time1, time2, orders)
        for i in range(len(orders["ID"])):
            if orders["eta"][i] > time2:
                break
            elif orders["eta"][i] >= time1:
                orderString += f"{orders['ID'][i]}, "
        if len(orderString) > 0:
            return "["+orderString[:-2]+"]\n"
        else:
            return "There are no orders in that time period\n"
    
    def printOrdersInRange2(start_time, end_time):
        # Print orders within a specified time range
        order_string = ""
        print(len(orders["ID"]))
        for i in range(len(orders["ID"])):
            if orders["eta"][i] > end_time:
                break
            elif orders["eta"][i] >= start_time:
                order_string += f"{orders['ID'][i]}, "
        if len(order_string) > 0:
            return "[" + order_string[:-2] + "]\n"
        else:
            return "No orders found within the specified time range.\n"

    def getOrderRank(id):
        """
        Get the rank of an order, indicating the number of orders that will be delivered before it.
        """
        if id not in orders["ID"]:
            return ""
        
        index = orders["ID"].index(id)
        return f"Order {id} will be delivered after {index} orders.\n"

    def createNewOrder(id, currTime, value, deliveryDuration):
        """
        Create a new order with the given details and insert it into the AVL tree.
        Updates the ETAs of affected orders and handles the delivery of orders that have already reached their ETA.
        Returns a string with the status of the new order creation.
        """
        global numOrders, lastReturnTimestamp
        timestamp = max(currTime, lastReturnTimestamp)
        startIndex = 0
        delivered = {}

        for i in range(numOrders):
            if currTime >= orders["eta"][i]:
                orders["status"][i] = 2
                delivered[orders["ID"][i]] = orders["eta"][i]
                startIndex = i + 1
                timestamp = max(timestamp, orders["eta"][i] + orders["deliveryTime"][i]) 
                lastReturnTimestamp = orders["eta"][i] + orders["deliveryTime"][i]

            elif currTime >= orders["eta"][i] - orders["deliveryTime"][i]:
                orders["status"][i] = 1
                startIndex = i + 1
                timestamp = orders["eta"][i] + orders["deliveryTime"][i]
                lastReturnTimestamp = orders["eta"][i] + orders["deliveryTime"][i]
                break
            else:
                break
        
        priority = calculatePriority(value, currTime)
        insertIndex = numOrders
        for i in range(startIndex, numOrders):
            if priority > orders["priority"][i]:
                insertIndex = i
                break

        if insertIndex == startIndex:
            eta = timestamp + deliveryDuration
        else:
            prevEnd = orders["eta"][insertIndex-1] + orders["deliveryTime"][insertIndex-1]
            eta = prevEnd + deliveryDuration
        
        updated = {}
        prevEnd = eta + deliveryDuration
        for i in range(insertIndex, numOrders):
            currStart = orders["eta"][i] - orders["deliveryTime"][i]
            if currStart < prevEnd:
                offset = abs(prevEnd - currStart)
                orders["eta"][i] += offset
                updated[orders["ID"][i]] = orders["eta"][i]
            prevEnd = orders["eta"][i] + orders["deliveryTime"][i]
        
        result = f"Order {id} has been created - ETA: {eta}\n"

        if updated:
            updatedStr = ", ".join([f"{orderId}: {orderEta}" for orderId, orderEta in updated.items()])
            result += f"Updated ETAs: [{updatedStr}]\n"

        if delivered:
            for orderId, orderEta in delivered.items():
                result += f"Order {orderId} has been delivered at time {orderEta}\n"

        orders["ID"].insert(insertIndex, id)
        orders["eta"].insert(insertIndex, eta)
        orders["priority"].insert(insertIndex, priority)
        orders["deliveryTime"].insert(insertIndex, deliveryDuration)
        orders["status"].insert(insertIndex, 0)

        cutIndex = startIndex if startIndex == 0 or orders["status"][startIndex-1] == 2 else startIndex-1
        
        for i in range(cutIndex):
            removeKey = orders["priority"][i]
            removeId = orders["ID"][i]
            tree.remove_node(tree.root, removeKey, removeId)
            nodes[orders["ID"][i]] = None
            del nodes[orders["ID"][i]]
           
        for l in orders.values():
            del l[:cutIndex]

        newNode = OrderNode(id, currTime, value, deliveryDuration, eta, priority)
        tree.insert_node(tree.root, newNode)
        nodes[id] = newNode

        print(numOrders, cutIndex, "numOrders, cutIndex")
        numOrders = numOrders - cutIndex + 1

        return result

    def cancelOrderById(id, currTime):
        """
        Cancel an order with the specified ID if it has not already been delivered.
        Removes the order from the AVL tree and associated data structures.
        Updates the ETAs of affected orders.
        Returns a string with the status of the cancellation.
        """
        global numOrders, lastReturnTimestamp
        result = ""
        
        delivered = {}
        for i in range(numOrders):
            if currTime >= orders["eta"][i]:
                delivered[orders["ID"][i]] = orders["eta"][i]
            else:
                break
        
        if id not in nodes or currTime >= nodes[id].eta - nodes[id].deliveryTime:
            result += f"Cannot cancel. Order {id} has already been delivered.\n"
            
            if delivered:
                for orderId, orderEta in delivered.items():
                    result += f"Order {orderId} has been delivered at time {orderEta}\n"

                for l in orders.values():
                    del l[:len(delivered)]

                for orderId in delivered:
                    key = nodes[orderId].priority
                    nodeId = nodes[orderId].id 
                    nodes[orderId] = None
                    del nodes[orderId]
                    tree.remove_node(tree.root, key, nodeId)

                numOrders -= len(delivered)
                    
            return result
        
        index = orders["ID"].index(id)
        if index == numOrders - 1:
            for l in orders.values():
                del l[index]
            nodes[id] = None
            del nodes[id]
            numOrders -= 1
            return f"Order {id} has been canceled\n"
        
        timestamp = max(currTime, lastReturnTimestamp)
        if index >= 1:
            timestamp = max(timestamp, orders["eta"][index-1] + orders["deliveryTime"][index-1])

        updated = {}
        prevEnd = timestamp
        for i in range(index+1, numOrders):
            currStart = orders["eta"][i] - orders["deliveryTime"][i]
            if currStart > prevEnd:
                offset = abs(currStart - prevEnd)
                orders["eta"][i] -= offset
                updated[orders["ID"][i]] = orders["eta"][i]
            prevEnd = orders["eta"][i] + orders["deliveryTime"][i]

        result += f"Order {id} has been canceled\n"

        if updated:
            updatedStr = ", ".join([f"{orderId}: {orderEta}" for orderId, orderEta in updated.items()])
            result += f"Updated ETAs: [{updatedStr}]\n"

        if delivered:
            for orderId, orderEta in delivered.items():
                result += f"Order {orderId} has been delivered at time {orderEta}\n"
        
        for l in orders.values():
            del l[index]
            del l[:len(delivered)]
        
        key = nodes[id].priority
        nodeId = nodes[id].id
        nodes[id] = None
        del nodes[id]
        tree.remove_node(tree.root, key, nodeId)

        for orderId in delivered:
            key = nodes[orderId].priority 
            nodeId = nodes[orderId].id
            nodes[orderId] = None
            del nodes[orderId]
            tree.remove_node(tree.root, key, nodeId)

        numOrders -= (1 + len(delivered))

        return result
    
    def deliver_orders(self, current_time):
        delivered_orders = []
        while self.eta_tree.root and self.eta_tree.root.key == current_time:
            min_node = self.eta_tree.pop_min()
            if min_node:
                order = min_node.value
                order.delivered = True
                delivered_orders.append(order)
                # Remove the delivered order from the order_tree
                self.order_tree.delete(order.priority, order)
                # Remove the delivered order from the eta_tree
                self.eta_tree.delete(min_node.key, order)
                # Remove the delivered order from self.orders
                if order.order_id in self.orders:
                    del self.orders[order.order_id]
        output_msg = ""
        for ind, order in enumerate(delivered_orders):
            if ind == 0:
                output_msg += f"Order {order.order_id} has been delivered at time {order.eta}"
                # print("ind", ind, "output", output_msg)
            else:
                # print("ind000000", ind, "output", output_msg)
                output_msg +=  "\n" + f"Order {order.order_id} has been delivered at time {order.eta}"
            # if ind != 0:
            #     output_msg = "\n" + output_msg
            # print(output_msg)
            # print(f"Order {order.order_id} has been delivered at time {current_time}")
        self.current_time = current_time
        return output_msg

    def updateDeliveryTime(id, currTime, newDuration):
        """
        Update the delivery time of an order with the specified ID.
        Adjusts the ETA of the order and updates the ETAs of affected orders accordingly.
        Returns a string with the status of the update.
        """
        global numOrders
        result = ""
        
        delivered = {}
        for i in range(numOrders):
            if currTime >= orders["eta"][i]:
                delivered[orders["ID"][i]] = orders["eta"][i]
            else:
                break

        for l in orders.values():
            del l[:len(delivered)]
        
        numOrders -= len(delivered)

        for orderId in delivered:
            key = nodes[orderId].priority
            nodeId = nodes[orderId].id
            nodes[orderId] = None
            del nodes[orderId]
            tree.remove_node(tree.root, key, nodeId)
        
        if id not in nodes or currTime >= nodes[id].eta - nodes[id].deliveryTime:
            result += f"Cannot update. Order {id} has already been delivered.\n"
            
            if delivered:
                for orderId, orderEta in delivered.items():
                    result += f"Order {orderId} has been delivered at time {orderEta}\n"
            
            return result

        index = orders["ID"].index(id)
        offset = newDuration - orders["deliveryTime"][index]
        orders["eta"][index] += offset
        orders["deliveryTime"][index] = newDuration
        nodes[id].eta = orders["eta"][index]
        nodes[id].deliveryTime = newDuration

        updated = {}
        if offset != 0:
            updated[id] = orders["eta"][index]

        prevEnd = orders["eta"][index] + newDuration
        for i in range(index+1, numOrders):
            currStart = orders["eta"][i] - orders["deliveryTime"][i]
            offset = prevEnd - currStart
            orders["eta"][i] += offset
            nodes[orders["ID"][i]].eta += offset
            updated[orders["ID"][i]] = orders["eta"][i]
            prevEnd = orders["eta"][i] + orders["deliveryTime"][i]

        if updated:
            updatedStr = ", ".join([f"{orderId}: {orderEta}" for orderId, orderEta in updated.items()])
            result += f"Updated ETAs: [{updatedStr}]\n"
        
        if delivered:
            for orderId, orderEta in delivered.items():
                result += f"Order {orderId} has been delivered at time {orderEta}\n"
        
        return result

    def printAllRemainingOrders():
        result = ""
        for id, eta in zip(orders["ID"], orders["eta"]):
            result += f"Order {id} has been delivered at time {eta}\n"

        return result

    def processCommand(cmd):
        """
        Process a command from the input file and call the appropriate function.
        
        Args:
            cmd (str): The command string to be processed.
            
        Returns:
            str: The output string generated by the corresponding function.
        """
        parsed = cmd.strip().split('(') 
        cmdType = parsed[0]
        args = [arg.strip() for arg in parsed[1][:-1].split(",")]
        
        if cmdType == "print" and len(args) == 1:
            id = int(args[0])
            return printOrder(id)
        
        elif cmdType == "print" and len(args) == 2:
            start, end = map(int, args)
            return printOrdersInRange(start, end)
        
        elif cmdType == "getRankOfOrder" and len(args) == 1:
            id = int(args[0])
            return getOrderRank(id)
        
        elif cmdType == "createOrder" and len(args) == 4:
            id, currTime, value, duration = map(int, args)
            return createNewOrder(id, currTime, value, duration)
        
        elif cmdType == "cancelOrder" and len(args) == 2:
            id, currTime = map(int, args)
            return cancelOrderById(id, currTime)
        
        elif cmdType == "updateTime" and len(args) == 3:
            id, currTime, newDuration = map(int, args)
            return updateDeliveryTime(id, currTime, newDuration)

        else:
            print("Invalid command. Please try again.")
            return ""

    if __name__ == "__main__":
        import sys

        inputFile = sys.argv[1]
        base = inputFile[:-4]

        output = ""

        with open(inputFile, 'r') as f:
            cmd = f.readline()
            while not cmd.startswith("Quit()"):
                output += processCommand(cmd[:-1])
                cmd = f.readline()

        if cmd.startswith("Quit()"):
            output += printAllRemainingOrders()

        with open(f"{base}_output_file.txt", 'w') as f:
            f.writelines(output)

main()