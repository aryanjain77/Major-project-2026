const jwt = require("jsonwebtoken");

exports.identifier = (req,res,next) => {
    let token;
    if(req.headers.client === 'not-browser') {
        token = req.headers.authorization;
    }
    else {
        token = req.cookies['Authorization'];
    }
    if(!token) {
        return res.status(403).json({success:false, message:"Unauthorized"});
    }
    try {
        console.log(token);
        const userToken = token.split(' ')[1];
        console.log(userToken);
        const jwtVerified = jwt.verify(userToken, process.env.TOKEN_SECRET);
        if(jwtVerified) {
            req.user = jwtVerified,
            next();
        }
        else {
            throw new Error('error in the token');
        }
    }
    catch(error) {
        console.log(error);
        // Handle expired JWT explicitly: clear cookie and respond so client can sign out
        if(error && error.name === 'TokenExpiredError') {
            res.clearCookie('Authorization');
            return res.status(401).json({success:false, message: 'TokenExpired'});
        }
        return res.status(403).json({success:false, message: 'Unauthorized'});
    }
}