const express = require("express");
const postsController = require("../controllers/postsController");
const {identifier} = require("../middlewares/identification");

const router = express.Router();

router.get('/all-posts', postsController.getPosts);
router.get('/single-post', identifier, postsController.getSinglePost);
router.post('/create-post', identifier, postsController.createPost);
router.put('/update-post',identifier, postsController.updatePost);
router.delete('/delete-post', identifier, postsController.deletePost);
router.post("/comment", identifier, postsController.addComment);
router.post("/vote", identifier, postsController.votePost);

module.exports = router;