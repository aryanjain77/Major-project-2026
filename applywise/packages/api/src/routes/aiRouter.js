const express = require("express");
const aiController = require("../controllers/aiController");

const router = express.Router();

router.post("/classify", aiController.classify);

module.exports = router;

