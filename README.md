# RETAIL_DATA_ANALYSIS

Digitally enabled customers like to shop on the run, and that is the reason why online shopping is one of the most popular online activities worldwide. In 2019, global e-commerce sales amounted to 3.53 trillion USD and are projected to grow to 6.54 trillion USD in 2022.

The analytical capabilities of big data have had a positive impact across industries, including e-commerce. Big data tools improve business performance by enabling companies to analyse trends and current consumer behavioural patterns and offer better and more customised products.

For the purposes of this project, you have been tasked with computing various Key Performance Indicators (KPIs) for an e-commerce company, RetailCorp Inc. You have been provided real-time sales data of the company across the globe. The data contains information related to the invoices of orders placed by customers all around the world. You will get to know the details of the data in the next segment.
At the industry level, an end-to-end data pipeline is built for this purpose. Tools such as HDFS(Hadoop Distributed File System) are used to store the data that is processed by the real-time processing framework and then shown on a dashboard with tools such as Tableau and PowerBI. The image given below is an example of such a complete data pipeline.
<img width="909" alt="image" src="https://github.com/user-attachments/assets/4c018667-5cc6-4856-861d-925ef9abe61b">

For our project, we will be focusing on the ‘Order Intelligence’ part of this data pipeline. The image given below shows the architecture of the data pipeline that we will follow in this project.

<img width="785" alt="image" src="https://github.com/user-attachments/assets/3bdbd25c-5792-488d-9e04-81369b3da94e">

Broadly, you will perform the following tasks in this project:

  Reading the sales data from the Kafka server
  
  Preprocessing the data to calculate additional derived columns such as total_cost etc
  
  Calculating the time-based KPIs and time and country-based KPIs
  
  Storing the KPIs (both time-based and time- and country-based) for a 10-minute interval into separate JSON files for further analysis

![image](https://github.com/user-attachments/assets/68cebd61-4ba6-4e28-96ae-f0d253121bac)

As you can see, the data contains the following information:

    Invoice number: Identifier of the invoice
    
    Country: Country where the order is placed
    
    Timestamp: Time at which the order is placed
    
    Type: Whether this is a new order or a return order
    
    SKU (Stock Keeping Unit): Identifier of the product being ordered
    
    Title: Name of the product is ordered
    
    Unit price: Price of a single unit of the product
    
    Quantity: Quantity of the product being ordered

You will be using these columns to derive some additional columns as well, which will help you in calculating the KPIs. You will learn more about this in the next segment.
