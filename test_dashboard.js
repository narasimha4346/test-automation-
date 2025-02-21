
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
