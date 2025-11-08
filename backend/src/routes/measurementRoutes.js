const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/measurements/');
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  },
});

const upload = multer({
  storage,
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    
    if (extname && mimetype) {
      return cb(null, true);
    }
    cb(new Error('Only image files (JPEG, JPG, PNG) are allowed'));
  },
});

/**
 * @route   POST /api/v1/measurements/upload
 * @desc    Upload measurement photos (4 photos required)
 * @access  Protected
 */
router.post('/upload', upload.array('photos', 4), async (req, res) => {
  try {
    // Ensure req.files is an array and has exactly 4 items
    if (!req.files || !Array.isArray(req.files) || req.files.length !== 4) {
      return res.status(400).json({
        status: 'error',
        message: 'Please upload exactly 4 photos (front, back, left, right)',
      });
    }

    const photos = req.files.map(file => ({
      filename: file.filename,
      path: file.path,
      size: file.size,
    }));

    res.json({
      status: 'success',
      message: 'Photos uploaded successfully',
      data: { photos },
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: error.message,
    });
  }
});

/**
 * @route   POST /api/v1/measurements/process
 * @desc    Process measurements using AI
 * @access  Protected
 */
router.post('/process', async (req, res) => {
  try {
    const { photos, height, weight, userId } = req.body;

    // TODO: Integrate with AI model
    // - Send photos to AI service
    // - Get measurements back
    // - Save to database
    
    // Mock AI response
    const measurements = {
      chest: 98,
      waist: 82,
      shoulders: 44,
      armLength: 62,
      neck: 38,
      hip: 96,
      height,
      weight,
      unit: 'cm',
    };

    res.json({
      status: 'success',
      message: 'Measurements processed successfully',
      data: {
        measurements,
        userId,
        processedAt: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: error.message,
    });
  }
});

/**
 * @route   GET /api/v1/measurements/:userId
 * @desc    Get user measurements
 * @access  Protected
 */
router.get('/:userId', async (req, res) => {
  try {
    const { userId } = req.params;

    // TODO: Fetch from database
    const measurements = {
      userId,
      chest: 98,
      waist: 82,
      shoulders: 44,
      armLength: 62,
      neck: 38,
      hip: 96,
      height: 175,
      weight: 70,
      unit: 'cm',
      lastUpdated: new Date().toISOString(),
    };

    res.json({
      status: 'success',
      data: { measurements },
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: error.message,
    });
  }
});

module.exports = router;
