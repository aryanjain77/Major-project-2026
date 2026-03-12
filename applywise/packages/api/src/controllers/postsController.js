const Post = require("../models/postsModel");
const {createPostSchema} = require("../middlewares/validator")

exports.getPosts = async (req,res) => {
    const {page} = req.query;
    const postsPerPage = 10;
    try {
        let pageNum = 0;
        if(page <= 1) {
            pageNum = 0;
        }
        else {
            pageNum = page - 1;
        }
        // const result = await Post.find()
        // .sort({createdAt: -1})
        // .skip(pageNum * postsPerPage)
        // .limit(postsPerPage)
        // .populate({
        //     path: 'userId',
        //     select: 'email', 
        // })
        // .populate("comments.userId", "email");
        // res.status(200).json({success:true, message:"posts", data: result}); 
        const result = await Post.find()
        .sort({ createdAt: -1 })
        .skip(pageNum * postsPerPage)
        .limit(postsPerPage)
        .populate("userId", "email")
        .select("title description upvotes downvotes comments createdAt");

        const formatted = result.map(post => ({
            ...post.toObject(),
            commentCount: post.comments.length,
            upvotes: post.upvotes.length,
            downvotes: post.downvotes.length,
            score: post.upvotes.length - post.downvotes.length
        }));

        res.json({ success: true, data: formatted }); 
    }
    catch(error) {
        console.log(error);
    }
}

// exports.getSinglePost = async (req,res) => {
//     const {_id} = req.query;
//     try {
//         const exisitingPost = await Post.findOne({_id}).populate({
//             path: 'userId',
//             select: 'email', 
//         });
//         if(!existingPost) {
//             return res.status(401).json({success:false, message:"post unavailable"});
//         }
//         res.status(200).json({success:true, message:"single post", data: exisitingPost});  
//     }
//     catch(error) {
//         console.log(error);
//     }
// }

exports.getSinglePost = async (req, res) => {
    const { _id } = req.query;
    const { userId } = req.user || {};

    try {
        const post = await Post.findById(_id)
            .populate("userId", "email")
            .populate("comments.userId", "email");

        if (!post) {
            return res.status(404).json({ success: false, message: "post unavailable" });
        }

        res.status(200).json({
            success: true,
            data: {
                ...post.toObject(),
                votes: {
                    upvotes: post.upvotes.length,
                    downvotes: post.downvotes.length,
                    score: post.upvotes.length - post.downvotes.length,
                    userVote: post.upvotes.includes(userId)
                        ? "upvote"
                        : post.downvotes.includes(userId)
                        ? "downvote"
                        : null
                }
            }
        });

    } catch (error) {
        console.log(error);
    }
};


exports.createPost = async (req,res) => {
    const {title, description} = req.body;
    const {userId} = req.user;
    try {
        const {error, value} = createPostSchema.validate({title, description, userId});
        if(error) {
            return res.status(401).json({success:false, message:error.details[0].message});     
        }
        const result = await Post.create({
            title,
            description,
            userId,
        });
        res.status(201).json({success:true, message:"post created", data:result});
    }
    catch(error) {
        console.log(error);
    }
}

exports.updatePost = async (req,res) => {
    const {_id} = req.query;
    const {title, description} = req.body;
    const {userId} = req.user;
    try {
        const {error, value} = createPostSchema.validate({title, description, userId});
        if(error) {
            return res.status(401).json({success:false, message:error.details[0].message});     
        }
        const existingPost = await Post.findOne({ _id });
        if(!existingPost) {
            return res.status(404).json({success:false, message:"post unavailable"});
        }
        if(existingPost.userId.toString() !== userId) {
            return res.status(403).json({success:false, message:"unauthorized"});
        }
        existingPost.title = title,
        existingPost.description = description;
        const result = await existingPost.save();
        res.status(200).json({success:true, message:"post updated", data:result});
    }
    catch(error) {
        console.log(error);
    }
}

exports.deletePost = async (req,res) => {
    const {_id} = req.query;
    const {userId} = req.user;
    try {
        const existingPost = await Post.findOne({ _id });
        if(!existingPost) {
            return res.status(404).json({success:false, message:"post already unavailable"});
        }
        if(existingPost.userId.toString() !== userId) {
            return res.status(403).json({success:false, message:"unauthorized"});
        }
        await Post.deleteOne({ _id });
        res.status(200).json({success:true, message:"deleted"});
    }
    catch(error) {
        console.log(error);
    }
}

exports.addComment = async (req, res) => {
    const { _id } = req.query;
    const { text } = req.body;
    const { userId } = req.user;

    try {
        const { error } = require("../middlewares/validator")
            .commentSchema.validate({ text });

        if (error) {
            return res.status(400).json({ success: false, message: error.details[0].message });
        }

        const post = await Post.findById(_id);
        if (!post) {
            return res.status(404).json({ success: false, message: "post unavailable" });
        }

        post.comments.push({ userId, text });
        await post.save();

        res.status(201).json({ success: true, message: "comment added" });
    } catch (error) {
        console.log(error);
    }
};

exports.votePost = async (req, res) => {
    const { _id } = req.query;
    const { type } = req.body; // "upvote" or "downvote"
    const { userId } = req.user;

    try {
        const { error } = require("../middlewares/validator")
            .voteSchema.validate({ type });

        if (error) {
            return res.status(400).json({ success: false, message: error.details[0].message });
        }

        const post = await Post.findById(_id);
        if (!post) {
            return res.status(404).json({ success: false, message: "post unavailable" });
        }

        const hasUpvoted = post.upvotes.includes(userId);
        const hasDownvoted = post.downvotes.includes(userId);

        // Remove existing vote
        post.upvotes = post.upvotes.filter(id => id.toString() !== userId);
        post.downvotes = post.downvotes.filter(id => id.toString() !== userId);

        // Apply new vote (toggle behavior)
        if (type === "upvote" && !hasUpvoted) {
            post.upvotes.push(userId);
        }

        if (type === "downvote" && !hasDownvoted) {
            post.downvotes.push(userId);
        }

        await post.save();

        res.status(200).json({
            success: true,
            message: "vote updated",
            votes: {
                upvotes: post.upvotes.length,
                downvotes: post.downvotes.length,
                score: post.upvotes.length - post.downvotes.length,
            }
        });
    } catch (error) {
        console.log(error);
    }
};
