import { expect, test } from '@playwright/test';

test('tokenizes entered text and does not restore it after reload', async ({ page }) => {
  await page.goto('/');
  const input = page.getByLabel('Text to tokenize');
  await input.fill('hello tokenizer');
  await page.getByRole('button', { name: /tokenize/i }).click();
  await expect(page.getByRole('heading', { name: 'Token breakdown' })).toBeVisible();
  await expect(page.getByRole('table').getByText('15339')).toBeVisible();

  await page.reload();
  await expect(page.getByLabel('Text to tokenize')).toHaveValue('');
});

test('keeps the workspace usable at a narrow viewport', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto('/');
  await expect(page.getByLabel('Text to tokenize')).toBeVisible();
  await expect(page.getByRole('button', { name: /tokenize/i })).toBeVisible();
});
