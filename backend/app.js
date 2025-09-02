const express = require('express');
const mongoose = require('mongoose');
const adminRoutes = require('./routes/admin');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

mongoose.connect('mongodb://localhost:27017/sva', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

app.use('/api/admin', adminRoutes);

app.listen(5000, () => {
  console.log('SVA backend running on port 5000');
});
