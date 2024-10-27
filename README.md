# Password Strength Checker

This Python script evaluates the strength of a given password based on various parameters, including general password validation rules, entropy (randomness), and whether the password has been exposed in any data breaches using the [Have I Been Pwned](https://haveibeenpwned.com/) API.

## Features

- **General Validation**: 
  - Evaluates password length and checks for the presence of uppercase letters, lowercase letters, digits, and special characters.
  - Provides a score from 0 to 7 based on these criteria.
  - Offers feedback on how to improve the password.

- **Entropy Calculation**: 
  - Calculates the entropy (randomness) of the password based on the character set size and password length.
  - Scores the entropy from 1 to 3, with a higher score indicating a more secure password.

- **Password Breach Check**: 
  - Uses the Have I Been Pwned (HIBP) API to check if the password has been involved in any known data breaches.
  - Deducts points if the password has been compromised, or adds points if it's safe.

- **Final Grade**:
  - Combines the scores from general validation, entropy, and breach check to provide a final score.
  - Grades the password as `Excellent`, `Good`, `Fair`, `Weak`, or `Very Weak` based on the final score.

## Scoring Breakdown

- **General Validation (Max Score: 7)**:
  - Password length and the inclusion of various character types determine this score.

- **Entropy (Max Score: 3)**:
  - Calculated based on the diversity and length of characters in the password.

- **Integrity Check (Max Score: 5 / Min Score: -5)**:
  - Adds 5 points if the password is not found in any known breaches.
  - Deducts 5 points if the password has been breached.

## How to Use

1. Clone or download the repository:
    ```bash
    git clonehttps://github.com/AYUSH18832/Password-Strength-Checker.git
    cd password-strength-checker
    ```
2. Install the required Python libraries (if not already installed):
    ```bash
    pip install requests
    ```
3. Run the script:
    ```bash
    python main.py
    ```
4. Enter the password you wish to evaluate when prompted.

## Example

```bash
Enter your password: MyStrongPassword123!

General Validation = 6
Entropy = 2
Password Integrity = 5
Final Score = 13
Password Grade = Excellent
Password is safe (not found in breaches).
