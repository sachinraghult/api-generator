# api-generator
API Generator for Java using Python


## installation guide
pip install sqlalchemy psycopg2 pandas

## Abstract

In the rapidly evolving landscape of software development, efficient management of data access is a critical requirement for most applications. Typically, creating data access APIs, especially CRUD (Create, Read, Update, Delete) operations, consumes a significant amount of time and resources. Development teams often spend considerable effort manually writing these APIs, which can introduce redundancies and potential errors. This project proposes the development of an automated tool that connects directly to a database via its connection string, extracts the data model, and automatically generates fully functional CRUD APIs based on this model. The tool aims to streamline the API development process by eliminating the need for manual coding, thereby reducing development time, minimizing errors, and allowing developers to focus on more complex and value-added tasks. By automating the generation of live APIs for data access, the proposed solution enhances productivity and ensures consistency across the application’s data access layer.

## Problem Statement

The increasing complexity and size of modern applications necessitate a more efficient approach to managing data access operations. In traditional software development practices, developers are required to manually write CRUD APIs, which is a repetitive and time-consuming process. This manual approach not only leads to inefficiencies but also increases the risk of human error, inconsistencies, and delays in development cycles. The problem is exacerbated as the number of developers working on a project grows, further complicating the coordination and integration of these APIs. Therefore, there is a pressing need for an automated solution that can dynamically generate CRUD APIs by directly interfacing with the database. Such a tool would streamline the development process by automatically extracting the database schema, generating the corresponding APIs, and making them immediately available for use in the application. This would not only save significant time and resources but also ensure that the APIs are consistent, reliable, and easy to maintain.
