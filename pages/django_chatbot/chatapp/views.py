import re
from sqlite3 import IntegrityError
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import auth
import requests
from django.contrib.auth.models import User
from .models import Chat
from django.urls import reverse
import speech_recognition as sr
from django.contrib.auth.decorators import login_required



api_key="Your_api_key"

# Create your views here.

def streamlit_view(request):
    """
    Renders the Streamlit HTML view.

    :param request: Django HTTP request object.
    :return: Rendered HTML response.
    """
    return render(request, 'streamlit.html')

# Function to interact with the AI chatbot API
def askAI(message):

    """
    Sends user's message to the AI chatbot it and returns the response.

    :param message: User's message.
    :type message: str
    :return: Response from the AI chatbot.
    :rtype: str
    """


    # Endpoint URL for the AI chatbot API
    url = "https://chatgpt-gpt4-ai-chatbot.p.rapidapi.com/ask"

    # Payload containing the user's query
    payload = {"query": message}

    # Headers required for accessing the API with RapidAPI key
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "chatgpt-gpt4-ai-chatbot.p.rapidapi.com"
    }

    # Making a POST request to the API
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response JSON and extract the generated text
        result = response.json()
        generated_text = result.get("response")
        return generated_text
    else:
        # Print error message if request fails
        print("Error:", response.text)
        return "Check your connection....."  # Return default response in case of error


def recognize_speech():

    """
    Recognizes speech from the user's microphone using Google Speech Recognition.

    :return: Recognized speech as text.
    :rtype: str
    """

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print("Recognized query:", query)
        return query
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Error fetching results; {0}".format(e))
        return None


# View function for the chatbot interface
@login_required
def chatbot(request):

    """
    Renders the chatbot interface and handles user interactions.

    :param request: Django HTTP request object.
    :return: Rendered HTML response.
    """

    if not request.user.is_authenticated:
        return redirect('login')
    # Load previous chat messages of the current user
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        # Handle POST request containing user message
        message = request.POST.get('message')
        if message.strip() == "":
            message = recognize_speech()
        response = askAI(message)  # Get AI response for the user's message
        # Save the user message and AI response to the database
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        # Return JSON response with user message and AI response
        return JsonResponse({'message': message, 'response': response})
    # Render the chatbot interface with previous chat messages
    return render(request, 'chatbot.html', {'chats': chats})

@login_required
def chat_history(request):

    """
    Renders the chat history page displaying previous conversations.

    :param request: Django HTTP request object.
    :return: Rendered HTML response.
    """

    chats = Chat.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'chat_history.html', {'chats': chats})

# View function for user login
def login(request):

    """
    Handles user login and renders the login page.

    :param request: Django HTTP request object.
    :return: Rendered HTML response.
    """

    if request.user.is_authenticated:
        return redirect('chatbot')
    
    
    if request.method == 'POST':
        # Handle POST request for user login
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            # If user is authenticated, login and redirect to chatbot interface
            auth.login(request, user)
            next_page = request.POST.get('next', reverse('chatbot'))
            return redirect(next_page)
        else:
            # If authentication fails, render login page with error message
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        # Render the login page for GET requests
        next_page = request.GET.get('next', reverse('chatbot'))
        return render(request, 'login.html')
 
# View function for user logout
@login_required
def logout_view(request):

    """
    Logs out the user and redirects to the login page.

    :param request: Django HTTP request object.
    :return: Redirect to login page.
    """

    auth.logout(request)  
    return redirect('login')  

# View function for user registration
def register(request):

    """
    Handles user registration and renders the registration page.

    :param request: Django HTTP request object.
    :return: Rendered HTML response.
    """

    if request.method == 'POST':
        # Handle POST request for user registration
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']


        # Check if the password meets the criteria
        if len(password1) < 6 or not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)', password1):
            error_message = 'Password must be at least 6 characters long and contain at least one alphabet and one number.'
            return render(request, 'register.html', {'error_message': error_message})


        if password1 == password2:
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                error_message = 'Username already exists.'
                return render(request, 'register.html', {'error_message': error_message})

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                error_message = 'Email is already registered.'
                return render(request, 'register.html', {'error_message': error_message})

            # Create the user with unique username and email
            try:
                user = User.objects.create_user(username, email=email, password=password1)
                auth.login(request, user)  # Login the newly registered user
                return redirect('chatbot')  # Redirect to the chatbot interface
            except IntegrityError:
                error_message = 'An error occurred while creating the user.'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            # Render the registration page with error message if passwords do not match
            error_message = 'Passwords do not match.'
            return render(request, 'register.html', {'error_message': error_message})

    else:
        # Render the registration page for GET requests
        return render(request, 'register.html')
