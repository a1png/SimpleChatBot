### A Simple Chatbot Application
The application uses Django and Django-channels to mock an intelligent chat bot. 
#### To run the application:
to initialize the application, enter the application directory, and run
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```
then run
```
python manage.py runserver
```

then open http://localhost:8000/chat/chatpage/ on browser.

#### design of the application:
A database table UserInfo is created to record the user information input in the chat.

The records will be saved to the databse if the user has input complete information.

Chat contents are stored in a json file containing the chat content, the next chat to be sent and the field 
that the response for this chat content to be stored in the database. 
Chat contents are read in the memory on start up and stored as node object in ```ChatNode``` in a ```ChatFlow```object. 
(in ```Chat/ChatFlow.py```).

With the ChatNode class, we can parse the response from the client according to the rules of the field this node requires 
and give corresponding message whether success parsed or not.
Further extension can be pointing this Node to a knowledge graph and give diagnosis message.

With the ChatFlow class, we can navigate through the whole process of chat, give ChatNode needed in different situations. 
This class can be exntended by adding conditions to the node and give different following chat node according to the conditions.