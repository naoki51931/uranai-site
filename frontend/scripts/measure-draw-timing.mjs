import { chromium, request } from "@playwright/test";

const BASE_URL = process.env.MOON_ARCANA_BASE_URL ?? "http://127.0.0.1";
const LOCALE = process.env.MOON_ARCANA_LOCALE ?? "ja";
const EMAIL = process.env.MOON_ARCANA_TEST_EMAIL ?? `timing-test-${Date.now()}@example.com`;
const PASSWORD = process.env.MOON_ARCANA_TEST_PASSWORD ?? "MoonArcanaTest123";
const FULL_NAME = process.env.MOON_ARCANA_TEST_NAME ?? "Timing Test";
const QUESTION =
  process.env.MOON_ARCANA_TEST_QUESTION ?? "今の仕事を続けるべきか、新しい挑戦に進むべきかを知りたいです。";

async function ensureUser() {
  const api = await request.newContext({ baseURL: BASE_URL });
  const registerResponse = await api.post("/api/v1/auth/register", {
    data: {
      email: EMAIL,
      password: PASSWORD,
      full_name: FULL_NAME,
    },
  });

  if (!registerResponse.ok() && registerResponse.status() !== 409) {
    throw new Error(`register failed: ${registerResponse.status()} ${await registerResponse.text()}`);
  }

  const loginResponse = await api.post("/api/v1/auth/login", {
    data: {
      email: EMAIL,
      password: PASSWORD,
    },
  });

  if (!loginResponse.ok()) {
    throw new Error(`login failed: ${loginResponse.status()} ${await loginResponse.text()}`);
  }

  await api.dispose();
}

async function main() {
  await ensureUser();

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ baseURL: BASE_URL });

  const samples = [];

  try {
    await page.goto(`/${LOCALE}/login`, { waitUntil: "networkidle" });
    await page.locator("#email").fill(EMAIL);
    await page.locator("#password").fill(PASSWORD);
    await Promise.all([
      page.waitForURL(`**/${LOCALE}/dashboard`),
      page.locator("button[type='submit']").click(),
    ]);

    await page.waitForSelector("#question");
    await page.locator("#question").fill(QUESTION);

    const submitButton = page.locator("form button[type='submit']").first();
    const overlayText = page.getByText("問いを受け取りました…");
    const lingerText = page.getByText("三枚のカードが静かにそろいました…");

    const startedAt = Date.now();
    await submitButton.click();
    await overlayText.waitFor({ state: "visible" });
    const preparingVisibleAt = Date.now();

    await lingerText.waitFor({ state: "visible", timeout: 30000 });
    const lingerVisibleAt = Date.now();

    await lingerText.waitFor({ state: "hidden", timeout: 30000 });
    const finishedAt = Date.now();

    samples.push({
      login_email: EMAIL,
      prepare_visible_ms: preparingVisibleAt - startedAt,
      reveal_linger_visible_ms: lingerVisibleAt - startedAt,
      overlay_complete_ms: finishedAt - startedAt,
      overlay_complete_seconds: Number(((finishedAt - startedAt) / 1000).toFixed(2)),
    });

    console.log(JSON.stringify({ base_url: BASE_URL, locale: LOCALE, question: QUESTION, samples }, null, 2));
  } finally {
    await page.close();
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
