import re 
import math
import hashlib
import requests

#basic validation:
def genral_validation(password):
    score=0 #Function Score 
    
    size=len(password)
    upper=re.search(r'[A-Z]',password)
    lower=re.search(r'[a-z]',password)
    digit=re.search(r'[0-9]',password)
    speical=re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    
    feedback=[]
    
    #Size points 
    if size > 12:
        score+=3
    elif size > 8 and size < 12:
        score+=2
    elif size == 8:
        score+=1
    else:
        feedback.append("Password should be at least 8 characters long.")
    #max point:3
    
    #other points
    if upper:
        score+=1
    else:
        feedback.append("Password should contain at least one uppercase letter.")
    if lower:
        score+=1
    else:
        feedback.append("Password should contain at least one lowercase letter.")
    if digit:
        score+=1
    else:
        feedback.append("Password should contain at least one digit.")
    if speical:
        score+=1
    else:
        feedback.append("Password should contain at least one special character.")
    #max point:4
    
    #max function point: 7

    return score,feedback

def calculate_entropy(password):
    # Determine the character set used
    character_set_size = 0
    score1=0
    
    if re.search(r'[a-z]', password):
        character_set_size += 26  # lowercase letters
    if re.search(r'[A-Z]', password):
        character_set_size += 26  # uppercase letters
    if re.search(r'[0-9]', password):
        character_set_size += 10  # digits
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        character_set_size += 32  # special characters
    
    # Calculate entropy
    length = len(password)
    if character_set_size == 0:
        return 0  # No characters found, entropy is 0
    
    entropy = length * math.log2(character_set_size)
    if entropy < 40:
        score1+=1
        return score1
    elif 40 <= entropy <= 60:
        score1+=2
        return score1
    else:
        score1+=3
        return score1
    #max point 3

def check_pwned_password(password):
    # Hash the password using SHA-1 (required by the HIBP API)
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    # The first 5 characters are sent to the API (k-anonymity principle)
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    
    # Query the HIBP API
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    response = requests.get(url)
    
    if response.status_code != 200:
        raise RuntimeError(f"Error fetching from HIBP API: {response.status_code}")
    
    # Check if the suffix is in the returned hash list
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return True, count
    
    return False, 0

#Gradeing of password 
def grade_password(score_Final):
    
    if score_Final >= 12:
        grade = "Excellent"
    elif 9 <= score_Final < 12:
        grade = "Good"
    elif 6 <= score_Final < 9:
        grade = "Fair"
    elif 0 <= score_Final < 6:
        grade = "Weak"
    else:
        grade = "Very Weak"
    return  grade
        
if __name__ == "__main__":
   
    password = input("Enter your password: ")
    
    #General Valdiation
    score0,feedback=genral_validation(password)
    
    #Entropy
    score1=calculate_entropy(password)
    
    #password breaches 
    is_pwned, count = check_pwned_password(password)
    
    if is_pwned:
        score2=-5
    else:
        score2=5
        
    
    score_Final=score0+score1+score2
    #Score break down
    print(f"Genral Validation = {score0}")
    print(f"Entropy = {score1}")
    print(f"Password Integrity = {score2}")
    print(f"Final Score = {score_Final}")
    
    grade=grade_password(score_Final)
    
    print(f"Password Grade = {grade}")
    
    #Integirty feedback
    if score2 == -5:
        print(f"Password has been pwned {count} times! Choose a different password.")
    else:
        print("Password is safe (not found in breaches).")
    
    #General Valdiation feedback
    if feedback:
        print("Feedback:")
        for msg in feedback:
            print(f"- {msg}")