const express = require("express");
const { identifier } = require("../middlewares/identification");
const jobsController = require("../controllers/jobsController");

const router = express.Router();

router.get("/", identifier, jobsController.getJobs);
router.get("/:id", identifier, jobsController.getJobById);
router.post("/", identifier, jobsController.createJob);
router.put("/:id", identifier, jobsController.updateJob);
router.patch("/:id", identifier, jobsController.updateJob);
router.delete("/:id", identifier, jobsController.deleteJob);

module.exports = router;

