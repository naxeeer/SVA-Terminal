const jwt = require('jsonwebtoken');

// Use process.env.JWT_SECRET in production!
const secret = process.env.JWT_SECRET || 'your_jwt_secret';

function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader) return res.status(401).json({ error: 'No token provided' });
  const token = authHeader.split(' ')[1];
  try {
    req.user = jwt.verify(token, secret);
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
}

module.exports = { authenticate, secret };