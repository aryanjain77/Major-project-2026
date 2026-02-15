const mongoose = require("mongoose");

const commentSchema = new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "User",
        required: true,
    },
    text: {
        type: String,
        required: true,
        trim: true,
        maxLength: 300,
    },
}, {
    timestamps: true,
});


const postsSchema = mongoose.Schema({
    title: {
        type: String,
        required: [true, "title is required"],
        trim: true,
    },
    description: {
        type: String,
        required: [true, "description is required"],
        trim: true,
    },
    userId: {               // to give user id to a post
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true,
    },
    comments: [commentSchema],

    upvotes: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: "User",
    }],

    downvotes: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: "User",
    }],
}, {
    timestamps: true,
});

module.exports = mongoose.model('Post', postsSchema);