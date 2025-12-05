import React from 'react';
import { Backdrop, CircularProgress, Typography, Box } from '@mui/material';

interface LoadingOverlayProps {
    open: boolean;
    message?: string;
}

const LoadingOverlay: React.FC<LoadingOverlayProps> = ({ open, message = "Processing..." }) => {
    return (
        <Backdrop
            sx={{
                color: '#fff',
                zIndex: (theme) => theme.zIndex.drawer + 1,
                flexDirection: 'column',
                gap: 2,
                backgroundColor: 'rgba(0, 0, 0, 0.7)' // Darker overlay for better contrast
            }}
            open={open}
        >
            <CircularProgress color="inherit" size={60} thickness={4} />
            <Box sx={{ mt: 2, textAlign: 'center' }}>
                <Typography variant="h5" component="div" sx={{ fontWeight: 'bold', letterSpacing: 1 }}>
                    {message}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8, mt: 1 }}>
                    Please wait while we fetch your results
                </Typography>
            </Box>
        </Backdrop>
    );
};

export default LoadingOverlay;
