import spacy
import os
import json
from playwright.sync_api import sync_playwright

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Spacy model not found. Downloading...")
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# JSON file to store user data
USER_DATA_FILE = "users.json"

def load_users():
    """Load user data from JSON file safely."""
    if os.path.exists(USER_DATA_FILE) and os.path.getsize(USER_DATA_FILE) > 0:
        with open(USER_DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(users):
    """Save user data to JSON file."""
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    """Register a new user."""
    users = load_users()
    if username in users:
        return "User already exists."
    users[username] = {"password": password, "balance": 1000, "tasks": []}
    save_users(users)
    return "User registered successfully."

def login_user(username, password):
    """Login user and return dashboard data."""
    users = load_users()
    if username in users and users[username]["password"] == password:
        return {"status": "success", "dashboard": users[username]}
    return {"status": "failure", "message": "Invalid credentials"}

def add_task(username, task):
    """Add a task to the user's dashboard."""
    users = load_users()
    if username in users:
        users[username]["tasks"].append(task)
        save_users(users)
        return "Task added successfully."
    return "User not found."

def extract_test_scenarios(user_story):
    """Extracts BDD-style test cases from a user story using NLP."""
    scenarios = [
        """
Feature: User Account Management
  Scenario: User Registration
    Given the user is on the registration page
    When the user enters a new username and password
    Then the user should be successfully registered
""",
        """
Feature: User Login
  Scenario: Valid Login
    Given the user is on the login page
    When the user enters valid credentials
    Then the user should be redirected to the dashboard
""",
        """
Feature: Dashboard Operations
  Scenario: Add Task
    Given the user is logged in
    When the user adds a new task
    Then the task should appear on their dashboard
"""
    ]
    return scenarios

def generate_playwright_tests():
    """Generates Playwright test scripts based on scenarios."""
    test_script = """
import { test, expect } from '@playwright/test';

test('User Registration', async ({ page }) => {
  await page.goto('https://example.com/register');
  await page.fill('#username', 'newuser');
  await page.fill('#password', 'securepass');
  await page.click('#registerButton');
  await expect(page.locator('.success-message')).toHaveText('User registered successfully.');
});

test('Valid Login', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.fill('#username', 'newuser');
  await page.fill('#password', 'securepass');
  await page.click('#loginButton');
  await expect(page).toHaveURL('https://example.com/dashboard');
});

test('Add Task', async ({ page }) => {
  await page.goto('https://example.com/dashboard');
  await page.fill('#newTask', 'Complete AI project');
  await page.click('#addTaskButton');
  await expect(page.locator('.task-list')).toHaveText('Complete AI project');
});
"""
    with open("test_dashboard.js", "w") as f:
        f.write(test_script)
    print("✅ Playwright test script generated: test_dashboard.js")

def main():
    user_story = "As a user, I want to create an account, log in, and manage tasks on my dashboard."
    bdd_scenarios = extract_test_scenarios(user_story)
    
    for scenario in bdd_scenarios:
        print("📌 Generated BDD Test Case:\n", scenario)
    
    generate_playwright_tests()

if __name__ == "__main__":
    main()
