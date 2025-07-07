# Welcome to the Tasty Tracker

###Introduction:

Unhealthy eating habits are a leading cause of global public health issues such as obesity and chronic diseases. Addressing these problems requires innovative approaches to guide individuals toward better food choices. The Healthy Food Recommender System is designed to tackle this challenge by providing users with personalized food recommendations that align with their taste preferences while promoting healthier alternatives. By leveraging advanced machine learning techniques, the system aims to encourage a gradual shift toward sustainable, nutritious diets.

Project Relevance:

Obesity rates and associated health issues are on the rise worldwide, emphasizing the urgent need for solutions that promote healthier eating behaviors. Recommendation systems have proven effective in influencing consumer decisions across various domains, including entertainment and e-commerce. This project extends that concept to nutrition, aiming to improve public health through better dietary choices. As well as increase user awareness of nutritional information available to them. An end goal would be to provide a scalable solution adaptable to diverse dietary needs and cultural preferences.

Installation Instructions:

With a replit account, click on new app.

Then select import from github. Paste the Github repolink when asked for.

Once you get to the configure you app page, it will ask for a command key, paste the following key.
```bash
streamlit run main.py --server.port 5000
```
Here's an example of what it should look like.

Some Unique Features:

Personalized Recommendations: For The purpose of making the project more unique, the recommendations will have text generated that explain the reasoning behind the chosen food option. Characteristics are asked from the user to take into consideration when looking what foods to suggest to them. Their personal food preferences and restrictions are core factors, but features like a personas bodily metics and personal food history will help more personalize the experience.

Food Consumption Analysis: There is an interest we have about using OpenAi to help summarize and find patterns in a users food history, to help create a mores specialized recommendation. An example of this system would be like suggesting movies on Netflix or product recommendations on amazon. The further use of Natural Language Processing (NLP) with Openai will help with tasks like creating recommendations with an appropriate analysis.

OpenAI: OpenAI is being tested for recommendation generation and analysis. Recommendations made by the program are from the local user data and an OpenAI explanation of the nutritional benefits of the recommendation. The prompt used in OpenAI for these recommendations use a person's food history logged onto a database and filters to form the most detail and accurate prompt to use in Open AI. Responses will need further testing for accuracy and reliability.  

Replit: Replit is an online coding platform that allows users to write, run, and share code directly from their web browser. It's widely used for learning, collaboration, and prototyping across various programming languages. For easy web deployment, I used Replit as resource to host the application. 

StreamLit: StreamLit is an open-source Python library that simplifies the process of building and deploying interactive web applications, specifically for data visualization and machine learning workflows. It’s designed for data scientists and developers who want to create powerful, user-friendly apps quickly without needing extensive web development knowledge. For my purposes, StreamLit is what Replit used to easily deploy my web app. The ease of getting my program on a web app was very really nice earlier into the project, it helped get me test the practical functionality of a web app without ever having built a web app. There would be future use of CSS to alter StreamLit's default styling settings, and would prove challenging 

NutritionIX API: I am using the NutritionIX API to get accurate nutrition stats for the food recommendation. It's usually used for logging foods eaten by the user in other apps. In this instance, will be using the API and NuritionIX database to return info for the recommendations made by the application. NuritionIX is trusted by and used in other diet tracking applications for its accuracy, making it a reliable tool to lean on for use in this project. The API can take a text description of a meal and return precise nutritional information, which works very well with how our app operates.

Spoonacular API: Another Tool I'll be using to verify the information given to me by the open model. Similar to the use of nutritionIX, I will be using Spoonacular to provide verified information for the recipe recommendation. For recipes, I'm looking not to just including nutrition stats for recipes, but also cook time and list of ingredients. Spoonacular is a trusted resource for integrate rich food, recipe, and nutrition data into various different applications. It provides over 2,600 ingredients with detailed nutrition data, price information, cooking tips, health insights, substitutions, and unit conversions.
