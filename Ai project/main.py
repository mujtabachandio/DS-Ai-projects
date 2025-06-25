from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,RunConfig
from colorama import init, Fore, Style
import time
import os
from datetime import datetime
import random
import webbrowser
import subprocess
import platform
import re

# Initialize colorama
init()

API = ""

external_cliet = AsyncOpenAI(
    api_key=API,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_cliet
)

config = RunConfig(
    model = model,
    model_provider = external_cliet,
    tracing_disabled=True
)

# Professional and versatile agent instructions
agent_instructions = """You are an advanced AI assistant with expertise across multiple domains including:
- Software Development (Frontend, Backend, Full-stack)
- Data Science and Machine Learning
- System Architecture and Design
- Best Practices and Code Optimization
- Problem Solving and Debugging
- Technical Documentation

Provide detailed, accurate, and professional responses. Include:
1. Clear explanations
2. Code examples when relevant
3. Best practices and considerations
4. Potential pitfalls to avoid
5. References to official documentation when applicable

Maintain a professional tone while being helpful and engaging. Focus on delivering high-quality, actionable information."""

agent = Agent(
    name="Advanced Technical Assistant",
    instructions=agent_instructions
)

def open_website(url):
    """Open a website in the default browser."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error opening website: {str(e)}{Style.RESET_ALL}")
        return False

def open_application(app_name):
    """Open a system application."""
    system = platform.system().lower()
    try:
        if system == 'windows':
            subprocess.Popen(['start', app_name], shell=True)
        elif system == 'darwin':  # macOS
            subprocess.Popen(['open', app_name])
        else:  # Linux
            subprocess.Popen([app_name])
        return True
    except Exception as e:
        print(f"{Fore.RED}Error opening application: {str(e)}{Style.RESET_ALL}")
        return False

def handle_system_command(command):
    """Handle system commands like opening websites or applications."""
    command = command.lower().strip()
    
    # Common website patterns
    website_patterns = {
        'google': 'google.com',
        'youtube': 'youtube.com',
        'github': 'github.com',
        'facebook': 'facebook.com',
        'twitter': 'twitter.com',
        'linkedin': 'linkedin.com',
        'instagram': 'instagram.com',
        'reddit': 'reddit.com',
        'amazon': 'amazon.com',
        'netflix': 'netflix.com'
    }
    
    # Common application patterns
    app_patterns = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'paint': 'mspaint.exe',
        'word': 'winword.exe',
        'excel': 'excel.exe',
        'powerpoint': 'powerpnt.exe',
        'chrome': 'chrome.exe',
        'firefox': 'firefox.exe',
        'edge': 'msedge.exe',
        'cmd': 'cmd.exe',
        'terminal': 'cmd.exe'
    }
    
    # Check for website commands
    for key, url in website_patterns.items():
        if f'open {key}' in command or f'launch {key}' in command:
            print(f"{Fore.GREEN}Opening {url}...{Style.RESET_ALL}")
            return open_website(url)
    
    # Check for application commands
    for key, app in app_patterns.items():
        if f'open {key}' in command or f'launch {key}' in command:
            print(f"{Fore.GREEN}Opening {key}...{Style.RESET_ALL}")
            return open_application(app)
    
    # Check for direct URL
    url_match = re.search(r'open\s+(https?://\S+|www\.\S+)', command)
    if url_match:
        url = url_match.group(1)
        print(f"{Fore.GREEN}Opening {url}...{Style.RESET_ALL}")
        return open_website(url)
    
    return False

def print_welcome():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.YELLOW}🤖 Advanced Technical Assistant")
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.WHITE}Session started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def print_thinking():
    print(f"\n{Fore.GREEN}Processing", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print(f"{Style.RESET_ALL}\n")

def print_help():
    print(f"\n{Fore.YELLOW}Available Commands:")
    print(f"{Fore.CYAN}  help    {Style.RESET_ALL}- Show this help message")
    print(f"{Fore.CYAN}  clear   {Style.RESET_ALL}- Clear the screen")
    print(f"{Fore.CYAN}  exit    {Style.RESET_ALL}- Exit the program")
    print(f"{Fore.CYAN}  time    {Style.RESET_ALL}- Show current session time")
    print(f"\n{Fore.YELLOW}System Commands:")
    print(f"{Fore.CYAN}  open [website]  {Style.RESET_ALL}- Open a website (e.g., 'open google')")
    print(f"{Fore.CYAN}  open [app]      {Style.RESET_ALL}- Open an application (e.g., 'open notepad')")
    print(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}\n")

def get_response_with_retry(question, max_retries=3, initial_delay=2):
    for attempt in range(max_retries):
        try:
            return Runner.run_sync(
                agent,
                input=question,
                run_config=config
            )
        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                delay = initial_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"{Fore.YELLOW}Model is busy. Retrying in {delay:.1f} seconds...{Style.RESET_ALL}")
                time.sleep(delay)
            else:
                raise e

print_welcome()
print_help()

while True:
    try:
        question = input(f"{Fore.YELLOW}Ask your question: {Style.RESET_ALL}")
        
        if question.lower() in ['exit', 'quit', 'bye']:
            print(f"\n{Fore.CYAN}Thank you for using Advanced Technical Assistant! Goodbye!{Style.RESET_ALL}\n")
            break
        elif question.lower() == 'help':
            print_help()
            continue
        elif question.lower() == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            print_welcome()
            continue
        elif question.lower() == 'time':
            print(f"\n{Fore.CYAN}Current session time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}\n")
            continue
        
        # Check for system commands first
        if handle_system_command(question):
            continue
            
        print_thinking()
        
        try:
            result = get_response_with_retry(question)
            print(f"{Fore.GREEN}Response: {Style.RESET_ALL}{result.final_output}\n")
        except Exception as e:
            if "503" in str(e):
                print(f"\n{Fore.RED}The model is currently overloaded. Please try again in a few moments.{Style.RESET_ALL}\n")
            else:
                print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}\n")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}Thank you for using Advanced Technical Assistant! Goodbye!{Style.RESET_ALL}\n")
        break
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}\n")
