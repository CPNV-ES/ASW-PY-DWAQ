# ASW-PY-DWAQ

Implémentation d'une infrastructure sur AWS depuis une base python

## Installation

### Requirements

| Name   | Version |
| ------ | ------- |
| Python | 3.9.5   |
| Pip    | 21.1.1  |
| Boto3 (SDK AWS) | 1.17.70 |
| Aws-Cli | 2.1.39 |

### Python

1. Download python [link](https://www.python.org/downloads/)
2. Check the case "Add Python 3.9 to PATH" and click on install now

### How to install boto

1. You need to run the command `pip install boto3`, for specific version `pip install boto3==1.17.70`

### Configure Aws-Cli
In our project we are using the default profile because a config file isn't implemented yet

1. Download Cli [link](https://aws.amazon.com/fr/cli/)
2. When it's installed run the command `aws configure`, you can modify the default profile by adding credientials given by your admin

## Testing

### Units Test
There is one unit for each class, you can run it to see if all the methods are working fine, after each test a tear down is made and delete all the changes in Aws Console.

### Integration test
This one is used to test the implementation of a Nat instance but it isn't finished yet. If you run the test you will have :
1. The main VPC
2. The 2 subnet atatched to the VPC
3. The internet gateway attached to the VPC
4. The Private/Public routes tables with correct routing (local & gateway for each) 

## Debugging

### Set break points
Be aware of async methods, if you want to break into it you need to precise by right clicking on the point and set it to Suspend All Threads. When doing that you can also set it to default if you think its a good idea.

![image](https://user-images.githubusercontent.com/36031708/122009805-be955180-cdba-11eb-84d9-70d7e4103ef7.png)

### Launching in debug mode
Click here to launch the test 
![image](https://user-images.githubusercontent.com/36031708/122014558-92300400-cdbf-11eb-9b38-ec9844a581b9.png)

And select debug 
![image](https://user-images.githubusercontent.com/36031708/122014642-a70c9780-cdbf-11eb-87a0-468dc4206b1b.png)



