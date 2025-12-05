import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';

const richTheme = createTheme({
    palette: {
        mode: 'light',
        background: {
            default: '#f8f9fa', // Soft off-white for depth
            paper: '#ffffff',
        },
        primary: {
            main: '#2563eb', // Vibrant Blue
            light: '#60a5fa',
            dark: '#1e40af',
        },
        secondary: {
            main: '#7c3aed', // Rich Violet
            light: '#a78bfa',
            dark: '#5b21b6',
        },
        text: {
            primary: '#1e293b', // Slate 800
            secondary: '#64748b', // Slate 500
        },
    },
    typography: {
        fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
        h3: {
            fontWeight: 800,
            letterSpacing: '-0.02em',
            background: 'linear-gradient(45deg, #2563eb 30%, #7c3aed 90%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
        },
        h5: {
            fontWeight: 600,
        },
        button: {
            textTransform: 'none',
            fontWeight: 600,
            borderRadius: 8,
        },
    },
    shape: {
        borderRadius: 12,
    },
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    boxShadow: 'none',
                    '&:hover': {
                        boxShadow: '0 4px 12px rgba(37, 99, 235, 0.2)',
                    },
                },
            },
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
                    transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                    '&:hover': {
                        transform: 'translateY(-4px)',
                        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
                    },
                },
            },
        },
        MuiTextField: {
            styleOverrides: {
                root: {
                    '& .MuiOutlinedInput-root': {
                        borderRadius: 12,
                        backgroundColor: '#fff',
                        transition: 'box-shadow 0.2s',
                        '&:hover': {
                            boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
                        },
                        '&.Mui-focused': {
                            boxShadow: '0 4px 12px rgba(37, 99, 235, 0.15)',
                        },
                    },
                },
            },
        },
    },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <ThemeProvider theme={richTheme}>
            <CssBaseline />
            <App />
        </ThemeProvider>
    </React.StrictMode>,
)
