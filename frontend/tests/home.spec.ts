import { test, expect } from "@playwright/test";

test("WATCHTOWER landing page loads", async ({ page }) => {
  await page.goto("/");

  await expect(page).toHaveTitle(/WATCHTOWER/i);

  await expect(
    page.getByRole("link", { name: /GitHub/i })
  ).toBeVisible();

  await expect(
    page.getByRole("link", { name: /About Us/i })
  ).toBeVisible();
});