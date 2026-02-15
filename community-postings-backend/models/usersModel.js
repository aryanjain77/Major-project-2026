const mongoose = require("mongoose");

const userSchema = mongoose.Schema({
    email: {
        type: String,
        required: [true, "Email is required"],
        trim: true,
        unique: [true, "Email must be unique"],
        minLength: [5, "Email must have atleast 5 characters"],
        lowercase: true,
    },
    password: {
        type: String,
        required: [true, "Password must be provided"],
        trim: true,
        select: false,   // to prevent password to be fetched from db
    },
    verified: {
        type: Boolean,
        default: false    // initially the verified status will be false
    },
    verificationCode: {
        type: String,
        select: false,
    },
    verificationCodeValidation: {
        type: Number,
        select: false,
    },
    forgotPasswordCode: {
        type: String,
        select: false,
    },
    forgotPasswordCodeValidation: {
        type: Number,
        select: false,
    }
}, {
    timestamps: true,
});

module.exports = mongoose.model("User", userSchema);