const baseUrl = process.env.LUGHA_BASE_URL ?? "http://localhost:8000";
const apiKey = process.env.LUGHA_API_KEY;

if (!apiKey) {
  throw new Error("Set LUGHA_API_KEY first");
}

const response = await fetch(`${baseUrl}/v1/generate`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model: "lugha-demo-large",
    prompt: "Explain Kampala to a developer visiting Uganda for the first time.",
    language: "en",
    max_tokens: 64,
    region: "ug",
  }),
});

const data = await response.json();

if (!response.ok) {
  throw new Error(`${data.error.type}: ${data.error.message} (${data.error.request_id})`);
}

console.log(data.output);
console.log("Tokens used:", data.usage.total_tokens);
