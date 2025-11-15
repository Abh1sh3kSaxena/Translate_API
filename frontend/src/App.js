import React, { useState } from 'react';
import { Container, Grid, TextField, Paper, Typography, Button } from '@mui/material';
import axios from 'axios';

const API_URL = window.location.origin;

function App() {
  const [inputText, setInputText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [isTranslating, setIsTranslating] = useState(false);

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleTranslate = async () => {
    if (!inputText.trim()) {
      setTranslatedText('');
      return;
    }

    setIsTranslating(true);
    try {
      const response = await axios.post(`${API_URL}/translate`, {
        text: inputText,
        max_length: 256
      });
      setTranslatedText(response.data.translation);
    } catch (error) {
      console.error('Translation error:', error);
      setTranslatedText('Error: Could not translate text');
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom align="center" sx={{ mb: 4 }}>
        English to French Translator
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
            <TextField
              fullWidth
              multiline
              rows={10}
              variant="outlined"
              label="Enter English Text"
              value={inputText}
              onChange={handleInputChange}
              placeholder="Type or paste English text here..."
            />
            <Button
              fullWidth
              variant="contained"
              onClick={handleTranslate}
              disabled={!inputText.trim() || isTranslating}
              sx={{ mt: 2 }}
            >
              {isTranslating ? 'Translating...' : 'Translate'}
            </Button>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
            <TextField
              fullWidth
              multiline
              rows={10}
              variant="outlined"
              label="French Translation"
              value={translatedText}
              InputProps={{
                readOnly: true,
              }}
              placeholder="Translation will appear here..."
            />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;