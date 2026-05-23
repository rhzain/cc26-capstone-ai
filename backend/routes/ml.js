const express = require("express");
const router = express.Router();
const { authenticateToken } = require("../middleware/auth");

const DEFAULT_ML_SERVICE_URL = "http://localhost:8000";

function getMlServiceUrl() {
  return (process.env.ML_SERVICE_URL || DEFAULT_ML_SERVICE_URL).replace(/\/+$/, "");
}

function getInternalApiToken() {
  return process.env.INTERNAL_API_TOKEN;
}

// POST /api/ml/risk-profile
// Proxy risk prediction requests to the private FastAPI service.
router.post("/risk-profile", authenticateToken, async (req, res) => {
  const internalToken = getInternalApiToken();

  if (!internalToken) {
    return res.status(500).json({
      success: false,
      message: "INTERNAL_API_TOKEN is not configured on the Express service",
    });
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);

  try {
    const response = await fetch(`${getMlServiceUrl()}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Internal-Token": internalToken,
      },
      body: JSON.stringify(req.body),
      signal: controller.signal,
    });

    const contentType = response.headers.get("content-type") || "";
    const responseBody = contentType.includes("application/json")
      ? await response.json()
      : { message: await response.text() };

    if (!response.ok) {
      return res.status(response.status).json({
        success: false,
        message: "ML service request failed",
        error: responseBody,
      });
    }

    return res.status(200).json({
      success: true,
      data: responseBody,
    });
  } catch (err) {
    const isTimeout = err.name === "AbortError";
    console.error("[ML Gateway] Error:", err);

    return res.status(isTimeout ? 504 : 502).json({
      success: false,
      message: isTimeout
        ? "ML service request timed out"
        : "Failed to contact ML service",
    });
  } finally {
    clearTimeout(timeout);
  }
});

module.exports = router;
