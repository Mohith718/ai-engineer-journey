def safe_process_lead(form):
    try:
        name=form["name"]
        email=form["email"]
        score=int(form["score"])
        if score<0:
            raise ValueError("Score cannot be negative")
        return f"{name} ({email}) — Score: {score}"
    except KeyError as e:
        return f"Missing field: {e}"
    except ValueError as e:
        return f"Bad data: {e}"
    except Exception as e:
        return e
good = {"name": "Arjun", "email": "arjun@redsage.in", "score": "85"}        # works fine
missing = {"name": "Sneha", "email": "sneha@fractal.ai"}                      # no score key → KeyError
bad_score = {"name": "Vikram", "email": "vik@deccan.com", "score": "-10"}     # negative → ValueError

print(safe_process_lead(good))
print(safe_process_lead(missing))
print(safe_process_lead(bad_score))

def greet(name):
    return f"Hello, {name}"

def shout(func):
    result = func("Mohith")
    return result.upper()

print(shout(greet))

def greet(name):
    return f"Hello, {name}"

def make_loud(func):
    def wrapper(name):
        result = func(name)
        return result.upper()
    return wrapper

loud_greet = make_loud(greet)
print(loud_greet("Mohith"))

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            return None
    return wrapper

@error_handler
def divide(a, b):
    return a / b

print(divide(10, 2))
print(divide(10, 0))

Your decorator from before — already done, don't change it
def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            return None
    return wrapper

# Just write a normal function with @ on top
@error_handler
def process_lead(data):
    # extract name, email, score
    # return formatted string
    name=data["name"]
    email=data["email"]
    score=data["score"]
    return f"{name} - {email} - {score}"

# Test it
good = {"name": "Arjun", "email": "arjun@redsage.in", "score": 85}
broken = {"name": "Sneha"}
print(process_lead(good))
print(process_lead(broken))

def logger(func):
    def wrapper(*args,**kwargs):
        print(f"Calling {func.__name__}...") 
        r=func(*args,**kwargs)
        print(f"Finished {func.__name__}")
        return r
    return wrapper
    
@logger
def greet(name):
    return f"Hello, {name}"

@logger
def add(a, b):
    return a + b

print(add(5, 3))
print(greet("Mohith"))

def retry(func):
    def wrapper(*args,**kwargs):
        try:
            re=func(*args,**kwargs)
            return re
        except Exception as e:
            print("Attempt failed, retrying...")
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print("Failed after 2 attempts")
                return None
    return wrapper
count = 0
@logger
@retry
def flaky_function():
    global count
    count += 1
    if count < 2:
        raise ValueError("Random failure")
    return "Success!"
def fetch_lead(url):
    # return a dictionary with name and source url
    return f"{__name__},{url}"

print(fetch_lead("https://api.example.com/leads"))
print(flaky_function())