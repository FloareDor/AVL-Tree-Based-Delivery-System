# GatorGlide Delivery Co. Order Management System

## This project implements an efficient order management system for GatorGlide Delivery Co. using AVL balanced binary search trees. The system supports various operations such as creating orders, canceling orders, updating delivery times, and retrieving order information.
### Features

    Create new orders with specified ID, creation time, order value, and delivery duration.
    Cancel existing orders based on their ID and current time.
    Update the delivery time of an order.
    Print the details of a specific order.
    Print all orders within a given time range.
    Get the rank of an order (i.e., the number of orders that will be delivered before it).
    Deliver orders automatically when the current time reaches their estimated time of arrival (ETA).
    Handle edge cases and provide appropriate error messages.

### Implementation Details

### The system utilizes two AVL Balanced Binary Search Trees:

    Order Priority Tree: This tree stores the orders based on their priority, which is calculated using a weighted combination of the order value and the current time. It ensures efficient insertion, deletion, and retrieval of orders while maintaining a balanced structure.
    ETA Tree: This tree stores the orders based on their estimated time of arrival (ETA). It is used to efficiently deliver orders when the current time reaches their ETA and to update the ETAs of affected orders.

### The main operations supported by the system are:

    createOrder: Creates a new order with the given details and inserts it into the appropriate position in the AVL trees. It also updates the ETAs of affected orders and handles the delivery of orders that have already reached their ETA.
    cancelOrder: Cancels an order with the specified ID if it has not already been delivered. It removes the order from the AVL trees and updates the ETAs of affected orders.
    updateTime: Updates the delivery time of an order with the specified ID. It adjusts the ETA of the order and updates the ETAs of affected orders accordingly.
    print(orderId): Prints the details of a specific order.
    print(time1, time2): Prints all orders within a given time range.
    getRankOfOrder: Retrieves the rank of an order, indicating the number of orders that will be delivered before it.

### Usage

#### To use the GatorGlide Delivery Co. order management system:

    Ensure that you have Java, C++, or Python installed on your system.
    Compile the source code using the provided Makefile.
    Run the compiled executable with the input file as a command-line argument. For example:

    python gatorDelivery.py input.txt

    The program will process the commands from the input file and generate an output file with the same name as the input file, appended with _output_file.txt.
    Review the generated output file to see the results of the executed commands.

### Input Format

The input file should contain a series of commands, one per line. Each command should follow the specified format as mentioned in the assignment description.

The Quit() command should be the last command in the input file.
Output Format

```
createOrder(101, 2, 300, 4)
createOrder(102, 3, 600, 3)
print(101)
createOrder(103, 7, 200, 2)
createOrder(104, 8, 500, 3)
cancelOrder(102, 9)
createOrder(105, 10, 300, 4)
getRankOfOrder(105)
Quit()
```

### The output file will contain the results of the executed commands, with each result on a separate line. The format of the results will vary depending on the command, as specified in the assignment description.

```
Order 101 has been created - ETA: 6
Order 102 has been created - ETA: 13
[101, 2, 300, 4, 6]
Order 103 has been created - ETA: 18
Order 101 has been delivered at time 6
Order 104 has been created - ETA: 19
Updated ETAs: [103: 24]
Order 102 has been canceled
Updated ETAs: [104: 13, 103: 18]
Order 105 has been created - ETA: 24
Order 105 will be delivered after 2 orders.
Order 104 has been delivered at time 13
Order 103 has been delivered at time 18
Order 105 has been delivered at time 24
```

Author: Sai Ravi Teja G

UFID: 10504370

UF Email: gangavarapus@ufl.edu